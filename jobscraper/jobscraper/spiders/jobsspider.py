import scrapy

class JobsspiderSpider(scrapy.Spider):
    name = "jobsspider"
    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
    }
    job_list = ['data%20scientist', 'Data%20analyst', 'Data%20Enginer', 'software%20engineer']
    job_location = ['France', 'United%20States', 'Luxembourg', 'Royaume-Uni', 'Canada']

    def start_requests(self):
        for location in self.job_location:
            for job in self.job_list:
                api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=' + job + '&location=' + location + '&position=1&pageNum=0&start='
                first_job_on_page = 0
                first_url = api_url + str(first_job_on_page)
                yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'api_url': api_url, 'first_job_on_page': first_job_on_page})

    def parse_job(self, response):
        api_url = response.meta['api_url']
        first_job_on_page = response.meta['first_job_on_page']
        jobs = response.css('li')

        for job in jobs:
            job_id = job.css('div.base-card::attr(data-entity-urn)').get().split(':')[-1]
            job_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/' + job_id
            yield response.follow(job_url, callback=self.parse_description, meta={'job_id': job_id})
        
        if len(jobs) > 0 and first_job_on_page < 125:
            first_job_on_page += 25
            next_url = api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'api_url': api_url, 'first_job_on_page': first_job_on_page})

    def parse_description(self, response):
        job_caracteristics = {}
        job_caracteristics['job_id'] = response.meta['job_id']
        job_caracteristics['job_title'] = response.css('h2.top-card-layout__title::text').get(default='not-found').strip()
        job_caracteristics['company_name'] = response.css('a.topcard__org-name-link::text').get(default='not-found').strip()
        job_caracteristics['company_link'] = response.css('a.topcard__org-name-link::attr(href)').get(default='not-found').strip()
        job_caracteristics['company_location'] = response.css('span.topcard__flavor--bullet::text').get(default='not-found').strip()
        job_caracteristics['job_description_url'] = response.css('div.top-card-layout__entity-info a::attr(href)').get(default='not-found').strip()
        job_caracteristics['company_logo'] = response.css('img.artdeco-entity-image::attr(data-delayed-url)').get(default='not-found').strip()
        job_caracteristics['job_description'] = ' '.join(response.xpath('//div[contains(@class, "description__text--rich")]/section//text()').getall()).strip()
        job_caracteristics['time'] = response.css('span.posted-time-ago__text.topcard__flavor--metadata::text').get(default='not-found').strip()
        
        yield job_caracteristics
