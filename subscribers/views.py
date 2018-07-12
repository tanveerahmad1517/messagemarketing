from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from twilio import twiml

from subscribers.models import Subscriber


@csrf_exempt
def message(request):
    response = twiml.Response()
    phone_number = request.POST['From']
    message_body = request.POST['Body']

    try:
        # If the Subscriber exists, return an appropriate response to this sms.
        sub = Subscriber.objects.get(phone_number=phone_number)
        reply_message = sub.handle_message(message_body.lower())
        response.message(reply_message)
    except Subscriber.DoesNotExist:
        # Create a subscriber with this phone number if one does not exist.
        new_subscriber = Subscriber(phone_number=phone_number)
        new_subscriber.save()
        response.message('Thanks for contacting us! Text "subscribe" to '
                         'receive updates via text message.')

    return HttpResponse(response.toxml(), content_type='text/xml')


@csrf_exempt
def notify(request):
    message_body = request.POST['message']
    image_url = request.POST['imageUrl']

    subscribers = Subscriber.objects.filter(subscribed=True)
    if subscribers:
        for subscriber in subscribers:
            subscriber.send_notification(message_body=message_body,
                                         image_url=image_url)
        messages.add_message(request, messages.SUCCESS,
                             'Messages on their way!')
    else:
        messages.add_message(request, messages.ERROR,
                             'Couldn\'t find any subscribers!')

    return redirect('/subscribers/form/')


@csrf_exempt
def view_form(request):
    return render(request, 'subscribers/index.html')
