let currentQuestion = 0;
let totalQuestions = 5;

async function startGame() {
    try {
        const response = await fetch('/start_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            showScreen('gameScreen');
            loadQuestion();
            updatePrizeLadder();
        }
    } catch (error) {
        console.error('Error starting game:', error);
        alert('Failed to start game. Please try again.');
    }
}

async function loadQuestion() {
    try {
        const response = await fetch('/get_question');
        const data = await response.json();
        
        if (data.game_over) {
            showResults();
            return;
        }
        
        // Update question
        document.getElementById('question').textContent = data.question.question;
        document.getElementById('currentQ').textContent = data.current_question;
        document.getElementById('totalQ').textContent = data.total_questions;
        document.getElementById('money').textContent = data.money;
        document.getElementById('correct').textContent = data.correct_answers;
        document.getElementById('incorrect').textContent = data.incorrect_answers;
        
        // Update options
        const optionsContainer = document.getElementById('options');
        optionsContainer.innerHTML = '';
        
        data.question.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'option';
            button.innerHTML = `${String.fromCharCode(65 + index)}: ${option}`;
            button.onclick = () => submitAnswer(index);
            optionsContainer.appendChild(button);
        });
        
        currentQuestion = data.current_question;
        totalQuestions = data.total_questions;
        updatePrizeLadder();
    } catch (error) {
        console.error('Error loading question:', error);
        alert('Failed to load question. Please try again.');
    }
}

async function submitAnswer(selectedIndex) {
    const options = document.querySelectorAll('.option');
    
    // Disable all options
    options.forEach(opt => {
        opt.classList.add('disabled');
        opt.onclick = null;
    });
    
    // Highlight selected answer
    options[selectedIndex].classList.add('selected');
    
    try {
        const response = await fetch('/submit_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ answer: selectedIndex })
        });
        
        const data = await response.json();
        
        // Show correct/incorrect
        setTimeout(() => {
            options[data.correct_answer].classList.add('correct');
            
            if (!data.correct) {
                options[selectedIndex].classList.add('incorrect');
            }
            
            // Update stats
            document.getElementById('money').textContent = data.money;
            document.getElementById('correct').textContent = data.correct_answers;
            document.getElementById('incorrect').textContent = data.incorrect_answers;
            
            // Move to next question or show results
            setTimeout(() => {
                if (data.game_over) {
                    showResults();
                } else {
                    loadQuestion();
                }
            }, 2000);
        }, 1000);
        
    } catch (error) {
        console.error('Error submitting answer:', error);
        alert('Failed to submit answer. Please try again.');
    }
}

async function showResults() {
    try {
        const response = await fetch('/get_results');
        const data = await response.json();
        
        document.getElementById('finalMoney').textContent = data.money;
        document.getElementById('finalCorrect').textContent = data.correct_answers;
        document.getElementById('finalIncorrect').textContent = data.incorrect_answers;
        
        // Generate message
        let message = '';
        if (data.money > 0) {
            message = '🎉 Congratulations!';
        } else if (data.money < 0) {
            message = '💪 Better luck next time!';
        } else {
            message = '👍 Not bad!';
        }
        message += `You scored ${data.correct_answers} out of ${data.total_questions} questions correctly.`;
        
        document.getElementById('finalMessage').innerHTML = message;
        
        showScreen('resultsScreen');
    } catch (error) {
        console.error('Error loading results:', error);
        alert('Failed to load results. Please try again.');
    }
}

function updatePrizeLadder() {
    const ladder = document.getElementById('ladder');
    ladder.innerHTML = '';
    
    for (let i = 0; i < totalQuestions; i++) {
        const item = document.createElement('div');
        item.className = 'ladder-item';
        
        if (i < currentQuestion - 1) {
            item.classList.add('completed');
        } else if (i === currentQuestion - 1) {
            item.classList.add('current');
        }
        
        item.innerHTML = `
            Question ${i + 1}
            ₹1000
        `;
        
        ladder.appendChild(item);
    }
}

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

function playAgain() {
    showScreen('startScreen');
}
