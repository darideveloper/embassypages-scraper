import os
from time import sleep
from dotenv import load_dotenv
from libs.web_scraping import WebScraping
from libs.xlsx import SpreadsheetManager

# env variables
load_dotenv()
CHROME_PATH = os.getenv("CHROME_PATH")

# Paths
CURRENT_FOLDER = os.path.dirname(__file__)
EXCEL_PATH = os.path.join(CURRENT_FOLDER, "data.xlsx")


class Scraper(WebScraping):

    def __init__(self):
        """ Start chrome and open excel file
        """

        # Start chrome
        self.home_page = "https://www.embassypages.com/spain"
        super().__init__(
            chrome_folder=CHROME_PATH,
        )
        
        # Open excel path
        sheet_name = "data"
        self.ss_manager = SpreadsheetManager(EXCEL_PATH)
        
        # Delete old data sheet
        try:
            self.ss_manager.delete_sheet(sheet_name)
            self.ss_manager.delete_sheet("Sheet")
        except Exception:
            pass
        
        # Set sheet
        self.ss_manager.create_set_sheet(sheet_name)
        
        # Write heder
        header = [
            "Name",
            "URL",
            "Address",
            "Phone",
            "Fax",
            "Emails",
            "Socials"
        ]
        self.ss_manager.write_data([header])
        self.ss_manager.save()
    
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
            "texts": {
                'address': '.address p',
                'phone': '.telephone a',
                'fax': '.fax p',
                'emails': '.email a',
            },
            "links": {
                'socials': '.social__media a',
            }
        }
        
        for selector_category, selectors_data in selectors.items():
            for _, selector_value in selectors_data.items():
                
                # Get text or links
                if selector_category == "texts":
                    values = self.get_texts(selector_value)
                else:
                    values = self.get_attribs(selector_value, "href")
                
                # Clean and save value
                values_clean = list(map(
                    lambda value: value.strip().replace("\n", ""), values
                ))
                value_formatted = ", ".join(values_clean)
                data.append(value_formatted)
            
        return data
    
    def scrape_business(self):
        """ Scrape all the business data, and save in excel
        """
        
        # Show status
        print("Scraping all business...")
        
        # Load home page
        self.set_page(self.home_page)
        
        # Selectors and counters
        selector_links = ".letter-block ul > li > a"
        business_index = 0
        business_num = len(self.get_elems(selector_links))
        
        # Extract each business
        while True:
            
            # End loop when no more business
            if business_index >= business_num:
                break

            # Debug status
            print(f"Scraping business {business_index + 1}/{business_num}")
            
            # Load home page
            sleep(20)
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
            
            # Increase counter
            business_index += 1
            sleep(20)
            
            # Write data in excel
            self.ss_manager.write_data(
                [business_data],
                start_row=business_index + 1
            )
            self.ss_manager.save()


if __name__ == "__main__":
    scraper = Scraper()
    data = scraper.scrape_business()
    print(data)