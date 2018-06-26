# verify-email 

``verify-email`` can verify the email by efficiently checking the domain name and pinging the handler to verify its existence.

## Features
- MX(Mail Exchange records) verification
- Handler verification
- Cache domain lookups
- Parallel domain lookups and handler checks
- Syntax checks

## Compatibility
- It is written in Python 2.7.
- Not tested in python3.X.
- It should work on Linux, Mac and Windows.

## Installation
### From [pypi.org](https://pypi.org/project/verify-email/)
```
pip install verify-email
```
### From source code
```
virtualenv env 
source env/bin/activate
python setup.py develop
```

## Usage
```
>>> from verify_email.verify_email import validate_email
>>> validate_email("foo@bar.com")
False
```
see for more details [usage.py](https://github.com/kakshay21/verify_email/blob/master/verify_email/usage.py)

## Contribute
- Issue Tracker: https://github.com/kakshay21/verify_email/issues
- Source Code: https://github.com/kakshay21/verify_email

## Support
If you are having issues, please let me know.
