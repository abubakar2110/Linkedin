from urllib.parse import quote
from .get_category import get_resume_data

resume_data = None

def get_job_search_params():
    global resume_data
    if resume_data is None:
        location, skills, job_title = get_resume_data()
        location = f"{location.strip()},Pakistan"
        resume_data = (
            skills,
            quote(job_title.strip()),
            quote(location.strip(), safe=',')
        )
    
    return resume_data