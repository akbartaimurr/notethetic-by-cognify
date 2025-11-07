import requests

def generate_study_planner_api(subjects, hours_available=8, days_per_week=5, weeks_to_schedule=4, assignments=None):
    """
    Generate a personalized study planner using the external API.

    Args:
        subjects: List of subject dictionaries from the DB, must include 'Id' and optional 'AverageTimeInMinutes'.
        hours_available: Available hours per day.
        days_per_week: Days per week to study.
        weeks_to_schedule: Planning period in weeks.
        assignments: List of assignment dictionaries with 'name' key (optional).

    Returns:
        str: Formatted study planner text or error message.
    """
    try:
        if not subjects:
            return "Error: No subjects provided."

        # Build subjectTimeData with actual DB IDs
        # Each item needs: subjectId (int), averageTimeInMinutes (int)
        subject_time_data = []
        for s in subjects:
            subject_time_data.append({
                "subjectId": int(s['id']),
                "averageTimeInMinutes": int(s.get('averagetimeinminutes', 60))
            })

        # Build assignments list (up to 10, as API limits)
        assignment_names = []
        if assignments:
            for a in assignments[:10]:
                name = a.get("name", "").strip()
                if name:
                    assignment_names.append(name)

        request_data = {
            "SubjectTimeData": subject_time_data,  # List of {subjectId: int, averageTimeInMinutes: int}
            "HoursAvailablePerDay": int(hours_available),  # int
            "DaysPerWeek": int(days_per_week),  # int
            "WeeksToSchedule": int(weeks_to_schedule),  # int
            "Assignments": assignment_names  # List<string>
        }

        api_url = "https://study-planner-api-n2ya.onrender.com/api/Ai/GenerateTimePlanner"

        response = requests.post(
            api_url,
            json=request_data,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": "CbsmBuKrAydc7Ito9eQRfwzUYivlPxpS"
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            # The API returns 'studyPlanner' key in the response
            return result.get("studyPlanner", str(result))
        else:
            return f"Error: API returned status {response.status_code}: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Error connecting to API: {str(e)}"
    except Exception as e:
        return f"Error generating study planner: {str(e)}"
