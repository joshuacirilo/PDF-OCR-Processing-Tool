from pdf2image import convert_from_path  # Converts PDF pages to images using Poppler
import pytesseract  # OCR library for text recognition
import fitz  # PyMuPDF: read and manipulate PDFs
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm  # For progress bar

# Configure paths for Poppler and Tesseract
poppler_path = r'C:/Users/jciri/OneDrive/Escritorio/programasIngeniero/Release-24.08.0-0/poppler-24.08.0/Library/bin'
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/jciri/OneDrive/Escritorio/programasIngeniero/ocr/tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:/Users/jciri/OneDrive/Escritorio/programasIngeniero/ocr/tessdata'

def create_ocr_pdf(input_pdf_path):
    # Validate that the file exists before processing
    if not os.path.exists(input_pdf_path):
        print(f"File does not exist: {input_pdf_path}")
        return

    try:
        # Open the PDF to check if it already contains selectable text (OCR present)
        with fitz.open(input_pdf_path) as pdf_document:
            if pdf_document.page_count > 0:
                first_page = pdf_document[0]
                text = first_page.get_text()
                if text.strip():
                    print(f"File already has OCR, skipping: {input_pdf_path}")
                    return

        # Extract folder and base file name to create a temporary OCR file
        folder, filename = os.path.split(input_pdf_path)
        base_name, _ = os.path.splitext(filename)
        temp_pdf_path = os.path.join(folder, f"{base_name}_ocr_temp.pdf")

        # Create a temporary directory to store page images
        with tempfile.TemporaryDirectory() as temp_dir:
            # Convert PDF to images
            pages = convert_from_path(input_pdf_path, poppler_path=poppler_path, dpi=200, output_folder=temp_dir)

            # Load the original PDF
            pdf_document = fitz.open(input_pdf_path)

            for i, page_image in enumerate(pages):
                try:
                    # OCR each page
                    ocr_text = pytesseract.image_to_pdf_or_hocr(page_image, lang='spa', config='--psm 6 pdf')
                    pdf_ocr = fitz.open("pdf", ocr_text)
                    page = pdf_document[i]
                    page.show_pdf_page(page.rect, pdf_ocr, 0)

                except Exception as page_error:
                    print(f"Error processing page {i + 1}: {page_error}")
                    print(f"Keeping original page without OCR.")

            # Save OCR result
            pdf_document.save(temp_pdf_path)
            pdf_document.close()

            # Replace original PDF
            os.remove(input_pdf_path)
            os.rename(temp_pdf_path, input_pdf_path)

    except Exception as e:
        print(f"Error processing file: {e}")

def process_directory(directory):
    print(f"Searching for PDFs in directory: {directory}")
    pdf_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file.lower().endswith('.pdf')
    ]

    # Progress bar + parallel processing
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(create_ocr_pdf, pdf): pdf for pdf in pdf_files}
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Processing PDFs", unit="file"):
            pass  # tqdm updates automatically

# ====== UI START ======
root = tk.Tk()
root.withdraw()  # Hide main tkinter window
base_directory = filedialog.askdirectory(title="Select the folder containing PDFs")

if base_directory:
    process_directory(base_directory)
else:
    print("No folder selected. Exiting...")
# ====== UI END ======
