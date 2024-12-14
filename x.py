from playwright.sync_api import Playwright, sync_playwright, expect
import csv
import json
import os
<<<<<<< HEAD
from settings import api_base_url
from Confirmation import TempMailAPI
=======
import time
>>>>>>> 60a338b00b2dd654d302b7b59e23f7565b8f3ab9

os.system('echo off')

class ReadFIle:
    def __init__(self, url_file, login_file):
        self.url_file = url_file
        self.login = login_file
        self.headers = ['email', 'password']

    @property
    def Links(self) -> list:
        with open(self.url_file) as file:
            return json.load(file)

    @property
    def login_data(self) -> list:
        login_data = []
        with open(self.login, 'r', newline='') as file:
            reader = csv.DictReader(file, fieldnames=self.headers, delimiter=',')
            next(reader)
            for row in reader:
                email, password = row.values()
                login_data.append((email, password))
        return login_data


def run(playwright: Playwright, login_info: tuple, links: list) -> Playwright:
    screenshot_path = os.path.join(os.getcwd(), 'screenshots', '{}.png'.format(login_info[0]))
    # retry mechanism
    for _ in range(2):
        try:
            browser = playwright.chromium.launch(headless=False, slow_mo=50)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://x.com/")

            # Login Process
            page.get_by_test_id("loginButton").click()
            time.sleep(2)

            page.locator("label div").nth(3).click()
            time.sleep(2)

            email_field = page.get_by_label("Phone, email, or username")
            email_field.fill(login_info[0])
            time.sleep(2)
            email_field.press("Enter")
            auth = page.locator('h2',has_text="Authenticate your account")
            if auth.is_visible():
                input('press any key')
            page.get_by_label("Password", exact=True).fill(login_info[1])
            page.get_by_label("Password", exact=True).press("Enter")
            confirmation = page.get_by_test_id("ocfEnterTextTextInput")
            if confirmation.is_visible():
                mail = TempMailAPI(api_base_url)
                email = mail.create_custom_email(login_info[0])
                confirmation.fill(email)
                code = mail.fetch_verification_code
                #I still need the Dom object for this page to know where and how to interact with it
                
                confirmation.press("Enter")

            for i in range(len(links)):
                page.goto(links[i])
                time.sleep(3)
                reply_buttons = page.locator("button[data-testid='reply']")
                reply_buttons.nth(1).click()
                time.sleep(2)
                page.get_by_role("textbox", name="Post text").fill("Nice")
                time.sleep(2)
                page.get_by_test_id("tweetButton").click()
                time.sleep(3)

                page.screenshot(path=screenshot_path)
            return True
        except Exception as exc:
            print(exc)
        finally:
            # Clean up
            context.close()
            browser.close()


def main():
    file_reading = ReadFIle(url_file='urls.json', login_file='login.csv')
    login_data: list = file_reading.login_data
    URLs: list = file_reading.Links
    with sync_playwright() as playwright:
        for i in range(len(login_data)):
            run(playwright, login_data[i], URLs)


if __name__ == '__main__':
    main()
