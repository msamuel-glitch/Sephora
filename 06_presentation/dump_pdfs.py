import fitz
import os

pdf_files = [
    r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\06_presentation\sephora_analysis_summary.pdf",
    r"c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\06_presentation\sephora_correspondance_profils.pdf"
]

for pdf_path in pdf_files:
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        with open(pdf_path + ".txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Dumped {pdf_path}")
    except Exception as e:
        print(f"Error on {pdf_path}: {e}")
