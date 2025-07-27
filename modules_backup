import streamlit as st
import streamlit_authenticator as stauth
import bcrypt
from database_manager import DatabaseManager
import yaml

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.setup_auth_config()
    
    def setup_auth_config(self):
        """Setup authentication configuration"""
        # Create default admin user if not exists
        admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.db.add_user("admin", "admin@example.com", admin_password, "administrator")
        
        # Create sample users
        pm_password = bcrypt.hashpw("pm123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.db.add_user("product_manager", "pm@example.com", pm_password, "product_manager")
        
        marketing_password = bcrypt.hashpw("marketing123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.db.add_user("marketing_team", "marketing@example.com", marketing_password, "marketing_team")
    
    def authenticate_user(self, username, password):
        """Authenticate user"""
        user = self.db.get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            return {
                'user_id': user[0],
                'username': user[1],
                'email': user[2],
                'role': user[4]
            }
        return None
    
    def get_user_permissions(self, role):
        """Get user permissions based on role"""
        permissions = {
            'administrator': [
                'manage_users', 'manage_data', 'view_all_reports', 
                'system_health', 'audit_logs', 'view_product_sentiment',
                'view_brand_sentiment', 'export_reports', 'product_analytics',
                'campaign_analytics', 'export_marketing_data'
            ],
            'product_manager': [
                'view_product_sentiment', 'export_reports', 
                'product_analytics', 'view_basic_dashboard'
            ],
            'marketing_team': [
                'view_brand_sentiment', 'campaign_analytics', 
                'export_marketing_data', 'view_basic_dashboard'
            ],
            'viewer': ['view_basic_dashboard']
        }
        return permissions.get(role, ['view_basic_dashboard'])
    
    def show_login_form(self):
        """Display login form"""
        st.title("User Sentiment Tracking System - Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                user = self.authenticate_user(username, password)
                if user:
                    st.session_state['authenticated'] = True
                    st.session_state['user'] = user
                    st.session_state['permissions'] = self.get_user_permissions(user['role'])
                    self.db.log_activity(user['user_id'], 'login', f"User {username} logged in")
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        # Show demo credentials
        st.info("""
        Demo Credentials:
        - Admin: admin / admin123
        - Product Manager: product_manager / pm123
        - Marketing Team: marketing_team / marketing123
        """)
    
    def logout(self):
        """Logout user"""
        if 'user' in st.session_state:
            self.db.log_activity(
                st.session_state['user']['user_id'], 
                'logout', 
                f"User {st.session_state['user']['username']} logged out"
            )
        
        for key in ['authenticated', 'user', 'permissions']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    def require_permission(self, permission):
        """Check if user has required permission"""
        if 'permissions' not in st.session_state:
            return False
        return permission in st.session_state['permissions']
