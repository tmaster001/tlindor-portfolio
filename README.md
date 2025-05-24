# flask-hello-world

A modern personal portfolio built with Flask.

## Running Locally

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd flask-hello-world
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Add your resume:**
   Place your `resume.pdf` file in the `static` folder:
   ```
   /workspaces/flask-hello-world/static/resume.pdf
   ```

5. **(Optional) Add project screenshots:**
   Place your project screenshots in the `static/screenshots` folder and reference them in your `data.json`:
   ```
   /workspaces/flask-hello-world/static/screenshots/your-screenshot.png
   ```
   Example in `data.json`:
   ```json
   "screenshot": "static/screenshots/your-screenshot.png"
   ```

6. **Run the Flask app:**
   ```sh
   python app.py
   ```
   The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Deploying to Vercel

1. **Install the Vercel CLI:**
   ```sh
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```sh
   vercel login
   ```

3. **Deploy the app:**
   ```sh
   vercel
   ```
   Follow the prompts to complete deployment.

**Note:**  
Make sure your `requirements.txt` and `vercel.json` files are present in the project root.

For more details, see [Vercel Python documentation](https://vercel.com/docs/functions/python).