import os
from datetime import datetime
import streamlit as st

class ReportGenerator:
    def __init__(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_product_report(self, data, product_name, output_path):
        """Generate a product sentiment report"""
        try:
            # For demo purposes, create a simple text report
            # In production, this would use reportlab for PDF generation
            
            report_content = f"""
PRODUCT SENTIMENT REPORT
========================

Product: {product_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
--------
Total Feedback: {len(data)}
Data Period: {data['date'].min() if 'date' in data.columns else 'N/A'} to {data['date'].max() if 'date' in data.columns else 'N/A'}

SENTIMENT BREAKDOWN:
-------------------
"""
            
            if 'sentiment' in data.columns:
                sentiment_counts = data['sentiment'].value_counts()
                for sentiment, count in sentiment_counts.items():
                    percentage = (count / len(data)) * 100
                    report_content += f"{sentiment}: {count} ({percentage:.1f}%)\n"
            
            report_content += "\n\nRECOMMENDATIONS:\n"
            report_content += "----------------\n"
            report_content += "• Monitor negative feedback trends\n"
            report_content += "• Focus on improving product quality\n"
            report_content += "• Enhance customer service response times\n"
            
            # Save as text file (in production, would be PDF)
            text_path = output_path.replace('.pdf', '.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            st.success(f"Report generated: {text_path}")
            return text_path
            
        except Exception as e:
            st.error(f"Error generating report: {e}")
            return None
    
    def generate_marketing_report(self, data, campaign_name, output_path):
        """Generate a marketing campaign report"""
        try:
            report_content = f"""
MARKETING CAMPAIGN REPORT
=========================

Campaign: {campaign_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CAMPAIGN PERFORMANCE:
--------------------
Total Mentions: {len(data)}
Engagement Rate: 5.2% (simulated)
Reach: 10,234 users (simulated)

SENTIMENT ANALYSIS:
------------------
"""
            
            if 'sentiment' in data.columns:
                sentiment_counts = data['sentiment'].value_counts()
                for sentiment, count in sentiment_counts.items():
                    percentage = (count / len(data)) * 100
                    report_content += f"{sentiment}: {count} ({percentage:.1f}%)\n"
            
            report_content += "\n\nRECOMMENDATIONS:\n"
            report_content += "----------------\n"
            report_content += "• Increase positive content engagement\n"
            report_content += "• Target high-performing demographics\n"
            report_content += "• Optimize posting times for better reach\n"
            
            # Save as text file
            text_path = output_path.replace('.pdf', '.txt')
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            st.success(f"Marketing report generated: {text_path}")
            return text_path
            
        except Exception as e:
            st.error(f"Error generating marketing report: {e}")
            return None
