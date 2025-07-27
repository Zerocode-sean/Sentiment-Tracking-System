import PyPDF2

pdf_path = r'c:/Users/Administrator/Desktop/Sentiments/Sentiments/src/Documantation.pdf'
output_txt_path = r'c:/Users/Administrator/Desktop/Sentiments/Sentiments/src/Documantation_extracted.txt'

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''

with open(output_txt_path, 'w', encoding='utf-8') as out_file:
    out_file.write(text)

print(f"Extracted text saved to {output_txt_path}")
