import streamlit as st
import bcrypt
import sqlite3
import os

class AuthManager:
    def __init__(self):
        self.db_path = 'data/sentiment_system.db'
        self.setup_auth_config()
    
    def setup_auth_config(self):
        """Setup authentication configuration"""
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Create default users
        self.create_default_users()
    
    def create_default_users(self):
        """Create default users for demo"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create users table if not exists
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
            
            # Create default admin user
            admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, role) 
            VALUES (?, ?, ?, ?)
            ''', ("admin", "admin@example.com", admin_password, "administrator"))
            
            # Create product manager user
            pm_password = bcrypt.hashpw("pm123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, role) 
            VALUES (?, ?, ?, ?)
            ''', ("product_manager", "pm@example.com", pm_password, "product_manager"))
            
            # Create marketing user
            marketing_password = bcrypt.hashpw("marketing123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, role) 
            VALUES (?, ?, ?, ?)
            ''', ("marketing", "marketing@example.com", marketing_password, "marketing"))
            
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Database setup error: {e}")
    
    def show_login_form(self):
        """Show login form"""
        st.title("🔐 Login to Sentiment Tracking System")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", type="primary"):
                user = self.authenticate_user(username, password)
                if user:
                    st.session_state['authenticated'] = True
                    st.session_state['user'] = user
                    st.session_state['permissions'] = self.get_user_permissions(user['role'])
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with col2:
            st.subheader("Demo Accounts")
            st.info("""
            **Available Demo Accounts:**
            
            🔧 **Administrator**
            - Username: `admin`
            - Password: `admin123`
            - Access: Full system access
            
            📈 **Product Manager**
            - Username: `product_manager`
            - Password: `pm123`
            - Access: Product analytics
            
            📊 **Marketing Team**
            - Username: `marketing`
            - Password: `marketing123`
            - Access: Brand sentiment
            """)
    
    def authenticate_user(self, username, password):
        """Authenticate user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT user_id, username, email, password_hash, role 
            FROM users WHERE username = ?
            ''', (username,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[3].encode('utf-8')):
                return {
                    'user_id': user_data[0],
                    'username': user_data[1],
                    'email': user_data[2],
                    'role': user_data[4]
                }
            return None
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    def get_user_permissions(self, role):
        """Get user permissions based on role"""
        permissions = {
            'administrator': ['manage_users', 'view_product_sentiment', 'view_brand_sentiment', 'export_data'],
            'product_manager': ['view_product_sentiment', 'export_data'],
            'marketing': ['view_brand_sentiment', 'export_data'],
            'user': ['view_dashboard']
        }
        return permissions.get(role, ['view_dashboard'])
    
    def require_permission(self, permission):
        """Check if user has required permission"""
        user_permissions = st.session_state.get('permissions', [])
        return permission in user_permissions
    
    def logout(self):
        """Logout user"""
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        st.session_state['permissions'] = []
        st.rerun()
