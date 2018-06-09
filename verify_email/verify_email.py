import dns.resolver
import logging
import smtplib
import socket


MX_DNS_CACHE = {}
MX_CHECK_CACHE = {}
smtp = smtplib.SMTP(timeout=0.4)


def get_mx_ip(hostname):
    if hostname not in MX_DNS_CACHE:
        try:
            MX_DNS_CACHE[hostname] = dns.resolver.query(hostname, 'MX')
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            MX_DNS_CACHE[hostname] = None
    return MX_DNS_CACHE[hostname]


def validate_email(email, verify=True, debug=False, smtp_timeout=10):
    """This will check hostname and local name
    by using the updated library dns.resolver and verify the email by smtp library.
    Caching the result in MX_DNS_CACHE to improve performance.
    """
    if debug:
        logger = logging.getLogger('validate_email')
        logger.setLevel(logging.DEBUG)
    else:
        logger = None
    
    try:
        if verify:
            hostname = email[email.find('@')+1:]
            if hostname in MX_DNS_CACHE:
                mx_hosts = MX_DNS_CACHE[hostname]
            else:
                mx_hosts = get_mx_ip(hostname)
            if mx_hosts is None:
                return False
            
            for mx in mx_hosts:
                try:
                    if not verify and mx in MX_CHECK_CACHE:
                        return MX_CHECK_CACHE[mx]
                    
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
                    if status == 250:
                        smtp.quit()
                        return True
                    if debug:
                        logger.debug(u'%s answer: %s - %s', mx, status, _)
                    smtp.quit()
                except smtplib.SMTPServerDisconnected:  # Server not permits verify user
                    if debug:
                        logger.debug(u'%s disconected.', mx)
                except smtplib.SMTPConnectError:
                    if debug:
                        logger.debug(u'Unable to connect to %s.', mx)
            return None
    except AssertionError:
        return False
    except socket.error as e:
        if debug:
            logger.debug('ServerError or socket.error exception raised (%s).', e)
        return None
    return True
