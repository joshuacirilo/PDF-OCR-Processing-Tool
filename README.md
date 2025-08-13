# PDF-OCR-Processing-Tool 🚀🚀
This Python application automates adding OCR (Optical Character Recognition) to large collections of PDFs, making them searchable and ready for database indexing.

With a user-friendly folder selection dialog and a real-time progress bar, the program processes all PDFs in the chosen directory (including subfolders), skipping those that already contain searchable text. Using Tesseract OCR and PyMuPDF, it embeds a hidden text layer without altering the original document layout.

The tool supports multithreaded processing for speed and handles thousands of PDFs efficiently, making it ideal for archival and enterprise document management workflows.

🦘 Key Features:

Graphical Folder Selection – Choose a directory without editing the code.

Automatic OCR Detection – Skips files that already contain text.

Recursive Batch Processing – Scans all subfolders for PDFs.

Multithreading – Uses multiple CPU cores for faster processing.

Progress Tracking – Displays a live progress bar with tqdm.

Preserves Layout – Adds a searchable text layer without altering visuals.

Language Support – Configured for Spanish (spa) but easily customizable.

Technologies Used:
Python, pdf2image, pytesseract, PyMuPDF, Poppler, Tesseract OCR, tkinter, tqdm
