from datetime import date

from django.utils.crypto import salted_hmac
from django.utils.crypto import constant_time_compare
from django.utils.http import int_to_base36, base36_to_int
from django.core.mail import send_mail
from django.template.loader import render_to_string
from possster.settings import DEFAULT_FROM_EMAIL
from possster.settings import EMAIL_AUTH_TIMEOUT_DAYS


class EmailAuthTokenGenerator(object):

    key_salt = 'possster.utils.EmailAuthTokenGenerator'

    def make_token(self, user):
        ts = (date.today() - date(2001, 1, 1)).days
        return self._make_token_with_timestamp(user, ts)

    def check_token(self, user, token):
        try:
            ts_b36, hash_val = token.split('-')
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if not constant_time_compare(
                self._make_token_with_timestamp(user, ts), token):
            return False

        # Check time limit
        now = (date.today() - date(2001, 1, 1)).days
        if now - ts > EMAIL_AUTH_TIMEOUT_DAYS:
            return False

        return True

    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(user.password) +
            str(user.date_joined) + str(timestamp)
       )

    def _make_token_with_timestamp(self, user, timestamp):
        ts_b36 = int_to_base36(timestamp)

        hash_val = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, timestamp)
        ).hexdigest()[::-3]

        return "%s-%s" % (ts_b36, hash_val)


def send_verify_mail(user):
    e = EmailAuthTokenGenerator()

    token = e.make_token(user)

    msg_subject = render_to_string('mail/mail_subject.txt', {
        'username': user.username,
        'site_name': 'Possster',
    })
    msg_text = render_to_string('mail/mail_msg.txt', {
        'username': user.username,
        'site_name': 'Possster',
        'token': token,
    })
    msg_html = render_to_string('mail/mail_msg.html', {
        'username': user.username,
        'site_name': 'Possster',
        'token': token,
    })

    send_mail(
        msg_subject,
        msg_text,
        DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=msg_html,
    )

