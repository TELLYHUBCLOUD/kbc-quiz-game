# app.py - Main Flask Application with MongoDB (Vercel Compatible)
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import os

# Import pymongo directly for Vercel compatibility
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# MongoDB Configuration - MUST USE MONGODB ATLAS FOR VERCEL
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/olevel_exam')

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.olevel_exam
    
    # Test connection
    client.server_info()
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    db = None

# Collections
def get_collections():
    if db is not None:
        return {
            'users': db.users,
            'questions': db.questions,
            'exams': db.exams,
            'results': db.results
        }
    return None

# Initialize Questions Database
QUESTIONS_DATA = {
    "python": [
        {"q": "What is Python?", "options": ["A programming language", "A snake", "A software", "A framework"], "answer": 0},
        {"q": "Which keyword is used to define a function in Python?", "options": ["function", "def", "func", "define"], "answer": 1},
        {"q": "What is the output of print(2 ** 3)?", "options": ["5", "6", "8", "9"], "answer": 2},
        {"q": "Which data type is mutable in Python?", "options": ["tuple", "string", "list", "int"], "answer": 2},
        {"q": "What does PEP stand for?", "options": ["Python Enhancement Proposal", "Python Execution Process", "Python Editor Program", "Python Essential Package"], "answer": 0},
        {"q": "Which method is used to add an element at the end of a list?", "options": ["add()", "append()", "insert()", "extend()"], "answer": 1},
        {"q": "What is the correct file extension for Python files?", "options": [".python", ".py", ".pt", ".pyt"], "answer": 1},
        {"q": "Which operator is used for floor division in Python?", "options": ["/", "//", "%", "**"], "answer": 1},
        {"q": "What is used to create a comment in Python?", "options": ["//", "/* */", "#", "<!--"], "answer": 2},
        {"q": "Which function is used to get the length of a list?", "options": ["length()", "size()", "len()", "count()"], "answer": 2},
        {"q": "What is the output of print(type([]))?", "options": ["<class 'array'>", "<class 'list'>", "<class 'tuple'>", "<class 'dict'>"], "answer": 1},
        {"q": "Which keyword is used to create a class in Python?", "options": ["class", "Class", "def", "object"], "answer": 0},
        {"q": "What does the 'self' keyword represent in Python?", "options": ["Current object", "Parent class", "Global variable", "Local variable"], "answer": 0},
        {"q": "Which module is used for regular expressions in Python?", "options": ["regex", "re", "regexp", "regular"], "answer": 1},
        {"q": "What is the output of print(bool(''))?", "options": ["True", "False", "None", "Error"], "answer": 1},
        {"q": "Which method converts a string to lowercase?", "options": ["lowercase()", "lower()", "toLower()", "casefold()"], "answer": 1},
        {"q": "What is used to handle exceptions in Python?", "options": ["try-catch", "try-except", "try-error", "catch-error"], "answer": 1},
        {"q": "Which function reads input from the user?", "options": ["scan()", "read()", "input()", "get()"], "answer": 2},
        {"q": "What is the output of 3 + 2 * 2?", "options": ["10", "7", "8", "12"], "answer": 1},
        {"q": "Which loop is used to iterate over a sequence?", "options": ["while", "for", "do-while", "repeat"], "answer": 1},
        {"q": "What is None in Python?", "options": ["Empty string", "Zero", "Null value", "False"], "answer": 2},
        {"q": "Which keyword is used to import modules?", "options": ["include", "import", "require", "use"], "answer": 1},
        {"q": "What is a lambda function?", "options": ["Named function", "Anonymous function", "Recursive function", "Built-in function"], "answer": 1},
        {"q": "Which method removes an element from a list?", "options": ["delete()", "remove()", "pop()", "Both B and C"], "answer": 3},
        {"q": "What is the purpose of __init__ method?", "options": ["Destructor", "Constructor", "Iterator", "Generator"], "answer": 1}
    ],
    "web_design": [
        {"q": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language"], "answer": 0},
        {"q": "Which tag is used to create a hyperlink?", "options": ["<link>", "<a>", "<href>", "<url>"], "answer": 1},
        {"q": "What does CSS stand for?", "options": ["Creative Style Sheets", "Cascading Style Sheets", "Computer Style Sheets", "Colorful Style Sheets"], "answer": 1},
        {"q": "Which property is used to change text color in CSS?", "options": ["text-color", "font-color", "color", "text-style"], "answer": 2},
        {"q": "What is the correct HTML tag for the largest heading?", "options": ["<h6>", "<heading>", "<h1>", "<head>"], "answer": 2},
        {"q": "Which HTML attribute specifies an alternate text for an image?", "options": ["title", "alt", "src", "longdesc"], "answer": 1},
        {"q": "How do you create a comment in HTML?", "options": ["// comment", "<!-- comment -->", "/* comment */", "# comment"], "answer": 1},
        {"q": "Which CSS property controls text size?", "options": ["font-style", "text-size", "font-size", "text-style"], "answer": 2},
        {"q": "What is the correct HTML for making a checkbox?", "options": ["<check>", "<checkbox>", "<input type='checkbox'>", "<input type='check'>"], "answer": 2},
        {"q": "Which tag is used to define an internal style sheet?", "options": ["<css>", "<script>", "<style>", "<styles>"], "answer": 2},
        {"q": "What is Bootstrap?", "options": ["JavaScript library", "CSS framework", "Database", "Programming language"], "answer": 1},
        {"q": "Which property is used to change background color?", "options": ["bgcolor", "background-color", "color", "bg-color"], "answer": 1},
        {"q": "What does DOM stand for?", "options": ["Document Object Model", "Data Object Model", "Display Object Management", "Digital Optimization Method"], "answer": 0},
        {"q": "Which tag is used to create an ordered list?", "options": ["<ul>", "<ol>", "<list>", "<dl>"], "answer": 1},
        {"q": "What is the correct HTML for inserting an image?", "options": ["<image src='pic.jpg'>", "<img href='pic.jpg'>", "<img src='pic.jpg'>", "<picture src='pic.jpg'>"], "answer": 2},
        {"q": "Which CSS property is used for text alignment?", "options": ["text-align", "align", "text-style", "align-text"], "answer": 0},
        {"q": "What is JavaScript?", "options": ["Styling language", "Markup language", "Programming language", "Database language"], "answer": 2},
        {"q": "Which HTML tag is used to define a table?", "options": ["<tab>", "<table>", "<tr>", "<td>"], "answer": 1},
        {"q": "What is the purpose of <div> tag?", "options": ["Division/Container", "Data validation", "Document type", "Display variable"], "answer": 0},
        {"q": "Which property adds space inside an element's border?", "options": ["margin", "padding", "spacing", "border-spacing"], "answer": 1},
        {"q": "What is responsive web design?", "options": ["Fast loading", "Adaptive to screen sizes", "Interactive design", "Animated design"], "answer": 1},
        {"q": "Which tag defines a paragraph?", "options": ["<para>", "<p>", "<pg>", "<paragraph>"], "answer": 1},
        {"q": "What is jQuery?", "options": ["CSS framework", "JavaScript library", "Database", "Server"], "answer": 1},
        {"q": "Which CSS property creates rounded corners?", "options": ["corner-radius", "border-radius", "round-corner", "corner-style"], "answer": 1},
        {"q": "What does SEO stand for?", "options": ["Search Engine Optimization", "Site Engine Operation", "Secure Engine Online", "System Engine Output"], "answer": 0}
    ],
    "iot": [
        {"q": "What does IoT stand for?", "options": ["Internet of Things", "Integration of Technology", "Internet of Tools", "Internal Operating Technology"], "answer": 0},
        {"q": "Which protocol is commonly used in IoT?", "options": ["FTP", "MQTT", "SMTP", "POP3"], "answer": 1},
        {"q": "What is a sensor in IoT?", "options": ["Output device", "Input device", "Storage device", "Network device"], "answer": 1},
        {"q": "Which Arduino board is most popular?", "options": ["Arduino Mega", "Arduino Uno", "Arduino Nano", "Arduino Pro"], "answer": 1},
        {"q": "What is Raspberry Pi?", "options": ["Sensor", "Microcontroller", "Single-board computer", "Programming language"], "answer": 2},
        {"q": "Which language is commonly used for Arduino?", "options": ["Python", "Java", "C/C++", "JavaScript"], "answer": 2},
        {"q": "What is the purpose of actuators in IoT?", "options": ["Sense data", "Process data", "Perform actions", "Store data"], "answer": 2},
        {"q": "Which wireless technology has the longest range?", "options": ["Bluetooth", "WiFi", "LoRa", "NFC"], "answer": 2},
        {"q": "What is a smart home?", "options": ["Automated home", "Big home", "Modern home", "Solar home"], "answer": 0},
        {"q": "Which component converts analog to digital?", "options": ["DAC", "ADC", "ALU", "CPU"], "answer": 1},
        {"q": "What is MQTT?", "options": ["Messaging protocol", "Programming language", "Hardware", "Database"], "answer": 0},
        {"q": "Which pin on Arduino provides 5V?", "options": ["GND", "VIN", "5V", "3.3V"], "answer": 2},
        {"q": "What is a DHT11 sensor used for?", "options": ["Light detection", "Temperature & Humidity", "Motion detection", "Sound detection"], "answer": 1},
        {"q": "Which technology enables device-to-device communication?", "options": ["M2M", "P2P", "B2B", "C2C"], "answer": 0},
        {"q": "What is cloud computing in IoT?", "options": ["Local storage", "Remote data storage", "Hardware component", "Programming method"], "answer": 1},
        {"q": "Which is an example of IoT application?", "options": ["MS Word", "Smart thermostat", "Calculator", "Paint"], "answer": 1},
        {"q": "What does GPIO stand for?", "options": ["General Purpose Input Output", "Global Port Interface Object", "General Port Integration Option", "Ground Pin Input Output"], "answer": 0},
        {"q": "Which protocol is used for web communication?", "options": ["HTTP", "MQTT", "CoAP", "AMQP"], "answer": 0},
        {"q": "What is the function of a relay?", "options": ["Sense temperature", "Switch high voltage", "Measure distance", "Display data"], "answer": 1},
        {"q": "Which sensor detects motion?", "options": ["LDR", "DHT11", "PIR", "Ultrasonic"], "answer": 2},
        {"q": "What is NodeMCU?", "options": ["Sensor", "WiFi-enabled microcontroller", "Display", "Power supply"], "answer": 1},
        {"q": "Which component stores IoT data?", "options": ["Sensor", "Database", "Actuator", "Resistor"], "answer": 1},
        {"q": "What is edge computing?", "options": ["Cloud storage", "Processing at device level", "Remote processing", "Network protocol"], "answer": 1},
        {"q": "Which is NOT an IoT platform?", "options": ["AWS IoT", "Google Cloud IoT", "Microsoft Excel", "ThingSpeak"], "answer": 2},
        {"q": "What powers most IoT devices?", "options": ["Nuclear energy", "Solar/Battery", "Wind energy", "Water energy"], "answer": 1}
    ],
    "fundamentals": [
        {"q": "What is a computer?", "options": ["Electronic device", "Mechanical device", "Chemical device", "Biological device"], "answer": 0},
        {"q": "Which is an input device?", "options": ["Monitor", "Printer", "Keyboard", "Speaker"], "answer": 2},
        {"q": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Computer Processing Utility"], "answer": 0},
        {"q": "Which is a primary memory?", "options": ["Hard Disk", "RAM", "CD-ROM", "USB Drive"], "answer": 1},
        {"q": "What does ROM stand for?", "options": ["Read Only Memory", "Random Operating Memory", "Read Operating Memory", "Random Only Memory"], "answer": 0},
        {"q": "Which is an output device?", "options": ["Mouse", "Scanner", "Monitor", "Microphone"], "answer": 2},
        {"q": "What is software?", "options": ["Physical components", "Programs and data", "Hardware parts", "Network cables"], "answer": 1},
        {"q": "Which is a system software?", "options": ["MS Word", "Operating System", "Chrome", "Photoshop"], "answer": 1},
        {"q": "What is binary code?", "options": ["Base 10", "Base 2", "Base 8", "Base 16"], "answer": 1},
        {"q": "Which is NOT an operating system?", "options": ["Windows", "Linux", "Oracle", "macOS"], "answer": 2},
        {"q": "What is 1 KB equal to?", "options": ["1000 bytes", "1024 bytes", "1024 MB", "1000 MB"], "answer": 1},
        {"q": "What does GUI stand for?", "options": ["Graphical User Interface", "General User Interface", "Global User Interaction", "Graphics Utility Interface"], "answer": 0},
        {"q": "Which device stores data permanently?", "options": ["RAM", "Cache", "Hard Disk", "Register"], "answer": 2},
        {"q": "What is malware?", "options": ["Good software", "Malicious software", "System software", "Application software"], "answer": 1},
        {"q": "Which is a programming language?", "options": ["HTTP", "HTML", "Python", "FTP"], "answer": 2},
        {"q": "What is the brain of computer?", "options": ["RAM", "Hard Disk", "CPU", "Monitor"], "answer": 2},
        {"q": "Which is a web browser?", "options": ["Windows", "Chrome", "Word", "Excel"], "answer": 1},
        {"q": "What does LAN stand for?", "options": ["Large Area Network", "Local Area Network", "Long Access Network", "Limited Access Network"], "answer": 1},
        {"q": "What is an algorithm?", "options": ["Programming language", "Step-by-step procedure", "Hardware component", "Software application"], "answer": 1},
        {"q": "Which is a search engine?", "options": ["Facebook", "Google", "Instagram", "WhatsApp"], "answer": 1},
        {"q": "What is a bit?", "options": ["8 bytes", "Smallest unit of data", "1024 bytes", "Storage device"], "answer": 1},
        {"q": "What does WWW stand for?", "options": ["World Wide Web", "World Web Window", "Wide World Web", "Web World Wide"], "answer": 0},
        {"q": "Which key is used to refresh a page?", "options": ["F1", "F5", "F10", "F12"], "answer": 1},
        {"q": "What is spam?", "options": ["Good emails", "Unwanted emails", "System files", "Hardware"], "answer": 1},
        {"q": "What is a firewall?", "options": ["Hardware component", "Security system", "Programming language", "Storage device"], "answer": 1}
    ]
}

def init_db():
    """Initialize database with questions and admin user"""
    collections = get_collections()
    if not collections:
        print("Warning: MongoDB not connected. Database initialization skipped.")
        return
    
    users = collections['users']
    questions = collections['questions']
    
    # Create admin user if not exists
    if users.find_one({"username": "admin"}) is None:
        users.insert_one({
            "username": "admin",
            "password": generate_password_hash("admin123"),
            "role": "admin",
            "created_at": datetime.now()
        })
        print("Admin user created")
    
    # Insert questions if not exists
    if questions.count_documents({}) == 0:
        for category, qs in QUESTIONS_DATA.items():
            for i, q in enumerate(qs):
                questions.insert_one({
                    "category": category,
                    "question": q["q"],
                    "options": q["options"],
                    "answer": q["answer"],
                    "question_number": i + 1
                })
        print("Questions inserted")

# Initialize database
init_db()

# ============= ROUTES =============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    collections = get_collections()
    if not collections:
        return jsonify({"success": False, "message": "Database not connected"}), 500
    
    if request.method == 'POST':
        data = request.json
        user = collections['users'].find_one({"username": data['username']})
        
        if user and check_password_hash(user['password'], data['password']):
            if user['role'] == 'admin':
                session['user_id'] = str(user['_id'])
                session['role'] = 'admin'
                session['username'] = user['username']
                return jsonify({"success": True, "message": "Login successful"})
        
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    return render_template('admin_login.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    collections = get_collections()
    if not collections:
        return jsonify({"success": False, "message": "Database not connected"}), 500
    
    if request.method == 'POST':
        data = request.json
        user = collections['users'].find_one({"username": data['username']})
        
        if user and check_password_hash(user['password'], data['password']):
            if user['role'] == 'student':
                session['user_id'] = str(user['_id'])
                session['role'] = 'student'
                session['username'] = user['username']
                return jsonify({"success": True, "message": "Login successful"})
        
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    return render_template('student_login.html')

@app.route('/register', methods=['POST'])
def register():
    collections = get_collections()
    if not collections:
        return jsonify({"success": False, "message": "Database not connected"}), 500
    
    data = request.json
    
    # Check if username exists
    if collections['users'].find_one({"username": data['username']}):
        return jsonify({"success": False, "message": "Username already exists"}), 400
    
    # Create new student
    collections['users'].insert_one({
        "username": data['username'],
        "password": generate_password_hash(data['password']),
        "name": data['name'],
        "email": data['email'],
        "roll_number": data['roll_number'],
        "role": "student",
        "created_at": datetime.now()
    })
    
    return jsonify({"success": True, "message": "Registration successful"})

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html')

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('student_login'))
    
    return render_template('student_dashboard.html')

@app.route('/exam')
def exam():
    collections = get_collections()
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('student_login'))
    
    if not collections:
        return "Database not connected", 500
    
    # Check if student already took exam
    user_id = ObjectId(session['user_id'])
    existing_exam = collections['exams'].find_one({"student_id": user_id, "status": "completed"})
    
    if existing_exam:
        return redirect(url_for('student_results'))
    
    return render_template('exam.html')

@app.route('/api/start_exam', methods=['POST'])
def start_exam():
    collections = get_collections()
    if 'user_id' not in session or not collections:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Get all questions from each category
    exam_questions = []
    for category in ['python', 'web_design', 'iot', 'fundamentals']:
        cat_questions = list(collections['questions'].find({"category": category}))
        exam_questions.extend(cat_questions[:25])
    
    # Create exam session
    exam_id = collections['exams'].insert_one({
        "student_id": ObjectId(session['user_id']),
        "status": "in_progress",
        "started_at": datetime.now(),
        "questions": [str(q['_id']) for q in exam_questions]
    }).inserted_id
    
    session['exam_id'] = str(exam_id)
    
    # Return questions without answers
    questions_data = []
    for i, q in enumerate(exam_questions):
        questions_data.append({
            "id": str(q['_id']),
            "number": i + 1,
            "category": q['category'],
            "question": q['question'],
            "options": q['options']
        })
    
    return jsonify({"questions": questions_data})

@app.route('/api/submit_exam', methods=['POST'])
def submit_exam():
    collections = get_collections()
    if 'user_id' not in session or 'exam_id' not in session or not collections:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    answers = data.get('answers', {})
    
    # Get exam
    exam = collections['exams'].find_one({"_id": ObjectId(session['exam_id'])})
    
    # Calculate score
    correct_count = 0
    total_questions = len(exam['questions'])
    results_detail = []
    
    for q_id in exam['questions']:
        question = collections['questions'].find_one({"_id": ObjectId(q_id)})
        student_answer = answers.get(q_id, -1)
        
        is_correct = int(student_answer) == question['answer']
        if is_correct:
            correct_count += 1
        
        results_detail.append({
            "question_id": q_id,
            "category": question['category'],
            "correct": is_correct
        })
    
    percentage = (correct_count / total_questions) * 100
    
    # Determine grade
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"
    
    # Update exam status
    collections['exams'].update_one(
        {"_id": ObjectId(session['exam_id'])},
        {"$set": {
            "status": "completed",
            "completed_at": datetime.now(),
            "answers": answers
        }}
    )
    
    # Save results
    collections['results'].insert_one({
        "student_id": ObjectId(session['user_id']),
        "exam_id": ObjectId(session['exam_id']),
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "incorrect_answers": total_questions - correct_count,
        "percentage": percentage,
        "grade": grade,
        "results_detail": results_detail,
        "submitted_at": datetime.now()
    })
    
    return jsonify({
        "success": True,
        "score": correct_count,
        "total": total_questions,
        "percentage": percentage,
        "grade": grade
    })

@app.route('/student/results')
def student_results():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('student_login'))
    
    return render_template('student_results.html')

@app.route('/api/my_results')
def get_my_results():
    collections = get_collections()
    if 'user_id' not in session or not collections:
        return jsonify({"error": "Unauthorized"}), 401
    
    result = collections['results'].find_one({"student_id": ObjectId(session['user_id'])})
    
    if not result:
        return jsonify({"error": "No results found"}), 404
    
    # Get student info
    user = collections['users'].find_one({"_id": ObjectId(session['user_id'])})
    
    # Calculate category-wise performance
    category_stats = {
        "python": {"correct": 0, "total": 0},
        "web_design": {"correct": 0, "total": 0},
        "iot": {"correct": 0, "total": 0},
        "fundamentals": {"correct": 0, "total": 0}
    }
    
    for detail in result['results_detail']:
        cat = detail['category']
        category_stats[cat]['total'] += 1
        if detail['correct']:
            category_stats[cat]['correct'] += 1
    
    return jsonify({
        "student_name": user.get('name', user['username']),
        "roll_number": user.get('roll_number', 'N/A'),
        "total_questions": result['total_questions'],
        "correct_answers": result['correct_answers'],
        "incorrect_answers": result['incorrect_answers'],
        "percentage": result['percentage'],
        "grade": result['grade'],
        "submitted_at": result['submitted_at'].strftime('%Y-%m-%d %H:%M:%S'),
        "category_stats": category_stats
    })

@app.route('/admin/all_results')
def admin_all_results():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    
    return render_template('admin_results.html')

@app.route('/api/all_results')
def get_all_results():
    collections = get_collections()
    if 'user_id' not in session or session.get('role') != 'admin' or not collections:
        return jsonify({"error": "Unauthorized"}), 401
    
    all_results = []
    
    for result in collections['results'].find():
        student = collections['users'].find_one({"_id": result['student_id']})
        all_results.append({
            "student_name": student.get('name', student['username']),
            "roll_number": student.get('roll_number', 'N/A'),
            "total_questions": result['total_questions'],
            "correct_answers": result['correct_answers'],
            "percentage": result['percentage'],
            "grade": result['grade'],
            "submitted_at": result['submitted_at'].strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({"results": all_results})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Health check for Vercel
@app.route('/api/health')
def health():
    if db is not None:
        return jsonify({"status": "healthy", "database": "connected"})
    return jsonify({"status": "unhealthy", "database": "disconnected"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
