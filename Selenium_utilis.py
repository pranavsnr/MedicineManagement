from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from typing import Union


def wait_visible(driver: webdriver.Chrome, by: Union[By, str], locator: str, timeout: int = 10) -> WebElement:
    """
    Waits for an element to be visible on the page and returns it.
    
    This function uses WebDriverWait with expected_conditions to wait for an element
    to become visible (displayed and has dimensions) within the specified timeout period.
    
    Args:
        driver (webdriver.Chrome): The WebDriver instance to use for waiting.
        by (Union[By, str]): The locator strategy (e.g., By.ID, By.XPATH, By.CSS_SELECTOR).
        locator (str): The locator value to find the element (e.g., element ID, XPath expression).
        timeout (int): Maximum time in seconds to wait for the element. Defaults to 10.
    
    Returns:
        WebElement: The visible WebElement once it becomes visible.
    
    Raises:
        TimeoutError: If the element does not become visible within the timeout period.
                     The error message includes the by strategy and locator value.
    
    Example:
        element = wait_visible(driver, By.ID, "my-element-id", timeout=15)
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.visibility_of_element_located((by, locator)))
        return element
    except TimeoutException:
        raise TimeoutError(f"Element not visible within {timeout} seconds. By: {by}, Locator: {locator}")


def wait_present(driver: webdriver.Chrome, by: Union[By, str], locator: str, timeout: int = 10) -> WebElement:
    """
    Waits for an element to be present in the DOM and returns it.
    
    This function uses WebDriverWait with expected_conditions to wait for an element
    to be present in the DOM (may not be visible) within the specified timeout period.
    
    Args:
        driver (webdriver.Chrome): The WebDriver instance to use for waiting.
        by (Union[By, str]): The locator strategy (e.g., By.ID, By.XPATH, By.CSS_SELECTOR).
        locator (str): The locator value to find the element (e.g., element ID, XPath expression).
        timeout (int): Maximum time in seconds to wait for the element. Defaults to 10.
    
    Returns:
        WebElement: The WebElement once it is present in the DOM.
    
    Raises:
        TimeoutError: If the element is not present in the DOM within the timeout period.
                     The error message includes the by strategy and locator value.
    
    Example:
        element = wait_present(driver, By.XPATH, "//div[@class='container']", timeout=15)
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, locator)))
        return element
    except TimeoutException:
        raise TimeoutError(f"Element not present within {timeout} seconds. By: {by}, Locator: {locator}")


def wait_clickable(driver: webdriver.Chrome, by: Union[By, str], locator: str, timeout: int = 10) -> WebElement:
    """
    Waits for an element to be clickable and returns it.
    
    This function uses WebDriverWait with expected_conditions to wait for an element
    to be both visible and enabled (clickable) within the specified timeout period.
    
    Args:
        driver (webdriver.Chrome): The WebDriver instance to use for waiting.
        by (Union[By, str]): The locator strategy (e.g., By.ID, By.XPATH, By.CSS_SELECTOR).
        locator (str): The locator value to find the element (e.g., element ID, XPath expression).
        timeout (int): Maximum time in seconds to wait for the element. Defaults to 10.
    
    Returns:
        WebElement: The clickable WebElement once it becomes clickable.
    
    Raises:
        TimeoutError: If the element does not become clickable within the timeout period.
                     The error message includes the by strategy and locator value.
    
    Example:
        button = wait_clickable(driver, By.CSS_SELECTOR, "button.submit-btn", timeout=15)
    """
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, locator)))
        return element
    except TimeoutException:
        raise TimeoutError(f"Element not clickable within {timeout} seconds. By: {by}, Locator: {locator}")

