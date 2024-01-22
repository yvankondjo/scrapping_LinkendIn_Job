import scrapy
import random 

class JobsspiderSpider(scrapy.Spider):
    name = "jobsspider"
    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.json': { 'format': 'json',}}
        }
    job_caracteristics={}
    api_url=''

    job_list=['data%20scientist','Data%20analyst','Data%20Enginer','software%20engineer']
    job_location=['France','United%20States','Luxembourg','Royaume-Uni','Canada']

    def start_requests(self):

        for location in self.job_location:
            for job in self.job_list:
                self.job_caracteristics['location']=location
                self.api_url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords='+job+'&location='+location+'&position=1&pageNum=0&start='
                first_job_on_page=0
                first_url=self.api_url+str(first_job_on_page)
                yield scrapy.Request(url=first_url,callback=self.parse_job,meta={'first_job_on_page':first_job_on_page})


    def parse_job(self, response):
        first_job_on_page=response.meta['first_job_on_page']
        jobs=response.css('li')
        num_jobs=len(jobs)

        for job in jobs:
            self.job_caracteristics['job_title']=job.css('h3::text').get(default='not-found').strip()
            self.job_caracteristics['job_description_url']=job.css('a.base-card__full-link::attr(href)').get(default='not-found').strip()
            self.job_caracteristics['time']=job.css('time::text').get(default='not-found').strip()
            self.job_caracteristics['company_logo']=job.css('img.artdeco-entity-image::attr(data-delayed-url)').get(default='not-found').strip()
            self.job_caracteristics['company_name']=job.css('h4 a::text').get(default='not-found').strip()
            self.job_caracteristics['company_link']=job.css('h4 a::attr(href)').get(default='not-found').strip()
            self.job_caracteristics['company_location']=job.css('span.job-search-card__location::text').get(default='not-found').strip()
            # now we go and scrap the description of the job 
            yield scrapy.Request(self.job_caracteristics['job_description_url'],callback=self.parse_description,meta={'first_job_on_page':first_job_on_page})
        if num_jobs>0 :
            first_job_on_page=int(first_job_on_page)+25
            first_url=self.api_url+str(first_job_on_page)
            yield scrapy.Request(url=first_url,callback=self.parse_job,meta={'first_job_on_page':first_job_on_page})


    def parse_description(self,response):
       self.job_caracteristics['job_ description']= ' '.join(response.xpath('//div[contains(@class, "description__text--rich")]/section//text()').getall()).strip()
       # we return our object job
       yield self.job_caracteristics