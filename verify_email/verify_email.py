import dns.resolver
import logging
import re
import smtplib
import socket
import threading
import collections.abc as abc


MX_DNS_CACHE = {}
MX_CHECK_CACHE = {}
threaded_result = None

def is_list(o):
    return isinstance(o, abc.Sequence) and not isinstance(o, str)

def get_mx_ip(hostname):
    """Get MX record by hostname.
    """
    if hostname not in MX_DNS_CACHE:
        try:
            MX_DNS_CACHE[hostname] = dns.resolver.query(hostname, 'MX')
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            MX_DNS_CACHE[hostname] = None
    return MX_DNS_CACHE[hostname]


def enable_logger(name):
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_mx_hosts(email):
    """Caching the result in MX_DNS_CACHE to improve performance.
    """
    hostname = email[email.find('@') + 1:]
    if hostname in MX_DNS_CACHE:
        mx_hosts = MX_DNS_CACHE[hostname]
    else:
        mx_hosts = get_mx_ip(hostname)
    return mx_hosts


def handler_verify(mx_hosts, email, debug):
    if debug:
        logger = enable_logger('verify_email')
    else:
        logger = None
    for mx in mx_hosts:
        res = network_calls(mx, email, debug, logger)
        if res:
            return res
        return False


def syntax_check(email):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return True
    return False


def validate_email(email, verify=True, debug=False):
    """Validate email by syntax check, domain check and handler check.
    """
    if is_list(email):
        result = []
        for e in email:
            if syntax_check(e):
                if verify:
                    mx_hosts = get_mx_hosts(e)
                    if mx_hosts is None:
                        result.append(False)
                    else:
                        result.append(handler_verify(mx_hosts, e, debug))
            else:
                result.append(False)
        return result
    else:
        if syntax_check(email):
            if verify:
                mx_hosts = get_mx_hosts(email)
                if mx_hosts is None:
                    return False
                return handler_verify(mx_hosts, email, debug)
        else:
            return False


def handler_verify_multi_threaded(mx_hosts, email, debug):
    global threaded_result
    if debug:
        logger = enable_logger('verify_email')
    else:
        logger = None
    threads = [threading.Thread(target=network_calls, args=(mx, email, debug, logger)) for mx in mx_hosts]
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    return threaded_result


def network_calls(mx, email, debug, logger):
    global threaded_result
    try:
        smtp = smtplib.SMTP(mx.exchange.to_text())
        status, _ = smtp.helo()
        if status != 250:
            smtp.quit()
            if debug:
                logger.debug(u'%s answer: %s - %s', mx, status, _)
            threaded_result = False
            return False
        smtp.mail('')
        status, _ = smtp.rcpt(email)
        if status == 550:  # status code for wrong gmail emails
            smtp.quit()
            if debug:
                logger.debug(u'%s answer: %s - %s', mx, status, _)
            threaded_result = False
            return False
        if status == 250:
            smtp.quit()
            threaded_result = True
            return True

        if debug:
            logger.debug(u'%s answer: %s - %s', mx, status, _)
        smtp.quit()
    except smtplib.SMTPServerDisconnected:
        if debug:
            logger.debug(u'Server not permits verify user, %s disconected.', mx)
    except smtplib.SMTPConnectError:
        if debug:
            logger.debug(u'Unable to connect to %s.', mx)
    except socket.error as e:
        if debug:
            logger.debug('ServerError or socket.error exception raised (%s).', e)
        threaded_result = None
        return None


def fast_validate_email(email):
    if is_list(email):
        result = []
        for e in email:
            if syntax_check(e):
                mx_hosts = get_mx_hosts(e)
                if mx_hosts is None:
                    result.append(False)
                    continue
                result.append(handler_verify_multi_threaded(mx_hosts, e, False))
            else:
                result.append(False)
                continue
        return result
    else:
        # t1 = threading.Thread(target=syntax_check, name='syntax_check', args=(email,))
        # t1.start()
        # t2 = threading.Thread(target=get_mx_hosts, name='get_mx_hosts', args=(email,))
        # t2.start()
        # t1.join()
        # t2.join()
        if syntax_check(email):
            mx_hosts = get_mx_hosts(email)
            if mx_hosts is None:
                return False
            return handler_verify_multi_threaded(mx_hosts, email, False)
