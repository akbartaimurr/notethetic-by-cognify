from login import get_supabase_admin

# update user data
def update_user_data(user_id, hours_available, days_per_week, weeks_to_schedule):
    try:
        supabase = get_supabase_admin()
        
        # Delete existing and insert new
        supabase.table('userdata').delete().eq('userid', user_id).execute()
        
        supabase.table('userdata').insert({
            'userid': user_id,
            'hoursavailable': hours_available,
            'daysperweek': days_per_week,
            'weekstoschedule': weeks_to_schedule
        }).execute()
        
        return True
    except Exception as e:
        print(f"Error updating user data: {e}")
        return False

