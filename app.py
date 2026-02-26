from flask import Flask, request, render_template_string
from utils import (
    extract_text_from_pdf,
    clean_text,
    vectorize_text,
    calculate_match_score,
    interpret_score
)
import os

app = Flask(__name__)
UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Resume Screening System</title>
</head>
<body>
    <h2>Resume Screening System</h2>
    <form method="post" enctype="multipart/form-data">
        <label>Upload Resume (PDF):</label><br><br>
        <input type="file" name="resume" required><br><br>

        <label>Job Description:</label><br><br>
        <textarea name="job_desc" rows="6" cols="50" required></textarea><br><br>

        <input type="submit" value="Check Match">
    </form>

    {% if score %}
        <h3>Match Score: {{ score }} %</h3>
        <h3>Result: {{ result }}</h3>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    score = None
    result = None

    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form["job_desc"]

        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            #file_path = "Abdul Salam Azadh.pdf"

            resume_text = extract_text_from_pdf(file_path)
            cleaned_resume = clean_text(resume_text)
            cleaned_job = clean_text(job_desc)

            vectors = vectorize_text(cleaned_resume, cleaned_job)
            score = round(calculate_match_score(vectors), 2)
            result = interpret_score(score)

    return render_template_string(HTML_FORM, score=score, result=result)


if __name__ == "__main__":
    app.run(debug=True)
