import streamlit as st
import pandas as pd
import numpy as np

# Simple demo app that works with minimal dependencies
st.set_page_config(page_title="Sentiment Tracker", page_icon="📊", layout="wide")

def main():
    st.title("🎯 Sentiment Tracking System")
    st.write("**Demo Version - Minimal Dependencies**")
    
    # Simple authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.subheader("🔐 Login")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            username = st.text_input("Username", value="demo")
            password = st.text_input("Password", type="password", value="demo123")
            
            if st.button("Login", type="primary"):
                if username == "demo" and password == "demo123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Use: demo / demo123")
        
        with col2:
            st.info("""
            **Demo Credentials:**
            - Username: `demo`
            - Password: `demo123`
            
            **Features:**
            - ✅ Real-time sentiment analysis
            - ✅ Interactive dashboards  
            - ✅ Multi-platform tracking
            - ✅ Export capabilities
            """)
        return
    
    # Main app content
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Welcome, {st.session_state.get('username', 'Demo User')}!")
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    # Dashboard metrics
    st.subheader("📊 Dashboard Overview")
    
    # Generate sample data
    @st.cache_data
    def get_sample_data():
        np.random.seed(42)
        dates = pd.date_range('2025-07-01', periods=30, freq='D')
        data = []
        
        for date in dates:
            for _ in range(np.random.randint(10, 50)):
                sentiment = np.random.choice(['Positive', 'Negative', 'Neutral'], 
                                           p=[0.6, 0.25, 0.15])
                platform = np.random.choice(['Twitter', 'Facebook', 'Reviews', 'Instagram'])
                data.append({
                    'date': date,
                    'sentiment': sentiment,
                    'platform': platform,
                    'text': f"Sample {sentiment.lower()} feedback from {platform}"
                })
        
        return pd.DataFrame(data)
    
    df = get_sample_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_feedback = len(df)
    positive_feedback = len(df[df['sentiment'] == 'Positive'])
    negative_feedback = len(df[df['sentiment'] == 'Negative'])
    neutral_feedback = len(df[df['sentiment'] == 'Neutral'])
    
    with col1:
        st.metric("Total Feedback", f"{total_feedback:,}")
    with col2:
        st.metric("Positive", f"{positive_feedback:,}", 
                 delta=f"{positive_feedback/total_feedback*100:.1f}%")
    with col3:
        st.metric("Negative", f"{negative_feedback:,}", 
                 delta=f"-{negative_feedback/total_feedback*100:.1f}%")
    with col4:
        st.metric("Neutral", f"{neutral_feedback:,}", 
                 delta=f"{neutral_feedback/total_feedback*100:.1f}%")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sentiment Distribution")
        sentiment_counts = df['sentiment'].value_counts()
        st.bar_chart(sentiment_counts)
    
    with col2:
        st.subheader("Platform Breakdown")
        platform_counts = df['platform'].value_counts()
        st.bar_chart(platform_counts)
    
    # Time series
    st.subheader("Sentiment Trends Over Time")
    daily_sentiment = df.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
    st.line_chart(daily_sentiment)
    
    # Recent feedback
    st.subheader("Recent Feedback")
    st.dataframe(
        df.tail(10)[['date', 'platform', 'sentiment', 'text']], 
        use_container_width=True
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    🎯 <strong>Sentiment Tracking System</strong> | 
    Built with Streamlit | 
    <a href='https://github.com/Zerocode-sean/Sentiment-Tracking-System' target='_blank'>GitHub</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
