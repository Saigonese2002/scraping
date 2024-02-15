import scrapy

class CarscraperSpider(scrapy.Spider):
    name = 'bonbanh_scraper'
    allowed_domains = ['bonbanh.com']
    page_number = 1
    start_urls = ['http://bonbanh.com/oto/page,1']

    custom_settings = {
        'FEEDS' : {
            'data.json' : {'format':'json', 'overwrite': True}
        }

    }

    def parse(self, response):
        for cars in response.css('li.car-item'):
            car_link = response.urljoin(cars.css('a[itemprop="url"]').attrib['href'])
            car_details = {
                'Name': cars.css('h3[itemprop="name"]::text').get(),
                'Condition': cars.css('div.cb1::text').get(),
                'Price': cars.css('b[itemprop="price"]::text').get(),
                'Location': cars.css('div.cb4 > b ::text').get(),
                'Link': car_link,
                'Description': cars.css('div.cb6_02::text').get(),
                'Car_code': cars.css('span.car_code::text').get()
            }
            yield scrapy.Request(car_link, callback=self.parse_car, meta={'car_details': car_details})

        next_page = 'http://bonbanh.com/oto/page,' + str(CarscraperSpider.page_number)
        if CarscraperSpider.page_number < 100: # Crawl 70% of the total pages
            CarscraperSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_car(self, response):
        car_details = response.meta['car_details']
        txt_inputs = response.css('div.box_car_detail div.row')
        for txt_input in txt_inputs:
            label = txt_input.css('div.label label::text').get()
            value = txt_input.css('div.txt_input span.inp::text, div.inputbox  span.inp::text').get()
            #value_inp = ' '.join(txt_input.css('div.txt_input span.inp::text').getall())
            #value_box = ' '.join(txt_input.css('div.inputbox  span.inp::text').getall())
            if label and value:
                car_details[label.strip()] = value.strip()

        yield car_details



        pass
