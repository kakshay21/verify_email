from datetime import datetime
from verify_email import validate_email
from verify_email import get_mx_ip

import multiprocessing


emails = [] # add emails
b = datetime.now()

def validate(email):
    a = datetime.now()
    value = validate_email(email, verify=True)
    delta = datetime.now() - a
    print(value, email, (delta.microseconds + delta.microseconds/1E6))

def lookup(email):
    hostname = email[email.find('@') + 1:]
    max_hosts = get_mx_ip(hostname)
    return max_hosts

    pool = multiprocessing.Pool()
    result = pool.map(lookup, emails)
    finalresult = pool.map(validate, emails)
    delta = datetime.now() - b
    print(delta.seconds + delta.microseconds/1E6)