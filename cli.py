import json
import logging
import sys
# from datetime import datetime, timedelta, timezone

import click

# from elf.forecaster.sp import get_service_portal_model_chain
# from elf.tools.utils import capture_exceptions, notify_slack

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

def say_hello(name):
    click.echo("Hello, {}".format(name))


def say_goodbye(name):
    click.echo('Good bye, {}'.format(name))


@click.option('--bye', is_flag=True, help="say good bye.")
@click.option('--hello', is_flag=True, help="say hello.")
@click.option('-v', '--version', is_flag=True, help="Show version of this program.")
@click.argument('name')
@click.command()
def main(name, version, hello, bye):

    if version:
        print('1.0.0')
        sys.exit()

    if bye:
        say_goodbye(name)
    else:
        say_hello(name)


if __name__ == "__main__":
    main()