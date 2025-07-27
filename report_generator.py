import os
from datetime import datetime
import streamlit as st

# Try to import reportlab for PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class ReportGenerator:
    def __init__(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_product_report(self, data, product_name, output_path):
        """Generate a product sentiment report as PDF"""
        try:
            # Ensure the reports directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if REPORTLAB_AVAILABLE:
                return self._generate_pdf_product_report(data, product_name, output_path)
            else:
                return self._generate_text_product_report(data, product_name, output_path)
            
        except Exception as e:
            st.error(f"Error generating report: {e}")
            import traceback
            st.text(traceback.format_exc())
            return None
    
    def _generate_pdf_product_report(self, data, product_name, output_path):
        """Generate PDF product report using ReportLab"""
        # Create the PDF document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.darkblue,
            spaceBefore=20,
            spaceAfter=10
        )
        
        # Title
        story.append(Paragraph("PRODUCT SENTIMENT REPORT", title_style))
        story.append(Spacer(1, 20))
        
        # Product info
        story.append(Paragraph(f"<b>Product:</b> {product_name}", styles['Normal']))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Summary section
        story.append(Paragraph("SUMMARY", heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Feedback', str(len(data))],
            ['Data Period', f"{data['date'].min() if 'date' in data.columns else 'N/A'} to {data['date'].max() if 'date' in data.columns else 'N/A'}"],
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Sentiment breakdown
        if 'sentiment' in data.columns:
            story.append(Paragraph("SENTIMENT BREAKDOWN", heading_style))
            sentiment_counts = data['sentiment'].value_counts()
            
            sentiment_data = [['Sentiment', 'Count', 'Percentage']]
            for sentiment, count in sentiment_counts.items():
                percentage = (count / len(data)) * 100
                sentiment_data.append([str(sentiment), str(count), f"{percentage:.1f}%"])
            
            sentiment_table = Table(sentiment_data)
            sentiment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(sentiment_table)
            story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("RECOMMENDATIONS", heading_style))
        recommendations = [
            "• Monitor negative feedback trends to identify product issues",
            "• Focus on improving product quality based on customer feedback",
            "• Enhance customer service response times for better satisfaction",
            "• Implement feedback-driven product improvements",
            "• Track sentiment changes over time for trend analysis"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        st.success(f"PDF report generated: {output_path}")
        return output_path
    
    def _generate_text_product_report(self, data, product_name, output_path):
        """Fallback text report generation"""
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
        
        # Save as text file with PDF extension for compatibility
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        st.warning("ReportLab not available - generated text report instead of PDF")
        st.success(f"Report generated: {output_path}")
        return output_path
    
    def generate_marketing_report(self, data, campaign_name, output_path):
        """Generate a marketing campaign report as PDF"""
        try:
            # Ensure the reports directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if REPORTLAB_AVAILABLE:
                return self._generate_pdf_marketing_report(data, campaign_name, output_path)
            else:
                return self._generate_text_marketing_report(data, campaign_name, output_path)
            
        except Exception as e:
            st.error(f"Error generating marketing report: {e}")
            import traceback
            st.text(traceback.format_exc())
            return None
    
    def _generate_pdf_marketing_report(self, data, campaign_name, output_path):
        """Generate PDF marketing report using ReportLab"""
        # Create the PDF document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.darkgreen,
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.darkgreen,
            spaceBefore=20,
            spaceAfter=10
        )
        
        # Title
        story.append(Paragraph("MARKETING CAMPAIGN REPORT", title_style))
        story.append(Spacer(1, 20))
        
        # Campaign info
        story.append(Paragraph(f"<b>Campaign:</b> {campaign_name}", styles['Normal']))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Campaign performance section
        story.append(Paragraph("CAMPAIGN PERFORMANCE", heading_style))
        performance_data = [
            ['Metric', 'Value'],
            ['Total Mentions', str(len(data))],
            ['Engagement Rate', '5.2% (simulated)'],
            ['Reach', '10,234 users (simulated)'],
            ['Campaign Period', f"{data['date'].min() if 'date' in data.columns else 'N/A'} to {data['date'].max() if 'date' in data.columns else 'N/A'}"],
        ]
        
        performance_table = Table(performance_data)
        performance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(performance_table)
        story.append(Spacer(1, 20))
        
        # Sentiment analysis
        if 'sentiment' in data.columns:
            story.append(Paragraph("SENTIMENT ANALYSIS", heading_style))
            sentiment_counts = data['sentiment'].value_counts()
            
            sentiment_data = [['Sentiment', 'Count', 'Percentage']]
            for sentiment, count in sentiment_counts.items():
                percentage = (count / len(data)) * 100
                sentiment_data.append([str(sentiment), str(count), f"{percentage:.1f}%"])
            
            sentiment_table = Table(sentiment_data)
            sentiment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(sentiment_table)
            story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("STRATEGIC RECOMMENDATIONS", heading_style))
        recommendations = [
            "• Increase positive content engagement through targeted messaging",
            "• Focus on high-performing demographics for better ROI",
            "• Optimize posting times based on audience activity patterns",
            "• Implement A/B testing for campaign messaging",
            "• Monitor competitor sentiment to identify market opportunities"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        st.success(f"PDF marketing report generated: {output_path}")
        return output_path
    
    def _generate_text_marketing_report(self, data, campaign_name, output_path):
        """Fallback text marketing report generation"""
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
        
        # Save as text file with PDF extension for compatibility
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        st.warning("ReportLab not available - generated text report instead of PDF")
        st.success(f"Marketing report generated: {output_path}")
        return output_path
