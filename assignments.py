from login import get_supabase_admin

def get_assignments(user_id):
    try:
        supabase = get_supabase_admin()
        result = supabase.table('assignments').select('*').eq('userid', user_id).execute()
        return result.data
    except:
        return []

def mark_assignment_done(user_id, assignment_id):
    try:
        supabase = get_supabase_admin()
        supabase.table('assignments').update({'status': 'completed'}).eq('id', assignment_id).eq('userid', user_id).execute()
        return True
    except:
        return False

def add_assignment(user_id, name, due, status):
    try:
        supabase = get_supabase_admin()
        supabase.table('assignments').insert({
            'userid': user_id,
            'name': name,
            'due': due,
            'status': status
        }).execute()
        return True
    except:
        return False

def delete_assignment(user_id, assignment_id):
    try:
        supabase = get_supabase_admin()
        supabase.table('assignments').delete().eq('id', assignment_id).eq('userid', user_id).execute()
        return True
    except:
        return False
