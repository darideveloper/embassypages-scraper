from time import sleep
from libs.web_scraping import WebScraping
from tqdm import tqdm


class Scraper(WebScraping):
    
    def __init__(self):
        """ Start chrome and load page
        """
        
        home_page = "https://www.embassypages.com/spain"
        super().__init__()
        
        self.set_page(home_page)
        
    def get_business_links(self) -> list:
        """ Get the links of the business

        Returns:
            list: list of links
        """
        
        selector_links = ".letter-block ul > li > a"
        links = self.get_attribs(selector_links, "href")
        return links
    
    def scrape_business(self, links: str) -> list:
        """ Scrape the business data
        
        Args:
            links (str): link of the business

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
        
        sleep(5)
        
        data = []
        
        self.set_page(links)
        
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
    
    def scrape_all_business(self) -> list:
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
        
        print("Scraping all business...")
        
        links = self.get_business_links()
        data = []
        
        for link in tqdm(links):
            data.append(self.scrape_business(link))
            
        return data
                

if __name__ == "__main__":
    scraper = Scraper()
    data = scraper.scrape_all_business()
    print(data)