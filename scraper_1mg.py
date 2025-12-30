#This code scrapes details from 1mg using selenium

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from typing import Any
from Selenium_utilis import wait_present, wait_visible


def get_driver(headless: bool = False) -> webdriver.Chrome:
    """
    Creates and returns a Chrome WebDriver instance with configured options.
    
    This function sets up a Selenium Chrome driver using WebDriver Manager to automatically
    handle ChromeDriver installation and version management. It configures Chrome options
    including headless mode (if requested) and window size.
    
    Args:
        headless (bool): If True, runs Chrome in headless mode (no GUI). Defaults to False.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance ready for use.
    
    Steps:
        1. Create ChromeOptions object to configure Chrome browser behavior
        2. If headless is True, add '--headless' argument to run browser without GUI
        3. Set window size to 1280x800 pixels for consistent viewport
        4. Create Service object using ChromeDriverManager to automatically manage driver
        5. Initialize and return Chrome WebDriver with the configured options and service
    """
    # Create ChromeOptions object to configure browser settings
    chrome_options = Options()
    
    # Enable headless mode if requested (runs browser without visible window)
    if headless:
        chrome_options.add_argument('--headless')
    
    # Set browser window size to 1280x800 pixels for consistent rendering
    chrome_options.add_argument('--window-size=1280,800')
    
    # Create Service object using ChromeDriverManager to automatically download and manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    # Create and return Chrome WebDriver instance with configured options and service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver


def open_homepage(driver: webdriver.Chrome) -> None:
    """
    Opens the 1mg homepage and waits for the page body to be present.
    
    This function navigates to https://www.1mg.com/ and waits for the body element
    to be present in the DOM to ensure the page has loaded.
    
    Args:
        driver (webdriver.Chrome): The WebDriver instance to use for navigation.
    
    Returns:
        None
    
    Raises:
        TimeoutError: If the body element is not present within the timeout period.
    """
    # Navigate to the 1mg homepage
    driver.get("https://www.1mg.com/")
    
    # Wait for the body element to be present in the DOM to ensure page has loaded
    print("wait for the driver")
    wait_present(driver, By.TAG_NAME, "body")


def find_search_input(driver: webdriver.Chrome) -> WebElement:
    """
    Finds and returns the search input element on the 1mg homepage.

    This function tries a series of CSS selectors (in order) using an explicit
    visibility wait. It returns the first WebElement that becomes visible.
    If none of the selectors match within their timeouts, it raises an
    exception listing all selectors that were tried.

    The selectors are tried in this order:
        1. "css: input[id='search-medicine']"
        2. "css: input[placeholder='Search for Medicines and Health Products']"

    Args:
        driver (webdriver.Chrome): The WebDriver instance currently on the 1mg homepage.

    Returns:
        WebElement: The located and visible search input element.

    Raises:
        Exception: If none of the configured selectors locate a visible element.
    """
    selectors = [
        "css: input[id='search-medicine']",
        "css: input[placeholder='Search for Medicines and Health Products']",
    ]

    for selector in selectors:
        strategy, value = selector.split(":", 1)
        strategy = strategy.strip().lower()
        locator = value.strip()

        if strategy == "css":
            by = By.CSS_SELECTOR
        else:
            by = By.CSS_SELECTOR

        try:
            element = wait_visible(driver, by, locator)
            print(f"Search input found using selector: {selector}")
            return element
        except TimeoutError:
            continue

    raise Exception(
        "Could not locate search input. Tried selectors: "
        + ", ".join(selectors)
    )


def search_medicine(driver: webdriver.Chrome, query: str) -> None:
    """
    Placeholder for future search implementation.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        query (str): Search query text.
    """
    pass
