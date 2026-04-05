import sys
try:
    import PyPDF2
    with open(r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\00_admin\Sephora Kick-off Deck and Data Schema.pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"\n--- PAGE {i} ---\n" + page.extract_text() + "\n"
    with open(r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\04_analysis\deck_text.txt', 'w', encoding='utf-8') as out:
        out.write(text)
    print("Done PyPDF2")
except ImportError:
    try:
        import fitz
        doc = fitz.open(r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\00_admin\Sephora Kick-off Deck and Data Schema.pdf')
        text = ""
        for i, page in enumerate(doc):
            text += f"\n--- PAGE {i} ---\n" + page.get_text() + "\n"
        with open(r'c:\Users\Hp\OneDrive - Université Paris Sciences et Lettres\BDD-Projects\BDD\Sephora\04_analysis\deck_text.txt', 'w', encoding='utf-8') as out:
            out.write(text)
        print("Done fitz")
    except ImportError:
        import os
        os.system('pdftotext "c:\\Users\\Hp\\OneDrive - Université Paris Sciences et Lettres\\BDD-Projects\\BDD\\Sephora\\00_admin\\Sephora Kick-off Deck and Data Schema.pdf" "c:\\Users\\Hp\\OneDrive - Université Paris Sciences et Lettres\\BDD-Projects\\BDD\\Sephora\\04_analysis\\deck_text.txt"')
        print("Done pdftotext")
except Exception as e:
    print(f"Error: {e}")
