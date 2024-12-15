from Confirmation import TempMailAPI
from settings import api_base_url
from faker import Faker
mail = TempMailAPI(base_url=api_base_url,email='john@undeep.xyz')
fake = Faker()
name = fake.name()
email =mail.create_custom_email('{}@undeep.xyz'.format(name))
print(email)
print(mail.fetch_verification_code)
