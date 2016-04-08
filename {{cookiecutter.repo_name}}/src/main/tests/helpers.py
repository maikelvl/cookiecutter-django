
from django.core.files.base import ContentFile
from model_mommy.generators import gen_image_field


def get_image(name='test.png'):
    return ContentFile(gen_image_field().read(), name)
