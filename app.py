from flask import Flask, render_template, abort  # Import Flask and helpers for web app and error handling
import json  # For reading JSON files
import os    # For file path operations

# Create the Flask web app
app = Flask(__name__)

# Define a simple Project class to hold project info
class Project:
    def __init__(self, name, description, url, tech_stack):
        # Save the project details as attributes
        self.name = name
        self.description = description
        self.url = url
        self.tech_stack = tech_stack

    @classmethod
    def from_dict(cls, d):
        # Create a Project from a dictionary (like from JSON)
        return cls(
            d.get("name", ""),           # Get name or empty string
            d.get("description", ""),    # Get description or empty string
            d.get("url", ""),            # Get url or empty string
            d.get("tech_stack", [])      # Get tech_stack or empty list
        )

# Function to load profile data from a JSON file
def load_profile_data(filepath):
    # If the file doesn't exist, show a 500 error
    if not os.path.exists(filepath):
        abort(500, "Profile data file not found.")
    # Open and read the JSON file
    with open(filepath, "r") as f:
        data = json.load(f)
    # Convert each project dictionary to a Project object
    data["projects"] = [Project.from_dict(p) for p in data.get("projects", [])]
    return data

# Define the main route for the website
@app.route("/")
def home():
    # Figure out the location of the data.json file
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    # Load the profile data from the file
    profile = load_profile_data(data_path)
    # Convert Project objects back to dictionaries for the template
    profile["projects"] = [vars(p) for p in profile["projects"]]
    # Render the hello.html template, passing in the profile data
    return render_template("hello.html", profile=profile)

# If this file is run directly, start the Flask web server
if __name__ == "__main__":
    app.run(debug=True)
