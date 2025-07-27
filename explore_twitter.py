import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
import joblib
import numpy as np

# Path to the Twitter dataset (update if needed)
dataset_path = 'data/Tweets.csv'

def clean_text(text):
    """Clean tweet text by removing URLs, mentions, hashtags, special characters, and extra whitespace."""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'#', '', text)  # Remove hashtag symbol (keep the word)
    text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters and numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text

def main():
    # Load the dataset
    df = pd.read_csv(dataset_path)
    # Clean the tweet text
    if 'text' in df.columns and 'airline_sentiment' in df.columns:
        df['cleaned_text'] = df['text'].apply(clean_text)
        print(df[['text', 'cleaned_text']].head())
        # Feature extraction
        X = df['cleaned_text']
        y = df['airline_sentiment']
        vectorizer = TfidfVectorizer(max_features=1000)
        X_vec = vectorizer.fit_transform(X)
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
        print(f"Feature matrix shape: {X_vec.shape}")
        print(f"Training samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")
        # Train a Logistic Regression model
        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)
        # Predict on test set
        y_pred = model.predict(X_test)
        # Evaluate the model
        acc = accuracy_score(y_test, y_pred)
        print(f"\nTest Accuracy: {acc:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        # Hyperparameter tuning with GridSearchCV
        param_grid = {'C': [0.01, 0.1, 1, 10, 100]}
        grid = GridSearchCV(LogisticRegression(max_iter=200), param_grid, cv=3, n_jobs=-1)
        grid.fit(X_train, y_train)
        print(f"Best parameters from GridSearchCV: {grid.best_params_}")
        # Use the best estimator
        best_model = grid.best_estimator_
        y_pred = best_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"\nTest Accuracy (tuned): {acc:.4f}")
        print("\nClassification Report (tuned):")
        print(classification_report(y_test, y_pred))
        # Visualize confusion matrix
        cm = confusion_matrix(y_test, y_pred, labels=best_model.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=best_model.classes_)
        disp.plot(cmap=plt.cm.Blues)
        plt.title('Confusion Matrix (Tuned)')
        plt.show()

        # Show a few misclassified tweets
        misclassified = np.where(y_test != y_pred)[0]
        print(f"\nNumber of misclassified tweets: {len(misclassified)}")
        if len(misclassified) > 0:
            print("\nSample misclassified tweets:")
            X_test_text = X.iloc[y_test.index]
            for idx in misclassified[:5]:
                print(f"Tweet: {X_test_text.iloc[idx]}")
                print(f"True label: {y_test.iloc[idx]}, Predicted: {y_pred[idx]}")
                print('-' * 60)

        # Visualize sentiment distribution
        sentiment_counts = df['airline_sentiment'].value_counts()
        sentiment_counts.plot(kind='bar', color=['red', 'gray', 'green'])
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Number of Tweets')
        plt.show()

        # Save the best model and vectorizer
        joblib.dump(best_model, 'sentiment_model.joblib')
        joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')
        print("Saved best model as 'sentiment_model.joblib' and vectorizer as 'tfidf_vectorizer.joblib'.")

    else:
        print("Required columns 'text' and/or 'airline_sentiment' not found in dataset. Available columns:", df.columns)

if __name__ == '__main__':
    main() 