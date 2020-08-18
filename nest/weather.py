
# wea is a weather report tool.
import click
import os
import sys
import subprocess


@click.command()
@click.argument('location', default='')
def wea_cli(location):
    """A weather query tool.\n
    Default weather query base on your location.
    """
    if location != '':
        location = '/' + location

    if sys.platform == 'win32':
        # use powershell to exec
        s = subprocess.Popen(
            [
                'powershell.exe',
                'Invoke-RestMethod "wttr.in{}?lang=zh&format=3"'.format(
                    location)
            ],
            stdout=sys.stdout
        )
        s.communicate()
    else:
        os.system('curl "wttr.in{}?lang=zh&format=3"'.format(location))


if __name__ == "__main__":
    wea_cli()
