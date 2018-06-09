from verify_email import validate_email
from verify_email import get_mx_ip

emails = [] # add emails

for email in emails:
    result = validate_email(email, debug=True)
    print(result)