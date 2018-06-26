import dns.resolver
import logging
import re
import smtplib
import socket

MX_DNS_CACHE = {}
MX_CHECK_CACHE = {}
smtp = smtplib.SMTP(timeout=0.6)


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


def handler_verify(mx_hosts, email, debug, verify):
    if debug:
        logger = enable_logger('verify_email')
    else:
        logger = None
    result = None
    for mx in mx_hosts:
        try:
            smtp.connect(mx.exchange.to_text())
            MX_CHECK_CACHE[mx] = True
            status, _ = smtp.helo()
            if status != 250:
                smtp.quit()
                if debug:
                    logger.debug(u'%s answer: %s - %s', mx, status, _)
                continue
            smtp.mail('')
            status, _ = smtp.rcpt(email)
            if status == 550:  # status code for wrong gmail emails
                smtp.quit()
                if debug:
                    logger.debug(u'%s answer: %s - %s', mx, status, _)
                result = False
                break
            if status == 250:
                smtp.quit()
                result = True
                break
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
            result = None
            break
    return result


def validate_email(email, mass, verify=True, debug=False):
    """Validate email by syntax check, domain check and handler check.
    """
    if mass:
        result = []
        for e in email:
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", e):
                if verify:
                    mx_hosts = get_mx_hosts(e)
                    if mx_hosts is None:
                        result.append(False)
                    else:
                        result.append(handler_verify(mx_hosts, e, debug, verify))
            else:
                result.append(False)
        return result
    else:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            if verify:
                mx_hosts = get_mx_hosts(email)
                if mx_hosts is None:
                    return False
                return handler_verify(mx_hosts, email, debug, verify)
        else:
            return False
