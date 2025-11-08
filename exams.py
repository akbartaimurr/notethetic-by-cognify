from login import get_supabase_admin

# get all exams for this user bro
def get_exams(user_id):
    try:
        # connect to database thingy
        supabase = get_supabase_admin()
        # get all the exams where userid matches (found this on stackoverflow)
        result = supabase.table('exams').select('*').eq('userid', user_id).execute()
        # return the data part cuz that's where the actual stuff is
        return result.data
    except:
        # if something breaks just return empty list idk
        return []

# delete exam function BRO I CANT IMAGINE DOING ALLIS WITHOUT SUPABASE DOCS BAAHHAHAHAHAHAH JERRICKA BABY
def delete_exam(user_id, exam_id):
    try:
        # get database connection
        supabase = get_supabase_admin()
        # delete from exams table where id matches AND userid matches (gotta check both for security i think)
        supabase.table('exams').delete().eq('id', exam_id).eq('userid', user_id).execute()
        # return true if it worked
        return True
    except:
        # return false if something went wrong
        return False

# add new exam to database
def add_exam(user_id, name, date):
    try:
        # connect to supabase
        supabase = get_supabase_admin()
        # insert new row with all the data
        supabase.table('exams').insert({
            'userid': user_id,
            'name': name,
            'date': date
        }).execute()
        # return true if successful
        return True
    except:
        # return false if it failed for some reason
        return False

