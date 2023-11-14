# from django.contrib.auth.tokens import PasswordResetTokenGenerator
#
# from six import text_type
#
# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             text_type(user.pk) + text_type(timestamp)
#         )
#
# generate_token = TokenGenerator()

from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp)
        )

generate_token = TokenGenerator()
