import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from datetime import datetime
import re


# TODO save as as csv
job_titles = ['Data%20Engineer', 'Data%20Analyst', 'Data%20Scientist', 'Machine%20Learning%20Engineer']
locations_df = pd.read_csv('./input_data/all_countries.csv', header=0).country
scraper_results_path = Path('./output_data/scrape_results.csv')

# Function to remove tags

if scraper_results_path.is_file():
    file = open('./output_data/scrape_results.csv', 'a')
    writer = csv.writer(file)
else:
    file = open('./output_data/scrape_results.csv', 'a')
    writer = csv.writer(file)
    writer.writerow(['job', 'job_location', 'scrape_result', 'scrape_time'])

for job in job_titles:
    for location in locations_df:
        if location == 'Austria':

            url = f'https://www.linkedin.com/jobs/search?keywords={job}&location={location}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
            print(f'Perform https request for {location}')
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                scrape_result = soup.find('div', class_='filter-values-container__filter-values')
                scrape_result = [text for text in scrape_result.stripped_strings]
            except:
                scrape_result = None
            print(scrape_result)
            writer.writerow([
                job,
                location,
                scrape_result,
                datetime.now()
            ])
