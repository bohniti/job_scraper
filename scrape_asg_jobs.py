import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    RemoteFilters
import sqlite3

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)


# Fired once for each successfully processed job
def on_data(data: EventData):
    scraped_data = (str(data.job_id),
    str(data.link),
    str(data.apply_link),
    str(data.title),
    str(data.company),
    str(data.company_link),
    str(data.company_img_link),
    str(data.place),
    str(data.description),
    str(data.description_html),
    str(data.insights))

    db_connector(scraped_data)


def db_connector(data):

    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()

    # create a table if it does not exsists
    try:
        c.execute('''CREATE TABLE jobs(job_id TEXT,link TEXT,apply_link TEXT,title TEXT,company TEXT,company_link TEXT,company_img_link TEXT,place TEXT,description TEXT,description_html TEXT,insights TEXT)''')
    except:
        print('Table already exsits!')


    # data to insert
    # sandwich = 'chicken'
    # fruit = 'orange'
    # tablenum = 22

    # insert and commit to database
    c.execute('''INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?,?,?,?)''', data)
    conn.commit()

    # select all data from table and print
    c.execute('''SELECT * FROM jobs''')
    results = c.fetchall()
    print(results)

    # close database connection
    conn.close()


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path='./chromedriver',  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=20  # Page load timeout (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        options=QueryOptions(
            locations=['Austria'],
            apply_link=False,  # Try to extract apply link (easy applies are skipped). Default to False.
            limit=1,
            filters=QueryFilters(
                company_jobs_url=None,  # Filter by companies.
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
                experience=None,
            )
        )
    ),
]

scraper.run(queries)
