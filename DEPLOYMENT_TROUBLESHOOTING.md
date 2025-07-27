# 🚨 DEPLOYMENT TROUBLESHOOTING GUIDE

## Common Issues & Solutions

### Issue 1: "Module not found" errors
**Cause**: Missing dependencies or incorrect import paths
**Solution**: 
```bash
# Check all imports work locally first
python -c "import streamlit, pandas, numpy, sklearn, matplotlib, plotly"
```

### Issue 2: Database connection fails
**Cause**: SQLite permissions or path issues  
**Solution**: Database auto-creation is handled in code

### Issue 3: File upload doesn't work
**Cause**: File path issues in cloud environment
**Solution**: All file operations use relative paths

### Issue 4: Memory errors during ML training
**Cause**: Large dataset processing
**Solution**: Dataset size limits implemented

### Issue 5: Authentication fails
**Cause**: Session state issues
**Solution**: Robust session management implemented

## Pre-Deployment Checks

```bash
# 1. Test locally first
cd Sentiments
streamlit run src/enhanced_dashboard.py

# 2. Test with fresh environment
python -m venv test_env
test_env\Scripts\activate  # Windows
pip install -r requirements.txt
streamlit run src/enhanced_dashboard.py

# 3. Check all user roles work
# Login as: admin/admin123, product_manager/pm123, marketing_team/marketing123
```

## Streamlit Cloud Specific Fixes

### secrets.toml (if needed)
```toml
[passwords]
admin_password = "admin123"
pm_password = "pm123" 
marketing_password = "marketing123"
```

### config.toml optimizations
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[client]
showErrorDetails = false
toolbarMode = "minimal"
```

## Emergency Fixes

### If deployment fails:
1. Check GitHub Actions logs
2. Verify all files committed
3. Check requirements.txt syntax
4. Test main file path: `src/enhanced_dashboard.py`

### If app crashes:
1. Check Streamlit Cloud logs
2. Verify database creation
3. Check file permissions
4. Test with smaller dataset first
