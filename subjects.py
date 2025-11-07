from login import get_supabase_admin

# grab all subjects for a user
def get_subjects(user_id):
    try:
        supabase = get_supabase_admin()
        result = supabase.table('subjects').select('*').eq('userid', user_id).execute()
        # make sure id is an integer
        subjects = result.data
        for s in subjects:
            if 'id' in s:
                s['id'] = int(s['id'])
            if 'Id' in s:
                s['Id'] = int(s['Id'])
        return subjects
    except:
        return []

# add a subject for a user
def add_subject(user_id, subject_name):
    try:
        supabase = get_supabase_admin()
        supabase.table('subjects').insert({
            'userid': user_id,
            'subject': subject_name
        }).execute()
        return True
    except:
        return False
