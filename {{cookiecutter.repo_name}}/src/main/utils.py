import os
import re

from django.conf import settings
from django.core.mail import send_mail
from django.template.context import Context
from django.template.loader import get_template
from django.utils import timezone


def send_template_mail(to, subject, template, context, html_template=None,
                       fail_silently=False):
    """
    Send mail with template
    """
    text_content = get_template(template).render(context)
    if html_template is not None:
        html_content = get_template(html_template).render(context)
    else:
        html_content = None

    return send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=to,
        html_message=html_content,
        fail_silently=fail_silently
    )


def now_no_micro():
    return timezone.now().replace(microsecond=0)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_filename(instance, filename):
    image = instance._meta.get_field('image')
    image.upload_to = instance.upload_to
    return os.path.join(
        image.get_directory_name(), image.get_filename(filename))


def insert_inline_images(content, inline_images):
    inline_images = list(inline_images)
    inline_image = ''

    if inline_images:
        def inline_image(matchobj):
            try:
                nr = int(matchobj.groupdict().get('number')) - 1
                if nr < 0:
                    raise IndexError

                context = Context({
                    'image': inline_images[nr]
                })

                return get_template('inc/inline-image.html') \
                    .render(context)
            except IndexError:
                pass
            return ''

    content = re.sub(r'\[\s?image\s*(?P<number>\d+)\s?\]', inline_image,
                     content, flags=re.IGNORECASE)

    return content
