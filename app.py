from datetime import datetime, timezone
import os
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


@app.route("/api/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    if not data:
        return (
            jsonify({"success": False, "message": "Invalid JSON body provided."}),
            400,
        )

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message_text = data.get("message", "").strip()

    if not name or not email or not message_text:
        return (
            jsonify(
                {"success": False, "message": "Name, email, and message are required."}
            ),
            400,
        )

    new_message = Message(name=name, email=email, message=message_text)
    db.session.add(new_message)
    db.session.commit()

    return (
        jsonify(
            {"success": True, "message": "Your message has been saved successfully."}
        ),
        201,
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
    port = int(os.getenv("PORT") or 8008)
    print(f"Starting server on http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
