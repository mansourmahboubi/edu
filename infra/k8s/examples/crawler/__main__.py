from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests

# AddCookieParameters

import time
from typing import List


# Close the browser
# driver.quit()
def login(driver: webdriver.Firefox) -> None:
    a = "https://trainingportal.linuxfoundation.org/learn/sign_in?return_to=%2Flearn%2Fcourse%2Fkubernetes-fundamentals-lfs258%2Fexam-domain-review%2Fdomain-review%3Fpage%3D1"
    # Open the login page
    driver.get(a)

    # Wait for the page to load
    time.sleep(2)

    # # Find the username and password fields and enter your credentials
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys("mansourmahboubi")
    password_field.send_keys(")%Bk~P63?-*p'58")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)


def get_urls() -> List[str]:
    urls = []
    with open("results.txt", "r") as file:
        for line in file:
            urls.append(line.strip())
    return urls


def store_main_topic(driver: webdriver.Firefox, url: str, file_name: str) -> None:
    driver.get(url)
    time.sleep(3)
    # Find the element with the class name "editor-content"
    element = driver.find_element(By.CLASS_NAME, "topic__container")
    # Get the text content of the element
    text = element.get_attribute("innerHTML")
    with open(f"files/{file_name}", "w") as file:
        file.write(text)


def download_pdf_from_url(pdf_url, file_name):
    response = requests.get(pdf_url, allow_redirects=True)
    if response.status_code == 200:
        with open(f"files/videos/{file_name}", "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully: {file_name}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def download_pdf(driver: webdriver.Firefox, url: str, pdf_file_name: str) -> None:
    driver.get(url)
    time.sleep(3)
    try:
        element = driver.find_element(By.ID, "pdf-viewer")
    except Exception as e:
        print("No pdf-viewer found")
        return
    if element:
        print("Found pdf-viewer")
        driver.switch_to.frame("pdf-viewer")
        time.sleep(3)
        pdf_url = driver.execute_script("return window.options.pdfAsset")
        download_pdf_from_url(pdf_url, pdf_file_name)


def find_video_url(text: str):
    import re

    # Sample text containing the URL
    # text = "sdsadasdaddashttp://embed.wistia.com/deliveries/9997c2b06070305cf4cf7509eb0ca21eb559350f.bin"

    # Define the regex pattern
    pattern = r"https://embed.*?\.bin"

    # Search for the pattern in the text
    match = re.search(pattern, text)

    # Check if a match is found and print it
    if match:
        print("Extracted URL:", match.group())
        # replace.bin with .mp4

        print(match.group().replace(".bin", ".mp4"))
        text = match.group().replace(".bin", ".mp4")
        # remove "url":
        text = text.replace('"url":', "")
        # remove quotes
        return text
    else:
        print("No match found.")


if __name__ == "__main__":
    # with open("test.html", "r") as file:
    #     text = file.read()
    #     find_video_url(text)
    driver = webdriver.Firefox()
    urls = get_urls()

    login(driver)

    for index, url in enumerate(urls):
        file_name = f"{index}-{url.split('/')[-2]}.html"
        pdf_file_name = f"{index}-{url.split('/')[-2]}.pdf"
        video_file_name = f"{index}-{url.split('/')[-2]}.mp4"

        with open(f"files/html/{file_name}", "r") as file:
            text = file.read()
            if "wistia" in text:
                print("Found wistia")
            else:
                print("No wistia found")
                continue

        driver.get(url)
        time.sleep(3)
        # find class w-json-ld
        element = driver.find_element(By.CLASS_NAME, "w-json-ld")
        import json

        data = json.loads(element.get_attribute("innerHTML"))
        video = data["embedUrl"]
        driver.get(video)
        time.sleep(3)
        file_url = find_video_url(driver.page_source)
        download_pdf_from_url(file_url, video_file_name)

        # download_pdf(driver, url, pdf_file_name)
        # store_main_topic(driver, url, file_name)
        time.sleep(1)
    driver.quit()
