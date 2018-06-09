from verify_email import validate_email

emails = ["k.akshay9721@gmail.com", "xyz231312dasdaf@gmail.com", "foo@bar.com", "ex@example.com"]  # add emails

for email in emails:
    result = validate_email(email, debug=True)
    print(result)
