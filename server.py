from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from login import get_google_login_url, get_supabase, logout_user
from dashboard import get_dashboard_data
from subjects import get_subjects, add_subject
from assignments import get_assignments, mark_assignment_done, add_assignment
from exams import get_exams, delete_exam, add_exam
from userdata import get_user_data
from planner import generate_study_planner
from data import update_user_data
import os
import json
from dotenv import load_dotenv



# used google for sign in and js to store tokens basically

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change-this-secret-key')

# check if they logged in
def check_login():
    return 'access_token' in session

# login page
@app.route('/signin')
def signin():
    # if they already logged in just send em to dashboard
    if check_login():
        return redirect('/')
    return render_template('signin.html')

# when they click google login button
@app.route('/auth/google')
def google_login():
    login_url = get_google_login_url()
    return redirect(login_url)

# google sends em back here after login
@app.route('/auth/callback')
def callback():
    return redirect('/signin')

# stack overflow code to save tokens lol
@app.route('/auth/save-tokens', methods=['POST'])
def save_tokens():
    data = request.get_json()
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    
    supabase = get_supabase()
    user_response = supabase.auth.get_user(access_token)
    user_data = user_response.user
    
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['user'] = {
        'id': user_data.id,
        'email': user_data.email
    }
    session.permanent = True
    return jsonify({'success': True})

# logout button
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/signin')

# main dashboard page
@app.route('/')
def dashboard():
    # gotta be logged in to see this
    if not check_login():
        return redirect('/signin')
    
    user_id = session['user'].get('id')
    
    # grab dashboard data
    dashboard_data = get_dashboard_data(user_id)
    
    return render_template('dashboard.html', 
                         notifications=dashboard_data['notifications'],
                         assignments=dashboard_data['assignment_names'],
                         exams=dashboard_data['exam_names'],
                         subjects=dashboard_data['subject_names'])

# exams page
@app.route('/exams')
def exams():
    # gotta be logged in
    if not check_login():
        return redirect('/signin')
    
    user_id = session['user'].get('id')
    
    # grab exams
    exams_list = get_exams(user_id)
    
    return render_template('exams.html', exams=exams_list)

# assignments page
@app.route('/assignments')
def assignments():
    # gotta be logged in
    if not check_login():
        return redirect('/signin')
    
    user_id = session['user'].get('id')
    
    # grab assignments
    assignments_list = get_assignments(user_id)
    
    return render_template('assignments.html', assignments=assignments_list)

# mark assignment as done endpoint
@app.route('/assignments/mark-done', methods=['POST'])
def mark_done_route():
    if not check_login():
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user_id = session['user'].get('id')
    data = request.get_json()
    assignment_id = data.get('id')
    
    if not assignment_id:
        return jsonify({'success': False, 'error': 'Assignment ID required'}), 400
    
    if mark_assignment_done(user_id, assignment_id):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to mark assignment as done'}), 500

# add assignment endpoint
@app.route('/assignments/add', methods=['POST'])
def add_assignment_route():
    if not check_login():
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user_id = session['user'].get('id')
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'success': False, 'error': 'Assignment name required'}), 400
    
    due = data.get('due') or None
    status = data.get('status') or None
    if add_assignment(user_id, name, due, status):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to add assignment'}), 500


@app.route('/subjects')
def subjects():
    # gotta be logged in
    if not check_login():
        return redirect('/signin')
    
    user_id = session['user'].get('id')
    
    # grab subjects
    subjects = get_subjects(user_id)
    subject_names = []
    for s in subjects:
        subject_names.append({'name': s.get('subject', '')})
    
    return render_template('subjects.html', subjects=subject_names)


@app.route('/subjects/add', methods=['POST'])
def add_subject_route():
    if not check_login():
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user_id = session['user'].get('id')
    data = request.get_json()
    subject_name = data.get('subject')
    
    if not subject_name: # check if empty
        return jsonify({'success': False, 'error': 'Subject name required'}), 400
    
    if add_subject(user_id, subject_name):
        return jsonify({'success': True}) # if it works return true
    else:
        return jsonify({'success': False, 'error': 'Failed to add subject'}), 500 # if it breaks return false

# add exam endpoint
@app.route('/exams/add', methods=['POST'])
def add_exam_route():
    if not check_login():
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user_id = session['user'].get('id')
    data = request.get_json()
    name = data.get('name')
    date = data.get('date')
    
    if not name or not date:
        return jsonify({'success': False, 'error': 'Exam name and date required'}), 400
    
    if add_exam(user_id, name, date):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to add exam'}), 500

# delete exam endpoint
@app.route('/exams/delete', methods=['POST'])
def delete_exam_route():
    if not check_login():
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user_id = session['user'].get('id')
    data = request.get_json()
    exam_id = data.get('id')
    
    if not exam_id:
        return jsonify({'success': False, 'error': 'Exam ID required'}), 400
    
    if delete_exam(user_id, exam_id):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to delete exam'}), 500

# planner page
@app.route('/planner')
def planner():
    # gotta be logged in
    if not check_login():
        return redirect('/signin')
    
    return render_template('planner.html')

# generate planner endpoint
@app.route('/planner/generate', methods=['POST'])
def generate_planner():
    # gotta be logged in
    if not check_login():
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user_id = session['user'].get('id')
    
    # grab all the data we need for planner
    subjects_list = get_subjects(user_id)
    user_data = get_user_data(user_id)
    
    # figure out total time per day from subjects
    total_time_per_day = 0
    for subject in subjects_list:
        avg_time = subject.get('averagetimeinminutes') or 60
        if avg_time:
            total_time_per_day += avg_time
    
    # grab data from userdata columns
    hours_available = user_data.get('hoursavailable') if user_data else 8
    days_per_week = user_data.get('daysperweek') if user_data else 5
    weeks_to_schedule = user_data.get('weekstoschedule') if user_data else 4
    
    # make study planner using openai
    # send all subjects with all their stuff
    planner_text = generate_study_planner(
        subjects=subjects_list,
        total_time_per_day=total_time_per_day,
        hours_available=hours_available,
        days_per_week=days_per_week,
        weeks_to_schedule=weeks_to_schedule
    )
    
    return jsonify({'success': True, 'planner_text': planner_text})

# data page
@app.route('/data')
def data():
    # gotta be logged in
    if not check_login():
        return redirect('/signin')
    
    user_id = session['user'].get('id')
    
    # grab user data
    user_data = get_user_data(user_id)
    
    return render_template('data.html', user_data=user_data)

# update data endpoint
@app.route('/data/update', methods=['POST'])
def update_data_route():
    if not check_login():
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user_id = session['user'].get('id')
    data = request.get_json()
    
    hours_available = data.get('hoursavailable')
    days_per_week = data.get('daysperweek')
    weeks_to_schedule = data.get('weekstoschedule')
    
    if update_user_data(user_id, hours_available, days_per_week, weeks_to_schedule):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to update data'}), 500

# start the server
if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=port)
