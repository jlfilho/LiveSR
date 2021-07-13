import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

def video_session(url = "http://192.168.100.20:8080/live/abrLoLP_index.html", process_id = "0",\
    run_time = 30, default_chrome_user_dir = '../../share/abr_browser_dir/chrome_data_dir',
    chrome_driver = '../../share/abr_browser_dir/chromedriver_linux64/chromedriver', url_mpd = "http://192.168.100.20:8080/dash/football.mpd"):

    # copy over the chrome user dir    
    chrome_user_dir = '/tmp/chrome_user_dir_id_' + process_id
    os.system('rm -r ' + chrome_user_dir)
    os.system('cp -r ' + default_chrome_user_dir + ' ' + chrome_user_dir)

    options=Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-data-dir=' + chrome_user_dir)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    options.add_argument('--window-size=650,500')
    driver=webdriver.Chrome(chrome_driver, options=options)
    try:
        driver.set_page_load_timeout(run_time)
        driver.get(url)
        #element = wait(driver, 30).until(EC.visibility_of_element_located((By.ID, "url-mpd")))
        #driver.find_element_by_id("url-mpd").clear()
        #element.send_keys(url_mpd)
        #element.send_keys(Keys.TAB)
        sleep(run_time)
    except Exception as e:
        print(e)
    finally:
        driver.close()



if __name__ == "__main__":
    # execute only if run as a script
    video_session()