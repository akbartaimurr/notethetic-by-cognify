import requests

def generate_study_planner_api(subjects, hours_available, days_per_week, weeks_to_schedule, assignments):
    try:
        # make list of subjects for api
        subject_list = []
        for subject in subjects:
            subject_list.append({
                "subjectId": subject['id'],
                "averageTimeInMinutes": subject.get('averagetimeinminutes', 60)
            })

        # make list of assignment names
        assignment_list = []
        if assignments:
            for assignment in assignments[:10]:
                assignment_list.append(assignment['name'])

        # data to send to api
        data = {
            "subjectTimeData": subject_list,
            "hoursAvailablePerDay": hours_available,
            "daysPerWeek": days_per_week,
            "weeksToSchedule": weeks_to_schedule,
            "assignments": assignment_list
        }

        # send request to api
        url = "https://study-planner-api-wes0.onrender.com/api/Ai/GenerateTimePlanner"
        response = requests.post(url, json=data, headers={"Content-Type": "application/json", "X-API-Key": "CbsmBuKrAydc7Ito9eQRfwzUYivlPxpS"})

        # get the planner text
        result = response.json()
        return result["studyPlanner"]

    except:
        return "Error"

def aria_ai_chat(message):
    try:
        url = "https://study-planner-api-wes0.onrender.com/api/Ai/chat"
        r = requests.post(url, json={"message": message}, headers={"Content-Type": "application/json", "X-API-Key": "CbsmBuKrAydc7Ito9eQRfwzUYivlPxpS"})
        return r.json().get("response", "Error")
    except:
        return "Error"