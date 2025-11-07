import requests
import json

def generate_study_planner_api(subjects, hours_available, days_per_week, weeks_to_schedule, assignments):
    """
    Generate a personalized study planner using the external API
    
    Args:
        subjects: List of subject dictionaries with all columns
        hours_available: Available hours per day
        days_per_week: Days per week to study
        weeks_to_schedule: Planning period in weeks
        assignments: List of assignment dictionaries
    
    Returns:
        str: Formatted study planner text
    """
    try:
        # format subject data
        subject_time_data = []
        subject_id = 1
        for s in subjects:
            avg_time = s.get('averagetimeinminutes') or 60
            subject_time_data.append({
                "subjectId": subject_id,
                "averageTimeInMinutes": avg_time
            })
            subject_id += 1
        
        # format assignments as list of strings
        assignment_names = []
        for a in assignments:
            assignment_name = a.get('name', '')
            if assignment_name:
                assignment_names.append(assignment_name)
        
        # build request body
        request_data = {
            "subjectTimeData": subject_time_data,
            "hoursAvailablePerDay": hours_available,
            "daysPerWeek": days_per_week,
            "weeksToSchedule": weeks_to_schedule,
            "assignments": assignment_names
        }
        
        # send request to API
        # update this URL based on the actual endpoint from swagger docs
        api_url = "https://study-planner-api-n2ya.onrender.com/api/Ai/GenerateTimePlanner"
        
        response = requests.post(
            api_url,
            json=request_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # check if request was successful
        if response.status_code == 200:
            result = response.json()
            # return the planner text (adjust based on actual API response structure)
            return result.get('plannerText', result.get('planner_text', str(result)))
        else:
            return f"Error: API returned status code {response.status_code}. {response.text}"
        
    except requests.exceptions.RequestException as e:
        return f"Error connecting to API: {str(e)}"
    except Exception as e:
        return f"Error generating study planner: {str(e)}"

