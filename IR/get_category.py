import pickle
import os
import mimetypes
from tkinter import Tk, filedialog
import requests
import json

# Select Resume
def select_resume():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Your Resume",
        filetypes=[
            ("PDF files", "*.pdf"),
            ("Word files", "*.docx *.doc")
        ]
    )
    root.destroy()

    if not file_path:
        print("No file selected.")
        return None

    file_size = os.path.getsize(file_path)
    if file_size > 100 * 1024 * 1024:
        print("File is too large. Must be less than 100MB.")
        return None

    mime_type, _ = mimetypes.guess_type(file_path)
    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if mime_type not in allowed_types:
        print("Invalid file type. Only PDF or Word documents are allowed.")
        return None

    return file_path

# Preprocessing
def preprocess_skills(skill_list):
    new_skill = [skill.lower() for skill in skill_list]
    punct = ",.()[]{}><'_!@|^`~#$%&\\"
    cleaned_skills = [skill.translate(str.maketrans("", "", punct)) for skill in new_skill]
    unique_skills = []
    for skill in cleaned_skills:
        if skill not in unique_skills:
            unique_skills.append(skill)
    return unique_skills

def clean_skills(skills_text):
    return ' '.join(skills_text.lower().split(','))

# Main Function
def get_resume_data():
    resume_path = select_resume()
    if not resume_path:
        return None, None, None

    url = "https://api.affinda.com/v3/documents"
    files = { "file": (resume_path, open(resume_path, "rb"), "application/pdf") }
    payload = {
        "wait": "true",
        "collection": "gifqFHYk"
    }
    headers = {
        "accept": "application/json",
        "authorization": "Bearer aff_6bbba06d36993a46a26e41dc43dfd14b31968efa"
    }

    response = requests.post(url, data=payload, files=files, headers=headers)
    data = json.loads(response.text)

    skill = []
    for s in data["data"]["skill"]:
        skill.append(s["raw"])

    processed_skills = preprocess_skills(skill)

    # Load model
    folder_path = r"E:\\Linedin_Project\\IR"
    model_path = os.path.join(folder_path, "my_model.pkl")
    vectorizer_path = os.path.join(folder_path, "tfidf_vectorizer.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(vectorizer_path, "rb") as f:
        tfidf = pickle.load(f)

    resume_skills_cleaned = clean_skills(' '.join(processed_skills))
    resume_tfidf = tfidf.transform([resume_skills_cleaned])
    predicted_job_title = model.predict(resume_tfidf)

    try:
        location = data["data"]["location"]["parsed"]["city"]
    except (TypeError, KeyError):
        location = input("Enter your city manually: ")
    return location, processed_skills, predicted_job_title[0]


