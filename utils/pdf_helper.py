# pdf
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
import pymupdf
# string parse

#M1 https://pymupdf.readthedocs.io/en/latest/recipes-text.html
import sys, pathlib, pymupdf

destination_txt_folder = '/Users/dawn.duan/Library/CloudStorage/OneDrive-CanadianTire/Documents/tetris/ivado_or/tetris-api-worker/optimization/local_experiments/aer1810/10_benchmark_datasets/all_paper_text/'
find_fname = lambda pdf_path: str(pdf_path).split('/')[-1]
def convert_text_pymupdf(pdf_path, destination_txt_folder):
    fname = find_fname(pdf_path)
    with pymupdf.open(pdf_path) as doc:  # open document
        text = chr(12).join([page.get_text() for page in doc])
    # write as a binary file to support non-ASCII characters
    final_path = destination_txt_folder+fname
    pathlib.Path(final_path+ ".txt").write_bytes(text.encode())
# convert_text_pymupdf(pdf_path, destination_txt_folder)
# [convert_text_pymupdf(pdf_path, destination_txt_folder) for pdf_path in sorted_pdf_paths]
# # end with .pdf.txt

find_fname = lambda pdf_path: str(pdf_path).split('/')[-1]

#M2
def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF at the specified path using PyMuPDF.
    """
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text
# Extract text from the downloaded PDF
# paper_text = extract_text_from_pdf(pdf_path)
# print(paper_text[1000:])

is_pdf = lambda pdf_path: str(pdf_path).split('.')[-1] == 'pdf'