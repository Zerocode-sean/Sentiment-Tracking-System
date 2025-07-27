import sqlite3
import pandas as pd
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='data/sentiment_system.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Feedback table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id TEXT,
            platform TEXT,
            text TEXT,
            sentiment TEXT,
            confidence REAL,
            date TIMESTAMP,
            campaign_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # User activity table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_activity (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # System health table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_health (
            health_id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT,
            metric_value REAL,
            status TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, username, email, password_hash, role):
        """Add a user to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, role) 
            VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, role))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def log_activity(self, user_id, action, details):
        """Log user activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO user_activity (user_id, action, details) 
            VALUES (?, ?, ?)
            ''', (user_id, action, details))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error logging activity: {e}")
    
    def log_system_health(self, metric_name, metric_value, status):
        """Log system health metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO system_health (metric_name, metric_value, status) 
            VALUES (?, ?, ?)
            ''', (metric_name, metric_value, status))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error logging system health: {e}")
    
    def insert_feedback_batch(self, feedback_df):
        """Insert batch feedback data"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            feedback_df.to_sql('feedback', conn, if_exists='append', index=False)
            
            conn.close()
            return True
        except Exception as e:
            print(f"Error inserting feedback batch: {e}")
            return False
    
    def get_feedback_data(self, limit=None):
        """Get feedback data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = "SELECT * FROM feedback ORDER BY date DESC"
            if limit:
                query += f" LIMIT {limit}"
                
            df = pd.read_sql(query, conn)
            conn.close()
            
            return df
        except Exception as e:
            print(f"Error getting feedback data: {e}")
            return pd.DataFrame()
    
    def get_user_activity(self, limit=10):
        """Get recent user activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
            SELECT u.username, ua.action, ua.details, ua.timestamp 
            FROM user_activity ua 
            JOIN users u ON ua.user_id = u.user_id 
            ORDER BY ua.timestamp DESC 
            LIMIT ?
            '''
            
            df = pd.read_sql(query, conn, params=(limit,))
            conn.close()
            
            return df
        except Exception as e:
            print(f"Error getting user activity: {e}")
            return pd.DataFrame()
