from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from login import get_google_login_url, get_supabase, logout_user
from dashboard import get_dashboard_data
from subjects import get_subjects, add_subject
from assignments import get_assignments, mark_assignment_done, add_assignment
from exams import get_exams, delete_exam, add_exam
from ai import generate_study_planner_api
from data import get_user_data, update_user_data
import os
from dotenv import load_dotenv

# load environment variables (learned this from flask docs)
load_dotenv()

# create flask app (basic flask setup from tutorial)
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change-this-secret-key')


# check if user is logged in
def check_login():
    return 'access_token' in session



# login page route
@app.route('/signin')
def signin():
    # if already logged in send to dashboard
    if check_login():
        return redirect('/')
    return render_template('signin.html')



# google login button route
@app.route('/auth/google')
def google_login():
    # get google login url and redirect there
    login_url = get_google_login_url()
    return redirect(login_url)



# google sends user back here after login
@app.route('/auth/callback')
def callback():
    # redirect back to signin page
    return redirect('/signin')



# save tokens from frontend (found this pattern on stackoverflow)
@app.route('/auth/save-tokens', methods=['POST'])
def save_tokens():
    # get json data from request
    data = request.get_json()
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    
    # get user info from supabase
    supabase = get_supabase()
    user_response = supabase.auth.get_user(access_token)
    user_data = user_response.user
    
    # save tokens in session (flask session docs helped with this)
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    session['user'] = {
        'id': user_data.id,
        'email': user_data.email
    }
    session.permanent = True
    return jsonify({'success': True})



# logout route
@app.route('/logout')
def logout():
    # clear session and logout
    logout_user()
    session.clear()
    return redirect('/signin')



# main dashboard page
@app.route('/')
def dashboard():
    # check if logged in first
    if not check_login():
        return redirect('/signin')
    
    # get user id from session
    user_id = session['user'].get('id')
    
    # get all dashboard data
    dashboard_data = get_dashboard_data(user_id)
    
    # get user email from session
    user_email = session['user'].get('email', '')
    
    # render template with data
    return render_template('dashboard.html', 
                         notifications=dashboard_data['notifications'],
                         assignments=dashboard_data['assignment_names'],
                         exams=dashboard_data['exam_names'],
                         subjects=dashboard_data['subject_names'],
                         user_email=user_email)



# exams page
@app.route('/exams')
def exams():
    # check login
    if not check_login():
        return redirect('/signin')
    
    # get user id
    user_id = session['user'].get('id')
    
    # get exams from database
    exams_list = get_exams(user_id)
    
    # show exams page
    return render_template('exams.html', exams=exams_list)



# assignments page
@app.route('/assignments')
def assignments():
    # check login
    if not check_login():
        return redirect('/signin')
    
    # get user id
    user_id = session['user'].get('id')
    
    # get assignments
    assignments_list = get_assignments(user_id)
    
    # show assignments page
    return render_template('assignments.html', assignments=assignments_list)



# mark assignment as done
@app.route('/assignments/mark-done', methods=['POST'])
def mark_done_route():
    # check login
    if not check_login():
        return jsonify({'success': False})
    
    # get user id and assignment id
    user_id = session['user'].get('id')
    data = request.get_json()
    assignment_id = data.get('id')
    
    # mark as done
    if mark_assignment_done(user_id, assignment_id):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})



# add new assignment
@app.route('/assignments/add', methods=['POST'])
def add_assignment_route():
    # check login
    if not check_login():
        return jsonify({'success': False})
    
    # get data from request
    user_id = session['user'].get('id')
    data = request.get_json()
    name = data.get('name')
    
    # get optional fields
    due = data.get('due') or None
    status = data.get('status') or None
    
    # add assignment
    if add_assignment(user_id, name, due, status):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})



# subjects page
@app.route('/subjects')
def subjects():
    # check login
    if not check_login():
        return redirect('/signin')
    
    # get user id
    user_id = session['user'].get('id')
    
    # get subjects
    subjects = get_subjects(user_id)
    
    # format subjects for template
    subject_names = []
    for s in subjects:
        subject_names.append({
            'name': s.get('subject', ''),
            'id': s['id']
        })
    
    # show subjects page
    return render_template('subjects.html', subjects=subject_names)



# add new subject
@app.route('/subjects/add', methods=['POST'])
def add_subject_route():
    # check login
    if not check_login():
        return jsonify({'success': False})
    
    # get data
    user_id = session['user'].get('id')
    data = request.get_json()
    subject_name = data.get('subject')
    
    # add subject
    if add_subject(user_id, subject_name):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})



# add new exam
@app.route('/exams/add', methods=['POST'])
def add_exam_route():
    # check login
    if not check_login():
        return jsonify({'success': False})
    
    # get data
    user_id = session['user'].get('id')
    data = request.get_json()
    name = data.get('name')
    date = data.get('date')
    
    # add exam
    if add_exam(user_id, name, date):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})



# delete exam
@app.route('/exams/delete', methods=['POST'])
def delete_exam_route():
    # check login
    if not check_login():
        return jsonify({'success': False})
    
    # get data
    user_id = session['user'].get('id')
    data = request.get_json()
    exam_id = data.get('id')
    
    # delete exam
    if delete_exam(user_id, exam_id):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})



# planner page
@app.route('/planner')
def planner():
    # check login
    if not check_login():
        return redirect('/signin')
    
    # show planner page
    return render_template('planner.html')



# generate study planner
@app.route('/planner/generate', methods=['POST'])
def generate_planner():
    # check login
    if not check_login():
        return jsonify({'success': False})
    
    # get user id
    user_id = session['user'].get('id')
    
    # get all data needed for planner
    subjects_list = get_subjects(user_id)
    user_data = get_user_data(user_id)
    assignments_list = get_assignments(user_id)
    
    # get hours and days from user data
    if user_data: 
        hours_available = user_data.get('hoursavailable')
        days_per_week = user_data.get('daysperweek')
        weeks_to_schedule = user_data.get('weekstoschedule')
    else:
        hours_available = 8
        days_per_week = 5
        weeks_to_schedule = 4
    
    # set defaults if None
    if hours_available is None:
        hours_available = 8
    if days_per_week is None:
        days_per_week = 5
    if weeks_to_schedule is None:
        weeks_to_schedule = 4
    
    # call api to generate planner
    planner_text = generate_study_planner_api(
        subjects=subjects_list,
        hours_available=hours_available,
        days_per_week=days_per_week,
        weeks_to_schedule=weeks_to_schedule,
        assignments=assignments_list
    )
    
    # return planner text
    return jsonify({'success': True, 'planner_text': planner_text})



# data settings page
@app.route('/data')
def data():
    # check login
    if not check_login():
        return redirect('/signin')
    
    # get user id
    user_id = session['user'].get('id')
    
    # get user data
    user_data = get_user_data(user_id)
    
    # show data page
    return render_template('data.html', user_data=user_data)



# update user data
@app.route('/data/update', methods=['POST'])
def update_data_route():
    # check login
    if not check_login():
        return jsonify({'success': False})
    
    # get data
    user_id = session['user'].get('id')
    data = request.get_json()
    
    # get values from request
    hours_available = data.get('hoursavailable')
    days_per_week = data.get('daysperweek')
    weeks_to_schedule = data.get('weekstoschedule')
    
    # update in database
    if update_user_data(user_id, hours_available, days_per_week, weeks_to_schedule):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})



# start server (flask docs showed me this)
if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=port)
