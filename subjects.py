from login import get_supabase_admin

# get all subjects for this user (copied from exams.py lol)
def get_subjects(user_id):
    try:
        # connect to database
        supabase = get_supabase_admin()
        # select everything from subjects table where userid matches
        result = supabase.table('subjects').select('*').eq('userid', user_id).execute()
        # return just the data part
        return result.data
    except:
        # if error happens return empty list
        return []

# add new subject to database
def add_subject(user_id, subject_name):
    try:
        # get database connection
        supabase = get_supabase_admin()
        # insert new subject with userid and subject name
        supabase.table('subjects').insert({
            'userid': user_id,
            'subject': subject_name
        }).execute()
        # return true if it worked
        return True
    except:
        # return false if something went wrong
        return False

# delete subject from database
def delete_subject(user_id, subject_id):
    try:
        # get database connection
        supabase = get_supabase_admin()
        # delete subject where id matches and userid matches (for security)
        supabase.table('subjects').delete().eq('id', subject_id).eq('userid', user_id).execute()
        # return true if it worked
        return True
    except:
        # return false if something went wrong
        return False
