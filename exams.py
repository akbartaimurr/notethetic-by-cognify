from login import get_supabase_admin

def get_exams(user_id):
    try:
        supabase = get_supabase_admin()
        result = supabase.table('exams').select('*').eq('userid', user_id).execute()
        return result.data
    except:
        return []

# delete an exam
def delete_exam(user_id, exam_id):
    try:
        supabase = get_supabase_admin()
        supabase.table('exams').delete().eq('id', exam_id).eq('userid', user_id).execute()
        return True
    except:
        return False

# add a new exam
def add_exam(user_id, name, date):
    try:
        supabase = get_supabase_admin()
        supabase.table('exams').insert({
            'userid': user_id,
            'name': name,
            'date': date
        }).execute()
        return True
    except:
        return False

