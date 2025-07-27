from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import pandas as pd
import io
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
    def create_chart_buffer(self, fig):
        """Convert matplotlib figure to buffer for PDF"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        buf.seek(0)
        return buf
    
    def generate_product_report(self, df, product_name, output_path):
        """Generate PDF report for product sentiment analysis"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph(f"Sentiment Analysis Report: {product_name}", title_style))
        story.append(Spacer(1, 20))
        
        # Report metadata
        story.append(Paragraph(f"<b>Generated on:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Total Feedback Entries:</b> {len(df)}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Sentiment Summary
        sentiment_counts = df['sentiment'] if 'sentiment' in df.columns else df.iloc[:, -1]
        sentiment_summary = sentiment_counts.value_counts()
        
        story.append(Paragraph("<b>Sentiment Distribution:</b>", self.styles['Heading2']))
        
        # Create sentiment table
        table_data = [['Sentiment', 'Count', 'Percentage']]
        total = len(df)
        for sentiment, count in sentiment_summary.items():
            percentage = f"{(count/total)*100:.1f}%"
            table_data.append([sentiment, str(count), percentage])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 30))
        
        # Generate sentiment chart
        fig, ax = plt.subplots(figsize=(8, 6))
        sentiment_summary.plot(kind='bar', ax=ax, color=['red', 'gray', 'green'])
        ax.set_title('Sentiment Distribution')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Add chart to PDF
        chart_buf = self.create_chart_buffer(fig)
        img = Image(chart_buf, width=6*inch, height=4*inch)
        story.append(img)
        plt.close(fig)
        
        # Sample feedback
        story.append(Spacer(1, 30))
        story.append(Paragraph("<b>Sample Feedback:</b>", self.styles['Heading2']))
        
        text_col = self.get_text_column(df)
        sentiment_col = self.get_sentiment_column(df)
        
        for sentiment in sentiment_summary.index[:3]:  # Top 3 sentiments
            sample = df[df[sentiment_col] == sentiment].head(2)
            story.append(Paragraph(f"<b>{sentiment.title()} Feedback:</b>", self.styles['Heading3']))
            for _, row in sample.iterrows():
                story.append(Paragraph(f"• {row[text_col][:200]}...", self.styles['Normal']))
            story.append(Spacer(1, 10))
        
        # Build PDF
        doc.build(story)
        plt.close('all')
        
    def generate_marketing_report(self, df, campaign_name, output_path):
        """Generate marketing campaign report"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph(f"Marketing Campaign Report: {campaign_name}", title_style))
        story.append(Spacer(1, 20))
        
        # Campaign metrics
        story.append(Paragraph(f"<b>Campaign Period:</b> {datetime.now().strftime('%Y-%m-%d')}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Total Mentions:</b> {len(df)}", self.styles['Normal']))
        
        # Platform breakdown if available
        if 'platform' in df.columns:
            platform_counts = df['platform'].value_counts()
            story.append(Paragraph("<b>Platform Distribution:</b>", self.styles['Heading2']))
            
            for platform, count in platform_counts.items():
                story.append(Paragraph(f"• {platform}: {count} mentions", self.styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(story)
    
    def get_text_column(self, df):
        """Guess text column name"""
        for col in df.columns:
            if 'text' in col.lower() or 'review' in col.lower() or 'comment' in col.lower():
                return col
        return df.columns[0]
    
    def get_sentiment_column(self, df):
        """Guess sentiment column name"""
        for col in df.columns:
            if 'sentiment' in col.lower() or 'label' in col.lower():
                return col
        return df.columns[-1]
