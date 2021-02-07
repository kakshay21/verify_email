import unittest

from verify_email import verify_email


class TestVerifyEmail(unittest.TestCase):
    def setUp(self):
        self.emails = [
            'k.akshay9721@gmail.com',
            'some.email.address.that.does.not.exist@gmail.com',
            'foo@bar.com',
            'ex@example.com'
        ]

    def test_valid_email(self):
        self.assertEqual(True, verify_email(self.emails[0]))

    def test_invalid_email(self):
        self.assertEqual(False, verify_email(self.emails[1]))

    def test_email_with_debugger(self):
        self.assertEqual(False, verify_email(self.emails[2], debug=True))

    def test_multiple_emails(self):
        self.assertEqual([True, False, False, False], verify_email(self.emails))


if __name__ == '__main__':
    unittest.main()
