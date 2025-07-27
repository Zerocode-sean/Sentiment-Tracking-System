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
            # Ensure the reports directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
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
            
            # For demo, save as text file but keep the original filename for compatibility
            # In production, would generate actual PDF
            if output_path.endswith('.pdf'):
                # Create a text file instead but return the correct path
                with open(output_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                    f.write(report_content)
                # Create a simple "PDF" file for download compatibility
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                st.success(f"Report generated: {output_path}")
                return output_path
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                st.success(f"Report generated: {output_path}")
                return output_path
            
        except Exception as e:
            st.error(f"Error generating report: {e}")
            import traceback
            st.text(traceback.format_exc())
            return None
    
    def generate_marketing_report(self, data, campaign_name, output_path):
        """Generate a marketing campaign report"""
        try:
            # Ensure the reports directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
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
            
            # For demo, create both text and "PDF" versions for compatibility
            if output_path.endswith('.pdf'):
                # Create a text file for reference
                with open(output_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                    f.write(report_content)
                # Create a simple "PDF" file for download compatibility
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                st.success(f"Marketing report generated: {output_path}")
                return output_path
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)
                st.success(f"Marketing report generated: {output_path}")
                return output_path
            
        except Exception as e:
            st.error(f"Error generating marketing report: {e}")
            import traceback
            st.text(traceback.format_exc())
            return None
