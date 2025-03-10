import codecs
import os

from chamber.shortcuts import change_and_save

from pymess.config import settings


def get_email_template_body_from_file(email_template_slug):
    with codecs.open(os.path.join(
            os.path.join(settings.EMAIL_HTML_DATA_DIRECTORY),
            '{}.html'.format(email_template_slug)), 'r', encoding='utf-8-sig') as file:
        return file.read()


class SyncEmailTemplates:

    def __init__(self, template_slugs=None):
        self.template_slugs = template_slugs

    def __call__(self, apps, schema_editor):
        email_template_class = apps.get_model(*settings.EMAIL_TEMPLATE_MODEL.split('.'))
        email_template_qs = email_template_class.objects.all()
        if self.template_slugs:
            email_template_qs = email_template_qs.filter(slug__in=self.template_slugs)
        email_template_list = list(email_template_qs)
        for email_template in email_template_list:
            email_template.body = get_email_template_body_from_file(email_template.slug)
        email_template_class.objects.bulk_update(email_template_list, ['body'])

