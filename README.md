# 🎓 O Level Exam System - Complete Setup Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [File Structure](#file-structure)
3. [Installation](#installation)
4. [MongoDB Setup](#mongodb-setup)
5. [Running the Application](#running-the-application)
6. [User Guide](#user-guide)
7. [Deployment](#deployment)

---

## 🎯 Project Overview

A complete examination system for O Level students with:
- **100 Questions** (25 Python, 25 Web Design, 25 IoT, 25 Fundamentals)
- **Admin Portal** - View all results
- **Student Portal** - Take exam once, view results
- **MongoDB Database** - Persistent storage
- **Secure Authentication** - Password hashing
- **Responsive Design** - Works on all devices

---

## 📁 File Structure

```
olevel-exam-system/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── README.md                      # This file
├── templates/
│   ├── index.html                 # Landing page
│   ├── admin_login.html           # Admin login
│   ├── student_login.html         # Student login/register
│   ├── admin_dashboard.html       # Admin dashboard
│   ├── admin_results.html         # All results view
│   ├── student_dashboard.html     # Student dashboard
│   ├── exam.html                  # Exam taking portal
│   └── student_results.html       # Individual results
└── static/                        # (Optional for CSS/JS)
```

---

## 🔧 Installation

### Step 1: Install Python
Download Python 3.8+ from [python.org](https://www.python.org/downloads/)

### Step 2: Create Project Directory
```bash
mkdir olevel-exam-system
cd olevel-exam-system
```

### Step 3: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Create requirements.txt
```txt
Flask==3.0.0
Flask-PyMongo==2.3.0
pymongo==4.6.1
Werkzeug==3.0.1
python-dotenv==1.0.0
gunicorn==21.2.0
dnspython==2.4.2
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🗄️ MongoDB Setup

### Option A: Local MongoDB (Recommended for Development)

#### Windows:
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Install with default settings
3. MongoDB runs automatically on `mongodb://localhost:27017`

#### Mac:
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux (Ubuntu):
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Create list file
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### Verify Installation:
```bash
# Check if MongoDB is running
mongosh
# Or
mongo

# You should see MongoDB shell
```

### Option B: MongoDB Atlas (Cloud - FREE)

1. **Create Account**
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for free

2. **Create Cluster**
   - Click "Build a Database"
   - Choose FREE tier (M0)
   - Select region closest to you
   - Click "Create Cluster"

3. **Setup Database Access**
   - Go to "Database Access"
   - Add new database user
   - Username: `admin`
   - Password: `your_password` (save this!)
   - Select "Read and write to any database"

4. **Setup Network Access**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Choose "Allow Access from Anywhere" (0.0.0.0/0)
   - Or add your specific IP

5. **Get Connection String**
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Copy connection string
   - Format: `mongodb+srv://admin:<password>@cluster0.xxxxx.mongodb.net/olevel_exam?retryWrites=true&w=majority`
   - Replace `<password>` with your actual password

6. **Update app.py**
   ```python
   # Replace this line in app.py:
   app.config["MONGO_URI"] = "mongodb://localhost:27017/olevel_exam"
   
   # With your Atlas connection string:
   app.config["MONGO_URI"] = "mongodb+srv://admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/olevel_exam?retryWrites=true&w=majority"
   ```

---

## 🚀 Running the Application

### Step 1: Copy All Files
Create `templates/` folder and copy all HTML files into it.

### Step 2: Update app.py MongoDB URI
```python
# For local MongoDB:
app.config["MONGO_URI"] = "mongodb://localhost:27017/olevel_exam"

# For MongoDB Atlas:
app.config["MONGO_URI"] = "your_atlas_connection_string"
```

### Step 3: Run the Application
```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Running on http://0.0.0.0:5000
```

### Step 4: Access the System
Open browser and go to: **http://localhost:5000**

---

## 👥 User Guide

### Admin Access
1. Go to: **http://localhost:5000/admin_login**
2. **Username:** `admin`
3. **Password:** `admin123`
4. Features:
   - View all student results
   - Export results to CSV
   - Search and filter results
   - View statistics

### Student Access
1. **Register First:**
   - Go to: **http://localhost:5000/student_login**
   - Click "Register" tab
   - Fill in details:
     - Full Name
     - Email
     - Roll Number
     - Username
     - Password
   - Click "Register"

2. **Login:**
   - Use your username and password
   - Click "Login"

3. **Take Exam:**
   - Click "Start Exam"
   - Answer all 100 questions
   - Questions are divided into 4 categories (25 each)
   - Navigate using Previous/Next buttons
   - Or click question numbers on sidebar
   - Click "Submit Exam" when done
   - **Important:** You can only take exam ONCE

4. **View Results:**
   - Go to "View Results"
   - See your score, grade, and category-wise performance
   - Print results if needed

---

## 📊 Question Categories

### 1. Python Programming (25 Questions)
Topics: Variables, functions, loops, data types, OOP, modules

### 2. Web Design (25 Questions)
Topics: HTML, CSS, JavaScript, Bootstrap, responsive design

### 3. IoT - Internet of Things (25 Questions)
Topics: Arduino, Raspberry Pi, sensors, protocols, smart devices

### 4. Computer Fundamentals (25 Questions)
Topics: Hardware, software, OS, networking, basic concepts

---

## 🎯 Grading System

| Grade | Percentage Range | Status |
|-------|-----------------|--------|
| A+    | 90-100%        | Outstanding |
| A     | 80-89%         | Excellent |
| B     | 70-79%         | Good |
| C     | 60-69%         | Satisfactory |
| D     | 50-59%         | Pass |
| F     | Below 50%      | Fail |

---

## 🌐 Deployment Options

### Option 1: Render (Free & Easy)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/olevel-exam.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Sign up/Login
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Settings:
     - **Name:** olevel-exam-system
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
   - Add Environment Variable:
     - Key: `MONGO_URI`
     - Value: Your MongoDB Atlas connection string
   - Click "Create Web Service"

3. **Access your app:**
   - URL: `https://olevel-exam-system.onrender.com`

### Option 2: Railway

1. **Push to GitHub** (same as above)

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select repository
   - Add environment variable:
     - `MONGO_URI`: Your connection string
   - Railway auto-deploys!

3. **Generate domain:**
   - Go to Settings → Generate Domain

### Option 3: PythonAnywhere

1. **Create account:** [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload files:**
   - Use "Files" tab to upload all files

3. **Setup Web App:**
   - Go to "Web" tab
   - "Add a new web app"
   - Choose Flask
   - Python 3.10

4. **Configure WSGI:**
   ```python
   import sys
   path = '/home/yourusername/olevel-exam-system'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **Install packages:**
   - Open Bash console
   - `pip install -r requirements.txt`

6. **Reload web app**

---

## 🔒 Security Notes

### Change Default Admin Password

After first login, update admin password in MongoDB:

```python
# In Python shell or add route in app.py
from werkzeug.security import generate_password_hash
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.olevel_exam

db.users.update_one(
    {"username": "admin"},
    {"$set": {"password": generate_password_hash("new_password_here")}}
)
```

### Use Environment Variables

Create `.env` file:
```env
MONGO_URI=mongodb://localhost:27017/olevel_exam
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

Update `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")
```

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```
pymongo.errors.ServerSelectionTimeoutError
```
**Solution:**
- Check if MongoDB is running: `mongosh` or `mongo`
- Verify connection string in app.py
- For Atlas: Check IP whitelist and credentials

### Port Already in Use
```
Address already in use
```
**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### Exam Already Taken
If student needs to retake (for testing):
```python
# Delete from MongoDB
db.exams.delete_many({"student_id": ObjectId("student_id_here")})
db.results.delete_many({"student_id": ObjectId("student_id_here")})
```

---

## 📝 Common Tasks

### Add New Questions

Edit `QUESTIONS_DATA` in `app.py`:
```python
QUESTIONS_DATA = {
    "python": [
        {
            "q": "Your question here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": 0  # Index of correct answer (0-3)
        },
        # Add more...
    ]
}
```

### View Database

Using MongoDB Compass (GUI):
1. Download from [mongodb.com/products/compass](https://www.mongodb.com/products/compass)
2. Connect to `mongodb://localhost:27017`
3. Browse `olevel_exam` database

Using Command Line:
```bash
mongosh
use olevel_exam
db.users.find()
db.questions.find()
db.results.find()
```

### Backup Database

```bash
# Backup
mongodump --db olevel_exam --out ./backup

# Restore
mongorestore --db olevel_exam ./backup/olevel_exam
```

---

## 📞 Support

For issues:
- Flask: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- MongoDB: [mongodb.com/docs](https://www.mongodb.com/docs/)
- Python: [python.org/doc](https://www.python.org/doc/)

---

## ✨ Features Summary

✅ 100 Questions (4 categories × 25 each)
✅ Admin dashboard with all results
✅ Student registration and login
✅ One-time exam attempt
✅ Real-time progress tracking
✅ Question navigator sidebar
✅ Category-wise performance analysis
✅ Automatic grading (A+ to F)
✅ Results export to CSV
✅ Search and filter results
✅ Responsive design
✅ MongoDB database
✅ Secure password hashing
✅ Session management
✅ Print-friendly results
✅ Timer tracking

---

## 🎉 You're All Set!

Your O Level Exam System is ready to use!

**Quick Start:**
```bash
# 1. Install MongoDB
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run application
python app.py

# 4. Open browser
http://localhost:5000

# 5. Login
Admin: admin/admin123
Students: Register first
```

---

**Good luck with your exams! 🎓📚**
