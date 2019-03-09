# verify-email 

`verify-email` can verify the email by efficiently checking the domain name and pinging the handler to verify its existence.

## Features

- Syntax checks
- MX(Mail Exchange records) verification
- Handler verification
- Cache domain lookups
- Multithread support (look in [usage.py](https://github.com/kakshay21/verify_email/blob/master/verify_email/usage.py))
- Multiprocess efficient (not recommended but have a look in [fast_verify.py](https://github.com/kakshay21/verify_email/blob/master/verify_email/fast_verify.py))

## Compatibility
- It is written in Python 2.7.
- Works on Python 3.7.
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
```
>>> from verify_email import verify_email
>>> verify_email("foo@bar.com")
False
>>> verify_email(["foo@bar.com", "example@foo.com"])
[False, False]
```
### Multithreaded
```
>>> from verify_email import fast_verify_email
>>> fast_validate_email(["foo@bar.com", 
"bar@bar.com", "foo@foo.com", "bar@foo.com"])
[False, False, False, False]
```
see for more examples [examples.py](https://github.com/kakshay21/verify_email/blob/master/examples.py)

## Contribute
- Issue Tracker: https://github.com/kakshay21/verify_email/issues
- Source Code: https://github.com/kakshay21/verify_email

## Support
If you are having issues, please create an issue for it.
