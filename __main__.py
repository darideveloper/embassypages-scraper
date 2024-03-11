import os
from time import sleep
from libs.web_scraping import WebScraping
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
CHROME_PATH = os.getenv("CHROME_PATH")


class Scraper(WebScraping):
    
    def __init__(self):
        """ Start chrome
        """
        
        self.home_page = "https://www.embassypages.com/spain"
        super().__init__(
            chrome_folder=CHROME_PATH,
        )        
    
    def get_business_data(self) -> list:
        """ Scrape the business data

        Returns:
            list: business data
            
            Structure:
            [
                "Address",
                "Phone",
                "Fax",
                "Emails",
                "Socials"
            ]
                
        """
                
        data = []
                
        selectors = {
            'address': '.address p',
            'phone': '.telephone a',
            'fax': '.fax p',
            'emails': '.email a',
            'socials': '.social__media',
        }
        
        for _, selector_value in selectors.items():
            values = self.get_texts(selector_value)
            values_clean = list(map(
                lambda value: value.strip().replace("\n", ""), values
            ))
            value_formatted = ", ".join(values_clean)
            data.append(value_formatted)
            
        return data
    
    def scrape_business(self) -> list:
        """ Scrape all the business data

        Returns:
            list: list of business data
            
            Structure:
            [
                [
                    "Address",
                    "Phone",
                    "Fax",
                    "Emails",
                    "Socials"
                ]
            ]
        """
        
        # Show status
        print("Scraping all business...")
        
        # Load home page
        self.set_page(self.home_page)
        
        # Selectors and counters
        selector_links = ".letter-block ul > li > a"
        business_index = 0
        business_num = len(self.get_elems(selector_links))
        
        # Get elements
        data = []
        while True:
            
            # End loop when no more business
            if business_index >= business_num:
                break

            # Debug status
            print(f"Scraping business {business_index + 1}/{business_num}")
            
            # Load home page
            sleep (20)
            self.set_page(self.home_page)
            
            # Get next link and load page
            links = self.get_elems(selector_links)
            link = links[business_index]
            business_name = link.text
            business_url = link.get_attribute("href")
            link.click()
            
            # Extract data
            business_data = self.get_business_data()
            business_data.insert(0, business_name)
            business_data.insert(1, business_url)
            data.append(business_data)
            
            # Increase counter
            business_index += 1
            sleep(20)
               

if __name__ == "__main__":
    scraper = Scraper()
    data = scraper.scrape_business()
    print(data)