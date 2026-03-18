# archive twitter trending scraper

## Description

Scrapers the https://archive.twitter-trending.com/ page
Gathers most tweeted (along with volumes), longest trending (along with duration), and hourly trending data

## Usage

```
python scraper.py --start_date=[%dd-%mm-%YYY] \\
    --start_date=[%dd-%mm-%YYY] \\
    --region=[region] \\ check website for available options
    --out_dir=[output path folder]
```

## Requirements

Packages required:
* pandas
* selenium
* selectolax