from urllib.parse import quote
from get_category import get_resume_data  

def get_job_search_params():
    
    location, skills, job_title = get_resume_data()
    location = f"{location.strip()},Pakistan"
    f_job = quote(job_title.strip())
    f_location = quote(location.strip(), safe=',')
    
    return skills,f_job, f_location

print(get_job_search_params())