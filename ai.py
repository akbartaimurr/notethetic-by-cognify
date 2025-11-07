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
        subject_time_data = []
        for s in subjects:
            # get id from either 'Id' or 'id' field
            subject_id = s.get("Id") or s.get("id")
            if subject_id is None:
                return f"Error: Subject missing 'Id' or 'id' field: {s}"
            # make sure it's an integer
            subject_id = int(subject_id)
            # get average time from either 'AverageTimeInMinutes' or 'averagetimeinminutes'
            avg_time = s.get("AverageTimeInMinutes") or s.get("averagetimeinminutes") or 60
            avg_time = int(avg_time)
            subject_time_data.append({
                "subjectId": subject_id,
                "averageTimeInMinutes": avg_time
            })

        # Build assignments list (up to 10, as API limits)
        assignment_names = []
        if assignments:
            for a in assignments[:10]:
                name = a.get("name", "").strip()
                if name:
                    assignment_names.append(name)

        request_data = {
            "subjectTimeData": subject_time_data,
            "hoursAvailablePerDay": hours_available,
            "daysPerWeek": days_per_week,
            "weeksToSchedule": weeks_to_schedule,
            "assignments": assignment_names
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
