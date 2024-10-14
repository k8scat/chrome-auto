import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core import run


def get_profile_email(driver):
    driver.get("https://myaccount.google.com/email")

    el = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/article/ul/li/div/div/div'))
    )
    return el.text


def main():
    profiles = ["Default"]

    for profile in profiles:
        def print_profile_email(driver):
            email = get_profile_email(driver)
            logging.info(f"Profile - {profile}, email: {email}")

        run(profile, print_profile_email)
        

if __name__ == "__main__":
    main()
