from assignments import get_assignments
from exams import get_exams
from subjects import get_subjects
from userdata import get_user_data


def get_dashboard_data(user_id):
    # fetch all data once (no duplicate queries)
    assignments = get_assignments(user_id)
    exams = get_exams(user_id)
    subjects = get_subjects(user_id)
    user_data = get_user_data(user_id)
    
    # process assignment names from already-fetched data
    assignment_names = [{'name': a.get('name', ''), 'emoji': '📝'} for a in assignments]
    
    # process exam names from already-fetched data
    exam_names = [{'name': e.get('name', ''), 'emoji': '📚'} for e in exams]
    
    # process subject names from already-fetched data
    subject_names = [{'name': s.get('subject', '')} for s in subjects]
    
    # build notifications
    notifications = []
    
    # check for pending assignments (not completed)
    pending_assignments = [a for a in assignments if a.get('status') != 'completed']
    if pending_assignments:
        notifications.append({
            'type': 'pending_assignments',
            'message': 'You have some pending assignments',
            'emoji': '📝'
        })
    
    # check for missing assignments
    missing_assignments = [a for a in assignments if a.get('status') == '']
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

