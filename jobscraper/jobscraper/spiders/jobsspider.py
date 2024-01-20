import scrapy
import random 

class JobsspiderSpider(scrapy.Spider):
    user_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MASMJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; FunWebProducts; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAARJS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 4.4.2; SM-T230NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSWOL; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 5.1; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWA Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174",
    "Mozilla/5.0 (Linux; Android 4.0.4; BNTV600 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie9; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 5.0.2; SM-T530NU Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A4325c Safari/601.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",]
    name = "jobsspider"
    job_caracteristics={}
    api_url=''
    job_list=['RH%2B','avocat%2B','medecin%2B','data%2Bscientist','software%2Bengineer','Data%2Banalyst','Data%2BEnginer','Developpeur%2B','stage%2Bdata%2Bscientist','stage%2Bsoftware%2Bengineer',
              'stage%2BData%2Banalyst','stage%2BData%2BEnginer']
    def start_requests(self):
        for job in self.job_list:
            self.api_url='https://fr.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords='+job+'&location=France&geoId=105015875&trk=public_jobs_jobs-search-bar_search-submit&start='
            first_job_on_page=0
            first_url=self.api_url+str(first_job_on_page)
            yield scrapy.Request(url=first_url,callback=self.parse_job,meta={'first_job_on_page':first_job_on_page},headers={'User-agents':self.user_agents[random.randint(0,len(self.user_agents)-1)]})


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
            yield scrapy.Request(self.job_caracteristics['job_description_url'],callback=self.parse_description,meta={'first_job_on_page':first_job_on_page},headers={'User-agents':self.user_agents[random.randint(0,len(self.user_agents)-1)]})
            # we return our object job
            yield self.job_caracteristics
        if (num_jobs>0 and int(first_job_on_page)<150):
            first_job_on_page=int(first_job_on_page)+25
            first_url=self.api_url+str(first_job_on_page)
            yield scrapy.Request(url=first_url,callback=self.parse_job,meta={'first_job_on_page':first_job_on_page},headers={'User-agents':self.user_agents[random.randint(0,len(self.user_agents)-1)]})


    def parse_description(self,response):
       self.job_caracteristics['job_ description']= ' '.join(response.xpath('//div[contains(@class, "description__text--rich")]/section//text()').getall()).strip()
