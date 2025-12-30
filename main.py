import scraper_1mg
import time

def main():
    print("Hello from medmgmnt!")
    
    # Test get_driver() method from scraper_1mg
    print("Testing get_driver()...")
    driver = scraper_1mg.get_driver()
    
    if driver is not None:
        try:
            scraper_1mg.open_homepage(driver)
            print("running find search input")
            scraper_1mg.find_search_input(driver)
            print("searching dolo650")
            scraper_1mg.search_medicine(driver, "dolo650")
            #time.sleep(10)
            print(f"Title: {driver.current_url}")
            # print(f"PageSource:{driver.page_source}")
        finally:
            driver.quit()
    else:
        print("✗ Error: get_driver() returned None")

    
    
    #load config
    #calls scraper
    #calls summariser
    #save artifacts
    #handle errors

    


if __name__ == "__main__":
    main()
