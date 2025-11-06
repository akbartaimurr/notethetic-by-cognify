from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def generate_study_planner(subjects, total_time_per_day, hours_available, days_per_week, weeks_to_schedule=4):
    """
    Generate a personalized study planner using OpenAI ChatGPT
    
    Args:
        subjects: List of subject dictionaries with all columns
        total_time_per_day: Total study time needed per cycle in minutes
        hours_available: Available hours per day
        days_per_week: Days per week to study
        weeks_to_schedule: Planning period in weeks (default 4)
    
    Returns:
        str: Formatted study planner text
    """
    try:
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Error: OPENAI_API_KEY not found in environment variables"
        
        client = OpenAI(api_key=api_key)
        
        # Build subject list - send all subject data
        subject_list = "\n".join([f"- {s.get('subject', 'Unknown Subject')}: {s.get('averagetimeinminutes', 60)} minutes per session" for s in subjects])
        
        # Build the prompt exactly like C# version
        prompt = f"Create a personalized study planner based on the following subject time requirements:\n\n" + \
                f"{subject_list}\n\n" + \
                f"Total study time needed per cycle: {total_time_per_day} minutes ({total_time_per_day / 60.0:.1f} hours)\n" + \
                f"Available hours per day: {hours_available}\n" + \
                f"Days per week: {days_per_week}\n" + \
                f"Planning period: {weeks_to_schedule} weeks\n\n" + \
                f"Generate a realistic and balanced study schedule that:\n" + \
                f"1. Distributes study time effectively across all subjects\n" + \
                f"2. Accounts for the time each subject requires\n" + \
                f"3. Includes breaks and prevents burnout\n" + \
                f"4. Suggests optimal times for different subjects based on complexity\n" + \
                f"5. Provides daily and weekly study breakdowns\n\n" + \
                f"IMPORTANT: Do NOT use markdown formatting (no **, ##, *, etc.). Instead, use separation lines (━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━) and LOTS of emojis throughout your response. Make it visually appealing with emojis for subjects, time slots, breaks, and activities."

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful study planner assistant that creates detailed, personalized study schedules."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating study planner: {str(e)}"

