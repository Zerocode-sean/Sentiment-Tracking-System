import pandas as pd
import os
from report_generator import ReportGenerator

# Test PDF generation
rg = ReportGenerator()
test_data = pd.DataFrame({
    'text': ['great product', 'bad quality', 'okay item', 'love it', 'terrible'],
    'sentiment': ['positive', 'negative', 'neutral', 'positive', 'negative'],
    'date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05']
})

print("Testing PDF report generation...")

# Test product report
result = rg.generate_product_report(test_data, 'Test Product', 'reports/test_product_report_pdf.pdf')
print(f'Product report result: {result}')

# Test marketing report  
result2 = rg.generate_marketing_report(test_data, 'Test Campaign', 'reports/test_campaign_report_pdf.pdf')
print(f'Marketing report result: {result2}')

# Check if files exist and are actual PDFs
import os
if os.path.exists("reports/test_product_report_pdf.pdf"):
    size = os.path.getsize("reports/test_product_report_pdf.pdf")
    print(f'Product PDF exists: True, Size: {size} bytes')
    
    # Check if it's a real PDF (should start with %PDF)
    with open("reports/test_product_report_pdf.pdf", "rb") as f:
        header = f.read(4)
        is_pdf = header == b'%PDF'
        print(f'Product file is PDF: {is_pdf}')

if os.path.exists("reports/test_campaign_report_pdf.pdf"):
    size = os.path.getsize("reports/test_campaign_report_pdf.pdf")
    print(f'Campaign PDF exists: True, Size: {size} bytes')
    
    # Check if it's a real PDF
    with open("reports/test_campaign_report_pdf.pdf", "rb") as f:
        header = f.read(4)
        is_pdf = header == b'%PDF'
        print(f'Campaign file is PDF: {is_pdf}')

print("\nReports directory contents:")
if os.path.exists("reports"):
    for file in os.listdir("reports"):
        if file.endswith('.pdf'):
            size = os.path.getsize(f"reports/{file}")
            print(f"  - {file} ({size} bytes)")
