import pdfquery
from lxml import etree
from pypdf import PdfReader

input_dir = 'resources/in'
output_dir = 'resources/out'

def pdf_extract(input_file_name: str):
    in_path = f'{input_dir}/{input_file_name}.pdf'
    write_to_file(extract_pdfquery(in_path), f'{input_file_name}-pdfquery.xml')
    write_to_file(extract_pdfreader(in_path), f'{input_file_name}-pdfreader.txt')


def write_to_file(output: str, file_name: str):
    out_path = f'{output_dir}/{file_name}'
    f = open(out_path, "w")
    f.write(output)
    f.close()


def extract_pdfquery(input_path: str):
    pdf = pdfquery.PDFQuery(input_path)
    pdf.load()
    return etree.tostring(pdf.tree, pretty_print = True).decode()


def extract_pdfreader(input_path: str):
    reader = PdfReader(input_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text


if __name__ == '__main__':
    file_name = 'ISCC-Sample-1'
    pdf_extract(file_name)

