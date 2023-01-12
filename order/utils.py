from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from f1store.settings import DEFAULT_FROM_EMAIL


def send_email_confirmation(*args):
    """
    Takes ``paid_amount``, ``to`` and ``items``
    and sends order confirmation email to customer. 
    """
    subject = 'Your order confirmation'
    to = args[1]
    context = {
        'paid_amount': args[0],
        'items': args[2],
        'first_name': args[3],
        'last_name': args[4]
    }
    html_message = render_to_string('order_confirmation.html', context)
    plain_message = strip_tags(html_message)
    from_email = DEFAULT_FROM_EMAIL

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
