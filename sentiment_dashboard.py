import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud
import joblib
import sqlite3
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit_authenticator as stauth
import bcrypt

st.title('Sentiment Analysis Dashboard')

# List available CSV files in the data folder
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
available_files = [f for f in os.listdir(data_folder) if f.lower().endswith('.csv')]

if not available_files:
    st.error('No CSV files found in the data folder.')
    st.stop()

selected_file = st.sidebar.selectbox('Select dataset', available_files)
data_path = os.path.join(data_folder, selected_file)

try:
    df = pd.read_csv(data_path)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Choose columns for text and sentiment
def guess_sentiment_column(df):
    for col in df.columns:
        if 'sentiment' in col.lower() or 'score' in col.lower() or 'label' in col.lower():
            return col
    return df.columns[-1]

def guess_text_column(df):
    for col in df.columns:
        if 'text' in col.lower() or 'review' in col.lower():
            return col
    return df.columns[0]

sentiment_col = guess_sentiment_column(df)
text_col = guess_text_column(df)

st.sidebar.header('Filters')
unique_sentiments = df[sentiment_col].unique()
selected_sentiments = st.sidebar.multiselect('Select Sentiments', unique_sentiments, default=list(unique_sentiments))

filtered_df = df[df[sentiment_col].isin(selected_sentiments)]

# Enhanced Time Range Selector
st.sidebar.subheader('Time Range Filter')
if 'date' in df.columns or 'time' in df.columns:
    date_col = 'date' if 'date' in df.columns else 'time'
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    
    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()
    
    date_range = st.sidebar.date_input(
        'Select date range',
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df[date_col].dt.date >= start_date) & 
            (filtered_df[date_col].dt.date <= end_date)
        ]

st.subheader('Sentiment Distribution')
fig, ax = plt.subplots()
filtered_df[sentiment_col].value_counts().plot(kind='bar', color=['red', 'gray', 'green'], ax=ax)
plt.xlabel('Sentiment')
plt.ylabel('Count')
st.pyplot(fig)

# Pie Chart Option for Sentiment Distribution
st.subheader('Sentiment Distribution (Pie Chart)')
fig_pie, ax_pie = plt.subplots()
filtered_df[sentiment_col].value_counts().plot(
    kind='pie', autopct='%1.1f%%', startangle=90, ax=ax_pie, colors=['red', 'gray', 'green'][:len(unique_sentiments)])
ax_pie.set_ylabel('')
ax_pie.set_xlabel('')
ax_pie.set_title('')
st.pyplot(fig_pie)

st.subheader('Sample Reviews')
st.write(filtered_df[[text_col, sentiment_col]].sample(min(5, len(filtered_df))))

if 'date' in df.columns or 'time' in df.columns:
    date_col = 'date' if 'date' in df.columns else 'time'
    st.subheader('Sentiment Over Time (with Rolling Average)')
    time_df = filtered_df.copy()
    time_df[date_col] = pd.to_datetime(time_df[date_col], errors='coerce')
    time_df = time_df.dropna(subset=[date_col])
    time_df = time_df.sort_values(date_col)
    # Group by date and sentiment
    grouped = time_df.groupby([pd.Grouper(key=date_col, freq='D'), sentiment_col]).size().unstack().fillna(0)
    # Rolling average
    window = st.slider('Rolling window (days)', min_value=1, max_value=30, value=7)
    grouped_rolling = grouped.rolling(window=window, min_periods=1).mean()
    fig2, ax2 = plt.subplots()
    grouped_rolling.plot(ax=ax2)
    plt.ylabel('Rolling Avg Count')
    plt.title(f'Sentiment Over Time ({window}-day Rolling Avg)')
    st.pyplot(fig2)

# Word Cloud Visualization
st.subheader('Word Cloud by Sentiment')
selected_wc_sentiment = st.selectbox('Select sentiment for word cloud', unique_sentiments)
wc_text = ' '.join(filtered_df[filtered_df[sentiment_col] == selected_wc_sentiment][text_col].astype(str))
if wc_text.strip():
    wc = WordCloud(width=800, height=400, background_color='white').generate(wc_text)
    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wc, interpolation='bilinear')
    ax_wc.axis('off')
    st.pyplot(fig_wc)
else:
    st.info('No text available for this sentiment.')

# Download Filtered Data
st.subheader('Download Filtered Data')
filtered_csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label='Download filtered data as CSV',
    data=filtered_csv,
    file_name='filtered_sentiment_data.csv',
    mime='text/csv'
)

# Search/Highlight Reviews by Keyword
st.subheader('Search Reviews by Keyword')
search_term = st.text_input('Enter keyword to search in reviews:')
if search_term:
    search_results = filtered_df[filtered_df[text_col].str.contains(search_term, case=False, na=False)]
    st.write(f"Found {len(search_results)} reviews containing '{search_term}':")
    st.write(search_results[[text_col, sentiment_col]].head(10))
    if len(search_results) == 0:
        st.info('No reviews found with that keyword.')

# Model Prediction Section
st.subheader('Predict Sentiment for Your Own Text')
user_input = st.text_area('Enter text to analyze sentiment:')
if st.button('Predict Sentiment') and user_input.strip():
    try:
        model = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'sentiment_model.joblib'))
        vectorizer = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'tfidf_vectorizer.joblib'))
        cleaned = user_input  # Optionally, apply your clean_text function here
        X_vec = vectorizer.transform([cleaned])
        pred = model.predict(X_vec)[0]
        st.success(f'Predicted Sentiment: {pred}')
    except Exception as e:
        st.error(f'Prediction failed: {e}')

# Platform Comparison Visualization (if platform column exists)
if any(col.lower() in ['platform', 'source', 'channel'] for col in df.columns):
    platform_col = next(col for col in df.columns if col.lower() in ['platform', 'source', 'channel'])
    st.subheader('Platform Comparison')
    fig_platform, ax_platform = plt.subplots()
    pd.crosstab(filtered_df[platform_col], filtered_df[sentiment_col]).plot(kind='bar', ax=ax_platform)
    plt.xlabel('Platform')
    plt.ylabel('Count')
    plt.title('Sentiment by Platform')
    st.pyplot(fig_platform)
else:
    st.info('No platform/source/channel column found for platform comparison.')
