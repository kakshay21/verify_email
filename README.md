# verify-email v 1.0.0

``verify-email`` can verify if the email exists or not by checking the domain name and pinging and verifying the handler.

## Features
TODO

## Compatibility
- It is written in Python 2.7.
- Not tested in python3.X.
- It should work on Linux, Mac and Windows.

## Documentation
TODO

## Installation
### From [pypi.org](https://pypi.org/project/verify-email/)
```
pip install verify-email
```
### From source code
```
virtualenv env 
source env/bin/activate
pip install -r requirements.txt
python setup.py develop
```

## Usage
```
>>> from verify_email import validate_email
>>> validate_email("foo@bar.com")
False
```
see for more details [usage.py](https://github.com/kakshay21/verify_email/blob/master/verify_email/usage.py)

## Contribute
- Issue Tracker: https://github.com/kakshay21/verify_email/issues
- Source Code: https://github.com/kakshay21/verify_email

## Support
If you are having issues, please let me know.
