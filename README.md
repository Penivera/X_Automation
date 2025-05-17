##Twitter Raid Bot Automation

This project automates the creation of Twitter (X) accounts using a temporary email service and utilizes those accounts to engage with specific posts at scale — useful for orchestrated raids (likes, retweets, replies) or botnet simulations.

Features

Temporary Email API Integration: Automatically fetches disposable email addresses for account registration.

OTP Verification: Extracts and confirms Twitter OTPs from inbox.

Automated Account Creation: Creates and verifies Twitter accounts without manual input.

Post Raiding Functionality: Uses the accounts to like, retweet, or comment on a given post URL.

Session Persistence: Stores account sessions (cookies/tokens) for reuse and scalability.


Tech Stack

Python (core automation)

Selenium / undetected-chromedriver (optional for stealth)

Temp Mail API (e.g., 1secmail, mail.tm, or custom)

Twitter web endpoints (non-API interactions)

Optional: Proxy support for IP rotation


Setup

1. Clone the repo


2. Install dependencies:

pip install -r requirements.txt


3. Add your temp mail API keys and Twitter target details in config.py


4. Run:

python main.py



Notes

Designed for educational and research purposes.

Avoid using on your main IP. Use proxies or containerized environments.

Twitter may rate-limit or ban accounts quickly — rotate IPs and user agents.


TODO

Improve human-like behavior (typing, delays, already implemented but vould be better )

Integrate captcha solving (e.g., 2Captcha)

Add CLI or dashboard for campaign control
