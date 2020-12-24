import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfFileReader
from nest.pdf import spilt_first_page, spilt_first_pages

here = os.path.abspath(os.path.dirname(__file__))


def create_pdf_file(content, target):
    my_pdf = SimpleDocTemplate(target)
    sample_style_sheet = getSampleStyleSheet()
    # add content
    flowables = []
    for c in content:
        flowables.append(Paragraph(c, style=sample_style_sheet["BodyText"]))
        flowables.append(PageBreak())

    my_pdf.build(flowables)
    target.close()


def test_create_pdf_file(tmpdir):
    content = ["page first", "page two", "page three", "page four", "page five"]
    target = tmpdir / 'target.pdf'
    with open(target, 'w+b') as file:
        create_pdf_file(content, file)

    with open(target, 'rb') as file:
        page_nums = PdfFileReader(file).getNumPages()

    assert page_nums == 5


def test_pdf_can_extract_first_page(tmpdir):
    content = ["page one", "page two", "page three", "page four", "page five"]
    fro = tmpdir / "fro.pdf"
    to = tmpdir / "to.pdf"

    with open(fro, 'w+b') as file:
        create_pdf_file(content, file)

    spilt_first_page(fro, to)

    with open(to, 'rb') as file:
        first_page = PdfFileReader(file).getPage(0).extractText()

    assert "page one" in first_page


def test_pdf_can_extract_first_pages(tmpdir):
    origin = tmpdir.mkdir("origin")
    target = tmpdir.mkdir("target")
    content = ["page first", "page two", "page three", "page four", "page five"]

    for i in range(1, 1001):
        with open(f'{origin}/{i}.pdf', 'w+b') as f:
            create_pdf_file(content, f)

    spilt_first_pages(origin, target)



