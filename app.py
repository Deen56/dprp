from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Assessment, Answer
from config import Config
from flask import jsonify
from rag import chunks, chunk_vectors, chat, ask_veyr
from questions import QUESTIONS

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



def calculate_score(answers):
    total_weight = sum(q['weight'] for q in QUESTIONS)
    risk_points = 0
    for question in QUESTIONS:
        answer = answers.get(str(question['id']), 0)
        if answer == 1:  # 1 = risky answer
            risk_points += question['weight']
    score = int((risk_points / total_weight) * 100)
    if score <= 25:
        risk_level = "Low"
    elif score <= 50:
        risk_level = "Medium"
    elif score <= 75:
        risk_level = "High"
    else:
        risk_level = "Critical"
    return score, risk_level

# ─── Routes ──────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Welcome back, ' + user.username + '!', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/assessment', methods=['GET', 'POST'])
@login_required
def assessment():
    if request.method == 'POST':
        answers = {}
        for question in QUESTIONS:
            answers[str(question['id'])] = int(request.form.get(str(question['id']), 0))
        score, risk_level = calculate_score(answers)
        new_assessment = Assessment(user_id=current_user.id, score=score, risk_level=risk_level)
        db.session.add(new_assessment)
        db.session.flush()
        for question in QUESTIONS:
            ans = Answer(
                assessment_id=new_assessment.id,
                question_id=question['id'],
                answer_value=answers[str(question['id'])]
            )
            db.session.add(ans)
        db.session.commit()
        return redirect(url_for('results', assessment_id=new_assessment.id))
    return render_template('assessment.html', questions=QUESTIONS)

@app.route('/results/<int:assessment_id>')
@login_required
def results(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    return render_template('results.html', assessment=assessment)

@app.route('/history')
@login_required
def history():
    assessments = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.taken_at.desc()).all()
    return render_template('history.html', assessments=assessments)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    users = User.query.all()
    assessments = Assessment.query.order_by(Assessment.taken_at.desc()).all()
    return render_template('admin/dashboard.html', users=users, assessments=assessments)


@app.route('/chat')
@login_required
def chat_page():
    return render_template('chat.html')

@app.route('/chat/message', methods=['POST'])
@login_required
def chat_message():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    response = ask_veyr(user_message, chat, chunks, chunk_vectors, user_id=current_user.id)
    return jsonify({'response': response})
# ─── Init DB & Run ───────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)