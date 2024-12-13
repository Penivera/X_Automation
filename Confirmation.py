import requests
import time
import re
import random
from bs4 import BeautifulSoup
from settings import api_base_url
from faker import Faker

class TempMailAPI:
    def __init__(self, rapidapi_key: str=None, base_url: str = "API LINK HERE ", max_wait_time=120, check_interval=20):
        self.headers = {
            "x-rapidapi-key": 'ed76df9621mshadb676447228e13p1a5bfbjsn7c4304a0b1c9',
            "x-rapidapi-host": "temp-mail-api3.p.rapidapi.com"
        }
        self.base_url = base_url
        self.email_address = None
        self.max_wait_time = max_wait_time
        self.check_interval = check_interval
        self.domain_list = self.__get_domains()
        self.consecutive_warnings = 0

    def create_custom_email(self, proxy=None):
        """
        Generates a new temporary email address with a randomly selected domain.
        """
        domain = random.choice(self.domain_list)
        fake = Faker()
        url = f"{self.base_url}/email"
        email = '_'.join([fake.word() for _ in range(2)])
        payload = { "email":f'{email}@{domain}'}
        proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

        response = requests.post(url, json=payload, headers=self.headers, proxies=proxy_dict)

        if response.status_code == 200:
            try:
                email_address = response.json().get("email")
                if email_address:
                    print("Email created:", email_address)
                    return email_address or None
                else:
                    print("Error: Email address not found in response.")
            except Exception as e:
                print(f"Error creating email: {e}")
        else:
            print("Failed to create email. Status code:", response.status_code)
        return False


    @property
    def fetch_verification_code(self):
        start_time = time.time()
        if self.email_address:
            while time.time() - start_time < self.max_wait_time:
                print(f"[INFO] Fetching messages for email: {self.email_address}")

                try:
                    # Fetch messages
                    messages_url = f"{self.base_url}/messages/{self.email_address}"
                    messages_response = requests.get(messages_url, headers=self.headers)
                    messages_response.raise_for_status()  # Raise an error for HTTP issues
                    messages_data = messages_response.json()

                    # Handle empty or invalid messages_data
                    if not messages_data or not isinstance(messages_data, list):
                        print("[WARNING] No valid messages found.")
                        self.consecutive_warnings += 1
                        
                        # Handle consecutive warnings
                        if self.consecutive_warnings >= 3:
                            print("[INFO] Three consecutive warnings detected. Sleeping for 60 seconds...")
                            time.sleep(60)
                            print("[INFO] Skipping this email due to repeated warnings.")
                            return None  # Skip processing this email
                        else:
                            time.sleep(self.check_interval)
                        continue

                    # Reset warning counter on valid messages
                    self.consecutive_warnings = 0

                    # Process messages to find the verification code
                    for message in messages_data:
                        if isinstance(message, dict) and 'content' in message:
                            match = re.search(r"(\d{6})", message['content'])
                            if match:
                                print(f"[INFO] Verification code found: {match.group(1)}")
                                return match.group(1)

                except requests.RequestException as e:
                    print(f"[ERROR] Error fetching messages: {e}")
                    time.sleep(self.check_interval)
                    continue

            print("[INFO] Max wait time reached. No verification code found.")
            return None
        raise TimeoutError('Failed to retrive mail')

    
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