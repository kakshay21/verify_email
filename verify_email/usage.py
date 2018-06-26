from verify_email import validate_email
from verify_email import fast_validate_email
from datetime import datetime

emails = ["k.akshay9721@gmail.com", "xyz231312dasdaf@gmail.com", "foo@bar.com", "ex@example.com"]  # add emails
queue = []

# Single email version
email = 'akshaysharma9721@gmail.com'
b = datetime.now()
result = validate_email(email, mass=False)
delta = datetime.now() - b
print(result, email)
print(delta.total_seconds())

c = datetime.now()
result = fast_validate_email(email, mass=False)
delta = datetime.now() - c
print(result, email)
print(delta.total_seconds())

# Mass email version
d = datetime.now()
result = validate_email(emails, mass=True)
delta = datetime.now() - d
print(result, emails)
print(delta.total_seconds())

e = datetime.now()
result = fast_validate_email(emails, mass=True)
delta = datetime.now() - e
print(result, emails)
print(delta.total_seconds())
