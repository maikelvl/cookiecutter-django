from django.core.management import call_command
from django.test.testcases import TestCase

from main.management.commands import create_content


class CommandTestCase(TestCase):

    def tearDown(self):
        call_command('clear_index', interactive=False)

    def test_create_content(self):
        command = create_content.Command()
        command.handle()

    def test_words(self):
        create_content.words(5)
        create_content.words(5, 10)

    def test_paragraph(self):
        create_content.paragraph(5)
        create_content.paragraph(5, False)

        create_content.paragraph((5, 10))
        create_content.paragraph((5, 10), False)
