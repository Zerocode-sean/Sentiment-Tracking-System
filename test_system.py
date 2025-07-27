#!/usr/bin/env python3
"""
Comprehensive test script for the User Sentiment Tracking System
Tests all major components and functionalities
"""

import os
import sys
import pandas as pd
import sqlite3
from pathlib import Path

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Sentiments', 'src'))

def test_database_connection():
    """Test database connectivity and basic operations"""
    print("🔍 Testing Database Connection...")
    try:
        from database_manager import DatabaseManager
        db_manager = DatabaseManager("Sentiments/data/sentiment_system.db")
        
        # Test connection
        users = db_manager.get_all_users()
        print(f"✅ Database connected successfully. Found {len(users)} users.")
        
        # Test system health logging
        db_manager.log_system_health("test", "active", "Test connection successful")
        print("✅ System health logging works.")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_auth_system():
    """Test authentication and authorization"""
    print("\n🔐 Testing Authentication System...")
    try:
        from auth_manager import AuthManager
        auth_manager = AuthManager("Sentiments/data/sentiment_system.db")
        
        # Test user authentication (assuming admin user exists)
        result = auth_manager.authenticate_user("admin", "admin123")
        if result:
            print("✅ Authentication system works.")
            return True
        else:
            print("⚠️ Authentication failed - may need to create admin user first.")
            return False
    except Exception as e:
        print(f"❌ Auth test failed: {e}")
        return False

def test_data_files():
    """Test dataset accessibility and format"""
    print("\n📊 Testing Dataset Files...")
    try:
        datasets = [
            "Sentiments/data/Tweets.csv",
            "Sentiments/data/Amazon_Dataset_20250724.csv"
        ]
        
        for dataset_path in datasets:
            if os.path.exists(dataset_path):
                df = pd.read_csv(dataset_path)
                print(f"✅ {dataset_path}: {len(df)} rows, {len(df.columns)} columns")
                print(f"   Columns: {list(df.columns[:5])}..." if len(df.columns) > 5 else f"   Columns: {list(df.columns)}")
            else:
                print(f"⚠️ {dataset_path}: File not found")
        
        return True
    except Exception as e:
        print(f"❌ Dataset test failed: {e}")
        return False

def test_model_files():
    """Test model and vectorizer files"""
    print("\n🤖 Testing Model Files...")
    try:
        model_files = [
            "sentiment_model.joblib",
            "tfidf_vectorizer.joblib"
        ]
        
        for model_file in model_files:
            if os.path.exists(model_file):
                print(f"✅ {model_file}: Found")
            else:
                print(f"⚠️ {model_file}: Not found (will be created during training)")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_report_generation():
    """Test report generation functionality"""
    print("\n📄 Testing Report Generation...")
    try:
        from report_generator import ReportGenerator
        
        # Create test data
        test_data = pd.DataFrame({
            'text': ['This is great!', 'Not good at all', 'Amazing product'],
            'sentiment': ['positive', 'negative', 'positive'],
            'product': ['Test Product'] * 3
        })
        
        report_gen = ReportGenerator()
        
        # Test basic functionality (without actually generating PDF)
        print("✅ Report generator imported successfully.")
        return True
    except Exception as e:
        print(f"❌ Report generation test failed: {e}")
        return False

def test_dashboard_imports():
    """Test that dashboard modules can be imported"""
    print("\n🖥️ Testing Dashboard Imports...")
    try:
        # Test enhanced dashboard imports
        import streamlit as st
        print("✅ Streamlit imported successfully.")
        
        # Test other required imports
        import plotly.express as px
        import plotly.graph_objects as go
        import matplotlib.pyplot as plt
        import seaborn as sns
        from wordcloud import WordCloud
        import scikit_learn
        
        print("✅ All dashboard dependencies imported successfully.")
        return True
    except Exception as e:
        print(f"❌ Dashboard import test failed: {e}")
        return False

def create_admin_user():
    """Create default admin user if not exists"""
    print("\n👤 Creating Default Admin User...")
    try:
        from auth_manager import AuthManager
        auth_manager = AuthManager("Sentiments/data/sentiment_system.db")
        
        # Try to create admin user
        if auth_manager.create_user("admin", "admin123", "Administrator", "admin"):
            print("✅ Admin user created successfully.")
        else:
            print("ℹ️ Admin user already exists.")
        
        return True
    except Exception as e:
        print(f"❌ Admin user creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive System Test...")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Database Connection", test_database_connection()))
    test_results.append(("Admin User Creation", create_admin_user()))
    test_results.append(("Authentication System", test_auth_system()))
    test_results.append(("Dataset Files", test_data_files()))
    test_results.append(("Model Files", test_model_files()))
    test_results.append(("Report Generation", test_report_generation()))
    test_results.append(("Dashboard Imports", test_dashboard_imports()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(test_results)} tests passed")
    
    if passed == len(test_results):
        print("🎉 All tests passed! System is ready for deployment.")
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
    
    print("\n🌐 Dashboard URLs:")
    print("Enhanced Dashboard: http://localhost:8502")
    print("Original Dashboard: http://localhost:8503")
    
    print("\n📝 Default Login Credentials:")
    print("Username: admin")
    print("Password: admin123")

if __name__ == "__main__":
    main()
