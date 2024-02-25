import json
import time
import undetected_chromedriver as uc
import schedule
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



class AvitoParse:
    def __init__(self, url:str, tags:list, cout_pages:int=100, version_main=None):
        self.url = url
        self.tags = tags
        self.cout_pages = cout_pages
        self.version_main = version_main
        self.data = []
    
    def __set_up__(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = uc.Chrome(version_main=self.version_main, options= options)
        
        
    def __get_url__(self):
        self.driver.get(self.url)
    
    def __paginator__(self):
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']") and self.cout_pages > 0:
            self.__parse_page__()
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']").click()
            self.cout_pages -= 1
            
    def __parse_page__(self):
        blocks = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for title in blocks:
            name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
            description = title.find_element(By.CSS_SELECTOR, "[class*='item-description']").text
            url = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute('href')
            price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute('content')
            data = {
                'name': name,
                'description': description,
                'url': url,
                'price':price
            }
            if any([item.lower() in name.lower() for item in self.tags]) and int(price) <= 10000:
                self.data.append(data)
        self.__save_data__()
            
    def __save_data__(self):
        with open("items.js", 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def parse(self):
        self.__set_up__()
        self.__get_url__()
        self.__paginator__()
 
def parsingAvito():
    AvitoParse(
            url="https://www.avito.ru/astrahan/bytovaya_tehnika/klimaticheskoe_oborudovanie-ASgBAgICAURguE8?s=104&user=1",
            cout_pages=1, tags=['Сплит-система','Сплит система', 'Газовый котел', 'кондиционер']           
        ).parse()
        
def main():
    # Start script every 1 minute
    schedule.every(1).minute.do(parsingAvito())
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        
if __name__=='__main__':    
    main()