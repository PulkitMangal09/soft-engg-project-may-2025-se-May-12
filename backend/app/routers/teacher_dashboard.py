from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..config import supabase
from datetime  import datetime,timedelta
from ..models import JoinRequestAction
from collections import defaultdict

router = APIRouter(prefix="/teacher/dashboard", tags=["teacher-dashboard"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

# @router.get("/")
# def get_dashboard_summary(token: str = Depends(oauth2)):
#     # TODO: Query supabase for class stats, health alerts, pending tasks, class average
#     return {
#         "class": {"grade": "9A", "subject": "Financial Literacy", "students": 28},
#         "healthAlerts": {"urgent": 2},
#         "pendingTasks": {"awaitingReview": 15},
#         "classAverage": {"grade": "B+", "trend": "Improving"}
#     }
@router.get("/")
def get_dashboard_summary(token: str = Depends(oauth2)):
    # Get current teacher
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        return {"error": "Unauthorized"}
    teacher_id = user_response.user.id

    # Fetch students
    students_response = supabase.table("students").select("*").eq("assigned_teacher", teacher_id).execute()
    students = students_response.data or []
    student_ids = [s["student_id"] for s in students]

    # Class Info
    class_info = {
        "grade": students[0]["class_name"] if students else "N/A",
        "subject": students[0].get("subject", "Life Skills") if students else "N/A",
        "students": len(students)
    }

    # Health alerts (placeholder)
    health_alerts = {
        "urgent": 2
    }

    # Pending task completions
    completions_response = supabase.table("task_completions") \
        .select("*") \
        .in_("student_id", student_ids) \
        .is_("verified_by", "null") \
        .execute()
    pending_reviews = len(completions_response.data or [])

    # Class average grade
    scores_response = supabase.table("task_completions") \
        .select("score") \
        .in_("student_id", student_ids) \
        .not_("score", "is", None) \
        .execute()
    scores = [r["score"] for r in scores_response.data if r.get("score") is not None]
    average_score = sum(scores) / len(scores) if scores else 0
    grade = (
        "A+" if average_score >= 90 else
        "A" if average_score >= 80 else
        "B+" if average_score >= 70 else
        "B" if average_score >= 60 else
        "C" if average_score >= 50 else
        "D"
    )

    # Class Achievements (mock + logic)
    achievements = []

    # Example 1: Perfect task completion
    for s in students:
        student_id = s["student_id"]
        completions = supabase.table("task_completions") \
            .select("task_id, completed_on") \
            .eq("student_id", student_id) \
            .execute().data
        if completions and len(completions) >= 3:
            achievements.append(f"{s['name']}: Perfect task completion week")
            break

    # Example 2: Grade improvement
    improvements = supabase.table("task_completions") \
        .select("student_id, score, recorded_on") \
        .in_("student_id", student_ids) \
        .order("recorded_on", desc=False) \
        .execute().data

    score_by_student = {}
    for row in improvements:
        sid = row["student_id"]
        score = row["score"]
        if sid not in score_by_student:
            score_by_student[sid] = []
        score_by_student[sid].append(score)

    for sid, score_list in score_by_student.items():
        if len(score_list) >= 2 and score_list[-1] - score_list[0] >= 15:
            name = next((s["name"] for s in students if s["student_id"] == sid), None)
            achievements.append(f"{name}: Improved from C to A-")

    # Example 3: Class attendance
    attendance_resp = supabase.table("attendance") \
        .select("present") \
        .in_("student_id", student_ids) \
        .gte("date", "2025-07-15") \
        .execute().data

    present_days = sum([1 for r in attendance_resp if r.get("present")])
    total_days = len(attendance_resp)
    attendance_rate = round((present_days / total_days) * 100) if total_days else 0
    if attendance_rate >= 90:
        achievements.append(f"Class: {attendance_rate}% attendance this week")

    # Example 4: Overall improvement
    if average_score > 60:  # assume last month average was 52
        achievements.append("Overall: 15% improvement in grades")

    return {
        "class": class_info,
        "healthAlerts": health_alerts,
        "pendingTasks": {"awaitingReview": pending_reviews},
        "classAverage": {"grade": grade, "trend": "Improving" if average_score >= 70 else "Needs Work"},
        "classAchievements": achievements
    }


@router.get("/attention")
def get_students_requiring_attention(token: str = Depends(oauth2)):
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        return {"error": "Unauthorized"}
    teacher_id = user_response.user.id

    # Fetch students assigned to this teacher
    students_response = supabase.table("students").select("*").eq("assigned_teacher", teacher_id).execute()
    students = students_response.data or []
    student_ids = [s["student_id"] for s in students]

    attention_list = []
    today = datetime.utcnow()
    seven_days_ago = today - timedelta(days=7)

    for student in students:
        sid = student["student_id"]
        name = student["name"]

        # 1. Check for overdue tasks
        overdue_tasks = supabase.table("tasks") \
            .select("task_id") \
            .lt("due_date", today.isoformat()) \
            .execute().data or []

        overdue_task_ids = {t["task_id"] for t in overdue_tasks}

        completed_task_ids = supabase.table("task_completions") \
            .select("task_id") \
            .eq("student_id", sid) \
            .execute().data or []
        completed_ids = {c["task_id"] for c in completed_task_ids}

        student_overdue = overdue_task_ids - completed_ids

        if len(student_overdue) >= 3:
            attention_list.append({
                "name": name,
                "issue": f"{len(student_overdue)} overdue assignments",
                "student_id": sid
            })
            continue

        # 2. Check for falling behind in tasks (e.g. completed < 2 tasks in past 7 days)
        recent_tasks = supabase.table("task_completions") \
            .select("*") \
            .eq("student_id", sid) \
            .gte("completed_on", seven_days_ago.isoformat()) \
            .execute().data or []

        if len(recent_tasks) <= 1:
            attention_list.append({
                "name": name,
                "issue": "Falling behind in tasks",
                "student_id": sid
            })
            continue

        # 3. Low engagement (no completions in last 7 days)
        if not recent_tasks:
            attention_list.append({
                "name": name,
                "issue": "Low engagement this week",
                "student_id": sid
            })

    return {
        "studentsRequiringAttention": attention_list
    }

@router.get("/health-alerts")
def get_urgent_health_alerts(token: str = Depends(oauth2)):
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        return {"error": "Unauthorized"}
    teacher_id = user_response.user.id

    # Fetch students assigned to the teacher
    students_response = supabase.table("students").select("*").eq("assigned_teacher", teacher_id).execute()
    students = students_response.data or []
    student_ids = [s["student_id"] for s in students]

    alerts = []

    for student in students:
        sid = student["student_id"]
        name = student["name"]

        # 1. Recent health data
        health_response = supabase.table("health_data") \
            .select("*") \
            .eq("student_id", sid) \
            .order("timestamp", desc=True) \
            .limit(1) \
            .execute()

        if health_response.data:
            health_entry = health_response.data[0]
            if health_entry.get("metric") == "blood_sugar" and health_entry.get("value", 0) > 180:
                time_diff = datetime.utcnow() - datetime.fromisoformat(health_entry["timestamp"])
                minutes_ago = int(time_diff.total_seconds() // 60)
                alerts.append({
                    "name": name,
                    "alert": "High Blood Sugar",
                    "details": f"{health_entry['value']} mg/dL ({minutes_ago} min ago)",
                    "student_id": sid
                })

        # 2. Check for known plans (e.g., asthma)
        if "asthma" in (student.get("health_conditions") or "").lower():
            alerts.append({
                "name": name,
                "alert": "Asthma Action Plan",
                "details": "Reminder: Inhaler check needed",
                "student_id": sid
            })

    return {
        "urgentHealthAlerts": alerts
    }



@router.get("/join-requests")
def get_join_requests(token: str = Depends(oauth2)):
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        return {"error": "Unauthorized"}
    teacher_id = user_response.user.id

    response = supabase.table("student_join_requests") \
        .select("id, student_id, student(name, email, grade, section)") \
        .eq("teacher_id", teacher_id) \
        .eq("status", "pending") \
        .execute()

    return response.data or []


@router.post("/join-requests/respond")
def respond_to_join_request(data: JoinRequestAction, token: str = Depends(oauth2)):
    user_response = supabase.auth.get_user(token)
    if not user_response or not user_response.user:
        return {"error": "Unauthorized"}
    teacher_id = user_response.user.id

    # Get the join request
    req = supabase.table("student_join_requests") \
        .select("*") \
        .eq("student_id", data.student_id) \
        .eq("teacher_id", teacher_id) \
        .eq("status", "pending") \
        .maybe_single() \
        .execute()

    if not req.data:
        return {"error": "Join request not found or already processed"}

    if data.action == "accept":
        # Update student assigned_teacher
        supabase.table("students").update({"assigned_teacher": teacher_id}) \
            .eq("student_id", data.student_id).execute()

        # Mark request as accepted
        supabase.table("student_join_requests").update({"status": "accepted"}) \
            .eq("id", req.data["id"]).execute()
        return {"message": "Student accepted"}
    
    elif data.action == "reject":
        supabase.table("student_join_requests").update({"status": "rejected"}) \
            .eq("id", req.data["id"]).execute()
        return {"message": "Student rejected"}

    return {"error": "Invalid action"}

@router.get("/students")
def get_student_cards(token: str = Depends(oauth2)):
    user = supabase.auth.get_user(token).user
    teacher_id = user.id

    # Step 1: Get classes assigned to the teacher
    classes_resp = supabase.table("classes").select("class_id, grade").eq("teacher_id", teacher_id).execute()
    classes = classes_resp.data

    if not classes:
        return []

    class_ids = [c["class_id"] for c in classes]
    class_grade_map = {c["class_id"]: c["grade"] for c in classes}

    # Step 2: Get students in those classes
    student_resp = supabase.table("student_classes").select("student_id, class_id").in_("class_id", class_ids).execute()
    student_class_map = {s["student_id"]: s["class_id"] for s in student_resp.data}
    student_ids = list(student_class_map.keys())

    # Step 3: Get student info
    students_resp = supabase.table("students").select("student_id, name, avatar_url").in_("student_id", student_ids).execute()
    students = students_resp.data

    # Step 4: Get latest health data per student
    health_resp = supabase.table("health_data").select("student_id, condition, timestamp").in_("student_id", student_ids).order("timestamp", desc=True).execute()
    latest_health = {}
    for record in health_resp.data:
        sid = record["student_id"]
        if sid not in latest_health:
            latest_health[sid] = record["condition"]

    # Step 5: Get task completion stats
    completions_resp = supabase.table("task_completions").select("student_id, completed").in_("student_id", student_ids).execute()
    completion_stats = defaultdict(lambda: {"done": 0, "total": 0})
    for r in completions_resp.data:
        sid = r["student_id"]
        completion_stats[sid]["total"] += 1
        if r["completed"]:
            completion_stats[sid]["done"] += 1

    # Step 6: Prepare response
    response = []
    for student in students:
        sid = student["student_id"]
        total = completion_stats[sid]["total"]
        done = completion_stats[sid]["done"]
        completion_rate = round((done / total) * 100, 1) if total > 0 else 0

        response.append({
            "name": student["name"],
            "avatar_url": student["avatar_url"],
            "health_condition": latest_health.get(sid, "None"),
            "grade": class_grade_map.get(student_class_map.get(sid)),
            "task_completion_rate": completion_rate
        })

    return response

@router.get("/student/{student_id}/report")
def get_student_report(student_id: str, token: str = Depends(oauth2)):
    # Basic Info
    student_resp = supabase.table("students").select("*").eq("student_id", student_id).single().execute()
    student = student_resp.data
    if not student:
        return {"error": "Student not found"}

    # Health Summary (latest + last 7 days)
    now = datetime.utcnow()
    one_week_ago = now - timedelta(days=7)

    health_resp = supabase.table("health_data") \
        .select("condition, timestamp, value") \
        .eq("student_id", student_id) \
        .gte("timestamp", one_week_ago.isoformat()) \
        .order("timestamp", desc=True).execute()

    health_entries = health_resp.data
    latest_health = health_entries[0] if health_entries else {}

    # Recent Task Activity
    tasks_resp = supabase.table("task_completions") \
        .select("task_id, completed, timestamp") \
        .eq("student_id", student_id) \
        .order("timestamp", desc=True).limit(5).execute()
    
    recent_tasks = tasks_resp.data

    # Attendance (Optional if you track it)
    attendance_resp = supabase.table("attendance") \
        .select("date, status") \
        .eq("student_id", student_id) \
        .gte("date", one_week_ago.date().isoformat()) \
        .order("date", desc=True).execute()
    attendance_data = attendance_resp.data

    # Parent Info
    parent_resp = supabase.table("parents") \
        .select("name, phone, email, relation") \
        .eq("student_id", student_id).execute()
    parents = parent_resp.data

    # Academic Performance
    grades_resp = supabase.table("grades") \
        .select("subject, grade, previous_grade, updated_at") \
        .eq("student_id", student_id) \
        .order("updated_at", desc=True).execute()
    grades = grades_resp.data

    return {
        "basicInfo": {
            "name": student["name"],
            "avatar_url": student["avatar_url"],
            "dob": student.get("dob"),
            "email": student.get("email"),
            "class": student.get("class"),
        },
        "healthSummary": {
            "latest": latest_health,
            "last7Days": health_entries
        },
        "recentActivity": {
            "tasks": recent_tasks,
            "attendance": attendance_data
        },
        "parentInfo": parents,
        "academicPerformance": grades
    }