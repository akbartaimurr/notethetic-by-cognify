from login import get_supabase_admin

# get user data from database
def get_user_data(user_id):
    try:
        supabase = get_supabase_admin()
        result = supabase.table('userdata').select('*').eq('userid', user_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
    except:
        pass
    return None # so like this makes sure that if the user data aint found it aint gon give nun

# update user data in database
def update_user_data(user_id, hours_available, days_per_week, weeks_to_schedule):
    try:
        supabase = get_supabase_admin()
        
        # delete old data
        supabase.table('userdata').delete().eq('userid', user_id).execute()
        
        # add new data
        supabase.table('userdata').insert({
            'userid': user_id,
            'hoursavailable': hours_available,
            'daysperweek': days_per_week,
            'weekstoschedule': weeks_to_schedule
        }).execute()
        
        return True
    except:
        return False
# omg stawppppp ittttt stawppppyyyyy omgogmgogmgomgogmgomg ik very good error handling 
