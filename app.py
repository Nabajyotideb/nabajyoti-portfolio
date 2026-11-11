from datetime import datetime, timezone
from email.message import EmailMessage
import os
import smtplib
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Application configuration
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "dev-secret-key-change-before-deployment"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)


# ==================================
# DATABASE MODELS
# ==================================
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)
    github_url = db.Column(
        db.String(300), nullable=True, default="https://github.com/Nabajyotideb"
    )
    demo_url = db.Column(db.String(300), nullable=True, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tech_stack": self.tech_stack,
            "github_url": self.github_url or "",
            "demo_url": self.demo_url or "",
        }


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ==================================
# DATABASE SEEDING
# ==================================
def seed_database():
    """Seeds initial projects and skills if tables are empty."""
    if Project.query.count() == 0:
        initial_projects = [
            Project(
                title="AI Virtual Mouse Using Hand Gesture Recognition",
                description=(
                    "A computer vision-based application that enables hands-free"
                    " computer interaction using real-time hand gesture"
                    " recognition."
                ),
                tech_stack="Python, OpenCV, MediaPipe, PyAutoGUI",
                github_url="https://github.com/Nabajyotideb",
                demo_url="",
            ),
            Project(
                title="Plant Profile Management System in Smart Gardening",
                description=(
                    "A full-stack smart gardening application for managing plant"
                    " profiles, fertilizer schedules, and plant-related information."
                ),
                tech_stack="Python, Flask, MySQL, JavaScript",
                github_url="https://github.com/Nabajyotideb",
                demo_url="",
            ),
        ]
        db.session.add_all(initial_projects)
        db.session.commit()
        print("Seeded initial projects successfully.")

    if Skill.query.count() == 0:
        initial_skills = [
            Skill(name="Python", category="Programming"),
            Skill(name="Java (Basics)", category="Programming"),
            Skill(name="HTML", category="Web Development"),
            Skill(name="CSS", category="Web Development"),
            Skill(name="Figma", category="Tools & Design"),
            Skill(name="Git (Basics)", category="Tools & Design"),
            Skill(name="Communication", category="Soft Skills"),
            Skill(name="Teamwork", category="Soft Skills"),
            Skill(name="Time Management", category="Soft Skills"),
            Skill(name="Problem-Solving", category="Soft Skills"),
            Skill(name="Adaptability", category="Soft Skills"),
        ]
        db.session.add_all(initial_skills)
        db.session.commit()
        print("Seeded initial skills successfully.")


# ==================================
# EMAIL NOTIFICATION FUNCTION
# ==================================
def send_contact_email(name, visitor_email, message):
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_APP_PASSWORD", "").replace(" ", "")
    mail_receiver = os.getenv("MAIL_RECEIVER")

    # Check email configuration
    if (
        not mail_username
        or not mail_password
        or not mail_receiver
        or mail_password == "your-16-character-app-password"
    ):
        app.logger.warning("Email configuration is incomplete or using placeholder.")
        return False

    try:
        email = EmailMessage()
        email["Subject"] = f"New Portfolio Message from {name}"
        email["From"] = mail_username
        email["To"] = mail_receiver
        email["Reply-To"] = visitor_email
        email.set_content(
            f"Hello Nabajyoti,\n\n"
            f"You have received a new message through your portfolio.\n\n"
            f"Visitor Name: {name}\n"
            f"Visitor Email: {visitor_email}\n\n"
            f"Message:\n{message}\n\n"
            f"You can reply directly to this email to contact the visitor."
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
            smtp.login(mail_username, mail_password)
            smtp.send_message(email)

        app.logger.info(f"Email notification sent to {mail_receiver}")
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email notification: {e}")
        return False


# ==================================
# ROUTES & API ENDPOINTS
# ==================================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])


@app.route("/api/skills", methods=["GET"])
def get_skills():
    skills = Skill.query.all()
    return jsonify([skill.to_dict() for skill in skills])


# ==================================
# CONTACT MESSAGE API WITH EMAIL
# ==================================
@app.route("/api/messages", methods=["POST"])
def save_message():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # Validate required fields
    if not name or not email or not message:
        return jsonify({"error": "All fields are required."}), 400

    # Validate lengths
    if len(name) > 100 or len(email) > 150 or len(message) > 5000:
        return jsonify({"error": "Input exceeds the allowed length."}), 400

    # Basic email validation
    if (
        "@" not in email
        or "." not in email.split("@")[-1]
        or "\r" in email
        or "\n" in email
    ):
        return jsonify({"error": "Invalid email address format."}), 400

    # 1. Save message to database
    try:
        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Database error saving message: {e}")
        return (
            jsonify({
                "error": "Failed to save your message. Please try again later.",
                "success": False,
            }),
            500,
        )

    # 2. Attempt email notification
    notification_sent = False
    try:
        notification_sent = send_contact_email(name, email, message)
    except Exception as e:
        app.logger.warning(f"Error during email delivery attempt: {e}")
        notification_sent = False

    return (
        jsonify({
            "success": True,
            "message": "Your message has been saved successfully.",
            "notification_sent": notification_sent,
        }),
        201,
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
    port = int(os.getenv("PORT") or 8008)
    print(f"Starting server on http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
