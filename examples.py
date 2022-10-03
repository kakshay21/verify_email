from verify_email import verify_email, verify_email_async
import time
import asyncio


emails = [
    'k.akshay9721@gmail.com',
    'some.email.address.that.does.not.exist@gmail.com',
    'foo@bar.com',
    'ex@example.com'
]

def time_it(func, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    print('used:', time.time() - start, 'seconds')


def single(email):
    print(email, 'is', verify_email(email) and 'valid' or 'invalid')


def multiple():
    print('\t'.join(emails))
    print('\t'.join(i and 'valid' or 'invalid' for i in verify_email(emails)))

async def main():
    print('\t'.join(emails))
    print('\t'.join(i and 'valid' or 'invalid' for i in await verify_email_async(emails)))


print('### single')
for email in emails:
    time_it(single, email)
print('### multiple')
time_it(multiple)
print('note that network condition may have impact on test results')
print("asyncio test")
asyncio.new_event_loop().run_until_complete(main())
