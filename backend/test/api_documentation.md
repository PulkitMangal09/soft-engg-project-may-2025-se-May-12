# API Documentation

## Table of Contents
- [Auth](#auth)
- [Health](#health)
- [Parent](#parent)
- [Parent-dashboard](#parent-dashboard)
- [Parent-family](#parent-family)
- [Parent-requests](#parent-requests)
- [Parent-tasks](#parent-tasks)
- [Roles](#roles)
- [Student-dashboard](#student-dashboard)
- [Student-emotions](#student-emotions)
- [Student-finance](#student-finance)
- [Student-profile](#student-profile)
- [Student-tasks](#student-tasks)
- [Teacher-dashboard](#teacher-dashboard)
- [Teacher-reports](#teacher-reports)
- [Teacher-students](#teacher-students)
- [Teacher-tasks](#teacher-tasks)
- [Uncategorized](#uncategorized)
- [Users](#users)

## Auth

### `POST /auth/signup`
**Signup**

- **Operation ID:** `signup_auth_signup_post`
- **Request Body:**
  - `application/json`: SignupRequest

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `POST /auth/token`
**Login**

- **Operation ID:** `login_auth_token_post`
- **Request Body:**
  - `application/x-www-form-urlencoded`: Body_login_auth_token_post

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Users

### `GET /users/profile`
**Profile**

- **Operation ID:** `profile_users_profile_get`
- **Responses:**
  - `200`: Successful Response

---

## Roles

### `GET /roles/`
**Get Roles**

- **Operation ID:** `get_roles_roles__get`
- **Responses:**
  - `200`: Successful Response

---

## Teacher-dashboard

### `GET /teacher/dashboard/`
**Get Dashboard Summary**

- **Operation ID:** `get_dashboard_summary_teacher_dashboard__get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /teacher/dashboard/attention`
**Get Students Requiring Attention**

- **Operation ID:** `get_students_requiring_attention_teacher_dashboard_attention_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /teacher/dashboard/health-alerts`
**Get Urgent Health Alerts**

- **Operation ID:** `get_urgent_health_alerts_teacher_dashboard_health_alerts_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /teacher/dashboard/join-requests`
**Get Join Requests**

- **Operation ID:** `get_join_requests_teacher_dashboard_join_requests_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /teacher/dashboard/join-requests/respond`
**Respond To Join Request**

- **Operation ID:** `respond_to_join_request_teacher_dashboard_join_requests_respond_post`
- **Request Body:**
  - `application/json`: JoinRequestAction

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /teacher/dashboard/students`
**Get Student Cards**

- **Operation ID:** `get_student_cards_teacher_dashboard_students_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /teacher/dashboard/student/{student_id}/report`
**Get Student Report**

- **Operation ID:** `get_student_report_teacher_dashboard_student__student_id__report_get`
- **Parameters:**
  - `student_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Teacher-students

### `GET /teacher/classrooms`
**List Classrooms**

List all classrooms owned by this teacher.

- **Operation ID:** `list_classrooms_teacher_classrooms_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /teacher/classrooms/{classroom_id}/students`
**List Classroom Students**

List all students in a given classroom.

- **Operation ID:** `list_classroom_students_teacher_classrooms__classroom_id__students_get`
- **Parameters:**
  - `classroom_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `POST /teacher/classrooms/{classroom_id}/students/{student_id}`
**Add Student To Class**

Enroll a student into a classroom.

- **Operation ID:** `add_student_to_class_teacher_classrooms__classroom_id__students__student_id__post`
- **Parameters:**
  - `classroom_id` (path, required, string): 
  - `student_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /teacher/classrooms/{classroom_id}/students/{student_id}`
**Remove Student From Class**

Remove a student from a classroom.

- **Operation ID:** `remove_student_from_class_teacher_classrooms__classroom_id__students__student_id__delete`
- **Parameters:**
  - `classroom_id` (path, required, string): 
  - `student_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /teacher/students/metrics`
**Students Metrics**

Return for each student across all this teacher's classrooms:
  - total tasks assigned & completed
  - overdue count
  - health alert count
  - average grade (if you have a grades table)

- **Operation ID:** `students_metrics_teacher_students_metrics_get`
- **Responses:**
  - `200`: Successful Response

---

## Teacher-tasks

### `GET /teacher/tasks/summary`
**Get Tasks Summary**

- **Operation ID:** `get_tasks_summary_teacher_tasks_summary_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /teacher/tasks/recent`
**Recent Tasks**

- **Operation ID:** `recent_tasks_teacher_tasks_recent_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /teacher/tasks/overdue`
**Overdue Tasks**

- **Operation ID:** `overdue_tasks_teacher_tasks_overdue_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /teacher/tasks/`
**Get All Tasks**

- **Operation ID:** `get_all_tasks_teacher_tasks__get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /teacher/tasks/`
**Create Task**

- **Operation ID:** `create_task_teacher_tasks__post`
- **Request Body:**
  - `application/json`: TaskCreate

- **Responses:**
  - `201`: Successful Response
  - `422`: Validation Error

---

### `GET /teacher/tasks/{task_id}`
**Get Task**

- **Operation ID:** `get_task_teacher_tasks__task_id__get`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PUT /teacher/tasks/{task_id}`
**Update Task**

- **Operation ID:** `update_task_teacher_tasks__task_id__put`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Request Body:**
  - `application/json`: TaskUpdate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /teacher/tasks/{task_id}`
**Delete Task**

- **Operation ID:** `delete_task_teacher_tasks__task_id__delete`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Teacher-reports

### `GET /teacher/reports/{student_id}`
**Student Report**

- **Operation ID:** `student_report_teacher_reports__student_id__get`
- **Parameters:**
  - `student_id` (path, required, string): The UUID of the student

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Student-dashboard

### `GET /student/dashboard/`
**Get Student Dashboard**

Return overview cards for student dashboard (tasks, finance, emotions, diet, health).

- **Operation ID:** `get_student_dashboard_student_dashboard__get`
- **Responses:**
  - `200`: Successful Response

---

## Student-tasks

### `GET /student/tasks/`
**List Tasks**

List all tasks assigned to the authenticated student.

- **Operation ID:** `list_tasks_student_tasks__get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /student/tasks/`
**Add Task**

Add a new task for the authenticated student.

- **Operation ID:** `add_task_student_tasks__post`
- **Request Body:**
  - `application/json`: TaskCreate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/tasks/{task_id}`
**Get Task**

Retrieve a specific task by ID for the authenticated student.

- **Operation ID:** `get_task_student_tasks__task_id__get`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /student/tasks/{task_id}`
**Update Task**

Update an existing task if it's not completed.

- **Operation ID:** `update_task_student_tasks__task_id__patch`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Request Body:**
  - `application/json`: TaskCreate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /student/tasks/{task_id}`
**Delete Task**

Delete a task by ID for the authenticated student.

- **Operation ID:** `delete_task_student_tasks__task_id__delete`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Student-finance

### `GET /student/finance/transactions`
**List Transactions**

- **Operation ID:** `list_transactions_student_finance_transactions_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /student/finance/transactions`
**Add Transaction**

- **Operation ID:** `add_transaction_student_finance_transactions_post`
- **Request Body:**
  - `application/json`: TransactionCreate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/finance/dashboard`
**Get Finance Dashboard**

- **Operation ID:** `get_finance_dashboard_student_finance_dashboard_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /student/finance/savings-goals`
**List Savings Goals**

- **Operation ID:** `list_savings_goals_student_finance_savings_goals_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /student/finance/savings-goals`
**Create Savings Goal**

- **Operation ID:** `create_savings_goal_student_finance_savings_goals_post`
- **Request Body:**
  - `application/json`: SavingsGoalCreate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/finance/savings-goals/{goal_id}`
**Get Savings Goal**

- **Operation ID:** `get_savings_goal_student_finance_savings_goals__goal_id__get`
- **Parameters:**
  - `goal_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /student/finance/savings-goals/{goal_id}`
**Update Savings Goal**

- **Operation ID:** `update_savings_goal_student_finance_savings_goals__goal_id__patch`
- **Parameters:**
  - `goal_id` (path, required, string): 

- **Request Body:**
  - `application/json`: SavingsGoalCreate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /student/finance/savings-goals/{goal_id}`
**Delete Savings Goal**

- **Operation ID:** `delete_savings_goal_student_finance_savings_goals__goal_id__delete`
- **Parameters:**
  - `goal_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Student-emotions

### `GET /student/emotions/entries`
**List Emotional Entries**

- **Operation ID:** `list_emotional_entries_student_emotions_entries_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /student/emotions/entries`
**Create Emotional Entry**

- **Operation ID:** `create_emotional_entry_student_emotions_entries_post`
- **Request Body:**
  - `application/json`: EmotionalEntry

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/entries/{entry_id}`
**Get Emotional Entry**

- **Operation ID:** `get_emotional_entry_student_emotions_entries__entry_id__get`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /student/emotions/entries/{entry_id}`
**Update Emotional Entry**

- **Operation ID:** `update_emotional_entry_student_emotions_entries__entry_id__patch`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Request Body:**
  - `application/json`: EmotionalEntry

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /student/emotions/entries/{entry_id}`
**Delete Emotional Entry**

- **Operation ID:** `delete_emotional_entry_student_emotions_entries__entry_id__delete`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/mood-logs`
**List Mood Logs**

- **Operation ID:** `list_mood_logs_student_emotions_mood_logs_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /student/emotions/mood-logs`
**Create Mood Log**

- **Operation ID:** `create_mood_log_student_emotions_mood_logs_post`
- **Request Body:**
  - `application/json`: MoodLog

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/mood-logs/{log_id}`
**Get Mood Log**

- **Operation ID:** `get_mood_log_student_emotions_mood_logs__log_id__get`
- **Parameters:**
  - `log_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /student/emotions/mood-logs/{log_id}`
**Update Mood Log**

- **Operation ID:** `update_mood_log_student_emotions_mood_logs__log_id__patch`
- **Parameters:**
  - `log_id` (path, required, string): 

- **Request Body:**
  - `application/json`: MoodLog

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /student/emotions/mood-logs/{log_id}`
**Delete Mood Log**

- **Operation ID:** `delete_mood_log_student_emotions_mood_logs__log_id__delete`
- **Parameters:**
  - `log_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/sessions`
**List Chat Sessions**

- **Operation ID:** `list_chat_sessions_student_emotions_sessions_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /student/emotions/sessions`
**Create Chat Session**

- **Operation ID:** `create_chat_session_student_emotions_sessions_post`
- **Request Body:**
  - `application/json`: ChatSession

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/sessions/{session_id}`
**Get Chat Session**

- **Operation ID:** `get_chat_session_student_emotions_sessions__session_id__get`
- **Parameters:**
  - `session_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /student/emotions/sessions/{session_id}`
**Update Chat Session**

- **Operation ID:** `update_chat_session_student_emotions_sessions__session_id__patch`
- **Parameters:**
  - `session_id` (path, required, string): 

- **Request Body:**
  - `application/json`: ChatSession

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /student/emotions/sessions/{session_id}`
**Delete Chat Session**

- **Operation ID:** `delete_chat_session_student_emotions_sessions__session_id__delete`
- **Parameters:**
  - `session_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `POST /student/emotions/messages`
**Create Chat Message**

- **Operation ID:** `create_chat_message_student_emotions_messages_post`
- **Request Body:**
  - `application/json`: ChatMessage

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/messages/{session_id}`
**List Chat Messages**

- **Operation ID:** `list_chat_messages_student_emotions_messages__session_id__get`
- **Parameters:**
  - `session_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/message/{message_id}`
**Get Chat Message**

- **Operation ID:** `get_chat_message_student_emotions_message__message_id__get`
- **Parameters:**
  - `message_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /student/emotions/message/{message_id}`
**Update Chat Message**

- **Operation ID:** `update_chat_message_student_emotions_message__message_id__patch`
- **Parameters:**
  - `message_id` (path, required, string): 

- **Request Body:**
  - `application/json`: ChatMessage

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /student/emotions/message/{message_id}`
**Delete Chat Message**

- **Operation ID:** `delete_chat_message_student_emotions_message__message_id__delete`
- **Parameters:**
  - `message_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/contacts`
**List Emergency Contacts**

- **Operation ID:** `list_emergency_contacts_student_emotions_contacts_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /student/emotions/contacts`
**Create Emergency Contact**

- **Operation ID:** `create_emergency_contact_student_emotions_contacts_post`
- **Request Body:**
  - `application/json`: EmergencyContact

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /student/emotions/contacts/{contact_id}`
**Get Emergency Contact**

- **Operation ID:** `get_emergency_contact_student_emotions_contacts__contact_id__get`
- **Parameters:**
  - `contact_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /student/emotions/contacts/{contact_id}`
**Update Emergency Contact**

- **Operation ID:** `update_emergency_contact_student_emotions_contacts__contact_id__patch`
- **Parameters:**
  - `contact_id` (path, required, string): 

- **Request Body:**
  - `application/json`: EmergencyContact

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /student/emotions/contacts/{contact_id}`
**Delete Emergency Contact**

- **Operation ID:** `delete_emergency_contact_student_emotions_contacts__contact_id__delete`
- **Parameters:**
  - `contact_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `POST /student/emotions/sessions/{session_id}/auto-reply`
**Auto Reply**

- **Operation ID:** `auto_reply_student_emotions_sessions__session_id__auto_reply_post`
- **Parameters:**
  - `session_id` (path, required, string): 

- **Request Body:**
  - `application/json`: Body_auto_reply_student_emotions_sessions__session_id__auto_reply_post

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Health

### `GET /health/student_diet`
**Get Diet Logs**

- **Operation ID:** `get_diet_logs_health_student_diet_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /health/student_diet`
**Log Student Diet**

- **Operation ID:** `log_student_diet_health_student_diet_post`
- **Request Body:**
  - `application/json`: DietEntry

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /health/student_diet/{entry_id}`
**Update Diet Entry**

- **Operation ID:** `update_diet_entry_health_student_diet__entry_id__patch`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Request Body:**
  - `application/json`: DietEntry

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /health/student_diet/{entry_id}`
**Delete Diet Entry**

- **Operation ID:** `delete_diet_entry_health_student_diet__entry_id__delete`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /health/meals`
**Get Meal Logs**

- **Operation ID:** `get_meal_logs_health_meals_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /health/meals`
**Log Meal**

- **Operation ID:** `log_meal_health_meals_post`
- **Request Body:**
  - `application/json`: MealEntry

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /health/meals/{entry_id}`
**Update Meal Entry**

- **Operation ID:** `update_meal_entry_health_meals__entry_id__patch`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Request Body:**
  - `application/json`: MealEntry

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /health/meals/{entry_id}`
**Delete Meal Entry**

- **Operation ID:** `delete_meal_entry_health_meals__entry_id__delete`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /health/metrics`
**Get Latest Metrics**

- **Operation ID:** `get_latest_metrics_health_metrics_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /health/metrics`
**Add Health Metrics**

- **Operation ID:** `add_health_metrics_health_metrics_post`
- **Request Body:**
  - `application/json`: HealthMetricsRequest

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /health/metrics/{entry_id}`
**Update Health Metrics**

- **Operation ID:** `update_health_metrics_health_metrics__entry_id__patch`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Request Body:**
  - `application/json`: HealthMetricsRequest

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /health/metrics/{entry_id}`
**Delete Health Metrics**

- **Operation ID:** `delete_health_metrics_health_metrics__entry_id__delete`
- **Parameters:**
  - `entry_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /health/analytics`
**Get Analytics**

- **Operation ID:** `get_analytics_health_analytics_get`
- **Responses:**
  - `200`: Successful Response

---

## Parent-dashboard

### `GET /parent/dashboard/`
**Get Parent Dashboard**

Aggregated parent dashboard endpoint. Returns summary, children, alerts, attention, achievements.
If child_id is provided, filters all metrics for that child only.

- **Operation ID:** `get_parent_dashboard_parent_dashboard__get`
- **Parameters:**
  - `child_id` (query, optional, unknown): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/dashboard/tasks`
**Get Parent Tasks**

Returns all tasks for the parent's children, with optional filtering by status, child_id, and sorting.

- **Operation ID:** `get_parent_tasks_parent_dashboard_tasks_get`
- **Parameters:**
  - `status` (query, optional, unknown): 
  - `child_id` (query, optional, unknown): 
  - `sortBy` (query, optional, unknown): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/dashboard/health/alerts`
**Get Parent Health Alerts**

Returns all active health alerts for the parent's children, with optional filtering by severity and child_id.

- **Operation ID:** `get_parent_health_alerts_parent_dashboard_health_alerts_get`
- **Parameters:**
  - `severity` (query, optional, unknown): 
  - `child_id` (query, optional, unknown): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/dashboard/finance/goals`
**Get Parent Finance Goals**

Returns all savings goals for the parent's children, with optional filtering by status and child_id.

- **Operation ID:** `get_parent_finance_goals_parent_dashboard_finance_goals_get`
- **Parameters:**
  - `status` (query, optional, unknown): 
  - `child_id` (query, optional, unknown): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/dashboard/family/join-requests`
**Get Family Join Requests**

Returns a list of pending join requests to the family group.

- **Operation ID:** `get_family_join_requests_parent_dashboard_family_join_requests_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /parent/dashboard/family/join-requests/respond`
**Respond Family Join Request**

Accept or reject a join request. Body: { "request_id": "<uuid>", "action": "accept" | "reject" }

- **Operation ID:** `respond_family_join_request_parent_dashboard_family_join_requests_respond_post`
- **Request Body:**
  - `application/json`: 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Parent

### `GET /parent/children/metrics`
**View All Children Metrics**

- **Operation ID:** `view_all_children_metrics_parent_children_metrics_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /parent/children`
**Get Children**

- **Operation ID:** `get_children_parent_children_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /parent/children/add`
**Add Child**

- **Operation ID:** `add_child_parent_children_add_post`
- **Request Body:**
  - `application/json`: ChildLinkRequest

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /parent/children/remove`
**Remove Child**

- **Operation ID:** `remove_child_parent_children_remove_delete`
- **Parameters:**
  - `child_id` (query, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PATCH /parent/children/relationship`
**Update Child Relationship**

- **Operation ID:** `update_child_relationship_parent_children_relationship_patch`
- **Request Body:**
  - `application/json`: UpdateChildLink

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/children/search`
**Search Child**

- **Operation ID:** `search_child_parent_children_search_get`
- **Parameters:**
  - `email` (query, optional, unknown): 
  - `student_id` (query, optional, unknown): 
  - `name` (query, optional, unknown): 
  - `school_name` (query, optional, unknown): 
  - `grade_level` (query, optional, unknown): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/other-parents`
**View Other Parents**

- **Operation ID:** `view_other_parents_parent_other_parents_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /parent/child/health`
**Get Child Health Data**

- **Operation ID:** `get_child_health_data_parent_child_health_get`
- **Parameters:**
  - `child_id` (query, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/children/diet`
**View Children Diet**

- **Operation ID:** `view_children_diet_parent_children_diet_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /parent/child/meals`
**Get Child Meal Logs**

- **Operation ID:** `get_child_meal_logs_parent_child_meals_get`
- **Parameters:**
  - `child_id` (query, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Parent-requests

### `GET /parent/requests/`
**List Requests**

List all pending 'family' join requests for families this user heads.

- **Operation ID:** `list_requests_parent_requests__get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /parent/requests/{request_id}/approve`
**Approve Request**

Approve a pending family-join request.

- **Operation ID:** `approve_request_parent_requests__request_id__approve_post`
- **Parameters:**
  - `request_id` (path, required, string): The join_request ID to approve

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `POST /parent/requests/{request_id}/reject`
**Reject Request**

Reject a pending family-join request.

- **Operation ID:** `reject_request_parent_requests__request_id__reject_post`
- **Parameters:**
  - `request_id` (path, required, string): The join_request ID to reject

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Parent-tasks

### `GET /parent/tasks/summary`
**Get Tasks Summary**

- **Operation ID:** `get_tasks_summary_parent_tasks_summary_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /parent/tasks/recent`
**Recent Tasks**

- **Operation ID:** `recent_tasks_parent_tasks_recent_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /parent/tasks/overdue`
**Overdue Tasks**

- **Operation ID:** `overdue_tasks_parent_tasks_overdue_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /parent/tasks/`
**Get All Tasks**

- **Operation ID:** `get_all_tasks_parent_tasks__get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /parent/tasks/`
**Create Task**

- **Operation ID:** `create_task_parent_tasks__post`
- **Request Body:**
  - `application/json`: TaskCreate

- **Responses:**
  - `201`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/tasks/{task_id}`
**Get Task**

- **Operation ID:** `get_task_parent_tasks__task_id__get`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `PUT /parent/tasks/{task_id}`
**Update Task**

- **Operation ID:** `update_task_parent_tasks__task_id__put`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Request Body:**
  - `application/json`: TaskUpdate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /parent/tasks/{task_id}`
**Delete Task**

- **Operation ID:** `delete_task_parent_tasks__task_id__delete`
- **Parameters:**
  - `task_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Parent-family

### `GET /parent/family/overview`
**Family Overview**

Return summary cards for tasks, finance, health across family.

- **Operation ID:** `family_overview_parent_family_overview_get`
- **Responses:**
  - `200`: Successful Response

---

### `GET /parent/family/groups`
**List Family Groups**

List all family groups you head.

- **Operation ID:** `list_family_groups_parent_family_groups_get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /parent/family/groups`
**Create Family Group**

Create a new family group (you become the head).

- **Operation ID:** `create_family_group_parent_family_groups_post`
- **Request Body:**
  - `application/json`: Body_create_family_group_parent_family_groups_post

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `GET /parent/family/groups/{group_id}`
**Get Family Group**

Get details (and members) of a single family group.

- **Operation ID:** `get_family_group_parent_family_groups__group_id__get`
- **Parameters:**
  - `group_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `POST /parent/family/groups/{group_id}/add/{child_id}`
**Add Family Member**

Add a child (or guardian) to your family group.

- **Operation ID:** `add_family_member_parent_family_groups__group_id__add__child_id__post`
- **Parameters:**
  - `group_id` (path, required, string): 
  - `child_id` (path, required, string): 

- **Request Body:**
  - `application/json`: Body_add_family_member_parent_family_groups__group_id__add__child_id__post

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /parent/family/groups/{group_id}/remove/{child_id}`
**Remove Family Member**

Remove a member from your family group.

- **Operation ID:** `remove_family_member_parent_family_groups__group_id__remove__child_id__delete`
- **Parameters:**
  - `group_id` (path, required, string): 
  - `child_id` (path, required, string): 

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Student-profile

### `GET /student/profile/`
**Get Profile**

Get the authenticated student's profile.

- **Operation ID:** `get_profile_student_profile__get`
- **Responses:**
  - `200`: Successful Response

---

### `POST /student/profile/`
**Create Profile**

Create initial student profile stub (if not existing).

- **Operation ID:** `create_profile_student_profile__post`
- **Request Body:**
  - `application/json`: StudentProfileUpdate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

### `DELETE /student/profile/`
**Delete Profile**

Delete the authenticated student's profile.

- **Operation ID:** `delete_profile_student_profile__delete`
- **Responses:**
  - `200`: Successful Response

---

### `PATCH /student/profile/`
**Update Profile**

Update the authenticated student's profile.

- **Operation ID:** `update_profile_student_profile__patch`
- **Request Body:**
  - `application/json`: StudentProfileUpdate

- **Responses:**
  - `200`: Successful Response
  - `422`: Validation Error

---

## Uncategorized

### `GET /`
**Read Root**

- **Operation ID:** `read_root__get`
- **Responses:**
  - `200`: Successful Response

---

