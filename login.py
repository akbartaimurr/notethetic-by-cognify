import os
from supabase import create_client
from dotenv import load_dotenv


load_dotenv()


SUPABASE_URL = os.getenv('SUPABASE_URL', 'your-supabase-url')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'your-supabase-key')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', os.getenv('SUPABASE_KEY', 'your-supabase-key'))


def get_supabase():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase


def get_supabase_admin():
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return supabase


def get_google_login_url():
    supabase = get_supabase()
    redirect_url = os.getenv('REDIRECT_URL', 'http://localhost:3000/signin')
    result = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": redirect_url
        }
    })
    return result.url

# log em out
def logout_user():
    supabase = get_supabase()
    supabase.auth.sign_out()
