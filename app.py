from flask import Flask, render_template, abort
import json
import os
from typing import Dict, Any, List

app = Flask(__name__)

def load_profile_data(filepath: str) -> Dict[str, Any]:
    """Load and return the profile data from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return validate_profile_data(data)

def validate_profile_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize the loaded profile data."""
    # Required top-level fields
    required_fields = ["name", "title", "bio", "projects", "contact", "color_scheme"]
    for field in required_fields:
        if field not in data:
            abort(500, f"Missing required field: {field}")

    # Validate projects
    if not isinstance(data["projects"], list):
        abort(500, "Projects should be a list.")
    for project in data["projects"]:
        if not isinstance(project, dict):
            abort(500, "Each project should be a dictionary.")
        for key in ["name", "description", "url", "tech_stack"]:
            if key not in project:
                abort(500, f"Project missing required field: {key}")
        # Sanitize tech_stack
        if not isinstance(project["tech_stack"], list):
            project["tech_stack"] = []
        # Optional fields
        project.setdefault("screenshot", "")
        project.setdefault("demo_url", "")

    # Validate contact
    if "email" not in data["contact"]:
        abort(500, "Contact must include an email.")

    # Validate color_scheme
    color_keys = ["primary", "secondary", "background", "text", "accent"]
    for key in color_keys:
        if key not in data["color_scheme"]:
            abort(500, f"Color scheme missing: {key}")

    # Validate social (optional)
    if "social" in data:
        if not isinstance(data["social"], list):
            data["social"] = []
        for social in data["social"]:
            if not isinstance(social, dict):
                abort(500, "Each social link should be a dictionary.")
            for key in ["name", "url", "icon"]:
                if key not in social:
                    abort(500, f"Social link missing required field: {key}")
    else:
        data["social"] = []

    return data

def aggregate_skills(projects: List[Dict[str, Any]]) -> List[str]:
    """Aggregate unique skills from all project tech stacks."""
    skills = set()
    for project in projects:
        for tech in project.get("tech_stack", []):
            skills.add(tech)
    return sorted(skills)

@app.route("/")
def home():
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    profile = load_profile_data(data_path)
    # Always aggregate skills from projects for consistency
    profile["skills"] = aggregate_skills(profile.get("projects", []))
    return render_template("hello.html", profile=profile)

if __name__ == "__main__":
    app.run(debug=True)