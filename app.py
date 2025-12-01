from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import os
import random
import tempfile
import hashlib

from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Configuration - Connect FIRST
# MongoDB Configuration - Connect FIRST
MONGO_URI = os.environ.get('MONGO_URI')

client = None
db = None

try:
    if MONGO_URI:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ MongoDB connected successfully!")
    else:
        raise Exception("No MONGO_URI provided")
except Exception as e:
    print(f"⚠️ MongoDB connection error or not configured: {e}")
    print("⚠️ Switching to mongomock for local development...")
    import mongomock
    client = mongomock.MongoClient()
    print("✅ Mock MongoDB connected successfully!")

db = client.olevel_exam

# Session Configuration - Use filesystem if MongoDB session fails
# Session Configuration - Use filesystem if MongoDB session fails
# FIXED: Use static secret key for dev to prevent session invalidation on restart
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_fixed_12345')
app.config['SESSION_COOKIE_SECURE'] = False  # Set True for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# NOTE: Removed Flask-Session (filesystem) to support serverless/Vercel environments.
# Default Flask sessions use signed cookies which persist on the client side.

def get_collections():
    """Get database collections with connection check"""
    if db is not None:
        try:
            # Test connection
            client.admin.command('ping')
            return {
                'users': db.users,
                'questions': db.questions,
                'exams': db.exams,
                'results': db.results
            }
        except Exception as e:
            print(f"❌ Database connection lost: {e}")
            return None
    return None

# =================== COMPLETE QUESTIONS DATABASE - 200 QUESTIONS ===================
QUESTIONS_DATA = {
    "python": [
        # Basic Level (1-15)
        {"q": "What is Python?", "options": ["A programming language", "A snake", "A software", "A framework"], "answer": 0, "difficulty": "basic"},
        {"q": "Which keyword is used to define a function in Python?", "options": ["function", "def", "func", "define"], "answer": 1, "difficulty": "basic"},
        {"q": "What is the output of print(2 ** 3)?", "options": ["5", "6", "8", "9"], "answer": 2, "difficulty": "basic"},
        {"q": "Which data type is mutable in Python?", "options": ["tuple", "string", "list", "int"], "answer": 2, "difficulty": "basic"},
        {"q": "What does PEP stand for?", "options": ["Python Enhancement Proposal", "Python Execution Process", "Python Editor Program", "Python Essential Package"], "answer": 0, "difficulty": "basic"},
        {"q": "Which method is used to add an element at the end of a list?", "options": ["add()", "append()", "insert()", "extend()"], "answer": 1, "difficulty": "basic"},
        {"q": "What is the correct file extension for Python files?", "options": [".python", ".py", ".pt", ".pyt"], "answer": 1, "difficulty": "basic"},
        {"q": "Which operator is used for floor division in Python?", "options": ["/", "//", "%", "**"], "answer": 1, "difficulty": "basic"},
        {"q": "What is used to create a comment in Python?", "options": ["//", "/* */", "#", "<!--"], "answer": 2, "difficulty": "basic"},
        {"q": "Which function is used to get the length of a list?", "options": ["length()", "size()", "len()", "count()"], "answer": 2, "difficulty": "basic"},
        {"q": "What is the output of print(type([]))?", "options": ["<class 'array'>", "<class 'list'>", "<class 'tuple'>", "<class 'dict'>"], "answer": 1, "difficulty": "basic"},
        {"q": "Which keyword is used to create a class in Python?", "options": ["class", "Class", "def", "object"], "answer": 0, "difficulty": "basic"},
        {"q": "What does the 'self' keyword represent in Python?", "options": ["Current object", "Parent class", "Global variable", "Local variable"], "answer": 0, "difficulty": "basic"},
        {"q": "Which module is used for regular expressions in Python?", "options": ["regex", "re", "regexp", "regular"], "answer": 1, "difficulty": "basic"},
        {"q": "What is the output of print(bool(''))?", "options": ["True", "False", "None", "Error"], "answer": 1, "difficulty": "basic"},
        
        # Intermediate Level (16-35)
        {"q": "Which method converts a string to lowercase?", "options": ["lowercase()", "lower()", "toLower()", "casefold()"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is used to handle exceptions in Python?", "options": ["try-catch", "try-except", "try-error", "catch-error"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which function reads input from the user?", "options": ["scan()", "read()", "input()", "get()"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is the output of 3 + 2 * 2?", "options": ["10", "7", "8", "12"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which loop is used to iterate over a sequence?", "options": ["while", "for", "do-while", "repeat"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is None in Python?", "options": ["Empty string", "Zero", "Null value", "False"], "answer": 2, "difficulty": "intermediate"},
        {"q": "Which keyword is used to import modules?", "options": ["include", "import", "require", "use"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is a lambda function?", "options": ["Named function", "Anonymous function", "Recursive function", "Built-in function"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which method removes an element from a list?", "options": ["delete()", "remove()", "pop()", "Both B and C"], "answer": 3, "difficulty": "intermediate"},
        {"q": "What is the purpose of __init__ method?", "options": ["Destructor", "Constructor", "Iterator", "Generator"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is list comprehension in Python?", "options": ["A loop structure", "A concise way to create lists", "A data type", "An import statement"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which keyword is used for inheritance?", "options": ["extends", "inherits", "class ChildClass(ParentClass)", "super"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What does the 'with' statement do?", "options": ["Import modules", "Handle exceptions", "Context management", "Define functions"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is the difference between '==' and 'is'?", "options": ["No difference", "== compares values, is compares identity", "is is faster", "== is for numbers only"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which decorator is used for static methods?", "options": ["@static", "@staticmethod", "@classmethod", "@method"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is a tuple in Python?", "options": ["Mutable sequence", "Immutable sequence", "Dictionary", "Set"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which function converts string to integer?", "options": ["integer()", "int()", "toInt()", "parse()"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is slicing in Python?", "options": ["Deleting elements", "Extracting parts of sequence", "Sorting", "Reversing"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which method joins list elements into a string?", "options": ["join()", "concat()", "merge()", "combine()"], "answer": 0, "difficulty": "intermediate"},
        {"q": "What is *args in Python?", "options": ["Multiplication", "Variable arguments", "Pointer", "Import statement"], "answer": 1, "difficulty": "intermediate"},
        
        # Advanced Level (36-50)
        {"q": "What is a generator in Python?", "options": ["Function that returns iterator", "Data type", "Loop structure", "Module"], "answer": 0, "difficulty": "advanced"},
        {"q": "Which method is used for deep copy?", "options": ["copy()", "deepcopy()", "clone()", "duplicate()"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is the GIL in Python?", "options": ["Global Interpreter Lock", "General Integer Limit", "Graphical Interface Library", "Global Import Lock"], "answer": 0, "difficulty": "advanced"},
        {"q": "What is monkey patching?", "options": ["Debugging", "Dynamic modification of code at runtime", "Error handling", "Testing method"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which library is used for parallel processing?", "options": ["threading", "multiprocessing", "asyncio", "All of these"], "answer": 3, "difficulty": "advanced"},
        {"q": "What is metaclass in Python?", "options": ["Class of a class", "Parent class", "Abstract class", "Interface"], "answer": 0, "difficulty": "advanced"},
        {"q": "What does __name__ == '__main__' check?", "options": ["Module name", "If script is run directly", "Function name", "Class name"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which decorator preserves function metadata?", "options": ["@wraps", "@preserve", "@metadata", "@functools"], "answer": 0, "difficulty": "advanced"},
        {"q": "What is the difference between __str__ and __repr__?", "options": ["No difference", "__str__ for users, __repr__ for developers", "Same output", "__repr__ is faster"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is context manager protocol?", "options": ["__enter__ and __exit__", "__init__ and __del__", "__get__ and __set__", "__call__ and __return__"], "answer": 0, "difficulty": "advanced"},
        {"q": "What is the purpose of __slots__?", "options": ["Memory optimization", "Speed optimization", "Type checking", "Documentation"], "answer": 0, "difficulty": "advanced"},
        {"q": "Which method makes an object callable?", "options": ["__call__", "__invoke__", "__execute__", "__run__"], "answer": 0, "difficulty": "advanced"},
        {"q": "What is the walrus operator (:=)?", "options": ["Comparison", "Assignment expression", "Loop", "Function"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is asyncio used for?", "options": ["Synchronous programming", "Asynchronous programming", "Database operations", "File handling"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is the difference between @property and @classmethod?", "options": ["No difference", "@property for attributes, @classmethod for class methods", "Same functionality", "@property is deprecated"], "answer": 1, "difficulty": "advanced"}
    ],
    
    "web_design": [
        # Basic Level (1-15)
        {"q": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language"], "answer": 0, "difficulty": "basic"},
        {"q": "Which tag is used to create a hyperlink?", "options": ["<link>", "<a>", "<href>", "<url>"], "answer": 1, "difficulty": "basic"},
        {"q": "What does CSS stand for?", "options": ["Creative Style Sheets", "Cascading Style Sheets", "Computer Style Sheets", "Colorful Style Sheets"], "answer": 1, "difficulty": "basic"},
        {"q": "Which property is used to change text color in CSS?", "options": ["text-color", "font-color", "color", "text-style"], "answer": 2, "difficulty": "basic"},
        {"q": "What is the correct HTML tag for the largest heading?", "options": ["<h6>", "<heading>", "<h1>", "<head>"], "answer": 2, "difficulty": "basic"},
        {"q": "Which HTML attribute specifies an alternate text for an image?", "options": ["title", "alt", "src", "longdesc"], "answer": 1, "difficulty": "basic"},
        {"q": "How do you create a comment in HTML?", "options": ["// comment", "<!-- comment -->", "/* comment */", "# comment"], "answer": 1, "difficulty": "basic"},
        {"q": "Which CSS property controls text size?", "options": ["font-style", "text-size", "font-size", "text-style"], "answer": 2, "difficulty": "basic"},
        {"q": "What is the correct HTML for making a checkbox?", "options": ["<check>", "<checkbox>", "<input type='checkbox'>", "<input type='check'>"], "answer": 2, "difficulty": "basic"},
        {"q": "Which tag is used to define an internal style sheet?", "options": ["<css>", "<script>", "<style>", "<styles>"], "answer": 2, "difficulty": "basic"},
        {"q": "What is Bootstrap?", "options": ["JavaScript library", "CSS framework", "Database", "Programming language"], "answer": 1, "difficulty": "basic"},
        {"q": "Which property is used to change background color?", "options": ["bgcolor", "background-color", "color", "bg-color"], "answer": 1, "difficulty": "basic"},
        {"q": "What does DOM stand for?", "options": ["Document Object Model", "Data Object Model", "Display Object Management", "Digital Optimization Method"], "answer": 0, "difficulty": "basic"},
        {"q": "Which tag is used to create an ordered list?", "options": ["<ul>", "<ol>", "<list>", "<dl>"], "answer": 1, "difficulty": "basic"},
        {"q": "What is the correct HTML for inserting an image?", "options": ["<image src='pic.jpg'>", "<img href='pic.jpg'>", "<img src='pic.jpg'>", "<picture src='pic.jpg'>"], "answer": 2, "difficulty": "basic"},
        
        # Intermediate Level (16-35)
        {"q": "Which CSS property is used for text alignment?", "options": ["text-align", "align", "text-style", "align-text"], "answer": 0, "difficulty": "intermediate"},
        {"q": "What is JavaScript?", "options": ["Styling language", "Markup language", "Programming language", "Database language"], "answer": 2, "difficulty": "intermediate"},
        {"q": "Which HTML tag is used to define a table?", "options": ["<tab>", "<table>", "<tr>", "<td>"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is the purpose of <div> tag?", "options": ["Division/Container", "Data validation", "Document type", "Display variable"], "answer": 0, "difficulty": "intermediate"},
        {"q": "Which property adds space inside an element's border?", "options": ["margin", "padding", "spacing", "border-spacing"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is responsive web design?", "options": ["Fast loading", "Adaptive to screen sizes", "Interactive design", "Animated design"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which tag defines a paragraph?", "options": ["<para>", "<p>", "<pg>", "<paragraph>"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is jQuery?", "options": ["CSS framework", "JavaScript library", "Database", "Server"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which CSS property creates rounded corners?", "options": ["corner-radius", "border-radius", "round-corner", "corner-style"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What does SEO stand for?", "options": ["Search Engine Optimization", "Site Engine Operation", "Secure Engine Online", "System Engine Output"], "answer": 0, "difficulty": "intermediate"},
        {"q": "Which CSS unit is relative to viewport width?", "options": ["px", "em", "vw", "pt"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is Flexbox used for?", "options": ["Layout design", "Animation", "Database", "Validation"], "answer": 0, "difficulty": "intermediate"},
        {"q": "Which HTML5 tag is used for navigation?", "options": ["<navigation>", "<nav>", "<menu>", "<navbar>"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is the box model in CSS?", "options": ["3D modeling", "Content, padding, border, margin", "Layout template", "Animation framework"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which method selects element by ID in JavaScript?", "options": ["getElementByID()", "getElementById()", "selectID()", "findID()"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is AJAX?", "options": ["Programming language", "Asynchronous JavaScript and XML", "CSS framework", "Database"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which CSS property controls element visibility?", "options": ["visible", "visibility", "display", "Both B and C"], "answer": 3, "difficulty": "intermediate"},
        {"q": "What is semantic HTML?", "options": ["Styling HTML", "Meaningful HTML tags", "JavaScript in HTML", "Database queries"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which attribute makes input field required?", "options": ["mandatory", "required", "compulsory", "needed"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is CSS Grid?", "options": ["Table layout", "2D layout system", "Animation", "Framework"], "answer": 1, "difficulty": "intermediate"},
        
        # Advanced Level (36-50)
        {"q": "What is Progressive Web App (PWA)?", "options": ["Mobile app", "Web app with native features", "Desktop app", "Database"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which CSS preprocessor is most popular?", "options": ["LESS", "SASS", "Stylus", "PostCSS"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is Virtual DOM?", "options": ["Real DOM copy", "Lightweight DOM copy in memory", "Database", "Server"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is webpack used for?", "options": ["Bundling modules", "Database", "Testing", "Hosting"], "answer": 0, "difficulty": "advanced"},
        {"q": "Which method prevents default event behavior?", "options": ["stopDefault()", "preventDefault()", "cancelEvent()", "stopEvent()"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is CORS?", "options": ["CSS framework", "Cross-Origin Resource Sharing", "Database", "API"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is Service Worker?", "options": ["Background script for PWA", "CSS preprocessor", "Database", "Framework"], "answer": 0, "difficulty": "advanced"},
        {"q": "Which HTTP method is idempotent?", "options": ["POST", "PUT", "GET", "Both B and C"], "answer": 3, "difficulty": "advanced"},
        {"q": "What is GraphQL?", "options": ["Database", "Query language for APIs", "CSS framework", "JavaScript library"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is Critical CSS?", "options": ["Important styles", "Above-fold CSS", "Inline CSS", "External CSS"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is tree shaking?", "options": ["Removing unused code", "Animation technique", "Layout method", "Testing approach"], "answer": 0, "difficulty": "advanced"},
        {"q": "Which storage has largest capacity?", "options": ["localStorage", "sessionStorage", "IndexedDB", "Cookies"], "answer": 2, "difficulty": "advanced"},
        {"q": "What is Content Security Policy (CSP)?", "options": ["SEO technique", "Security standard", "CSS framework", "API"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is Shadow DOM?", "options": ["Dark theme", "Encapsulated DOM tree", "Animation", "Layout"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which framework uses Virtual DOM?", "options": ["Angular", "React", "Vue", "Both B and C"], "answer": 3, "difficulty": "advanced"}
    ],
    
    "iot": [
        # Basic Level (1-15)
        {"q": "What does IoT stand for?", "options": ["Internet of Things", "Integration of Technology", "Internet of Tools", "Internal Operating Technology"], "answer": 0, "difficulty": "basic"},
        {"q": "Which protocol is commonly used in IoT?", "options": ["FTP", "MQTT", "SMTP", "POP3"], "answer": 1, "difficulty": "basic"},
        {"q": "What is a sensor in IoT?", "options": ["Output device", "Input device", "Storage device", "Network device"], "answer": 1, "difficulty": "basic"},
        {"q": "Which Arduino board is most popular?", "options": ["Arduino Mega", "Arduino Uno", "Arduino Nano", "Arduino Pro"], "answer": 1, "difficulty": "basic"},
        {"q": "What is Raspberry Pi?", "options": ["Sensor", "Microcontroller", "Single-board computer", "Programming language"], "answer": 2, "difficulty": "basic"},
        {"q": "Which language is commonly used for Arduino?", "options": ["Python", "Java", "C/C++", "JavaScript"], "answer": 2, "difficulty": "basic"},
        {"q": "What is the purpose of actuators in IoT?", "options": ["Sense data", "Process data", "Perform actions", "Store data"], "answer": 2, "difficulty": "basic"},
        {"q": "Which wireless technology has the longest range?", "options": ["Bluetooth", "WiFi", "LoRa", "NFC"], "answer": 2, "difficulty": "basic"},
        {"q": "What is a smart home?", "options": ["Automated home", "Big home", "Modern home", "Solar home"], "answer": 0, "difficulty": "basic"},
        {"q": "Which component converts analog to digital?", "options": ["DAC", "ADC", "ALU", "CPU"], "answer": 1, "difficulty": "basic"},
        {"q": "What is MQTT?", "options": ["Messaging protocol", "Programming language", "Hardware", "Database"], "answer": 0, "difficulty": "basic"},
        {"q": "Which pin on Arduino provides 5V?", "options": ["GND", "VIN", "5V", "3.3V"], "answer": 2, "difficulty": "basic"},
        {"q": "What is a DHT11 sensor used for?", "options": ["Light detection", "Temperature & Humidity", "Motion detection", "Sound detection"], "answer": 1, "difficulty": "basic"},
        {"q": "Which technology enables device-to-device communication?", "options": ["M2M", "P2P", "B2B", "C2C"], "answer": 0, "difficulty": "basic"},
        {"q": "What is cloud computing in IoT?", "options": ["Local storage", "Remote data storage", "Hardware component", "Programming method"], "answer": 1, "difficulty": "basic"},
        
        # Intermediate Level (16-35)
        {"q": "Which is an example of IoT application?", "options": ["MS Word", "Smart thermostat", "Calculator", "Paint"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What does GPIO stand for?", "options": ["General Purpose Input Output", "Global Port Interface Object", "General Port Integration Option", "Ground Pin Input Output"], "answer": 0, "difficulty": "intermediate"},
        {"q": "Which protocol is used for web communication?", "options": ["HTTP", "MQTT", "CoAP", "AMQP"], "answer": 0, "difficulty": "intermediate"},
        {"q": "What is the function of a relay?", "options": ["Sense temperature", "Switch high voltage", "Measure distance", "Display data"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which sensor detects motion?", "options": ["LDR", "DHT11", "PIR", "Ultrasonic"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is NodeMCU?", "options": ["Sensor", "WiFi-enabled microcontroller", "Display", "Power supply"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which component stores IoT data?", "options": ["Sensor", "Database", "Actuator", "Resistor"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is edge computing?", "options": ["Cloud storage", "Processing at device level", "Remote processing", "Network protocol"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which is NOT an IoT platform?", "options": ["AWS IoT", "Google Cloud IoT", "Microsoft Excel", "ThingSpeak"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What powers most IoT devices?", "options": ["Nuclear energy", "Solar/Battery", "Wind energy", "Water energy"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is I2C protocol?", "options": ["Serial communication", "Parallel communication", "Wireless protocol", "Storage method"], "answer": 0, "difficulty": "intermediate"},
        {"q": "Which sensor measures distance?", "options": ["DHT11", "LDR", "Ultrasonic", "PIR"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is PWM in Arduino?", "options": ["Power Management", "Pulse Width Modulation", "Program Write Mode", "Parallel Wire Method"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which communication protocol uses start and stop bits?", "options": ["I2C", "SPI", "UART", "CAN"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is the purpose of analog pins in Arduino?", "options": ["Digital input", "Analog to digital conversion", "Power supply", "Ground"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which IoT layer handles data processing?", "options": ["Perception", "Network", "Application", "Processing"], "answer": 3, "difficulty": "intermediate"},
        {"q": "What is LoRaWAN?", "options": ["WiFi protocol", "Long range network protocol", "Bluetooth variant", "Wired protocol"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which microcontroller has built-in WiFi?", "options": ["Arduino Uno", "ESP8266", "ATmega328", "PIC16F"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is fog computing?", "options": ["Cloud computing", "Decentralized computing", "Wireless technology", "Database"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which sensor is used for gas detection?", "options": ["MQ series", "DHT11", "PIR", "LDR"], "answer": 0, "difficulty": "intermediate"},
        
        # Advanced Level (36-50)
        {"q": "What is MQTT QoS level 2?", "options": ["At most once", "At least once", "Exactly once", "Never"], "answer": 2, "difficulty": "advanced"},
        {"q": "Which protocol is best for constrained devices?", "options": ["HTTP", "MQTT", "CoAP", "WebSocket"], "answer": 2, "difficulty": "advanced"},
        {"q": "What is Digital Twin in IoT?", "options": ["Backup system", "Virtual replica of physical device", "Clone device", "Mirror network"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which security protocol is used in IoT?", "options": ["SSL/TLS", "DTLS", "IPSec", "All of these"], "answer": 3, "difficulty": "advanced"},
        {"q": "What is Time Series Database used for in IoT?", "options": ["User data", "Time-stamped sensor data", "Configuration", "Logs"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which is a real-time operating system for IoT?", "options": ["Windows", "FreeRTOS", "Linux", "macOS"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is OTA update?", "options": ["Over The Air update", "Online Transfer Application", "Optimal Time Access", "Offline Testing App"], "answer": 0, "difficulty": "advanced"},
        {"q": "Which technology enables indoor positioning?", "options": ["GPS", "Bluetooth Beacons", "WiFi", "Both B and C"], "answer": 3, "difficulty": "advanced"},
        {"q": "What is the role of gateway in IoT?", "options": ["Storage", "Protocol translation", "Power supply", "Display"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which consensus algorithm is used in IoT blockchain?", "options": ["Proof of Work", "Proof of Stake", "PBFT", "All of these"], "answer": 3, "difficulty": "advanced"},
        {"q": "What is NB-IoT?", "options": ["WiFi variant", "Narrowband IoT", "Network Bridge", "Node Based IoT"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which attack is common in IoT?", "options": ["DDoS", "Man-in-the-middle", "Replay attack", "All of these"], "answer": 3, "difficulty": "advanced"},
        {"q": "What is the purpose of watchdog timer?", "options": ["Time keeping", "System reset on hang", "Schedule tasks", "Measure duration"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which protocol supports both request-response and publish-subscribe?", "options": ["MQTT", "CoAP", "AMQP", "Both B and C"], "answer": 3, "difficulty": "advanced"},
        {"q": "What is the maximum devices in Zigbee network?", "options": ["256", "65000+", "1024", "Unlimited"], "answer": 1, "difficulty": "advanced"}
    ],
    
    "fundamentals": [
        # Basic Level (1-15)
        {"q": "What is a computer?", "options": ["Electronic device", "Mechanical device", "Chemical device", "Biological device"], "answer": 0, "difficulty": "basic"},
        {"q": "Which is an input device?", "options": ["Monitor", "Printer", "Keyboard", "Speaker"], "answer": 2, "difficulty": "basic"},
        {"q": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Computer Processing Utility"], "answer": 0, "difficulty": "basic"},
        {"q": "Which is a primary memory?", "options": ["Hard Disk", "RAM", "CD-ROM", "USB Drive"], "answer": 1, "difficulty": "basic"},
        {"q": "What does ROM stand for?", "options": ["Read Only Memory", "Random Operating Memory", "Read Operating Memory", "Random Only Memory"], "answer": 0, "difficulty": "basic"},
        {"q": "Which is an output device?", "options": ["Mouse", "Scanner", "Monitor", "Microphone"], "answer": 2, "difficulty": "basic"},
        {"q": "What is the brain of computer?", "options": ["Monitor", "CPU", "Keyboard", "Mouse"], "answer": 1, "difficulty": "basic"},
        {"q": "Which memory is volatile?", "options": ["ROM", "Hard Disk", "RAM", "Flash Drive"], "answer": 2, "difficulty": "basic"},
        {"q": "What does ALU stand for?", "options": ["Arithmetic Logic Unit", "Advanced Logic Unit", "Automated Logic Unit", "Analog Logic Unit"], "answer": 0, "difficulty": "basic"},
        {"q": "Which is secondary storage?", "options": ["RAM", "Cache", "Hard Disk", "Registers"], "answer": 2, "difficulty": "basic"},
        {"q": "What is the smallest unit of data?", "options": ["Byte", "Bit", "Nibble", "Word"], "answer": 1, "difficulty": "basic"},
        {"q": "Which converts source code to machine code?", "options": ["Interpreter", "Compiler", "Assembler", "All of these"], "answer": 3, "difficulty": "basic"},
        {"q": "What is an operating system?", "options": ["Hardware", "System software", "Application software", "Utility software"], "answer": 1, "difficulty": "basic"},
        {"q": "Which is an example of system software?", "options": ["MS Word", "Windows", "Chrome", "Photoshop"], "answer": 1, "difficulty": "basic"},
        {"q": "What does GUI stand for?", "options": ["Graphical User Interface", "General User Interface", "Graphics Utility Interface", "Global User Integration"], "answer": 0, "difficulty": "basic"},
        
        # Intermediate Level (16-35)
        {"q": "What is cache memory?", "options": ["Permanent storage", "High-speed temporary storage", "Input device", "Output device"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which number system does computer use?", "options": ["Decimal", "Binary", "Octal", "Hexadecimal"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is 1 MB equal to?", "options": ["1000 KB", "1024 KB", "1000 GB", "1024 GB"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which port is fastest?", "options": ["USB 2.0", "USB 3.0", "Serial Port", "Parallel Port"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is firmware?", "options": ["Application software", "Software in ROM", "Operating system", "Utility program"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which topology connects all devices to central hub?", "options": ["Star", "Ring", "Bus", "Mesh"], "answer": 0, "difficulty": "intermediate"},
        {"q": "What is the purpose of BIOS?", "options": ["Run applications", "Boot system", "Store data", "Network connection"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which is NOT a programming paradigm?", "options": ["Object-oriented", "Procedural", "Functional", "Sequential"], "answer": 3, "difficulty": "intermediate"},
        {"q": "What is virtual memory?", "options": ["RAM extension using disk", "Cache memory", "ROM", "Cloud storage"], "answer": 0, "difficulty": "intermediate"},
        {"q": "Which protocol is used for email?", "options": ["HTTP", "FTP", "SMTP", "TCP"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is defragmentation?", "options": ["Deleting files", "Organizing fragmented data", "Formatting disk", "Backing up data"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which device connects different networks?", "options": ["Switch", "Hub", "Router", "Modem"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is multitasking?", "options": ["Multiple users", "Multiple programs running", "Multiple processors", "Multiple computers"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which is a lossless compression format?", "options": ["JPG", "PNG", "MP3", "MP4"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What does LAN stand for?", "options": ["Large Area Network", "Local Area Network", "Long Access Network", "Logical Area Network"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which is NOT an operating system?", "options": ["Windows", "Linux", "Oracle", "macOS"], "answer": 2, "difficulty": "intermediate"},
        {"q": "What is booting?", "options": ["Shutting down", "Starting computer", "Installing software", "Formatting disk"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which memory is closest to CPU?", "options": ["RAM", "Cache", "Hard Disk", "ROM"], "answer": 1, "difficulty": "intermediate"},
        {"q": "What is a cookie in web browsing?", "options": ["Virus", "Small data file", "Browser", "Website"], "answer": 1, "difficulty": "intermediate"},
        {"q": "Which file system does Windows use?", "options": ["ext4", "NTFS", "HFS+", "APFS"], "answer": 1, "difficulty": "intermediate"},
        
        # Advanced Level (36-50)
        {"q": "What is the von Neumann architecture?", "options": ["GPU design", "Stored program concept", "Network architecture", "Database model"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which sorting algorithm has best average case?", "options": ["Bubble Sort", "Quick Sort", "Selection Sort", "Insertion Sort"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is Big-O notation?", "options": ["Memory usage", "Algorithm complexity", "Data type", "Programming syntax"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which is a NoSQL database?", "options": ["MySQL", "PostgreSQL", "MongoDB", "Oracle"], "answer": 2, "difficulty": "advanced"},
        {"q": "What is RAID?", "options": ["Virus type", "Redundant Array of Independent Disks", "Network protocol", "Programming language"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which layer is NOT in OSI model?", "options": ["Application", "Session", "Internet", "Transport"], "answer": 2, "difficulty": "advanced"},
        {"q": "What is a deadlock in OS?", "options": ["System crash", "Process waiting indefinitely", "Memory full", "Disk error"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which scheduling algorithm prevents starvation?", "options": ["FCFS", "Round Robin", "SJF", "Priority"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is thrashing in OS?", "options": ["Excessive paging", "Memory leak", "Disk failure", "Network congestion"], "answer": 0, "difficulty": "advanced"},
        {"q": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Tree", "Graph"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is normalization in databases?", "options": ["Data encryption", "Reducing redundancy", "Increasing speed", "Data backup"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which is a symmetric encryption algorithm?", "options": ["RSA", "AES", "Diffie-Hellman", "ECC"], "answer": 1, "difficulty": "advanced"},
        {"q": "What is pipelining in CPU?", "options": ["Data storage", "Parallel instruction execution", "Memory management", "I/O operation"], "answer": 1, "difficulty": "advanced"},
        {"q": "Which protocol ensures reliable delivery?", "options": ["UDP", "IP", "TCP", "ICMP"], "answer": 2, "difficulty": "advanced"},
        {"q": "What is a hash collision?", "options": ["Memory error", "Two inputs same hash", "Network error", "Disk failure"], "answer": 1, "difficulty": "advanced"}
    ]
}

# =================== HELPER FUNCTIONS ===================

IS_MOCK_DB = False

def init_db():
    """Initialize database with questions if empty"""
    global IS_MOCK_DB
    try:
        if db is not None:
            # Check if we are using mongomock
            if 'mongomock' in str(type(client)):
                IS_MOCK_DB = True
                print("⚠️ Running in MOCK DB mode (Stateless).")
            
            # Check if questions exist
            try:
                count = db.questions.count_documents({})
            except:
                count = 0
                
            if count == 0:
                print("⚠️ Database empty. Seeding questions...")
                questions_to_insert = []
                for category, questions in QUESTIONS_DATA.items():
                    for q in questions:
                        q['category'] = category
                        questions_to_insert.append(q)
                
                if questions_to_insert:
                    db.questions.insert_many(questions_to_insert)
                    print(f"✅ Seeded {len(questions_to_insert)} questions into database.")
            else:
                print(f"✅ Database already contains {count} questions.")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Initialize DB on startup
init_db()

def login_required(f):
    """Decorator to check if user is logged in"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            if request.is_json:
                return jsonify({"error": "Unauthorized. Please login."}), 401
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to check if user is admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or session.get('role') != 'admin':
            if request.is_json:
                return jsonify({"error": "Admin access required"}), 403
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# =================== ROUTES ===================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student_login')
def student_login():
    # Clear any existing session
    session.clear()
    return render_template('student_login.html')

@app.route('/admin_login')
def admin_login():
    session.clear()
    return render_template('admin_login.html')

# ✅ FIXED REGISTRATION
@app.route('/api/register', methods=['POST'])
def register():
    # If Mock DB, just simulate success
    if IS_MOCK_DB:
        data = request.json
        return jsonify({
            "message": "Registration successful! (Demo Mode)",
            "user_id": "demo_user_id"
        })

    collections = get_collections()
    if not collections:
        return jsonify({"error": "Database not available. Please try again later."}), 500
    
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        print(f"📝 Registration attempt: {data.get('roll_number')}")
        
        # Validate input
        name = data.get('name', '').strip()
        roll_number = data.get('roll_number', '').strip()
        password = data.get('password', '')
        
        if not name or not roll_number or not password:
            return jsonify({"error": "All fields are required"}), 400
        
        if len(password) < 4:
            return jsonify({"error": "Password must be at least 4 characters"}), 400
        
        # Check if user exists
        existing_user = collections['users'].find_one({"roll_number": roll_number})
        if existing_user:
            print(f"❌ Roll number already exists: {roll_number}")
            return jsonify({"error": "Roll number already registered"}), 400
        
        # Create user
        user_data = {
            "name": name,
            "roll_number": roll_number,
            "password": generate_password_hash(password, method='pbkdf2:sha256'),
            "role": "student",
            "registered_at": datetime.now()
        }
        
        result = collections['users'].insert_one(user_data)
        user_id = result.inserted_id
        print(f"✅ User registered: {roll_number} (ID: {user_id})")
        
        return jsonify({
            "message": "Registration successful! Please login.",
            "user_id": str(user_id)
        })
    
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

# ✅ FIXED LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        roll_number = data.get('roll_number', '').strip()
        password = data.get('password', '')
        
        print(f"🔑 Login attempt: {roll_number}")
        
        if not roll_number or not password:
            return jsonify({"error": "Roll number and password required"}), 400
            
        # DEMO MODE LOGIN
        if IS_MOCK_DB:
            print("⚠️ Demo Mode Login: Accepting any credentials")
            session.clear()
            session['user_id'] = 'demo_user_id'
            session['roll_number'] = roll_number
            session['name'] = 'Demo Student'
            session['role'] = 'student'
            session['logged_in'] = True
            session.permanent = True
            return jsonify({
                "message": "Login successful (Demo)",
                "name": "Demo Student",
                "roll_number": roll_number
            })
        
        collections = get_collections()
        if not collections:
            return jsonify({"error": "Database not available. Please try again later."}), 500

        # Find user
        user = collections['users'].find_one({"roll_number": roll_number})
        
        if not user:
            print(f"❌ User not found: {roll_number}")
            return jsonify({"error": "Invalid roll number or password"}), 401
        
        # Check password
        if not check_password_hash(user['password'], password):
            print(f"❌ Wrong password for: {roll_number}")
            return jsonify({"error": "Invalid roll number or password"}), 401
        
        # Check if already completed exam
        existing_result = collections['results'].find_one({"student_id": user['_id']})
        if existing_result:
            print(f"⚠️ User already completed exam: {roll_number}")
            return jsonify({"error": "You have already completed the exam"}), 403
        
        # ✅ CLEAR OLD SESSION AND SET NEW ONE
        session.clear()
        session['user_id'] = str(user['_id'])
        session['roll_number'] = user['roll_number']
        session['name'] = user['name']
        session['role'] = 'student'
        session['logged_in'] = True
        session.permanent = True
        
        print(f"✅ Login successful: {roll_number}")
        print(f"   Session ID: {session.get('user_id')}")
        print(f"   Session logged_in: {session.get('logged_in')}")
        
        return jsonify({
            "message": "Login successful",
            "name": user['name'],
            "roll_number": user['roll_number']
        })
    
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

# ✅ FIXED ADMIN LOGIN
@app.route('/api/admin_login', methods=['POST'])
def admin_login_api():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        print(f"🔐 Admin login attempt: '{username}'")
        
        # Default admin credentials
        ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
        ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.clear()
            session['user_id'] = 'admin'
            session['role'] = 'admin'
            session['name'] = 'Administrator'
            session['logged_in'] = True
            session.permanent = True
            
            print("✅ Admin login successful")
            return jsonify({"message": "Admin login successful"})
        
        print(f"❌ Invalid admin credentials")
        return jsonify({"error": "Invalid admin credentials"}), 401
    
    except Exception as e:
        print(f"❌ Admin login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

# ✅ CHECK SESSION (DEBUG ENDPOINT)
@app.route('/api/check_session')
def check_session_api():
    return jsonify({
        "session_exists": 'user_id' in session,
        "user_id": session.get('user_id'),
        "roll_number": session.get('roll_number'),
        "name": session.get('name'),
        "role": session.get('role'),
        "logged_in": session.get('logged_in', False),
        "is_mock_db": IS_MOCK_DB
    })

# ✅ EXAM PAGE
@app.route('/exam')
def exam():
    print(f"📄 Exam page request")
    print(f"   Session user_id: {session.get('user_id')}")
    print(f"   Session role: {session.get('role')}")
    print(f"   Session logged_in: {session.get('logged_in')}")
    
    if not session.get('logged_in') or session.get('role') != 'student':
        print("❌ Unauthorized - redirecting to login")
        return redirect('/student_login')
    
    return render_template('exam.html', 
                         name=session.get('name'),
                         roll_number=session.get('roll_number'))

# ✅ ADMIN DASHBOARD
@app.route('/admin_dashboard')
def admin_dashboard():
    print(f"📊 Admin dashboard request")
    print(f"   Session user_id: {session.get('user_id')}")
    print(f"   Session role: {session.get('role')}")
    
    if not session.get('logged_in') or session.get('role') != 'admin':
        print("❌ Unauthorized - redirecting to admin login")
        return redirect('/admin_login')
    
    return render_template('admin_dashboard.html')

# ✅ DEBUG SESSION
@app.route('/api/debug/session')
def debug_session():
    return jsonify({
        "session_data": dict(session),
        "has_user_id": 'user_id' in session,
        "user_id": session.get('user_id'),
        "roll_number": session.get('roll_number'),
        "name": session.get('name'),
        "role": session.get('role'),
        "logged_in": session.get('logged_in')
    })

# ✅ START EXAM
@app.route('/api/start_exam', methods=['POST'])
def start_exam():
    if not session.get('logged_in') or session.get('role') != 'student':
        print(f"❌ Unauthorized exam start attempt")
        return jsonify({"error": "Unauthorized. Please login again."}), 401
    
    try:
        # DEMO MODE: Store exam in session
        if IS_MOCK_DB:
            print("⚠️ Starting Demo Exam (Session Storage)")
            
            # Generate questions
            exam_questions = []
            for category in ['python', 'web_design', 'iot', 'fundamentals']:
                questions_in_category = QUESTIONS_DATA.get(category, [])
                if len(questions_in_category) >= 25:
                    selected = random.sample(questions_in_category, 25)
                else:
                    selected = questions_in_category
                for q in selected:
                    # Add category if missing (should be there from init_db logic but safe to add)
                    q_copy = q.copy()
                    q_copy['category'] = category
                    exam_questions.append(q_copy)
            
            random.shuffle(exam_questions)
            
            # Store full exam state in session (compressed/minimal)
            # We can't store objects, so store indices or full data?
            # Storing full data might be too big for cookie (4KB limit).
            # Strategy: Store only indices if possible, or use QUESTIONS_DATA lookup.
            # But QUESTIONS_DATA is static. So we can just store list of (category, index).
            
            # Better: Just store the question list in session? 100 questions * ~200 bytes = 20KB. Too big for cookie.
            # We MUST use server-side storage or reduce size.
            # Since we removed server-side session, we have a problem for 100 questions in cookie.
            
            # ALTERNATIVE: Just return questions to client and trust client for Demo?
            # Or assume random seed?
            # Let's use a fixed seed based on user_id for demo?
            # No, random.shuffle.
            
            # OK, for Vercel Demo without DB, we can't easily persist 100 questions state securely.
            # Compromise: Send questions to client. When submitting, client sends back answers.
            # We re-grade based on the question text/ID?
            # We can send the "correct answer" to the client but encrypted? No.
            
            # Let's just generate the questions and send them.
            # For submission, we will rely on the client sending back the Question ID and we look it up in QUESTIONS_DATA.
            # We don't need to persist the *exact* exam instance in DB.
            # We just need to grade the answers provided against the static data.
            
            questions_data = []
            for i, q in enumerate(exam_questions):
                # Generate a deterministic ID
                q_id = generate_id(q['q'] + q['category'])
                questions_data.append({
                    "id": q_id,
                    "number": i + 1,
                    "category": q['category'],
                    "question": q['q'],
                    "options": q['options'],
                    "difficulty": q.get('difficulty', 'basic')
                })
            
            return jsonify({"questions": questions_data, "resumed": False})

        # REAL DB LOGIC
        collections = get_collections()
        if not collections:
            return jsonify({"error": "Database not available"}), 500
        
        user_id = session.get('user_id')
        
        # Check if user already has an ongoing exam
        existing_exam = collections['exams'].find_one({
            "student_id": ObjectId(user_id),
            "status": "in_progress"
        })
        
        if existing_exam:
            # Return existing exam questions
            exam_questions = []
            for q_id in existing_exam['questions']:
                q = collections['questions'].find_one({"_id": ObjectId(q_id)})
                if q:
                    exam_questions.append(q)
            
            session['exam_id'] = str(existing_exam['_id'])
            
            questions_data = []
            for i, q in enumerate(exam_questions):
                questions_data.append({
                    "id": str(q['_id']),
                    "number": i + 1,
                    "category": q['category'],
                    "question": q['question'],
                    "options": q['options'],
                    "difficulty": q.get('difficulty', 'basic')
                })
            
            print(f"📋 Returning existing exam for {session.get('roll_number')}")
            return jsonify({"questions": questions_data, "resumed": True})
        
        # Check if already completed
        existing_result = collections['results'].find_one({"student_id": ObjectId(user_id)})
        if existing_result:
            return jsonify({"error": "You have already completed the exam"}), 400
        
        # RANDOMIZE: Get random 25 questions from each category (total 100)
        exam_questions = []
        for category in ['python', 'web_design', 'iot', 'fundamentals']:
            all_cat_questions = list(collections['questions'].find({"category": category}))
            
            if len(all_cat_questions) >= 25:
                selected_questions = random.sample(all_cat_questions, 25)
            else:
                selected_questions = all_cat_questions
            
            exam_questions.extend(selected_questions)
        
        # Shuffle all questions
        random.shuffle(exam_questions)
        
        # Create exam session
        exam_doc = {
            "student_id": ObjectId(user_id),
            "roll_number": session.get('roll_number'),
            "name": session.get('name'),
            "status": "in_progress",
            "started_at": datetime.now(),
            "questions": [str(q['_id']) for q in exam_questions],
            "randomized": True
        }
        
        result = collections['exams'].insert_one(exam_doc)
        exam_id = result.inserted_id
        
        session['exam_id'] = str(exam_id)
        
        # Return questions without answers
        questions_data = []
        for i, q in enumerate(exam_questions):
            questions_data.append({
                "id": str(q['_id']),
                "number": i + 1,
                "category": q['category'],
                "question": q['question'],
                "options": q['options'],
                "difficulty": q.get('difficulty', 'basic')
            })
        
        print(f"✅ Exam started for {session.get('roll_number')} - {len(questions_data)} questions")
        
        return jsonify({"questions": questions_data, "resumed": False})
    
    except Exception as e:
        print(f"❌ Start exam error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to start exam: {str(e)}"}), 500

# ✅ SUBMIT EXAM
@app.route('/api/submit_exam', methods=['POST'])
def submit_exam():
    if not session.get('logged_in') or session.get('role') != 'student':
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.json
        answers = data.get('answers', {})
        
        # DEMO MODE SUBMISSION
        if IS_MOCK_DB:
            print("⚠️ Demo Mode Submission")
            score = 0
            total_questions = 0
            category_scores = {
                "python": {"correct": 0, "total": 0}, 
                "web_design": {"correct": 0, "total": 0},
                "iot": {"correct": 0, "total": 0},
                "fundamentals": {"correct": 0, "total": 0}
            }
            
            # Grade based on static data
            # We need to find the question by ID (which we generated as hash or used real ID?)
            # In start_exam demo mode, I used hash(q['q'] + q['category']).
            # Let's rebuild the lookup map.
            
            question_lookup = {}
            for category, questions in QUESTIONS_DATA.items():
                for q in questions:
                    q_id = generate_id(q['q'] + category)
                    question_lookup[q_id] = {**q, "category": category}
            
            for q_id, user_answer in answers.items():
                question = question_lookup.get(q_id)
                if question:
                    cat = question['category']
                    category_scores[cat]['total'] += 1
                    total_questions += 1
                    
                    try:
                        user_answer = int(user_answer)
                    except:
                        user_answer = -1
                        
                    if user_answer == question['answer']:
                        score += 1
                        category_scores[cat]['correct'] += 1
            
            # Adjust total if not all answered (assume 100 for demo?)
            # The client sends all answers? Or only answered ones?
            # Let's assume the exam had 100 questions.
            total_questions = 100 
            
            percentage = (score / total_questions * 100) if total_questions > 0 else 0
            passed = percentage >= 40
            
            return jsonify({
                "score": score,
                "total": total_questions,
                "percentage": round(percentage, 2),
                "passed": passed,
                "category_scores": category_scores,
                "grade": "Pass" if passed else "Fail" # Simple grade
            })

        # REAL DB LOGIC
        collections = get_collections()
        if not collections:
            return jsonify({"error": "Database not available"}), 500
            
        if not session.get('exam_id'):
            return jsonify({"error": "No active exam found"}), 400
            
        exam_id = session.get('exam_id')
        user_id = session.get('user_id')
        
        exam = collections['exams'].find_one({"_id": ObjectId(exam_id)})
        if not exam:
            return jsonify({"error": "Exam not found"}), 404
            
        if exam['status'] == 'completed':
            return jsonify({"error": "Exam already submitted"}), 400
        
        # Calculate score
        score = 0
        total_questions = len(exam['questions'])
        category_scores = {
            "python": {"correct": 0, "total": 0}, 
            "web_design": {"correct": 0, "total": 0},
            "iot": {"correct": 0, "total": 0},
            "fundamentals": {"correct": 0, "total": 0}
        }
        
        detailed_results = []
        
        for q_id in exam['questions']:
            question = collections['questions'].find_one({"_id": ObjectId(q_id)})
            if question:
                category = question['category']
                category_scores[category]['total'] += 1
                
                user_answer = answers.get(q_id, -1)
                if isinstance(user_answer, str):
                    try:
                        user_answer = int(user_answer)
                    except:
                        user_answer = -1
                
                is_correct = (user_answer == question['answer'])
                
                if is_correct:
                    score += 1
                    category_scores[category]['correct'] += 1
                
                detailed_results.append({
                    "question_id": q_id,
                    "user_answer": user_answer,
                    "correct_answer": question['answer'],
                    "is_correct": is_correct
                })
        
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        # Determine pass/fail (40% pass mark)
        passed = percentage >= 40
        
        # Save result
        result_data = {
            "exam_id": ObjectId(exam_id),
            "student_id": ObjectId(user_id),
            "roll_number": session.get('roll_number'),
            "name": session.get('name'),
            "score": score,
            "total": total_questions,
            "percentage": round(percentage, 2),
            "passed": passed,
            "category_scores": category_scores,
            "submitted_at": datetime.now(),
            "answers": answers,
            "detailed_results": detailed_results
        }
        
        collections['results'].insert_one(result_data)
        
        # Update exam status
        collections['exams'].update_one(
            {"_id": ObjectId(exam_id)},
            {"$set": {"status": "completed", "completed_at": datetime.now()}}
        )
        
        print(f"✅ Exam submitted: {session.get('roll_number')} - Score: {score}/{total_questions} ({percentage:.1f}%)")
        
        # Clear exam session but keep user logged in
        session.pop('exam_id', None)
        
        return jsonify({
            "score": score,
            "total": total_questions,
            "percentage": round(percentage, 2),
            "passed": passed,
            "category_scores": category_scores
        })
    
    except Exception as e:
        print(f"❌ Submit exam error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to submit exam: {str(e)}"}), 500

# ✅ GET RESULTS
@app.route('/api/results')
def get_results():
    collections = get_collections()
    
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    if not collections:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        if session.get('role') == 'admin':
            results = list(collections['results'].find().sort("submitted_at", -1))
        else:
            results = list(collections['results'].find({
                "student_id": ObjectId(session['user_id'])
            }).sort("submitted_at", -1))
        
        # Convert ObjectId to string for JSON serialization
        formatted_results = []
        for result in results:
            formatted_result = {
                '_id': str(result['_id']),
                'exam_id': str(result['exam_id']),
                'student_id': str(result['student_id']),
                'roll_number': result.get('roll_number', 'N/A'),
                'name': result.get('name', 'N/A'),
                'score': result.get('score', 0),
                'total': result.get('total', 0),
                'percentage': result.get('percentage', 0),
                'passed': result.get('passed', False),
                'category_scores': result.get('category_scores', {}),
                'submitted_at': result['submitted_at'].strftime("%Y-%m-%d %H:%M:%S") if result.get('submitted_at') else 'N/A'
            }
            formatted_results.append(formatted_result)
        
        return jsonify(formatted_results)
    
    except Exception as e:
        print(f"❌ Get results error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ✅ GET ALL STUDENTS (ADMIN)
@app.route('/api/admin/students')
def get_all_students():
    collections = get_collections()
    
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    if not collections:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        students = list(collections['users'].find({"role": "student"}))
        
        formatted_students = []
        for student in students:
            # Check if student has completed exam
            result = collections['results'].find_one({"student_id": student['_id']})
            
            formatted_student = {
                '_id': str(student['_id']),
                'name': student.get('name', 'N/A'),
                'roll_number': student.get('roll_number', 'N/A'),
                'registered_at': student['registered_at'].strftime("%Y-%m-%d %H:%M:%S") if student.get('registered_at') else 'N/A',
                'exam_completed': result is not None,
                'score': result.get('score') if result else None,
                'total': result.get('total') if result else None,
                'percentage': result.get('percentage') if result else None
            }
            formatted_students.append(formatted_student)
        
        return jsonify(formatted_students)
    
    except Exception as e:
        print(f"❌ Get students error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ✅ DELETE STUDENT (ADMIN)
@app.route('/api/admin/delete_student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    collections = get_collections()
    
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    if not collections:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        # Delete user
        collections['users'].delete_one({"_id": ObjectId(student_id)})
        # Delete their exams
        collections['exams'].delete_many({"student_id": ObjectId(student_id)})
        # Delete their results
        collections['results'].delete_many({"student_id": ObjectId(student_id)})
        
        return jsonify({"message": "Student deleted successfully"})
    
    except Exception as e:
        print(f"❌ Delete student error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ✅ RESET STUDENT EXAM (ADMIN)
@app.route('/api/admin/reset_exam/<student_id>', methods=['POST'])
def reset_student_exam(student_id):
    collections = get_collections()
    
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    if not collections:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        # Delete their exams
        collections['exams'].delete_many({"student_id": ObjectId(student_id)})
        # Delete their results
        collections['results'].delete_many({"student_id": ObjectId(student_id)})
        
        return jsonify({"message": "Student exam reset successfully"})
    
    except Exception as e:
        print(f"❌ Reset exam error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ✅ LOGOUT
@app.route('/api/logout', methods=['POST'])
def logout():
    roll = session.get('roll_number', session.get('name', 'Unknown'))
    session.clear()
    print(f"👋 Logout: {roll}")
    return jsonify({"message": "Logged out successfully"})

# ✅ INIT DATABASE
@app.route('/api/init_db', methods=['POST'])
def init_database():
    collections = get_collections()
    if not collections:
        return jsonify({"error": "Database not available"}), 500
    
    # Optional: Require admin for this
    # if not session.get('logged_in') or session.get('role') != 'admin':
    #     return jsonify({"error": "Admin access required"}), 403
    
    try:
        # Clear existing questions
        collections['questions'].delete_many({})
        
        # Insert all questions
        total_inserted = 0
        for category, questions in QUESTIONS_DATA.items():
            for q_data in questions:
                question_doc = {
                    "category": category,
                    "question": q_data['q'],
                    "options": q_data['options'],
                    "answer": q_data['answer'],
                    "difficulty": q_data['difficulty']
                }
                collections['questions'].insert_one(question_doc)
                total_inserted += 1
        
        print(f"✅ Database initialized with {total_inserted} questions")
        
        # Count by category
        stats = {}
        for category in ['python', 'web_design', 'iot', 'fundamentals']:
            count = collections['questions'].count_documents({"category": category})
            stats[category] = count
        
        return jsonify({
            "message": "Database initialized successfully",
            "total_questions": total_inserted,
            "by_category": stats
        })
    
    except Exception as e:
        print(f"❌ Init DB error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ✅ GET QUESTION STATS
@app.route('/api/question_stats')
def get_question_stats():
    collections = get_collections()
    if not collections:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        stats = {}
        total = 0
        for category in ['python', 'web_design', 'iot', 'fundamentals']:
            count = collections['questions'].count_documents({"category": category})
            stats[category] = count
            total += count
        
        stats['total'] = total
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ HEALTH CHECK
@app.route('/api/health')
def health_check():
    db_status = "connected" if get_collections() else "disconnected"
    return jsonify({
        "status": "ok",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    })

# =================== ERROR HANDLERS ===================

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({"error": "Endpoint not found"}), 404
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    print(f"❌ Server error: {str(e)}")
    if request.path.startswith('/api/'):
        return jsonify({"error": "Internal server error"}), 500
    return render_template('index.html'), 500

# =================== MAIN ===================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting Flask app on port {port}")
    print(f"🔑 Secret key: {app.config['SECRET_KEY'][:16]}...")
    print(f"📦 Session type: {app.config['SESSION_TYPE']}")
    print(f"🐛 Debug mode: {debug}")
    
    # Initialize database on startup
    collections = get_collections()
    if collections:
        question_count = collections['questions'].count_documents({})
        print(f"📚 Questions in database: {question_count}")
        if question_count == 0:
            print("⚠️ No questions found. Initialize database by calling POST /api/init_db")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
