from scraper_peviitor import Scraper
from unidecode import unidecode
from getCounty import get_county
from utils import (
    publish,
    publish_logo,
    show_jobs
)

company = "mobexpert"
url = "https://mobexpert.ro/pages/cariera-si-oameni"

scraper = Scraper(url)

scraper.getSoup()
content = scraper._soup

jobs = content.find_all('div', class_ = "job")

final_jobs = []

for job in jobs:
    job_info = {
        "job_title": unidecode(job.find('h2').text.strip()),
        "city": unidecode(job.find('p', class_="oras").text.strip()),
        "job_link": f"https://mobexpert.ro{job.find('a').get('href')}",
        "country": "Romania",
        "company": company,
    }
    job_info["county"] = get_county(job_info["city"])
    final_jobs.append(job_info)

publish(4, company, final_jobs, "APIKEY")

logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Logo-Mobexpert.png/180px-Logo-Mobexpert.png"
publish_logo(company, logo_url)

show_jobs(final_jobs)
