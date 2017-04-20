from datetime import date

from django.utils.crypto import salted_hmac
from django.utils.crypto import constant_time_compare
from django.utils.http import int_to_base36, base36_to_int
from possster.settings import EMAIL_AUTH_TIMEOUT_DAYS


class EmailAuthTokenGenerator(object):

    key_salt = 'possster.utils.EmailAuthTokenGenerator'

    def make_token(self, user):
        ts = (date.today() - date(2001, 1, 1)).days
        return self._make_token_with_timestamp(user, ts)

    def check_token(self, user, token):
        try:
            ts_b36, hash_val = token.split('-')
            print(ts_b36, hash_val)
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
            print(ts_b36, ts, hash_val)
        except ValueError:
            return False

        if not constant_time_compare(
                self._make_token_with_timestamp(user, ts), token):
            print(self._make_token_with_timestamp(user, ts), token)
            return False

        # Check time limit
        now = (date.today() - date(2001, 1, 1)).days
        if now - ts > EMAIL_AUTH_TIMEOUT_DAYS:
            print(now, ts, now-ts)
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
