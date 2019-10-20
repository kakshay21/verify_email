import asyncio
import aiodns
import logging
import re
import smtplib
import socket
import threading
import collections.abc as abc


MX_DNS_CACHE = {}
MX_CHECK_CACHE = {}

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


async def enable_logger(name):
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

async def handler_verify(mx_hosts, email, debug, timeout=None):
    logger = None
    if debug:
        logger = await enable_logger('verify_email')
    for mx in mx_hosts:
        res = await network_calls(mx, email, debug, logger, timeout)
        if res:
            return res
        return False


async def syntax_check(email):
    if re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
        return True
    return False


async def _verify_email(email, timeout=None, verify=True, debug=False):
    '''Validate email by syntax check, domain check and handler check.
    '''
    is_valid_syntax = await syntax_check(email)
    if is_valid_syntax:
        if verify:
            mx_hosts = await get_mx_hosts(email)
            if mx_hosts is None:
                return False
            else:
                return await handler_verify(mx_hosts, email, debug, timeout)
    else:
        return False

def verify_email(emails, timeout=None, verify=True, debug=False):
    result = []
    if not is_list(emails):
        emails = [emails]

    for email in emails:
        resp = asyncio.run(_verify_email(email, timeout, verify, debug))
        result.append(resp)

    return result if len(result) > 1 else result[0]

async def network_calls(mx, email, debug, logger, timeout):
    if not timeout:
        timeout = 20
    try:
        smtp = smtplib.SMTP(mx.host)
        status, _ = smtp.ehlo()
        if status != 250:
            smtp.quit()
            if debug:
                logger.debug(f'{mx} answer: {status} - {_}')
            return False
        smtp.mail('')
        status, _ = smtp.rcpt(email)
        if status >= 500:
            smtp.quit()
            if debug:
                logger.debug(f'{mx} answer: {status} - {_}')
            return False
        if status == 250:
            smtp.quit()
            return True

        if debug:
            logger.debug(f'{mx} answer: {status} - {_}', mx, status, _)
        smtp.quit()

    except smtplib.SMTPServerDisconnected:
        if debug:
            logger.debug(f'Server not permits verify user, {mx} disconected.')
    except smtplib.SMTPConnectError:
        if debug:
            logger.debug(f'Unable to connect to {mx}.')
    except socket.error as e:
        if debug:
            logger.debug(f'ServerError or socket.error exception raised {e}.')
        return None
