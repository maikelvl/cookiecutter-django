import io

import pytest
from django.core.management import call_command


def test_for_missing_migrations():
    output = io.StringIO()
    try:
        call_command(
            'makemigrations', interactive=False, dry_run=True, exit_code=True,
            stdout=output)
    except SystemExit as e:
        # The exit code will be 1 when there are no missing migrations
        assert str(e) == '1'
    else:
        pytest.fail("There are missing migrations:\n %s" % output.getvalue())
