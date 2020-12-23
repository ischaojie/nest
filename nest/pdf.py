"""
PDF is a series tools for pdf split、convert、merge and so on...
"""
from PyPDF2 import PdfFileReader, PdfFileWriter
import concurrent.futures
import os
import click
from tqdm import tqdm


def spilt_first_page(fro, to):
    """ extract first page of pdf files """

    with open(fro, 'rb') as f:
        pdf = PdfFileReader(f)

        # extract first pdf page
        writer = PdfFileWriter()
        writer.addPage(pdf.getPage(0))
        # write to file
        with open(to, "w+b") as f:
            writer.write(f)

    return "ok"


def spilt_first_pages(origin, target):
    pdf_files = [
        (os.path.join(origin, name), os.path.join(target, name))
        for name in os.listdir(origin)
        if os.path.isfile(os.path.join(origin, name))
    ]
    pdf_nums = len(pdf_files)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        result_bar = tqdm(zip(pdf_files, executor.map(lambda x: spilt_first_page(*x), pdf_files)), total=pdf_nums)
        for bar in result_bar:
            pass
        # for file, result in zip(
        #         pdf_files, executor.map(lambda x: spilt_first_page(*x), pdf_files)
        # ):
        #     print("{} extract result is {}".format(file, result))


@click.command()
@click.argument("origin")
@click.argument("target")
def pdf_split_cli(origin, target):
    """this is a pdf tool."""
    click.echo("\033[1;31m---------------------\033[0m")
    spilt_first_pages(origin, target)


if __name__ == "__main__":
    pdf_split_cli()
