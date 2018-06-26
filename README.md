# verify-email 

`verify-email` can verify the email by efficiently checking the domain name and pinging the handler to verify its existence.

## Features

- Syntax checks
- MX(Mail Exchange records) verification
- Handler verification
- Cache domain lookups (For multiple emails)
- Multithread support (look in [usage.py](https://github.com/kakshay21/verify_email/blob/master/verify_email/usage.py))
- Multiprocess efficient (look in [fast_verify.py](https://github.com/kakshay21/verify_email/blob/master/verify_email/fast_verify.py))

## Compatibility
- It is written in Python 2.7.
- Not tested in python3.X.
- It should work on Linux, Mac and Windows.

## Installation
### From [pypi.org](https://pypi.org/project/verify-email/)
```
$ pip install verify-email
```
### From source code
```
$ git clone https://github.com/kakshay21/verify_email
$ cd verify_email
$ virtualenv env
$ source env/bin/activate
$ python setup.py develop
```

## Usage
### For single email
```
>>> from verify_email.verify_email import validate_email
>>> validate_email("foo@bar.com", mass=False)
False
```
### For multiple emails
```
>>> emails = ["foo@bar.com", "example@foo.com"]
>>> validate_email(emails, mass=True)
[False, False]
```
### Multithreaded Version (Single/Multiple emails)
```
>>> from verify_email.verify_email import fast_validate_email
>>> fast_validate_email("foo@bar.com", mass=False)
False
```
see for more details [usage.py](https://github.com/kakshay21/verify_email/blob/master/verify_email/usage.py)

## Contribute
- Issue Tracker: https://github.com/kakshay21/verify_email/issues
- Source Code: https://github.com/kakshay21/verify_email

## Support
If you are having issues, please create an issue for it.
