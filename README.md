# Archive Twitter Trending Scraper

Scrapes historical trending data from `https://archive.twitter-trending.com/` using Selenium, then saves parsed results as CSV files.

The scraper collects:
- hourly trending topics
- most-tweeted topics and volumes
- longest-trending topics and durations

## Requirements

- Python 3
- Google Chrome installed
- A compatible ChromeDriver available to Selenium

Python packages:
- `pandas`
- `selenium`
- `selectolax`

## Install

```bash
pip install pandas selenium selectolax
```

## Usage

```bash
python scraper.py --start_date=01-01-2019 --end_date=01-10-2019 --region=united-states --out_dir=out
```

Arguments:
- `--start_date`: start date for the scrape range
- `--end_date`: end date for the scrape range
- `--region`: region slug used by `archive.twitter-trending.com`
- `--out_dir`: directory where CSV files are written

Defaults:
- `start_date=01-01-2019`
- `end_date=01-02-2019`
- `region=united-states`
- `out_dir=out`

## Output

For each run, the scraper writes:
- `trending_<timestamp>.csv`
- `most_<timestamp>.csv`
- `longest_<timestamp>.csv`

It also writes logs to `scraper.log` and prints progress to the console while the script runs.

## Notes

- Dates are passed directly into `pandas.date_range`, so use a consistent month-day-year format such as `01-10-2019`.
- Available region values come from the site URL structure, for example `united-states`.
