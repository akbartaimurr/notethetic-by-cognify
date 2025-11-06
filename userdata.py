from login import get_supabase_admin

# get user data
def get_user_data(user_id):
    try:
        supabase = get_supabase_admin()
        result = supabase.table('userdata').select('*').eq('userid', user_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
    except:
        pass
    return None

