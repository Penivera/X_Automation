from Confirmation import TempMailAPI
from settings import api_base_url
mail = TempMailAPI(base_url=api_base_url,email='john@undeep.xyz')
email =mail.create_custom_email('john@undeep.xyz')

mail.fetch_verification_code
