"""
PDF is a series tools for pdf split、convert、merge and so on...
"""
from functools import partial
from time import sleep

from PyPDF2 import PdfFileReader, PdfFileWriter
from concurrent.futures import ThreadPoolExecutor
import os
import click
from PyPDF2.utils import PdfReadError
from tqdm import tqdm, trange
from threading import RLock

from tqdm.contrib.concurrent import thread_map


def spilt_first_page(fro, to):
    """ extract first page of pdf files """

    with open(fro, 'rb') as f:
        try:
            pdf = PdfFileReader(f)
        except PdfReadError as e:
            return 'pdf read error'

        # extract first pdf page
        writer = PdfFileWriter()
        try:
            writer.addPage(pdf.getPage(0))
        except PdfReadError as e:
            return 'pdf read error'
        # write to file
        with open(to, "w+b") as to_f:
            writer.write(to_f)

    return "ok"


def spilt_first_pages(origin, target):
    pdf_files = [
        (os.path.join(origin, name), os.path.join(target, name))
        for name in os.listdir(origin)
        if os.path.isfile(os.path.join(origin, name))
    ]

    thread_map(lambda x: spilt_first_page(*x), pdf_files)



@click.command()
@click.argument("origin")
@click.argument("target")
def pdf_split_cli(origin, target):
    """this is a pdf tool."""
    click.echo("\033[1;31m---------------------\033[0m")
    spilt_first_pages(origin, target)


if __name__ == "__main__":
    pdf_split_cli()
