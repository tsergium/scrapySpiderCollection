# scrapySpiderCollection
Just a collection of Scrapy spiders I made

1. [justshowerthoughts.com](http://www.justshowerthoughts.com)

# Scraping using Scrapy and Scrapy Cloud

## Installing Scrapy (Ubuntu 9.10 or above)
```bash
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
pip install Scrapy 
```
For other OS follow this link doc.scrapy.org

## Creating a project
```bash
scrapy startproject tutorial
```
## Generating a spider
Navigate to the root of your project and execute the following command.
```bash
scrapy genspider example example.com
```
this will create a file with the following structure
```python
# -*- coding: utf-8 -*-
import scrapy
 
 
class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = (
        'http://www.example.com/',
    )
 
    def parse(self, response):
        pass
```
functional spider used to scrape the list of urls for accommodation
```python
# # -*- coding: utf-8 -*-
import scrapy


class UniplacesSpider(scrapy.Spider):
    name = "uniplaces"
    allowed_domains = ["uniplaces.com"]
    start_urls = (
        'https://www.uniplaces.com/accommodation',
    )

    file = open("data.json", "w")

    def parse(self, response):
        for href in response.css(
                "div.country.full-border-bottom div.country__bottom a.btn.btn-secondary.btn-huge::attr(href)"
        ):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_city)

    def parse_city(self, response):
        for href in response.css(
            "div.country.full-border-bottom div.country__row--info div.row__block a::attr(href)"
        ):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_properties)

    def parse_properties(self, response):
        for href in response.css(
            "div.offers div div.offer div.offer-container div.offer-summary span span a.offer-link::attr(href)"
         ):
            # ToDo: go through all pages inside pagination
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_property)

    @staticmethod
    def parse_property(response):
        for href in response.css(
            "div.uniplaces-container section.summary header h1 span::text"
         ):
            name = href.extract().strip().encode('utf-8')
            description = response.css(
                "section.details div.details-entry.description div.entry-data p::text"
            ).extract_first().strip().encode("utf-8")

            yield {
                "name": name,
                "description": description
            } 
```
you can test it using the CLI
```bash
scrapy crawl student -o student.json
```
-o parameter specifies the output and student is the name of our spider
## Deploying a spider to Scrapinghub
First you need to install shub (the Scrapinghub command line client). Shub allows you to deploy projects or dependencies, schedule spiders, and retrieve scraped data or logs without leaving the command line.
```bash
pip install shub --upgrade
```
login
```bash
shub login
```
deploy project
```bash
$ shub deploy
Target project ID: 77301
Save as default [Y/n]: y
Project 77301 was set as default in scrapinghub.yml. You can deploy to it via 'shub deploy' from now on.
Packing version 1467637508
Deploying to Scrapy Cloud project "77301"
{"status": "ok", "project": 77301, "version": "1467637508", "spiders": 1}
Run your spiders at: https://dash.scrapinghub.com/p/77301/
```
schedule spider
```bash
$ shub schedule student
Spider student scheduled, job ID: 12345/1/1
Watch the log on the command line:
    shub log -f 1/1
or print items as they are being scraped:
    shub items -f 1/1
or watch it running in Scrapinghub's web interface:
    https://app.scrapinghub.com/p/12345/job/1/1
```
## Fetch data from scrapinghub
```bash
curl -u API_KEY: https://storage.scrapinghub.com/items/PROJECT_ID/JOB_ID
```
## Periodic jobs
There is an undocumented API for fetching periodic jobs (details here) https://support.scrapinghub.com/topics/708-api-for-periodic-jobs/
```bash
curl -u APIKEY: "http://dash.scrapinghub.com/api/periodic_jobs?project=PROJECTID"
```
