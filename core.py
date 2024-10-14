import os
import signal
import subprocess
import logging

from selenium import webdriver


logging.basicConfig(level=logging.INFO)


def start_chrome(profile: str, port=9223):
    """
    Start Chrome with the specified profile and debugging port.
    
    Args:
        profile (str): The Chrome profile directory name.
        port (int): The remote debugging port (default: 9223).
    
    Returns:
        int: The process ID (PID) of the started Chrome instance.
    """
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    
    cmd = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        f"--profile-directory={profile}"
    ]
    
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    chrome_log_file = os.path.join(log_dir, f"chrome-{profile}-startup.log")
    
    with open(chrome_log_file, 'a') as log_file:
        process = subprocess.Popen(cmd, stdout=log_file, stderr=log_file)
    
    logging.info(f"Profile - {profile}, Started Chrome with PID {process.pid}. Logs are being written to {chrome_log_file}")
    return process.pid


def run(profile, fn):
    """
    profile: 指定 profile 名称
    fn: 执行函数，函数参数为 Chrome WebDriver 对象
    """

    pid = None
    try:
        port = 9223
        pid = start_chrome(profile, port)
        logging.info(f"Profile - {profile}, started chrome with pid: {pid}")

        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(options=options)

        try:
            fn(driver)
        
        finally:
            driver.close()
    
    except Exception as e:
        logging.error(f"Profile - {profile}, error: {e}")

    finally:
        # kill chrome
        if pid:
            logging.info(f"Profile - {profile}, killing chrome with pid: {pid}")
            os.kill(pid, signal.SIGKILL)
