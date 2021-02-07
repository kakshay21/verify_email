# verify-email

`verify-email` can verify any email address by efficiently checking the domain name and pinging the handler to verify its existence.

## Features

- Syntax checks
- MX(Mail Exchange records) verification
- Email Handler verification
- Caching domain lookups to improve performance
- Supports `asyncio` for concurrency
- For `multiprocessing` usage, see [fast_verify.py](https://github.com/kakshay21/verify_email/blob/master/verify_email/fast_verify.py)).

## Compatibility
- Written in Python 3.7.
- Supports Python 3.7+.
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
>>> verify_email('foo@bar.com')
False
>>> verify_email(['foo@bar.com', 'example@foo.com'])
[False, False]
```
Also, note that some emails will likely fail in validation, if so you can check the reason of failure
using debug flag.
```
>>> from verify_email import verify_email
>>> verify_email('foo@bar.com', debug=True)
```

see for more examples [examples.py](https://github.com/kakshay21/verify_email/blob/master/examples.py)

## Contribute
- Issue Tracker: https://github.com/kakshay21/verify_email/issues
- Source Code: https://github.com/kakshay21/verify_email

## Support
If you are having issues, please create an issue for it. And feel free to contribute as well 😄.
