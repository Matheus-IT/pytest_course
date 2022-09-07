from unittest.mock import patch
from django.test import TestCase
from django.core import mail
import pytest


def test_send_email_should_succeed(mailoutbox, settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    assert len(mailoutbox) == 0

    mail.send_mail(
        subject='test subject',
        message='here is the message',
        from_email='test@mail.com',
        recipient_list=['testemail2@mail.com'],
        fail_silently=False,
    )

    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == 'test subject'


# def test_send_email_without_arguments_should_send_empty_email(self):
#     with patch('companies.views.send_mail') as mock_send_mail:
#         res = self.client.post('/send-email/')

#         res_content = res.json()

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res_content['status'], 'success')
#         self.assertEqual(res_content['info'], 'email sent successfully')

#         mock_send_mail.assert_called_with(
#             subject=None,
#             message=None,
#             from_email='thea76@ethereal.email',
#             recipient_list=['thea76@ethereal.email'],
#         )


# def test_send_email_with_get_verb_should_fail(self):
#     res = self.client.get('/send-email/')
#     assert res.status_code == 405
#     assert res.json() == {'detail': 'Method "GET" not allowed.'}
