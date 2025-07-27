# 🚀 CLIENT SETUP GUIDE - LOCAL DEPLOYMENT

## 📋 **QUICK START FOR CLIENT**

### **⚡ 2-Minute Setup Process**

Your client can run this system locally on their machine by following these simple steps:

---

## 🎯 **STEP 1: PREREQUISITES**

### **System Requirements:**
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: Version 3.9+ (recommended: 3.11)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Required for initial setup only

### **Install Python (if not already installed):**

#### **Windows:**
1. Download Python from [python.org](https://python.org/downloads/)
2. ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify: Open Command Prompt, type `python --version`

#### **macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

## 🎯 **STEP 2: GET THE CODE**

### **Option A: Download ZIP (Easiest)**
1. Go to the GitHub repository
2. Click green "Code" button → "Download ZIP"
3. Extract the ZIP file to desired location (e.g., `C:\Projects\Sentiments`)

### **Option B: Git Clone (if Git installed)**
```bash
git clone https://github.com/YOUR_USERNAME/sentiment-tracking-system.git
cd sentiment-tracking-system
```

---

## 🎯 **STEP 3: SETUP VIRTUAL ENVIRONMENT (Recommended)**

### **Create and activate virtual environment:**

#### **Windows:**
```cmd
cd Sentiments
python -m venv .venv
.venv\Scripts\activate
```

#### **macOS/Linux:**
```bash
cd Sentiments
python3 -m venv .venv
source .venv/bin/activate
```

**You should see `(.venv)` in your command prompt when activated.**

---

## 🎯 **STEP 4: INSTALL DEPENDENCIES**

```bash
# Install all required packages
pip install -r requirements.txt

# This installs:
# - streamlit (web interface)
# - pandas (data processing)
# - scikit-learn (machine learning)
# - matplotlib/plotly (charts)
# - reportlab (PDF generation)
# - And other dependencies
```

**Expected output:** Installation of ~15-20 packages (takes 2-3 minutes)

---

## 🎯 **STEP 5: RUN THE APPLICATION**

### **Start the system:**
```bash
streamlit run app.py
```

### **Expected behavior:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  For better performance, install these optional dependencies:
  pip install watchdog
```

**🎉 The application will automatically open in your default web browser!**

---

## 🎯 **STEP 6: LOGIN AND EXPLORE**

### **Demo Credentials:**

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Administrator** | `admin` | `admin123` | Full system access |
| **Product Manager** | `product_manager` | `pm123` | Product analytics |
| **Marketing Team** | `marketing` | `marketing123` | Campaign analytics |

### **First Login Walkthrough:**
1. **Open**: http://localhost:8501
2. **Login**: Use admin credentials for full access
3. **Explore**: Navigate through different dashboards
4. **Test**: Upload sample data and generate reports

---

## 📁 **PROJECT STRUCTURE FOR CLIENT**

```
Sentiments/
├── 🎯 app.py                    # Main application (START HERE)
├── 🔐 auth_manager.py           # User authentication
├── 🗄️ database_manager.py       # Data management
├── 📄 report_generator.py       # PDF reports
├── 📦 requirements.txt          # Dependencies list
├── 📊 data/                     # Sample datasets
│   ├── database.sqlite          # User database (auto-created)
│   ├── Tweets.csv              # Sample Twitter data
│   └── Amazon_Dataset.csv      # Sample product reviews
├── 🤖 models/                   # ML models (auto-created)
│   ├── sentiment_model.joblib  # Trained model
│   └── tfidf_vectorizer.joblib # Text processor
├── 📋 reports/                  # Generated reports (auto-created)
└── 📚 Documentation/            # Complete documentation
```

---

## 🔧 **TROUBLESHOOTING GUIDE**

### **Common Issues & Solutions:**

#### **Problem 1: Python not found**
```bash
# Error: 'python' is not recognized
# Solution: Use python3 instead
python3 -m venv .venv
python3 -m pip install -r requirements.txt
streamlit run app.py
```

#### **Problem 2: Permission errors (Windows)**
```cmd
# Run Command Prompt as Administrator
# Or use PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **Problem 3: Port already in use**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

#### **Problem 4: Missing dependencies**
```bash
# Upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

#### **Problem 5: Antivirus blocking**
- Add the project folder to antivirus exclusions
- Or temporarily disable real-time protection during setup

---

## 🌐 **NETWORK ACCESS (Optional)**

### **Share with team members on same network:**
```bash
streamlit run app.py --server.address 0.0.0.0
```

**Access from other devices:**
- Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Share URL: `http://YOUR_IP:8501`

---

## 💾 **DATA PERSISTENCE**

### **What gets saved locally:**
- ✅ **User accounts**: Stored in SQLite database
- ✅ **Uploaded datasets**: Saved in `data/` folder
- ✅ **Trained models**: Saved in `models/` folder
- ✅ **Generated reports**: Saved in `reports/` folder
- ✅ **Activity logs**: Complete audit trail

### **Backup important data:**
```bash
# Backup essential files
cp data/database.sqlite backup/
cp -r models/ backup/
cp -r reports/ backup/
```

---

## 🎯 **DEVELOPMENT MODE (Optional)**

### **For developers/customization:**
```bash
# Enable debug mode
streamlit run app.py --server.runOnSave true

# View logs
streamlit run app.py --logger.level debug
```

---

## 📱 **CLIENT SUCCESS CHECKLIST**

### **✅ Pre-Demo Verification:**
- [ ] Python 3.9+ installed and working
- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] Application starts and opens in browser
- [ ] Login with admin credentials successful
- [ ] Sample data visible in dashboards
- [ ] Can upload new datasets
- [ ] PDF reports generate successfully
- [ ] All role-based dashboards accessible

### **✅ Demo Preparation:**
- [ ] Test with client's own data (CSV format)
- [ ] Verify report generation works
- [ ] Check all visualizations display correctly
- [ ] Ensure smooth navigation between dashboards
- [ ] Test model training with new datasets

---

## 🎉 **SUCCESS!**

**Your client now has:**
- ✅ **Fully functional local system**
- ✅ **Complete sentiment analysis platform**
- ✅ **Professional PDF reporting**
- ✅ **Multi-role dashboard access**
- ✅ **Real-time analytics capabilities**

**Next steps for client:**
1. **Explore** the system with sample data
2. **Upload** their own datasets
3. **Generate** reports for their business
4. **Train** models with their specific data
5. **Customize** user accounts for their team

**🚀 The system is production-ready and can scale with their business needs!**
