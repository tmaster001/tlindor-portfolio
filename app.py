from flask import Flask, render_template, abort
import json
import os
from typing import Dict, Any, List, Optional, Set, Tuple, Generator, Union
from dataclasses import dataclass, asdict
from enum import Enum, auto
import logging
from functools import wraps

# --- Logging setup (foundational: logging module) ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Decorator example (foundational: decorators) ---
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# --- Enum example (foundational: enumerations) ---
class ProjectType(Enum):
    WEB = "Web"
    DATA_SCIENCE = "Data Science"
    SCRIPT = "Script"
    OTHER = "Other"

# --- Dataclass example (foundational: dataclasses) ---
@dataclass
class SocialLink:
    name: str
    url: str
    icon: str

# --- Inheritance and properties (foundational: OOP) ---
class BaseItem:
    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class Project(BaseItem):
    def __init__(self, name: str, description: str, url: str, tech_stack: List[str],
                 screenshot: str = "", demo_url: str = "", project_type: ProjectType = ProjectType.OTHER):
        self.name = name
        self.description = description
        self.url = url
        self.tech_stack = tech_stack
        self.screenshot = screenshot
        self.demo_url = demo_url
        self.project_type = project_type

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        # Use Enum with fallback
        ptype = ProjectType(data.get("project_type", "Other")) if "project_type" in data else ProjectType.OTHER
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            url=data.get("url", ""),
            tech_stack=data.get("tech_stack", []),
            screenshot=data.get("screenshot", ""),
            demo_url=data.get("demo_url", ""),
            project_type=ptype
        )

    @property
    def tech_summary(self) -> str:
        return ", ".join(self.tech_stack)

    def __repr__(self):
        return f"Project({self.name!r}, {self.url!r})"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        return url.startswith("http://") or url.startswith("https://")

# --- Custom exception (foundational: exception hierarchy) ---
class ProfileDataError(Exception):
    pass

# --- Context manager example (foundational: context managers) ---
class DummyContext:
    def __enter__(self):
        logger.info("Entering dummy context")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Exiting dummy context")

# --- Generator example (foundational: generators) ---
def project_generator(projects: List[Project]) -> Generator[Project, None, None]:
    for project in projects:
        yield project

# --- Main logic ---
@log_call
def load_profile_data(filepath: str) -> Dict[str, Any]:
    """Load and return the profile data from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Profile data file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            abort(500, f"JSON decode error: {e}")
    return validate_profile_data(data)

@log_call
def validate_profile_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize the loaded profile data."""
    required_fields = ("name", "title", "bio", "projects", "contact", "color_scheme")
    for field in required_fields:
        if field not in data:
            raise ProfileDataError(f"Missing required field: {field}")

    # Validate projects
    if not isinstance(data["projects"], list):
        raise ProfileDataError("Projects should be a list.")
    validated_projects: List[Project] = []
    for project_data in data["projects"]:
        if not isinstance(project_data, dict):
            raise ProfileDataError("Each project should be a dictionary.")
        for key in ("name", "description", "url", "tech_stack"):
            if key not in project_data:
                raise ProfileDataError(f"Project missing required field: {key}")
        if not isinstance(project_data["tech_stack"], list):
            project_data["tech_stack"] = []
        project_data.setdefault("screenshot", "")
        project_data.setdefault("demo_url", "")
        validated_projects.append(Project.from_dict(project_data))
    data["projects"] = validated_projects

    # Validate contact
    if "email" not in data["contact"]:
        raise ProfileDataError("Contact must include an email.")

    # Validate color_scheme
    color_keys = ("primary", "secondary", "background", "text", "accent")
    for key in color_keys:
        if key not in data["color_scheme"]:
            raise ProfileDataError(f"Color scheme missing: {key}")

    # Validate social (optional, using dataclass)
    if "social" in data:
        if not isinstance(data["social"], list):
            data["social"] = []
        validated_social: List[SocialLink] = []
        for social in data["social"]:
            if not isinstance(social, dict):
                raise ProfileDataError("Each social link should be a dictionary.")
            for key in ("name", "url", "icon"):
                if key not in social:
                    raise ProfileDataError(f"Social link missing required field: {key}")
            validated_social.append(SocialLink(**social))
        data["social"] = validated_social
    else:
        data["social"] = []

    return data

@log_call
def aggregate_skills(projects: List[Project]) -> List[str]:
    """Aggregate unique skills from all project tech stacks."""
    skills: Set[str] = set()
    for project in projects:
        skills.update(project.tech_stack)
    return sorted(skills)

@log_call
def get_project_names(projects: List[Project]) -> List[str]:
    """Return a list of project names."""
    return [project.name for project in projects]

@log_call
def get_contact_email(contact: Dict[str, Any]) -> Optional[str]:
    """Safely get the contact email."""
    return contact.get("email")

@log_call
def get_color_scheme(data: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
    """Return the color scheme as a tuple."""
    cs = data["color_scheme"]
    return (cs["primary"], cs["secondary"], cs["background"], cs["text"], cs["accent"])

@log_call
def filter_projects_by_type(projects: List[Project], ptype: ProjectType) -> List[Project]:
    """Filter projects by ProjectType using a list comprehension."""
    return [p for p in projects if p.project_type == ptype]

@log_call
def get_projects_with_valid_urls(projects: List[Project]) -> List[Project]:
    """Use a lambda and filter to get projects with valid URLs."""
    return list(filter(lambda p: Project.is_valid_url(p.url), projects))

@app.route("/")
def home():
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    profile = load_profile_data(data_path)
    # Use context manager (for demonstration)
    with DummyContext():
        # Always aggregate skills from projects for consistency
        profile["skills"] = aggregate_skills(profile.get("projects", []))
        project_names = get_project_names(profile["projects"])
        contact_email = get_contact_email(profile["contact"])
        color_scheme = get_color_scheme(profile)
        # Use generator to iterate projects (for demonstration)
        project_titles = [p.name for p in project_generator(profile["projects"])]
        # Use filter and enum
        web_projects = filter_projects_by_type(profile["projects"], ProjectType.WEB)
        valid_url_projects = get_projects_with_valid_urls(profile["projects"])
        # Prepare social links for template
        profile["projects"] = [vars(p) for p in profile["projects"]]
        profile["social"] = [asdict(s) for s in profile["social"]]
    return render_template(
        "hello.html",
        profile=profile,
        project_names=project_names,
        contact_email=contact_email,
        color_scheme=color_scheme,
        project_titles=project_titles,
        web_projects=[vars(p) for p in web_projects],
        valid_url_projects=[vars(p) for p in valid_url_projects]
    )

if __name__ == "__main__":
    # Use environment variable for debug mode as a best practice
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug_mode)