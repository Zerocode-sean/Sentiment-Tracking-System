import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import sqlite3

# Try to import optional dependencies with fallbacks
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    st.warning("WordCloud not available - word cloud features disabled")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not available - some charts may use matplotlib instead")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    import joblib
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("Scikit-learn not available - ML features disabled")

# Configure Streamlit page
st.set_page_config(
    page_title="Sentiment Tracking System",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("🎯 User Sentiment Tracking System")
    st.write("Welcome to the Sentiment Analysis Dashboard!")
    
    # Simple authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        with st.sidebar:
            st.header("Login")
            username = st.text_input("Username", value="demo")
            password = st.text_input("Password", type="password", value="demo123")
            
            if st.button("Login"):
                # Simple demo authentication
                if username in ["demo", "admin", "user"] and password in ["demo123", "admin123"]:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try: demo/demo123")
        
        st.info("Please log in to access the dashboard. Use demo/demo123 for quick access.")
        return
    
    # Main dashboard
    st.sidebar.write(f"Welcome, {st.session_state['username']}!")
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.rerun()
    
    # Dashboard content
    st.header("📊 Dashboard Overview")
    
    # Sample data
    @st.cache_data
    def load_sample_data():
        np.random.seed(42)
        data = {
            'text': [
                'This product is amazing!', 'Terrible quality, very disappointed',
                'Good value for money', 'Could be better', 'Excellent service',
                'Poor customer support', 'Love this product!', 'Not worth the price',
                'Great features', 'Delivery was slow'
            ],
            'sentiment': ['positive', 'negative', 'positive', 'neutral', 'positive',
                         'negative', 'positive', 'negative', 'positive', 'negative'],
            'date': pd.date_range('2025-07-01', periods=10, freq='D'),
            'platform': np.random.choice(['Twitter', 'Facebook', 'Reviews'], 10)
        }
        return pd.DataFrame(data)
    
    df = load_sample_data()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Feedback", len(df))
    with col2:
        positive_count = len(df[df['sentiment'] == 'positive'])
        st.metric("Positive", positive_count)
    with col3:
        negative_count = len(df[df['sentiment'] == 'negative'])
        st.metric("Negative", negative_count)
    with col4:
        neutral_count = len(df[df['sentiment'] == 'neutral'])
        st.metric("Neutral", neutral_count)
    
    # Sentiment distribution
    st.subheader("Sentiment Distribution")
    sentiment_counts = df['sentiment'].value_counts()
    
    if PLOTLY_AVAILABLE:
        fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                     title="Sentiment Distribution")
        st.plotly_chart(fig)
    else:
        # Use matplotlib as fallback
        fig, ax = plt.subplots()
        ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
        ax.set_title('Sentiment Distribution')
        st.pyplot(fig)
        plt.close()
    
    # Timeline
    st.subheader("Sentiment Over Time")
    daily_sentiment = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
    
    if PLOTLY_AVAILABLE:
        fig = px.line(daily_sentiment, title="Sentiment Trends Over Time")
        st.plotly_chart(fig)
    else:
        # Use matplotlib as fallback
        fig, ax = plt.subplots(figsize=(10, 6))
        for sentiment in daily_sentiment.columns:
            ax.plot(daily_sentiment.index, daily_sentiment[sentiment], 
                   label=sentiment, marker='o')
        ax.set_title('Sentiment Trends Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        plt.close()
    
    # Platform breakdown
    st.subheader("Platform Breakdown")
    platform_sentiment = df.groupby(['platform', 'sentiment']).size().unstack(fill_value=0)
    
    if PLOTLY_AVAILABLE:
        fig = px.bar(platform_sentiment, title="Sentiment by Platform")
        st.plotly_chart(fig)
    else:
        # Use matplotlib as fallback
        fig, ax = plt.subplots()
        platform_sentiment.plot(kind='bar', ax=ax)
        ax.set_title('Sentiment by Platform')
        ax.set_xlabel('Platform')
        ax.set_ylabel('Count')
        ax.legend(title='Sentiment')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close()
    
    # Data table
    st.subheader("Recent Feedback")
    st.dataframe(df)
    
    # Word cloud (if available)
    if WORDCLOUD_AVAILABLE:
        st.subheader("Word Cloud")
        text_data = ' '.join(df['text'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        plt.close()
    
    # System info
    with st.expander("System Information"):
        st.write("**Available Features:**")
        st.write(f"- WordCloud: {'✅' if WORDCLOUD_AVAILABLE else '❌'}")
        st.write(f"- Plotly Charts: {'✅' if PLOTLY_AVAILABLE else '❌'}")
        st.write(f"- Scikit-learn ML: {'✅' if SKLEARN_AVAILABLE else '❌'}")
        st.write(f"- Matplotlib: ✅")
        st.write(f"- Pandas: ✅")
        st.write(f"- NumPy: ✅")

if __name__ == "__main__":
    main()
