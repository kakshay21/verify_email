import asyncio
import aiodns
import logging
import re
import smtplib
import socket
import threading
import collections.abc as abc
import sys

EMAIL_REGEX = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
MX_DNS_CACHE = {}
MX_CHECK_CACHE = {}

# Set up logging on module load and avoid adding 'ch' or 'logger' to module
# namespace.  We could assign the logger to a module level name, but it is only
# used by two functions, and this approach demonstrates using the 'logging'
# namespace to retrieve arbitrary loggers.

def setup_module_logger(name):
    """Set up module level logging with formatting"""
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    # Really should not be configuring formats in a library, see
    # https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


setup_module_logger('verify_email')


def is_list(obj):
    return isinstance(obj, abc.Sequence) and not isinstance(obj, str)

async def get_mx_ip(hostname):
    '''Get MX record by hostname.
    '''
    if hostname not in MX_DNS_CACHE:
        try:
            resolver = aiodns.DNSResolver()
            MX_DNS_CACHE[hostname] = await  resolver.query(hostname, 'MX')
        except aiodns.error.DNSError as e:
            MX_DNS_CACHE[hostname] = None
    return MX_DNS_CACHE[hostname]


async def get_mx_hosts(email):
    '''Caching the result in MX_DNS_CACHE to improve performance.
    '''
    hostname = email[email.find('@') + 1:]
    if hostname in MX_DNS_CACHE:
        mx_hosts = MX_DNS_CACHE[hostname]
    else:
        mx_hosts = await get_mx_ip(hostname)
    return mx_hosts



async def handler_verify(mx_hosts, email, timeout=None):
    for mx in mx_hosts:
        res = await network_calls(mx, email, timeout)
        if res:
            return res
        return False


async def syntax_check(email):
    if re.match(EMAIL_REGEX, email):
        return True
    return False


async def _verify_email(email, timeout=None, verify=True):
    '''Validate email by syntax check, domain check and handler check.
    '''
    is_valid_syntax = await syntax_check(email)
    if is_valid_syntax:
        if verify:
            mx_hosts = await get_mx_hosts(email)
            if mx_hosts is None:
                return False
            else:
                return await handler_verify(mx_hosts, email, timeout)
    else:
        return False

def verify_email(emails, timeout=None, verify=True, debug=False):
    if debug:
        logger = logging.getLogger('verify_email')
        logger.setLevel(logging.DEBUG)
    result = []
    if not is_list(emails):
        emails = [emails]

    # asyncio events doesn't fully support windows platform
    # See: https://github.com/kakshay21/verify_email/issues/34#issuecomment-616971628
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()

    for email in emails:
        resp = loop.run_until_complete(_verify_email(email, timeout, verify))
        result.append(resp)

    return result if len(result) > 1 else result[0]

async def verify_email_async(emails, timeout=None, verify=True, debug=False):
    if debug:
        logger = logging.getLogger('verify_email')
        logger.setLevel(logging.DEBUG)
    result = []
    if not is_list(emails):
        emails = [emails]


    for email in emails:
        result.append(await _verify_email(email, timeout, verify))

    return result if len(result) > 1 else result[0]

async def network_calls(mx, email, timeout=20):
    logger = logging.getLogger('verify_email')
    result = False
    try:
        smtp = smtplib.SMTP(mx.host, timeout=timeout)
        status, _ = smtp.ehlo()
        if status >= 400:
            smtp.quit()
            logger.debug(f'{mx} answer: {status} - {_}\n')
            return False
        smtp.mail('')
        status, _ = smtp.rcpt(email)
        if status >= 400:
            logger.debug(f'{mx} answer: {status} - {_}\n')
            result = False
        if status >= 200 and status <= 250:
            result = True

        logger.debug(f'{mx} answer: {status} - {_}\n')
        smtp.quit()

    except smtplib.SMTPServerDisconnected:
        logger.debug(f'Server does not permit verify user, {mx} disconnected.\n')
    except smtplib.SMTPConnectError:
        logger.debug(f'Unable to connect to {mx}.\n')
    except socket.timeout as e:
        logger.debug(f'Timeout connecting to server {mx}: {e}.\n')
        return None
    except socket.error as e:
        logger.debug(f'ServerError or socket.error exception raised {e}.\n')
        return None

    return result
