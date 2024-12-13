from Confirmation import TempMailAPI
from settings import api_base_url
mail = TempMailAPI(base_url=api_base_url)
email =mail.create_custom_email
print(email)
code = mail.fetch_verification_code(email)