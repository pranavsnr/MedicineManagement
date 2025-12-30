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
           # print("running find search input")
            scraper_1mg.find_search_input(driver)
            print("searching dolo650")
            scraper_1mg.search_medicine(driver, "dolo650")
            result = scraper_1mg.open_first(driver, "dolo650")
            #print(f"Result URL: {result['url']}")
            print(f"Result Title: {result['title']}")
            if not scraper_1mg.title_matches_query(result['title'], "dolo650"):
                print("Match not found")
            summary = scraper_1mg.extract_medicine_summary(driver)
            print(f"Extracted Summary - Title: {summary['title']}")
            print(f"Extracted Summary - URL: {summary['url']}")
            print(f"Extracted Sections: {list(summary['sections'].values())[0]}")
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
