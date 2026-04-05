import sys
try:
    import PyPDF2
    files = [
        ('sephora_analysis_summary.pdf', 'sephora_analysis_summary_text.txt'),
        ('sephora_correspondance_profils.pdf', 'sephora_correspondance_profils_text.txt')
    ]
    for in_file, out_file in files:
        with open(r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\\' + in_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for i, page in enumerate(reader.pages):
                text += f"\n--- PAGE {i} ---\n" + page.extract_text() + "\n"
        with open(r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\04_analysis\\' + out_file, 'w', encoding='utf-8') as out:
            out.write(text)
    print("Done PyPDF2")
except Exception as e:
    print(f"Error: {e}")
