import shutil
import urllib.request
import requests
import urllib3
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from random import uniform, randint
import urllib
import analyse_img
import json


def set_captcha_frames(driver):
    print("set_captcha_frames")
    global check_box_iframe, image_iframe
    time.sleep(1)
    recaptchaFrames = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))


    for frames in recaptchaFrames:
        if frames.get_attribute("title") == "reCAPTCHA":
            check_box_iframe = frames
        elif frames.get_attribute("title") == "recaptcha challenge expires in two minutes":
            image_iframe = frames


def download_image(driver):
    print("dl img")
    driver.switch_to.frame(image_iframe)
    elem = driver.find_element(By.TAG_NAME, "img")
    url = elem.get_attribute("src")
    urllib.request.urlretrieve(url, "payload.jpg")
    driver.switch_to.parent_frame()


def read_json(driver):
    print("read_json")
    driver.switch_to.frame(image_iframe)
    lookfor = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div>div>strong")))
    lookfor = lookfor.get_attribute("innerHTML")
    f = open('classes.json')
    data = json.load(f)
    number = data[lookfor]
    driver.switch_to.parent_frame()
    return int(number)


def click_verify(driver):
    print("click_verify")
    driver.switch_to.frame(image_iframe)
    verify_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "recaptcha-verify-button")))
    verify_button.click()
    driver.switch_to.parent_frame()


def check_if_done(driver):
    print("checkifdone")
    driver.switch_to.frame(image_iframe)
    canfindbluetext = driver.find_elements(By.CSS_SELECTOR, '.rc-imageselect-desc-no-canonical>span')
    driver.switch_to.parent_frame()
    if len(canfindbluetext) != 0:
        return False
    else:
        return True


def solve_type(driver):
    print("solve_type")
    driver.switch_to.frame(image_iframe)
    typeOfSolve = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.rc-imageselect-desc-no-canonical>span')))
    if typeOfSolve.get_attribute("innerHTML") == "If there are none, click skip":
        print("Solve 4 x 4")
        driver.switch_to.parent_frame()
        return "Solve 4 x 4"
    else:
        print("Solve 3 x 3")
        driver.switch_to.parent_frame()
        return "Solve 3 x 3"


def click_refresh(driver):
    print("refresh")
    driver.switch_to.frame(image_iframe)
    refresh_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "recaptcha-reload-button")))
    refresh_button.click()
    driver.switch_to.parent_frame()


def click_checkbox(driver):
    print("checkbox")
    driver.switch_to.frame(check_box_iframe)
    check_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "recaptcha-anchor")))
    time.sleep(0.4)
    check_box.click()
    driver.switch_to.parent_frame()


def click_items(driver):
    print("clickitems")
    json_data = read_json(driver)
    if read_json(driver) != 0:
        driver.switch_to.frame(image_iframe)
        click_array = analyse_img.get_click_array(json_data)
        tableGrid = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "rc-imageselect-tile")))
        for index, item in enumerate(tableGrid):
            if click_array[index]:
                item.click()
        driver.switch_to.parent_frame()
    else:
        click_refresh(driver)
        click_items(driver)



def solve_grid(driver):
    print("solvegrid")
    if check_if_done(driver) == False:
        solve_typ = solve_type(driver)
        if solve_typ == "Solve 4 x 4":
            download_image(driver)
            click_items(driver)
            driver.switch_to.parent_frame()
            click_verify(driver)
            time.sleep(1)
            solve_grid(driver)
        else:
            driver.switch_to.parent_frame()
            click_refresh(driver)
            time.sleep(1)
            solve_grid(driver)
            print("Cant do this yet")
    else:
        return True


def solveRecaptcha(browser):
    print("start")
    # Set global iFrames
    set_captcha_frames(browser)

    click_checkbox(browser)

    solve_grid(browser)











    time.sleep(4)
    #analyse_img.
    #if is 4 by 4
    #solve4x4Grid()

    #print(getImageUrl())
    #print(imageFrame)
    #driver.switch_to.frame(imageFrame)
    #driver.switch_to.parent_frame()
    #typeOfSolve = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rc-imageselect-desc-no-canonical>span')))
    #print(typeOfSolve.get_attribute("innerHTML"))

#Recheck if 4x4 or 3x3
