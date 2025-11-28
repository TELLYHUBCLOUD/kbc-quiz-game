# app.py - Main Flask Application
from flask import Flask, render_template, request, jsonify, session
import os
import secrets
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Questions database
QUESTIONS = [
    {
        'id': 1,
        'question': "Where was India's first national Museum opened?",
        'options': ['Delhi', 'Hyderabad', 'Rajasthan', 'Mumbai'],
        'correct': 3,
        'prize': 1000
    },
    {
        'id': 2,
        'question': "The green planet in the solar system is?",
        'options': ['Mars', 'Uranus', 'Venus', 'Earth'],
        'correct': 1,
        'prize': 1000
    },
    {
        'id': 3,
        'question': "Which of these is the small-scale industry in India?",
        'options': ['Jute Industry', 'Paper Industry', 'Textile Industry', 'Handloom Industry'],
        'correct': 3,
        'prize': 1000
    },
    {
        'id': 4,
        'question': "What is the term duration for the President of India?",
        'options': ['3 years', '5 years', '4 years', '6 years'],
        'correct': 1,
        'prize': 1000
    },
    {
        'id': 5,
        'question': "Who is the father of Indian Constitution?",
        'options': ['Jawaharlal Nehru', 'B R Ambedkar', 'Mahatma Gandhi', 'Sardar Patel'],
        'correct': 1,
        'prize': 1000
    }
]

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    """Initialize a new game session"""
    session['current_question'] = 0
    session['money'] = 0
    session['correct_answers'] = 0
    session['incorrect_answers'] = 0
    return jsonify({'success': True, 'message': 'Game started!'})

@app.route('/get_question', methods=['GET'])
def get_question():
    """Get current question"""
    current = session.get('current_question', 0)
    
    if current >= len(QUESTIONS):
        return jsonify({'game_over': True})
    
    question = QUESTIONS[current].copy()
    # Don't send the correct answer to the client
    question.pop('correct', None)
    
    return jsonify({
        'question': question,
        'current_question': current + 1,
        'total_questions': len(QUESTIONS),
        'money': session.get('money', 0),
        'correct_answers': session.get('correct_answers', 0),
        'incorrect_answers': session.get('incorrect_answers', 0)
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Check the submitted answer"""
    data = request.json
    logging.info(f"Received data: {data}")
    selected_answer = data.get('answer')
    logging.info(f"Selected answer: {selected_answer}")
    
    current = session.get('current_question', 0)
    
    if current >= len(QUESTIONS):
        return jsonify({'error': 'No more questions'}), 400
    
    question = QUESTIONS[current]
    is_correct = selected_answer == question['correct']
    logging.info(f"Correct answer: {question['correct']}")
    logging.info(f"Is correct: {is_correct}")
    
    # Update session data
    if is_correct:
        session['correct_answers'] = session.get('correct_answers', 0) + 1
        session['money'] = session.get('money', 0) + question['prize']
    else:
        session['incorrect_answers'] = session.get('incorrect_answers', 0) + 1
        session['money'] = session.get('money', 0) - 500
    
    session['current_question'] = current + 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': question['correct'],
        'money': session['money'],
        'correct_answers': session['correct_answers'],
        'incorrect_answers': session['incorrect_answers'],
        'game_over': session['current_question'] >= len(QUESTIONS)
    })

@app.route('/get_results', methods=['GET'])
def get_results():
    """Get final game results"""
    return jsonify({
        'money': session.get('money', 0),
        'correct_answers': session.get('correct_answers', 0),
        'incorrect_answers': session.get('incorrect_answers', 0),
        'total_questions': len(QUESTIONS)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.logger.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
