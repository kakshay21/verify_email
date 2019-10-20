from datetime import datetime
from verify_email import verify_email

import multiprocessing


emails = ["k.akshay9721@gmail.com", "xyz231312dasdaf@gmail.com", "foo@bar.com", "ex@example.com"]  # add emails
b = datetime.now()


def validate(email):
    a = datetime.now()
    value = verify_email(email)
    delta = datetime.now() - a
    print(value, email, (delta.microseconds + delta.microseconds/1E6))


pool = multiprocessing.Pool()
result = pool.map(validate, emails)
delta = datetime.now() - b
print(delta.total_seconds())
