import pandas as pd
import os
from report_generator import ReportGenerator

# Test report generation
rg = ReportGenerator()
test_data = pd.DataFrame({
    'text': ['great product', 'bad quality', 'okay item'],
    'sentiment': ['positive', 'negative', 'neutral'],
    'date': ['2025-01-01', '2025-01-02', '2025-01-03']
})

print("Testing report generation...")

# Test product report
result = rg.generate_product_report(test_data, 'Test Product', 'reports/test_product_report.pdf')
print(f'Product report result: {result}')

# Test marketing report  
result2 = rg.generate_marketing_report(test_data, 'Test Campaign', 'reports/test_campaign_report.pdf')
print(f'Marketing report result: {result2}')

# Check if files exist
print(f'Product report exists: {os.path.exists("reports/test_product_report.pdf")}')
print(f'Campaign report exists: {os.path.exists("reports/test_campaign_report.pdf")}')

# List reports directory
print("Reports directory contents:")
if os.path.exists("reports"):
    for file in os.listdir("reports"):
        print(f"  - {file}")
else:
    print("  - Reports directory does not exist!")
