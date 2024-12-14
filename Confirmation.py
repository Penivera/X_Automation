import requests
import time
import re
import random
from bs4 import BeautifulSoup
from settings import api_base_url

class TempMailAPI:
    def __init__(self, rapidapi_key: str=None, base_url: str = "API LINK HERE ",email=None):
        self.headers = {
            "x-rapidapi-key": 'fea0c8351dmsh217155a16a6e35fp15a233jsn7c8b2bae0795',
            "x-rapidapi-host": "temp-mail-api3.p.rapidapi.com"
        }
        self.base_url = base_url
        self.email_address = email


    def create_custom_email(self, email,proxy=None):
        """
        Generates a new temporary email address with a randomly selected domain.
        """
        url = f"{self.base_url}/email"
        payload = { "email":email}
        proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

        response = requests.post(url, json=payload, headers=self.headers, proxies=proxy_dict)

        if response.status_code == 200:
            try:
                self.email_address = response.json().get("email")
                if self.email_address:
                    print("Email created:", self.email_address)
                    return self.email_address or None
                else:
                    print("Error: Email address not found in response.")
            except Exception as e:
                print(f"Error creating email: {e}")
        else:
            print("Failed to create email. Status code:", response.status_code)
        return False

    @property
    def fetch_verification_code(self):

        if self.email_address:
            for i in range(3):
                print(f"[INFO] Fetching messages for email: {self.email_address}")

                try:
                    # Fetch messages
                    messages_url = f"{self.base_url}/messages/{self.email_address}"
                    messages_response = requests.get(messages_url, headers=self.headers)
                    messages_data = messages_response.json()
                    print(messages_data)
                    
                    for message in messages_data:
                        if isinstance(message, dict) and 'content' in message:
                            match = re.search(r"(\d{6})", message['content'])
                            if match:
                                print(f"[INFO] Verification code found: {match.group(1)}")
                                return match.group(1)

                except requests.RequestException as e:
                    print(f"[ERROR] Error fetching messages: {e}")
                    time.sleep(5)


            print("[INFO] Max wait time reached. No verification code found.")
            return None

    
    def __get_domains(self):
        domian_url = f'{api_base_url}/domains'
        response = requests.get(domian_url, headers=self.headers)
        response = response.json()
        return response.get('domains') or ["dunkos.xyz","smallntm.lol","undeep.xyz"]

    @staticmethod
    def extract_verification_code_from_html(html_content):
        """
        Extracts the verification code from the HTML content using BeautifulSoup.
        """
        if not html_content:
            return None

        try:
            soup = BeautifulSoup(html_content, "html.parser")
            match = re.search(r"(\d{6})", soup.get_text())
            if match:
                return match.group(1)
        except Exception as e:
            print(f"[ERROR] HTML parsing failed: {e}")
        return None