import dns.resolver
import logging
import smtplib
import socket
import re

MX_DNS_CACHE = {}
MX_CHECK_CACHE = {}
smtp = smtplib.SMTP(timeout=0.6)


def get_mx_ip(hostname):
    if hostname not in MX_DNS_CACHE:
        try:
            MX_DNS_CACHE[hostname] = dns.resolver.query(hostname, 'MX')
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            MX_DNS_CACHE[hostname] = None
    return MX_DNS_CACHE[hostname]


def enable_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


def get_mx_hosts(email):
    hostname = email[email.find('@') + 1:]
    if hostname in MX_DNS_CACHE:
        mx_hosts = MX_DNS_CACHE[hostname]
    else:
        mx_hosts = get_mx_ip(hostname)
    return mx_hosts


def handler_verify(mx_hosts, email, logger, debug, verify):
    for mx in mx_hosts:
        try:
            smtp.connect(mx.exchange.to_text())
            MX_CHECK_CACHE[mx] = True
            if not verify:
                try:
                    smtp.quit()
                except smtplib.SMTPServerDisconnected:
                    pass
                return True
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
                return False
            if status == 250:
                smtp.quit()
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
    return None


def validate_email(email, mass, verify=True, debug=False):
    """This will check hostname and local name
    by using the updated library dns.resolver and verify the email by smtp library.
    Caching the result in MX_DNS_CACHE to improve performance.
    """
    if debug:
        logger = enable_logger('verify_email')
    else:
        logger = None

    if mass:
        result = []
        for e in email:
            result.append(validate_email(e, mass=False, verify=True))
        return result
    else:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            try:
                if verify:
                    mx_hosts = get_mx_hosts(email)
                    if mx_hosts is None:
                        return False
                    return handler_verify(mx_hosts, email, logger, debug, verify)
            except AssertionError:
                return False
            except socket.error as e:
                if debug:
                    logger.debug('ServerError or socket.error exception raised (%s).', e)
                return None
            return True
        else:
            return False
