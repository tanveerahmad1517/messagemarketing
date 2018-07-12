from __future__ import unicode_literals
import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from twilio.rest import TwilioRestClient

# TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
TWILIO_PHONE_NUMBER = '+12672145849'
twilio_client = TwilioRestClient()


@python_2_unicode_compatible
class Subscriber(models.Model):
    phone_number = models.CharField(max_length=15)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return '{0} - {1}'.format(self.phone_number, self.subscribed)

    def handle_message(self, message_body):
        # Conditional logic to do different things based on the command from
        # the user
        if message_body == 'subscribe' or message_body == 'unsub':
            # If the user has elected to subscribe for messages, flip the bit
            # and indicate that they have done so.
            self.subscribed = message_body == 'subscribe'
            self.save()

            # Otherwise, our subscription has been updated
            response_message = 'You are now subscribed for updates.'
            if not self.subscribed:
                response_message = 'You have unsubscribed. Text "subscribe"' \
                                   ' to start receiving updates again.'
            return response_message
        else:
            return 'Sorry, we didn\'t understand that. available commands are' \
                   ': subscribe or unsubscribe'

    def send_notification(self, message_body='', image_url=None):
        if image_url:
            message = twilio_client.messages.create(to=self.phone_number,
                                                    from_=TWILIO_PHONE_NUMBER,
                                                    body=message_body,
                                                    media_url=image_url)
        else:
            message = twilio_client.messages.create(to=self.phone_number,
                                                    from_=TWILIO_PHONE_NUMBER,
                                                    body=message_body)

        return message
