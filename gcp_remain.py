import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml

from core import run


def load_accounts() -> list[dict]:
    with open("accounts.yml", "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_gcp_remain_quota(driver, credits_url):
    driver.get(credits_url)

    el = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/pan-shell/pcc-shell/cfc-panel-container/div/div/cfc-panel/div/div/div[3]/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-container/div/div/cfc-panel[2]/div/div/central-page-area/div/div/pcc-content-viewport/div/div/pangolin-home-wrapper/pangolin-home/cfc-router-outlet/div/ng-component/cfc-single-panel-layout/cfc-panel-container/div/div/cfc-panel/div/div/cfc-panel-body/cfc-virtual-viewport/div[1]/div/mat-tab-nav-panel/cfc-router-outlet/div/ng-component/cfc-tree-grid/cfc-table/div[2]/cfc-table-columns-presenter-v2/div/div[3]/table/tbody/tr/td[4]/p'))
    )
    return el.text


def main():
    accounts: dict = load_accounts()
    logging.info(f"accounts: {accounts}")

    for email, config in accounts.items():
        profile = config.get("profile")
        if not profile:
            logging.error(f"profile not found: {config}")
            continue

        def check_gcp_remain(driver):
            credits_url = config.get("credits_url")
            if not credits_url:
                logging.error(f"Profile - {profile}, credits_url not found: {email}")
                return

            logging.info(f"Profile - {profile}, credits_url: {credits_url}")
            remain_quota = get_gcp_remain_quota(driver, credits_url)
            remain_quota = float(remain_quota.replace("$", "").replace(",", ""))
            logging.info(f"Profile - {profile}, remain_quota: {remain_quota}")

        run(profile, check_gcp_remain)
        

if __name__ == "__main__":
    main()
