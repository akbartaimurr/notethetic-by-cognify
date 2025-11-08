from assignments import get_assignments
from exams import get_exams
from subjects import get_subjects
from data import get_user_data


def get_dashboard_data(user_id):
    # grab all data once (no duplicate queries)
    assignments = get_assignments(user_id)
    exams = get_exams(user_id)
    subjects = get_subjects(user_id)
    user_data = get_user_data(user_id)
    
    # process assignment names from data we already got
    assignment_names = []
    for a in assignments:
        assignment_names.append({'name': a.get('name', ''), 'emoji': '📝'})
    
    # process exam names from data we already got
    exam_names = []
    for e in exams:
        exam_names.append({'name': e.get('name', ''), 'emoji': '📚'})
    
    # process subject names from data we already got
    subject_names = []
    for s in subjects:
        subject_names.append({'name': s.get('subject', '')})
    
    # make notifications
    notifications = []
    
    # check for pending assignments (not done yet)
    pending_assignments = []
    for a in assignments:
        if a.get('status') != 'completed':
            pending_assignments.append(a)
    if pending_assignments:
        notifications.append({
            'type': 'pending_assignments',
            'message': 'You have some pending assignments',
            'emoji': '📝'
        })
    
    # check for missing assignments
    missing_assignments = []
    for a in assignments:
        if a.get('status') == '':
            missing_assignments.append(a)
    if missing_assignments:
        notifications.append({
            'type': 'missing_assignments',
            'message': 'You have some missing assignments',
            'emoji': '⚠️'
        })
    
    # check for upcoming exams
    if exams:
        notifications.append({
            'type': 'upcoming_exams',
            'message': 'You have some exams coming up',
            'emoji': '📚'
        })
    
    return {
        'assignments': assignments,
        'exams': exams,
        'user_data': user_data,
        'notifications': notifications,
        'assignment_names': assignment_names,
        'exam_names': exam_names,
        'subject_names': subject_names
    }

