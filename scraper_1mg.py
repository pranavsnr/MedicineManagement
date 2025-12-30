#This code scrapes details from 1mg using selenium

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import Any, Dict
from Selenium_utilis import wait_present, wait_visible
import re


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
    Searches for a medicine on the 1mg website using the provided query.
    
    This function locates the search input field, clears it, enters the search query,
    submits the search by pressing Enter, and waits for the search results to load.
    It waits for either the URL to change from the homepage or for a result container
    element to appear on the page.
    
    Args:
        driver (webdriver.Chrome): The WebDriver instance currently on the 1mg homepage.
        query (str): The medicine name or search term to query (e.g., "dolo650").
    
    Returns:
        None
    
    Raises:
        TimeoutError: If search results do not load within the timeout period.
        Exception: If the search input element cannot be found.
    """
    # Get the current URL to detect if it changes after search
    homepage_url = driver.current_url
    
    # Find and interact with the search input element
    search_input = find_search_input(driver)
    search_input.click()
    search_input.clear()
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
    
    # Wait for search results to load - check if URL changed or result container appears
    try:
        # Try waiting for URL to change from homepage
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, 10)
        wait.until(lambda d: d.current_url != homepage_url)
    except TimeoutException:
        # If URL didn't change, wait for result container element to appear
        result_selectors = [
            (By.CSS_SELECTOR, "[class*='search-result']"),
            (By.CSS_SELECTOR, "[class*='result-container']"),
            (By.CSS_SELECTOR, "[class*='product-list']"),
            (By.CSS_SELECTOR, "[class*='search-results']"),
        ]
        
        result_found = False
        for by, locator in result_selectors:
            try:
                wait_present(driver, by, locator)
                result_found = True
                break
            except TimeoutError:
                continue
        
        if not result_found:
            raise TimeoutError(
                f"Search results did not load after searching for '{query}'. "
                "URL did not change and no result container elements were found."
            )

def open_first(driver: webdriver.Chrome, query: str, timeout: int = 15) -> Dict[str, str]:
    """
    Opens the first medicine result from search results in a new tab and returns its URL and title.
    
    This function assumes the first result opens in a new tab (target="_blank"). It stores
    the current window handle, finds the first medicine result link using fallback selectors,
    scrolls it into view, clicks it, waits for a new tab to appear, switches to it, and
    returns the URL and title of the new tab.
    
    Args:
        driver (webdriver.Chrome): The WebDriver instance on the search results page.
        query (str): The search query that was used (for debugging purposes).
        timeout (int): Maximum time in seconds to wait for elements and new tab. Defaults to 15.
    
    Returns:
        Dict[str, str]: A dictionary with 'url' and 'title' keys containing the new tab's URL and title.
    
    Raises:
        Exception: If no medicine result links are found or if a new tab does not appear.
        TimeoutError: If elements do not appear within the timeout period.
    """
    # Store the current window handle before clicking
    before_handle = driver.current_window_handle
    print(f"Stored current window handle: {before_handle}")
    
    # Define selectors to try in order
    selectors = [
        "CSS: div[class*='product-box'] a[href^='/drugs/']",
        "CSS: a[href^='/drugs/']",
    ]
    
    # Find the first medicine result link using fallback strategy
    first_link = None
    used_selector = None
    
    for selector in selectors:
        strategy, value = selector.split(":", 1)
        strategy = strategy.strip().upper()
        locator = value.strip()
        
        if strategy == "CSS":
            by = By.CSS_SELECTOR
        else:
            by = By.CSS_SELECTOR
        
        try:
            # Wait until at least one element is present/visible
            wait_present(driver, by, locator, timeout=timeout)
            elements = driver.find_elements(by, locator)
            if elements:
                first_link = elements[0]
                used_selector = selector
                print(f"Found medicine result link using selector: {selector}")
                break
        except TimeoutError:
            continue
    
    if first_link is None:
        raise Exception(
            f"Could not locate medicine result link. Tried selectors: {', '.join(selectors)}"
        )
    
    # Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_link)
    
    # Try clicking the element, fallback to JS click if it fails
    try:
        first_link.click()
        print("Clicked medicine result link using standard click")
    except Exception as e:
        print(f"Standard click failed: {e}, trying JavaScript click")
        driver.execute_script("arguments[0].click();", first_link)
        print("Clicked medicine result link using JavaScript click")
    
    # Wait until new tab appears
    print("Waiting for new tab to appear...")
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(lambda d: len(d.window_handles) > 1)
        print("New tab detected")
    except TimeoutException:
        raise Exception(
            f"New tab did not appear within {timeout} seconds after clicking the medicine result link"
        )
    
    # Get all window handles and switch to the new one
    all_handles = driver.window_handles
    new_handle = [h for h in all_handles if h != before_handle][0]
    driver.switch_to.window(new_handle)
    print(f"Switched to new tab with handle: {new_handle}")
    
    # Get URL and title of the new tab
    new_url = driver.current_url
    new_title = driver.title
    print(f"New tab URL: {new_url}")
    print(f"New tab title: {new_title}")
    
    return {"url": new_url, "title": new_title}


def title_matches_query(page_title: str, query: str) -> bool:
    """
    Checks if all tokens from the query appear in the page title.
    
    Normalizes both strings to lowercase, removes punctuation, keeps only
    letters, numbers, and spaces. Splits the query into tokens and verifies
    that every token appears in the normalized page title.
    
    Args:
        page_title (str): The page title to check against.
        query (str): The search query to match.
    
    Returns:
        bool: True if every token from the query appears in the page title, False otherwise.
    """
    # Normalize to lowercase and remove punctuation, keep only letters, numbers, and spaces
    normalized_title = re.sub(r'[^\w\s]', '', page_title.lower())
    normalized_query = re.sub(r'[^\w\s]', '', query.lower())
    
    # Split query into tokens (words/numbers) - first by whitespace, then split alphanumeric sequences
    query_tokens = []
    for word in normalized_query.split():
        # Split alphanumeric sequences into separate letter and number groups
        # e.g., "dolo650" becomes ["dolo", "650"]
        tokens = re.findall(r'[a-z]+|\d+', word)
        query_tokens.extend(tokens)
    
    # Check if every token appears in the normalized title
    for token in query_tokens:
        if token not in normalized_title:
            return False
    
    return True
