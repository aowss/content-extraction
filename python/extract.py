import os

import pdfquery
from lxml import etree

from pypdf import PdfReader

from textractor import Textractor
from textractor.data.constants import TextractFeatures

input_dir = 'resources/in'
output_dir = 'resources/out'

def pdf_extract(input_file_name: str):
    in_path = f'{input_dir}/{input_file_name}.pdf'
    write_to_file(extract_pdfquery(in_path), f'{input_file_name}-pdfquery.xml')
    write_to_file(extract_pdfreader(in_path), f'{input_file_name}-pdfreader.txt')
    write_to_file(extract_textractor_text(in_path), f'{input_file_name}-textractor_text.txt')
    extract_textractor_form(in_path, f'{input_file_name}-textractor-forms.csv')
    for index, result in enumerate(extract_textractor_tables(in_path)):
        write_to_file(result, f'{input_file_name}-textractor-tables-{index}.csv')


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


def extract_textractor_text(input_path: str):
    extractor = Textractor(profile_name="default")
    # Text extraction
    document = extractor.detect_document_text(file_source=input_path)
    return document.text


def extract_textractor_form(input_path: str, output_file_name: str):
    extractor = Textractor(profile_name="default")

    # analyze_document doesn't work when there is more than 1 page
    # start_document_analysis requires the path to be an S3 path
    document = extractor.analyze_document(
        file_source=input_path,
        features=[TextractFeatures.FORMS]
    )

    document.export_kv_to_csv(
        include_kv=True,
        include_checkboxes=True,
        filepath=os.path.join(f'{output_dir}/{output_file_name}'),
        sep="|"
    )


def extract_textractor_tables(input_path: str):
    extractor = Textractor(profile_name="default")

    # analyze_document doesn't work when there is more than 1 page
    # start_document_analysis requires the path to be an S3 path
    document = extractor.analyze_document(
        file_source=input_path,
        features=[TextractFeatures.TABLES]
    )

    result = []
    for table in document.tables:
        result.append(table.to_csv())

    return result


if __name__ == '__main__':
    file_name = 'ISCC-Sample-2'
    pdf_extract(file_name)
