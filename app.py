from flask import Flask, request, render_template_string
from subprocess import Popen, PIPE
import os

app = Flask(__name__)

# HTML template for the app interface
HTML_TEMPLATE = """
<!doctype html>
<html>
    <head>
        <title>Bandcamp Album Downloader</title>
    </head>
    <body>
        <h1>Download Bandcamp Album</h1>
        <form action="/" method="POST">
            <label for="url">Enter Bandcamp Album URL:</label>
            <input type="text" id="url" name="url" placeholder="https://your-album-url.bandcamp.com/album/album-name" required>
            <button type="submit">Download Album</button>
        </form>
        {% if message %}
            <p>{{ message }}</p>
        {% endif %}
    </body>
</html>
"""

def run_bandcamp_dl(url):
    """Run bandcamp-dl as a subprocess and capture output."""
    # Assuming bandcamp-dl.py is in the same directory
    command = ["python", "bandcamp_dl.py", url]
    process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return f"Album downloaded successfully: {stdout}"
    else:
        return f"Error downloading album: {stderr}"

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            # Run bandcamp-dl to download the album
            message = run_bandcamp_dl(url)
        else:
            message = "Please enter a valid URL."
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == "__main__":
    app.run(debug=True)
