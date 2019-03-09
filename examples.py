import dns.resolver
resolver = dns.resolver.get_default_resolver()
resolver.nameservers[0] = '8.8.8.8'

from verify_email import verify_email
from verify_email import fast_verify_email
import timeit

emails = ["k.akshay9721@gmail.com", "xyz231312dasdaf@gmail.com", "foo@bar.com", "ex@example.com"]

print("used: ", timeit.timeit("""
print("single")
for email in emails:
    print(
        email,
        "is",
        verify_email(email) and "valid" or "invalid"
    )
""", number=1, globals=globals()), "seconds")

print("\n")

print("used: ", timeit.timeit("""
print("list")
print("|".join(emails))
print("|".join(i and "valid" or "invalid" for i in verify_email(emails)))
""", number=1, globals=globals()), "seconds")

print("\n")

print("used: ", timeit.timeit("""
print("threaded")
print("|".join(emails))
print("|".join(i and "valid" or "invalid" for i in fast_verify_email(emails)))
""", number=1, globals=globals()), "seconds")

