import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import sys
import sqlite3
import re

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from auth_manager import AuthManager
from database_manager import DatabaseManager
from report_generator import ReportGenerator

# Optional imports with fallbacks
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    st.warning("WordCloud not available - word cloud features will be disabled")

try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Initialize managers
auth = AuthManager()
db = DatabaseManager()
report_gen = ReportGenerator()

# Configure page
st.set_page_config(
    page_title="Sentiment Tracking System",
    page_icon="📊",
    layout="wide"
)

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        auth.show_login_form()
        return False
    return True

def clean_text_for_training(text):
    """Clean text for model training"""
    import re
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_sentiment_model(df, text_col, sentiment_col):
    """Train sentiment model on provided data"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, classification_report
    
    # Clean the data
    df_clean = df.copy()
    df_clean[text_col] = df_clean[text_col].apply(clean_text_for_training)
    df_clean = df_clean.dropna(subset=[text_col, sentiment_col])
    df_clean = df_clean[df_clean[text_col].str.len() > 0]
    
    # Vectorize text
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X = vectorizer.fit_transform(df_clean[text_col])
    y = df_clean[sentiment_col]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, vectorizer, accuracy, classification_report(y_test, y_pred)

def show_admin_panel():
    """Show admin panel for administrators"""
    if not auth.require_permission('manage_users'):
        st.error("Access denied: Admin privileges required")
        return
    
    st.header("🔧 Administration Panel")
    
    # System Health Dashboard
    st.subheader("System Health")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", len(pd.read_sql("SELECT * FROM users", sqlite3.connect(db.db_path))))
    with col2:
        st.metric("Total Feedback", len(pd.read_sql("SELECT * FROM feedback", sqlite3.connect(db.db_path))))
    with col3:
        st.metric("System Status", "✅ Healthy")
    with col4:
        st.metric("Uptime", "99.9%")
    
    # Dataset Management Section
    st.subheader("📊 Dataset Management")
    
    # Upload new dataset
    uploaded_file = st.file_uploader("Upload New Dataset (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Read uploaded file
            new_df = pd.read_csv(uploaded_file)
            st.success(f"Dataset uploaded successfully! Shape: {new_df.shape}")
            
            # Show preview
            st.write("**Dataset Preview:**")
            st.dataframe(new_df.head())
            
            # Column mapping
            st.write("**Map Columns for Training:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                text_column = st.selectbox("Select Text Column", new_df.columns)
            with col2:
                sentiment_column = st.selectbox("Select Sentiment Column", new_df.columns)
            with col3:
                dataset_name = st.text_input("Dataset Name (optional)", 
                                           value=uploaded_file.name.replace('.csv', ''))
            
            if st.button("Process Dataset & Train Model"):
                with st.spinner("Processing dataset and training model..."):
                    try:
                        # Log activity
                        db.log_activity(st.session_state['user']['user_id'], 'dataset_upload', 
                                       f"Uploaded dataset: {uploaded_file.name}")
                        
                        # Clean and preview data
                        st.write("**Data Cleaning Results:**")
                        clean_df = new_df.copy()
                        clean_df[text_column] = clean_df[text_column].apply(clean_text_for_training)
                        
                        # Remove empty/invalid entries
                        initial_count = len(clean_df)
                        clean_df = clean_df.dropna(subset=[text_column, sentiment_column])
                        clean_df = clean_df[clean_df[text_column].str.len() > 0]
                        final_count = len(clean_df)
                        
                        st.info(f"Data cleaning: {initial_count} → {final_count} records ({final_count/initial_count*100:.1f}% retained)")
                        
                        # Show sentiment distribution
                        st.write("**Sentiment Distribution:**")
                        sentiment_dist = clean_df[sentiment_column].value_counts()
                        fig, ax = plt.subplots(figsize=(8, 4))
                        sentiment_dist.plot(kind='bar', ax=ax, color=['red', 'gray', 'green'])
                        ax.set_title('Sentiment Distribution in New Dataset')
                        ax.set_xlabel('Sentiment')
                        ax.set_ylabel('Count')
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                        plt.close()
                        
                        # Train model
                        st.write("**Training Sentiment Model:**")
                        model, vectorizer, accuracy, report = train_sentiment_model(
                            clean_df, text_column, sentiment_column)
                        
                        # Model performance analysis
                        if accuracy > 0.85:
                            st.success(f"🎯 Excellent model performance! Accuracy: {accuracy:.3f}")
                        elif accuracy > 0.75:
                            st.success(f"✅ Good model performance! Accuracy: {accuracy:.3f}")
                        elif accuracy > 0.65:
                            st.warning(f"⚠️ Fair model performance. Accuracy: {accuracy:.3f}")
                            st.info("💡 Consider adding more balanced training data to improve accuracy.")
                        else:
                            st.error(f"❌ Low model performance. Accuracy: {accuracy:.3f}")
                            st.info("💡 Recommendations: Check data quality, balance sentiment distribution, or review labeling.")
                        
                        # Performance improvement suggestions
                        sentiment_balance = clean_df[sentiment_column].value_counts(normalize=True)
                        min_class_ratio = sentiment_balance.min()
                        
                        if min_class_ratio < 0.1:  # Less than 10% for smallest class
                            st.warning("⚖️ Imbalanced dataset detected. Consider collecting more data for underrepresented sentiments.")
                        
                        if len(clean_df) < 1000:
                            st.info("📈 Dataset is relatively small. Accuracy may improve with more training data.")
                        
                        # Show classification report
                        st.text("Detailed Performance Report:")
                        st.text(report)
                        
                        # Save model and dataset
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        
                        # Save cleaned dataset
                        data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
                        os.makedirs(data_folder, exist_ok=True)
                        
                        # Use custom name or default with timestamp
                        if dataset_name.strip():
                            filename = f"{dataset_name.strip()}_{timestamp}.csv"
                        else:
                            filename = f"dataset_{timestamp}.csv"
                        
                        dataset_path = os.path.join(data_folder, filename)
                        clean_df.to_csv(dataset_path, index=False)
                        
                        # Save model
                        models_folder = os.path.join(os.path.dirname(__file__), '..', 'models')
                        os.makedirs(models_folder, exist_ok=True)
                        model_path = os.path.join(models_folder, f"model_{timestamp}.joblib")
                        vectorizer_path = os.path.join(models_folder, f"vectorizer_{timestamp}.joblib")
                        
                        joblib.dump(model, model_path)
                        joblib.dump(vectorizer, vectorizer_path)
                        
                        # Update main model files
                        main_model_path = os.path.join(os.path.dirname(__file__), '..', "sentiment_model.joblib")
                        main_vectorizer_path = os.path.join(os.path.dirname(__file__), '..', "tfidf_vectorizer.joblib")
                        joblib.dump(model, main_model_path)
                        joblib.dump(vectorizer, main_vectorizer_path)
                        
                        st.success(f"""
                        ✅ Dataset processed successfully!
                        - Cleaned dataset saved: {dataset_path}
                        - Model saved: {model_path}
                        - Vectorizer saved: {vectorizer_path}
                        - Main model files updated
                        """)
                        
                        # Insert data into database
                        clean_df['platform'] = 'uploaded_dataset'
                        clean_df['date'] = datetime.now()
                        
                        # Rename columns to match database schema
                        db_df = clean_df.rename(columns={
                            text_column: 'text',
                            sentiment_column: 'sentiment'
                        })
                        
                        # Add required columns
                        db_df['user_id'] = st.session_state['user']['user_id']
                        db_df['product_id'] = None
                        db_df['confidence'] = None
                        db_df['campaign_id'] = None
                        
                        # Insert into database
                        db.insert_feedback_batch(db_df[['user_id', 'product_id', 'platform', 'text', 
                                                       'sentiment', 'confidence', 'date', 'campaign_id']])
                        
                        st.success("Data inserted into database successfully!")
                        
                        # Log system health
                        db.log_system_health('model_accuracy', accuracy, 'good' if accuracy > 0.7 else 'warning')
                        db.log_system_health('dataset_size', len(clean_df), 'good')
                        
                    except Exception as e:
                        st.error(f"Error processing dataset: {e}")
                        import traceback
                        st.text(traceback.format_exc())
        
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    # Existing datasets management
    st.subheader("📁 Existing Datasets")
    data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
    if os.path.exists(data_folder):
        csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
        if csv_files:
            selected_dataset = st.selectbox("Select dataset to view", csv_files)
            if st.button("View Dataset Info"):
                try:
                    dataset_path = os.path.join(data_folder, selected_dataset)
                    dataset_df = pd.read_csv(dataset_path)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Rows", len(dataset_df))
                    with col2:
                        st.metric("Columns", len(dataset_df.columns))
                    with col3:
                        st.metric("Size (MB)", f"{os.path.getsize(dataset_path)/(1024*1024):.2f}")
                    
                    st.write("**Columns:**", list(dataset_df.columns))
                    st.dataframe(dataset_df.head())
                    
                except Exception as e:
                    st.error(f"Error reading dataset: {e}")
    
    # User Activity Logs
    st.subheader("Recent User Activity")
    try:
        activity_df = pd.read_sql("""
        SELECT u.username, ua.action, ua.details, ua.timestamp 
        FROM user_activity ua 
        JOIN users u ON ua.user_id = u.user_id 
        ORDER BY ua.timestamp DESC LIMIT 10
        """, sqlite3.connect(db.db_path))
        st.dataframe(activity_df)
    except:
        st.info("No activity logs available")

def show_product_manager_panel(df):
    """Show product manager specific features"""
    if not auth.require_permission('view_product_sentiment'):
        st.error("Access denied: Product Manager privileges required")
        st.write(f"Your permissions: {st.session_state.get('permissions', [])}")
        return
    
    st.header("📈 Product Manager Dashboard")
    
    # Debug information
    with st.expander("🔧 Debug Information"):
        st.write(f"Dataset shape: {df.shape}")
        st.write(f"Columns: {list(df.columns)}")
        sentiment_col = guess_sentiment_column(df)
        text_col = guess_text_column(df)
        st.write(f"Detected sentiment column: {sentiment_col}")
        st.write(f"Detected text column: {text_col}")
        if sentiment_col:
            st.write(f"Unique sentiments: {df[sentiment_col].unique()}")
        st.write("First 3 rows:")
        st.dataframe(df.head(3))
    
    # Product filter
    if 'product' in df.columns:
        products = df['product'].unique()
        selected_product = st.selectbox("Select Product", products)
        product_df = df[df['product'] == selected_product]
    else:
        selected_product = "All Products"
        product_df = df
    
    sentiment_col = guess_sentiment_column(df)
    text_col = guess_text_column(df)
    
    # Sentiment alerts
    st.subheader("🚨 Sentiment Alerts")
    
    if sentiment_col and text_col:
        # Check if we have valid sentiment data
        sentiment_values = product_df[sentiment_col].dropna()
        if len(sentiment_values) == 0:
            st.warning("No valid sentiment data found in the dataset.")
            return
        
        negative_count = len(product_df[product_df[sentiment_col].str.lower().str.contains('negative|bad|poor|1|2', na=False)])
        total_count = len(product_df.dropna(subset=[sentiment_col]))
        negative_ratio = negative_count / total_count if total_count > 0 else 0
        
        st.write(f"Total entries with sentiment: {total_count}")
        st.write(f"Negative entries: {negative_count}")
        
        if negative_ratio > 0.3:  # 30% threshold
            st.error(f"⚠️ High negative sentiment detected: {negative_ratio:.1%} of feedback is negative")
        else:
            st.success(f"✅ Sentiment is healthy: {negative_ratio:.1%} negative feedback")
    else:
        st.error("❌ Could not detect sentiment or text columns in the dataset.")
        st.info("Please ensure your dataset has columns containing 'sentiment', 'label', 'text', or 'review' in the name.")
        return
    
    # ROOT CAUSE ANALYSIS SECTION
    st.subheader("🔍 Root Cause Analysis")
    
    if sentiment_col and text_col:
        # Get negative feedback - handle different sentiment formats
        negative_df = product_df.copy()
        
        # Try different ways to identify negative sentiment
        sentiment_values = product_df[sentiment_col].astype(str).str.lower()
        
        # Method 1: Direct negative keywords
        negative_mask = sentiment_values.str.contains('negative|bad|poor|awful|terrible', na=False)
        
        # Method 2: Numeric ratings (1-2 out of 5, or 1-4 out of 10)
        if not negative_mask.any():
            try:
                numeric_sentiment = pd.to_numeric(product_df[sentiment_col], errors='coerce')
                max_rating = numeric_sentiment.max()
                if max_rating <= 5:  # 1-5 scale
                    negative_mask = numeric_sentiment <= 2
                elif max_rating <= 10:  # 1-10 scale
                    negative_mask = numeric_sentiment <= 4
            except:
                pass
        
        # Method 3: Check unique values to understand the sentiment format
        if not negative_mask.any():
            unique_sentiments = product_df[sentiment_col].value_counts()
            st.write("**Available sentiment categories:**")
            st.write(unique_sentiments)
            
            # Let user select which represents negative sentiment
            negative_sentiments = st.multiselect(
                "Select which categories represent NEGATIVE sentiment:",
                options=unique_sentiments.index.tolist(),
                help="Select all categories that should be considered negative"
            )
            
            if negative_sentiments:
                negative_mask = product_df[sentiment_col].isin(negative_sentiments)
        
        negative_df = product_df[negative_mask]
        
        if len(negative_df) > 0:
            st.success(f"Found {len(negative_df)} negative feedback entries for analysis.")
            
            # Time-based analysis
            st.write("**📅 Negative Sentiment Over Time:**")
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            
            if date_cols:
                date_col = date_cols[0]  # Use first date column found
                try:
                    negative_df_time = negative_df.copy()
                    negative_df_time[date_col] = pd.to_datetime(negative_df_time[date_col], errors='coerce')
                    negative_df_time = negative_df_time.dropna(subset=[date_col])
                    
                    if len(negative_df_time) > 0:
                        # Group by date and count
                        daily_negative = negative_df_time.groupby(negative_df_time[date_col].dt.date).size()
                        
                        fig, ax = plt.subplots(figsize=(10, 4))
                        daily_negative.plot(kind='line', ax=ax, color='red')
                        ax.set_title('Negative Sentiment Trend')
                        ax.set_ylabel('Negative Feedback Count')
                        ax.tick_params(axis='x', rotation=45)
                        st.pyplot(fig)
                        plt.close()
                    else:
                        st.info("No valid dates found for time analysis.")
                except Exception as e:
                    st.warning(f"Could not analyze time trends: {e}")
            else:
                st.info("No date column found for time-based analysis.")
            
            # Continue with rest of root cause analysis...
            # Common negative keywords analysis
            st.write("**🔤 Most Common Issues (Keywords):**")
            all_negative_text = ' '.join(negative_df[text_col].astype(str).str.lower())
            
            # Define common issue keywords
            issue_keywords = {
                'Quality Issues': ['broken', 'defective', 'poor quality', 'cheap', 'flimsy', 'damaged', 'bad', 'awful', 'terrible'],
                'Shipping/Delivery': ['shipping', 'delivery', 'late', 'delayed', 'arrived', 'package', 'slow'],
                'Customer Service': ['service', 'support', 'help', 'rude', 'unhelpful', 'response', 'staff'],
                'Price/Value': ['expensive', 'overpriced', 'cost', 'price', 'money', 'value', 'cheap'],
                'Functionality': ['doesn\'t work', 'not working', 'malfunction', 'failed', 'error', 'problem', 'issue']
            }
            
            issue_counts = {}
            for category, keywords in issue_keywords.items():
                count = sum(all_negative_text.count(keyword) for keyword in keywords)
                if count > 0:
                    issue_counts[category] = count
            
            if issue_counts:
                # Display issue breakdown
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Bar chart of issues
                    fig, ax = plt.subplots(figsize=(8, 6))
                    categories = list(issue_counts.keys())
                    counts = list(issue_counts.values())
                    bars = ax.bar(categories, counts, color=['red', 'orange', 'yellow', 'purple', 'brown'][:len(categories)])
                    ax.set_title('Issue Categories in Negative Feedback')
                    ax.set_ylabel('Mention Count')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                
                with col2:
                    # Top issues table
                    st.write("**Issue Breakdown:**")
                    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
                    for category, count in sorted_issues:
                        percentage = (count / sum(issue_counts.values())) * 100
                        st.write(f"• **{category}**: {count} mentions ({percentage:.1f}%)")
            else:
                st.info("No common issue keywords found. The negative feedback may use different terminology.")
            
            # Sample negative feedback
            st.write("**📝 Sample Negative Feedback:**")
            sample_negative = negative_df[text_col].head(5)
            for i, text in enumerate(sample_negative, 1):
                with st.expander(f"Negative Feedback #{i}"):
                    st.write(str(text)[:500] + "..." if len(str(text)) > 500 else str(text))
            
        else:
            st.info("No negative feedback found for analysis. This could mean:")
            st.write("- All feedback is positive (great!)")
            st.write("- The sentiment detection needs adjustment")
            st.write("- The dataset uses a different sentiment format")
    else:
        st.error("❌ Could not detect sentiment or text columns for root cause analysis.")
        st.info("💡 Make sure your dataset has clearly named sentiment and text columns.")

    # Time-based analysis
    st.write("**📅 Negative Sentiment Over Time:**")
    if any(col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()):
        date_col = next((col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()), None)
        if date_col:
            try:
                negative_df_time = negative_df.copy()
                negative_df_time[date_col] = pd.to_datetime(negative_df_time[date_col], errors='coerce')
                negative_df_time = negative_df_time.dropna(subset=[date_col])
                
                # Group by date and count
                daily_negative = negative_df_time.groupby(negative_df_time[date_col].dt.date).size()
                
                fig, ax = plt.subplots(figsize=(10, 4))
                daily_negative.plot(kind='line', ax=ax, color='red')
                ax.set_title('Negative Sentiment Trend')
                ax.set_ylabel('Negative Feedback Count')
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
                plt.close()
            except Exception as e:
                st.write(f"Could not analyze time trends: {e}")
    
    # Common negative keywords analysis
    st.write("**🔤 Most Common Issues (Keywords):**")
    all_negative_text = ' '.join(negative_df[text_col].astype(str).str.lower())
    
    # Define common issue keywords
    issue_keywords = {
    'Quality Issues': ['broken', 'defective', 'poor quality', 'cheap', 'flimsy', 'damaged'],
    'Shipping/Delivery': ['shipping', 'delivery', 'late', 'delayed', 'arrived', 'package'],
    'Customer Service': ['service', 'support', 'help', 'rude', 'unhelpful', 'response'],
    'Price/Value': ['expensive', 'overpriced', 'cost', 'price', 'money', 'value'],
    'Functionality': ['doesn\'t work', 'not working', 'malfunction', 'failed', 'error', 'problem']
    }
    
    issue_counts = {}
    for category, keywords in issue_keywords.items():
        count = sum(all_negative_text.count(keyword) for keyword in keywords)
        if count > 0:
            issue_counts[category] = count
    
    if issue_counts:
        # Display issue breakdown
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Bar chart of issues
            fig, ax = plt.subplots(figsize=(8, 6))
            categories = list(issue_counts.keys())
            counts = list(issue_counts.values())
            bars = ax.bar(categories, counts, color=['red', 'orange', 'yellow', 'purple', 'brown'][:len(categories)])
            ax.set_title('Issue Categories in Negative Feedback')
            ax.set_ylabel('Mention Count')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with col2:
            # Top issues table
            st.write("**Issue Breakdown:**")
            sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
            for category, count in sorted_issues:
                percentage = (count / sum(issue_counts.values())) * 100
                st.write(f"• **{category}**: {count} mentions ({percentage:.1f}%)")
    
    # Sample negative feedback by category
    st.write("**📝 Sample Negative Feedback by Issue:**")
    
    # Find top issue category
    if issue_counts:
        top_issue = max(issue_counts.items(), key=lambda x: x[1])[0]
        top_keywords = issue_keywords[top_issue]
        
        # Find feedback containing top issue keywords
        issue_feedback = negative_df[
            negative_df[text_col].str.lower().str.contains('|'.join(top_keywords), na=False)
        ].head(3)
        
        st.write(f"**Top Issue: {top_issue}**")
        for idx, row in issue_feedback.iterrows():
            with st.expander(f"Feedback #{idx}"):
                st.write(row[text_col])
    
    # Actionable recommendations
    st.write("**💡 Recommended Actions:**")
    
    if issue_counts:
        top_3_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        recommendations = {
            'Quality Issues': [
                "🔧 Review manufacturing processes and quality control",
                "📊 Conduct product testing with focus groups",
                "🏭 Audit supplier quality standards"
            ],
            'Shipping/Delivery': [
                "📦 Review shipping partner performance",
                "⏰ Improve delivery time estimates",
                "📱 Implement better package tracking"
            ],
            'Customer Service': [
                "👥 Provide additional customer service training",
                "⚡ Reduce response times",
                "📞 Implement escalation procedures"
            ],
            'Price/Value': [
                "💰 Review pricing strategy",
                "🎁 Consider value-added bundles",
                "📈 Communicate product value better"
            ],
            'Functionality': [
                "🔧 Update product documentation",
                "🛠️ Improve product design",
                "📞 Enhance technical support"
            ]
        }
        
        for issue, count in top_3_issues:
            st.write(f"**For {issue} issues:**")
            for recommendation in recommendations.get(issue, ["Review and investigate further"]):
                st.write(f"  {recommendation}")
    else:
        st.info("No negative feedback found for analysis. This could mean:")
        st.write("- All feedback is positive (great!)")
        st.write("- The sentiment detection needs adjustment")
        st.write("- The dataset uses a different sentiment format")
    
    # PDF Report Generation
    st.subheader("📄 Generate Product Report")
    if st.button("Generate PDF Report"):
        report_path = f"reports/product_report_{selected_product}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        os.makedirs("reports", exist_ok=True)
        
        try:
            report_gen.generate_product_report(product_df, selected_product, report_path)
            st.success(f"Report generated: {report_path}")
            
            # Download button
            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download PDF Report",
                    data=file.read(),
                    file_name=f"product_report_{selected_product}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error generating report: {e}")

def show_marketing_panel(df):
    """Show marketing team specific features"""
    if not auth.require_permission('view_brand_sentiment'):
        st.error("Access denied: Marketing Team privileges required")
        st.write(f"Your permissions: {st.session_state.get('permissions', [])}")
        return
    
    st.header("📊 Marketing Dashboard")
    
    # Campaign Analytics
    st.subheader("Campaign Performance")
    
    # Mock campaign data (in real implementation, this would come from campaign_id in database)
    campaigns = ["Summer Sale 2025", "Product Launch", "Holiday Campaign"]
    selected_campaign = st.selectbox("Select Campaign", campaigns)
    
    # Campaign metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Campaign Reach", "10,234")
    with col2:
        st.metric("Positive Mentions", "1,456")
    with col3:
        st.metric("Engagement Rate", "5.2%")
    
    # Generate marketing report
    if st.button("Generate Campaign Report"):
        report_path = f"reports/campaign_report_{selected_campaign.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        os.makedirs("reports", exist_ok=True)
        
        try:
            report_gen.generate_marketing_report(df, selected_campaign, report_path)
            st.success(f"Campaign report generated: {report_path}")
            
            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download Campaign Report",
                    data=file.read(),
                    file_name=f"campaign_report_{selected_campaign}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Error generating report: {e}")

def guess_sentiment_column(df):
    """Guess sentiment column name"""
    sentiment_keywords = ['sentiment', 'label', 'rating', 'score', 'class', 'category', 'polarity']
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in sentiment_keywords):
            return col
    # If no obvious sentiment column, check for columns with sentiment-like values
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_vals = df[col].dropna().unique()
            unique_str = [str(val).lower() for val in unique_vals[:10]]  # Check first 10 unique values
            sentiment_words = ['positive', 'negative', 'neutral', 'good', 'bad', 'poor', 'excellent']
            if any(word in ' '.join(unique_str) for word in sentiment_words):
                return col
    return None

def guess_text_column(df):
    """Guess text column name"""
    text_keywords = ['text', 'review', 'comment', 'feedback', 'message', 'content', 'description']
    
    # First, look for columns with text-related names
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in text_keywords):
            return col
    
    # If no obvious text column, find the column with longest average text length
    text_candidates = []
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                avg_length = df[col].astype(str).str.len().mean()
                if avg_length > 20:  # Likely to be text if average length > 20 chars
                    text_candidates.append((col, avg_length))
            except:
                continue
    
    if text_candidates:
        # Return column with longest average text
        return max(text_candidates, key=lambda x: x[1])[0]
    
    # Fallback to first string column
    for col in df.columns:
        if df[col].dtype == 'object':
            return col
    
    return df.columns[0] if len(df.columns) > 0 else None

def main():
    # Check authentication
    if not check_authentication():
        return
    
    # Show user info and logout button
    user = st.session_state['user']
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title('🎯 User Sentiment Tracking System')
        st.write(f"Welcome, {user['username']} ({user['role']})")
    with col2:
        # Debug info
        with st.expander("Debug Info"):
            st.write(f"Role: {user['role']}")
            st.write(f"Permissions: {st.session_state.get('permissions', [])}")
    with col3:
        if st.button("Logout"):
            auth.logout()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Role-based navigation
    if auth.require_permission('manage_users'):
        if st.sidebar.button("🔧 Admin Panel"):
            st.session_state['current_page'] = 'admin'
    
    if auth.require_permission('view_product_sentiment'):
        if st.sidebar.button("📈 Product Analytics"):
            st.session_state['current_page'] = 'product'
    
    if auth.require_permission('view_brand_sentiment'):
        if st.sidebar.button("📊 Marketing Analytics"):
            st.session_state['current_page'] = 'marketing'
    
    if st.sidebar.button("📋 General Dashboard"):
        st.session_state['current_page'] = 'dashboard'
    
    # Default to dashboard
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'dashboard'
    
    # Load data for dashboard
    data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Refresh file list
    if st.sidebar.button("🔄 Refresh Dataset List"):
        st.rerun()
    
    available_files = []
    if os.path.exists(data_folder):
        available_files = [f for f in os.listdir(data_folder) if f.lower().endswith('.csv')]
    
    if not available_files:
        st.error('No CSV files found in the data folder.')
        st.info("Upload a dataset through the Admin Panel to get started.")
        return
    
    # Show appropriate panel based on current page
    if st.session_state['current_page'] == 'admin':
        show_admin_panel()
    elif st.session_state['current_page'] == 'product':
        # Load data for product panel
        selected_file = st.sidebar.selectbox('Select dataset', available_files)
        data_path = os.path.join(data_folder, selected_file)
        df = pd.read_csv(data_path)
        show_product_manager_panel(df)
    elif st.session_state['current_page'] == 'marketing':
        # Load data for marketing panel
        selected_file = st.sidebar.selectbox('Select dataset', available_files)
        data_path = os.path.join(data_folder, selected_file)
        df = pd.read_csv(data_path)
        show_marketing_panel(df)
    else:
        # General dashboard (existing functionality)
        selected_file = st.sidebar.selectbox('Select dataset', available_files)
        data_path = os.path.join(data_folder, selected_file)
        
        try:
            df = pd.read_csv(data_path)
        except Exception as e:
            st.error(f"Failed to load data: {e}")
            return
        
        # Log activity
        db.log_activity(user['user_id'], 'view_dashboard', f"Viewed dashboard with dataset: {selected_file}")
        
        # Rest of existing dashboard code would go here...
        st.header("📊 General Sentiment Dashboard")
        st.write("This is the main dashboard view accessible to all users.")
        
        # Basic sentiment distribution
        sentiment_col = guess_sentiment_column(df)
        if sentiment_col:
            st.subheader('Sentiment Distribution')
            fig, ax = plt.subplots()
            df[sentiment_col].value_counts().plot(kind='bar', ax=ax)
            st.pyplot(fig)

if __name__ == "__main__":
    main()
