# 🚀 Client Setup Guide - Quick Model Training

## After Cloning: Setup in 3 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

### Step 3: Train the Sentiment Model
1. **Open your browser** to the local URL (usually http://localhost:8501)
2. **Login as Administrator:**
   - Username: `admin`
   - Password: `admin123`
3. **Navigate to Admin Panel** (top menu)
4. **Click "Dataset Management"**
5. **Upload Sample Dataset:**
   - Click "Browse files"
   - Select `sample_dataset.csv` (included in repository)
   - Click "Process Dataset"
6. **Wait for training** (30-60 seconds)
7. **Success!** Model is now trained and ready

### Step 4: Test Live Sentiment Analysis
1. **Navigate to Admin Panel** → "Live Sentiment Analysis"
2. **Type any text** in the text box
3. **See real-time sentiment prediction** with confidence scores

### Step 5: Explore Other Features
- **Product Manager Panel:** Product-specific analytics
- **Marketing Panel:** Campaign and brand monitoring
- **Generate Reports:** PDF reports with insights

## Why Model Files Are Missing

**Technical Explanation:**
- Pre-trained model files are large (10-50MB)
- They are excluded from git repository (`.gitignore`)
- This keeps the repository lightweight and fast to clone
- Models are generated automatically when you upload data

**Benefits:**
- ✅ Faster repository cloning
- ✅ Models trained on your specific data
- ✅ Customizable for your use case
- ✅ Always up-to-date with your latest data

## Troubleshooting

### If Training Fails:
1. Check dataset format (columns: `text`, `sentiment`)
2. Ensure sufficient data (minimum 10 rows recommended)
3. Check console for error messages

### If Login Fails:
1. Try default credentials: `admin` / `admin123`
2. Clear browser cache
3. Restart the application

### If Charts Don't Show:
1. Ensure all dependencies installed
2. Try refreshing the page
3. Check browser console for errors

## Sample Data Format

Your CSV should have these columns:
```csv
text,sentiment
"Great product!",positive
"Poor quality",negative  
"It's okay",neutral
```

The included `sample_dataset.csv` has 55 examples and is perfect for initial testing.

## Next Steps

Once the model is trained:
1. **Upload your own data** for better accuracy
2. **Explore all dashboard features** 
3. **Generate reports** for stakeholders
4. **Set up user accounts** for your team
5. **Deploy to cloud** for production use

## Production Deployment

For production use:
1. **Streamlit Cloud:** Free, easy setup
2. **Heroku:** Professional hosting
3. **Docker:** Enterprise deployment

See main README.md for detailed deployment instructions.

---

**Need Help?** Check `DEPLOYMENT_TROUBLESHOOTING.md` for additional support.
