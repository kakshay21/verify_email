import dns.resolver
resolver = dns.resolver.get_default_resolver()
resolver.nameservers[0] = '8.8.8.8'
from verify_email import verify_email
from verify_email import fast_verify_email
import time


def time_it(func, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    print("used:", time.time() - start, "seconds")

emails = [
    "k.akshay9721@gmail.com",
    "some.email.address.that.does.not.exist@gmail.com",
    "foo@bar.com",
    "ex@example.com"
]

def test_single(email):
    print(email, "is", verify_email(email) and "valid" or "invalid")


def test_multiple():
    print("\t".join(emails))
    print("\t".join(i and "valid" or "invalid" for i in verify_email(emails)))


def test_threaded():
    print("\t".join(emails))
    print("\t".join(i and "valid" or "invalid" for i in fast_verify_email(emails)))


print("### single")
for email in emails:
    time_it(test_single, email)
print("### multiple")
time_it(test_multiple)
print("### threaded")
time_it(test_threaded)
print("note that network condition may have impact on test results")
