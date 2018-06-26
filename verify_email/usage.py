from verify_email import validate_email

emails = ["k.akshay9721@gmail.com", "xyz231312dasdaf@gmail.com", "foo@bar.com", "ex@example.com"]  # add emails
queue = []

# Single version
email = 'k.akshay9721@gmail.com'
result = validate_email(email, mass=False, debug=True)
print(result, email)

# Mass version
result = validate_email(emails, mass=True, debug=True)
print(result, emails)
