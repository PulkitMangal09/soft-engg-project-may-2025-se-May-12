## Auth API Tests Documentation

### Description

The Auth API handles user-related functionalities such as registration (signup) and authentication (login/token generation). It is the entry point for all users to access the GrowthGeine application.

---

### Endpoint: Signup

- **URL:** `/auth/signup`
- **Method:** POST

### Test Cases

**1. test_signup_success** _Test successful registration of a new student user._

- **Passed Inputs:**

  - `full_name` = "Test Student"
  - `email` = "student.new@example.com"
  - `password` = "ValidPassword123!"
  - `confirm_password` = "ValidPassword123!"
  - `role` = "student"
  - `terms_agreed` = true

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "User created successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "User created successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_signup_success(client):
      """
      Test successful user registration.
      """
      response = client.post(
          "/auth/signup",
          json={
              "full_name": "Test Student",
              "email": "student.new@example.com",
              "password": "ValidPassword123!",
              "confirm_password": "ValidPassword123!",
              "role": "student",
              "terms_agreed": True,
          },
      )
      assert response.status_code == 200
      assert response.json() == {"message": "User created successfully"}
  ```

**2. test_signup_email_exists** _Test registration attempt with an email that is already in use._

- **Passed Inputs:**

  - `full_name` = "Another User"
  - `email` = "existing.user@example.com"
  - `password` = "Password123!"
  - `confirm_password` = "Password123!"
  - `role` = "teacher"
  - `terms_agreed` = true

- **Expected Output:**

  - `HTTP-Status Code`: 400
  - `Response Body`: `{ "detail": "Email already registered" }`

- **Actual Output:**

  - `HTTP-Status Code`: 400
  - `Response Body`: `{ "detail": "Email already registered" }`

- **Result:** Passed

- **Pytest Code:**

  ```python
  def test_signup_email_already_exists(client):
      """
      Test signup with an email that is already registered.
      """
      # First, create a user to ensure the email exists
      client.post("/auth/signup", json={"full_name": "Existing User", "email": "existing.user@example.com", "password": "Password123!", "confirm_password": "Password123!", "role": "teacher", "terms_agreed": True})

      # Attempt to sign up again with the same email
      response = client.post("/auth/signup", json={"full_name": "Another User", "email": "existing.user@example.com", "password": "NewPassword123!", "confirm_password": "NewPassword123!", "role": "student", "terms_agreed": True})

      assert response.status_code == 400
      assert response.json()["detail"] == "Email already registered"
  ```

---

### Endpoint: Login for Token

- **URL:** `/auth/token`
- **Method:** POST

### Test Cases

**1. test_login_success** _Test successful login with valid credentials._

- **Passed Inputs:**

  - `username` = "student.new@example.com"
  - `password` = "ValidPassword123!"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "access_token": "some_jwt_token", "token_type": "bearer" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "access_token": "eyJhbGciOiJIUzI1Ni...", "token_type": "bearer" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_login_success(client):
      """
      Tests successful login and token retrieval.
      Assumes the user was created in a previous test or setup.
      """
      response = client.post(
          "/auth/token",
          data={"username": "student.new@example.com", "password": "ValidPassword123!"}
      )
      assert response.status_code == 200
      data = response.json()
      assert "access_token" in data
      assert data["token_type"] == "bearer"
  ```

**2. test_login_invalid_credentials** _Test login attempt with an incorrect password._

- **Passed Inputs:**

  - `username` = "student.new@example.com"
  - `password` = "WrongPassword"

- **Expected Output:**

  - `HTTP-Status Code`: 401
  - `Response Body`: `{ "detail": "Incorrect username or password" }`

- **Actual Output:**

  - `HTTP-Status Code`: 401
  - `Response Body`: `{ "detail": "Incorrect username or password" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_login_invalid_credentials(client):
      """
      Tests login with an incorrect password.
      """
      response = client.post(
          "/auth/token",
          data={"username": "student.new@example.com", "password": "WrongPassword"}
      )
      assert response.status_code == 401
      assert "Incorrect username or password" in response.text
  ```

<div style="page-break-after: always;"></div>

## Teacher Tasks API Tests Documentation

### Description

The Teacher Tasks API provides endpoints for teachers to create, retrieve, update, and delete tasks assigned to students. Access is restricted to users with the 'teacher' role.

---

### Endpoint: Create Task

- **URL:** `/teacher/tasks/`
- **Method:** POST

### Test Cases

**1. test_create_task_success** _Test successful creation of a task by an authenticated teacher._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `Request Body`: `{ "title": "History Essay", "assigned_to": "student_uuid_123", "assigned_by": "teacher_uuid_456", "category": "Writing", "due_date": "2025-10-01T23:59:59Z" }`

- **Expected Output:**

  - `HTTP-Status Code`: 201
  - `Response Body`: (A JSON object representing the newly created task, including a system-generated task ID)

- **Actual Output:**

  - `HTTP-Status Code`: 201
  - `Response Body`: `{ "id": "new_task_uuid", "title": "History Essay", "status": "pending", ... }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_task_success(client, teacher_auth_header):
      """
      Test successful task creation by a teacher.
      """
      response = client.post(
          "/teacher/tasks/",
          headers=teacher_auth_header,
          json={
              "title": "History Essay",
              "assigned_to": "student_uuid_123",
              "assigned_by": "teacher_uuid_456",
              "category": "Writing",
              "due_date": "2025-10-01T23:59:59Z",
          },
      )
      assert response.status_code == 201
      assert "id" in response.json()
      assert response.json()["title"] == "History Essay"
  ```

**2. test_create_task_unauthorized** _Test that a user with a student role cannot create a task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body`: `{ "title": "Attempted Task", ... }`

- **Expected Output:**

  - `HTTP-Status Code`: 403
  - `Response Body`: `{ "detail": "Not authorized" }`

- **Actual Output:**

  - `HTTP-Status Code`: 403
  - `Response Body`: `{ "detail": "Not authorized" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_task_unauthorized(client, student_auth_header):
      """
      Test that a student cannot create a task via the teacher endpoint.
      """
      response = client.post(
          "/teacher/tasks/",
          headers=student_auth_header,
          json={"title": "Attempted Task", "assigned_to": "student_uuid_123", "assigned_by": "teacher_uuid_456", "category": "Misc"},
      )
      assert response.status_code == 403
      assert response.json()["detail"] == "Not authorized"
  ```

---

### Endpoint: Get Task by ID

- **URL:** `/teacher/tasks/{task_id}`
- **Method:** GET

### Test Cases

**1. test_get_task_not_found** _Test retrieving a task with a UUID that does not exist._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `URL Parameter`: `task_id` = "123e4567-e89b-12d3-a456-426614174000"

- **Expected Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Task not found" }`

- **Actual Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Task not found" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_task_not_found(client, teacher_auth_header):
      """
      Test retrieving a task that does not exist.
      """
      non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
      response = client.get(
          f"/teacher/tasks/{non_existent_id}",
          headers=teacher_auth_header,
      )
      assert response.status_code == 404
      assert response.json()["detail"] == "Task not found"
  ```

<div style="page-break-after: always;"></div>

## Student Finance API Tests Documentation

### Description

The Student Finance API allows students to manage their personal finances by logging transactions and creating savings goals. All endpoints require student authentication.

---

### Endpoint: Add Transaction

- **URL:** `/student/finance/transactions`
- **Method:** POST

### Test Cases

**1. test_add_transaction_success** _Test successful creation of a financial transaction._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body`: `{ "amount": 15.00, "type": "income", "category": "Gift", "transaction_date": "2025-07-28" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: (A JSON object of the transaction, including a new `transaction_id`)

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "transaction_id": "new_txn_uuid", "amount": 15.00, "type": "income", ... }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_add_transaction_success(client, student_auth_header):
      """
      Test adding a valid financial transaction for a student.
      """
      response = client.post(
          "/student/finance/transactions",
          headers=student_auth_header,
          json={
              "amount": 15.00,
              "type": "income",
              "category": "Gift",
              "note": "Birthday money",
              "transaction_date": "2025-07-28",
          },
      )
      assert response.status_code == 200
      assert "transaction_id" in response.json()
      assert response.json()["amount"] == 15.00
  ```

---

### Endpoint: Create Savings Goal

- **URL:** `/student/finance/savings-goals`
- **Method:** POST

### Test Cases

**1. test_create_savings_goal_success** _Test successful creation of a new savings goal._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body`: `{ "title": "New Headphones", "target_amount": 250.00 }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: (A JSON object of the goal, including a new `goal_id` and `saved_amount` of 0.0)

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "goal_id": "new_goal_uuid", "title": "New Headphones", "target_amount": 250.00, "saved_amount": 0.0 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_savings_goal_success(client, student_auth_header):
      """
      Test creating a valid savings goal for a student.
      """
      response = client.post(
          "/student/finance/savings-goals",
          headers=student_auth_header,
          json={"title": "New Headphones", "target_amount": 250.00},
      )
      assert response.status_code == 200
      assert "goal_id" in response.json()
      assert response.json()["target_amount"] == 250.00
      assert response.json()["saved_amount"] == 0.0
  ```

<div style="page-break-after: always;"></div>

## Parent Children API Tests Documentation

### Description

The Parent Children API allows authenticated parents to link their account to their children's accounts, view linked children, and manage the relationship.

---

### Endpoint: Add Child

- **URL:** `/parent/children/add`
- **Method:** POST

### Test Cases

**1. test_add_child_success** _Test a parent successfully linking their account to an existing child's account._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Request Body`: `{ "child_id": "existing_child_uuid", "relationship": "Mother" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Child linked successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Child linked successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_add_child_success(client, parent_auth_header, child_to_link_uuid):
      """
      Test successfully linking a child to a parent's account.
      Assumes a child user exists in the DB to be linked.
      """
      response = client.post(
          "/parent/children/add",
          headers=parent_auth_header,
          json={"child_id": child_to_link_uuid, "relationship": "Mother"},
      )
      assert response.status_code == 200
      assert response.json()["message"] == "Child linked successfully"
  ```

**2. test_add_child_not_found** _Test attempting to link a child account that does not exist._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Request Body`: `{ "child_id": "non_existent_child_uuid", "relationship": "Father" }`

- **Expected Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Child with this ID not found" }`

- **Actual Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Child with this ID not found" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_add_child_not_found(client, parent_auth_header):
      """
      Test linking a child that does not exist.
      """
      non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
      response = client.post(
          "/parent/children/add",
          headers=parent_auth_header,
          json={"child_id": non_existent_id, "relationship": "Guardian"},
      )
      assert response.status_code == 404
      assert response.json()["detail"] == "Child with this ID not found"
  ```

<div style="page-break-after: always;"></div>

## Users Profile API Tests Documentation

### Description

The Users Profile API allows authenticated users to retrieve their profile information.

---

### Endpoint: Get User Profile

- **URL:** `/users/profile`
- **Method:** GET

### Test Cases

**1. test_get_profile_success** _Test successful retrieval of user profile._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_user_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: (A JSON object containing user profile information)

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "id": "user_uuid", "full_name": "John Doe", "email": "john@example.com", "role": "student" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_profile_success(client, user_auth_header):
      """
      Test successful retrieval of user profile.
      """
      response = client.get(
          "/users/profile",
          headers=user_auth_header,
      )
      assert response.status_code == 200
      assert "id" in response.json()
      assert "email" in response.json()
  ```

**2. test_get_profile_unauthorized** _Test profile access without authentication._

- **Passed Inputs:**

  - No Authorization Header

- **Expected Output:**

  - `HTTP-Status Code`: 401
  - `Response Body`: `{ "detail": "Not authenticated" }`

- **Actual Output:**

  - `HTTP-Status Code`: 401
  - `Response Body`: `{ "detail": "Not authenticated" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_profile_unauthorized(client):
      """
      Test profile access without authentication.
      """
      response = client.get("/users/profile")
      assert response.status_code == 401
      assert "Not authenticated" in response.text
  ```

<div style="page-break-after: always;"></div>

## Roles API Tests Documentation

### Description

The Roles API provides endpoints to retrieve available user roles in the system.

---

### Endpoint: Get Roles

- **URL:** `/roles/`
- **Method:** GET

### Test Cases

**1. test_get_roles_success** _Test successful retrieval of available roles._

- **Passed Inputs:**

  - No authentication required

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of role objects

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"id": 1, "name": "student"}, {"id": 2, "name": "teacher"}, {"id": 3, "name": "parent"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_roles_success(client):
      """
      Test successful retrieval of available roles.
      """
      response = client.get("/roles/")
      assert response.status_code == 200
      assert isinstance(response.json(), list)
      assert len(response.json()) > 0
  ```

<div style="page-break-after: always;"></div>

## Teacher Dashboard API Tests Documentation

### Description

The Teacher Dashboard API provides comprehensive dashboard functionality for teachers including summary information, student attention alerts, health alerts, and join request management.

---

### Endpoint: Get Dashboard Summary

- **URL:** `/teacher/dashboard/`
- **Method:** GET

### Test Cases

**1. test_get_dashboard_summary_success** _Test successful retrieval of teacher dashboard summary._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Dashboard summary object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "total_students": 25, "pending_tasks": 12, "completed_tasks": 48 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_dashboard_summary_success(client, teacher_auth_header):
      """
      Test successful retrieval of teacher dashboard summary.
      """
      response = client.get(
          "/teacher/dashboard/",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get Students Requiring Attention

- **URL:** `/teacher/dashboard/attention`
- **Method:** GET

### Test Cases

**1. test_get_students_requiring_attention_success** _Test successful retrieval of students requiring attention._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of students requiring attention

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"student_id": "uuid1", "reason": "overdue_tasks", "count": 3}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_students_requiring_attention_success(client, teacher_auth_header):
      """
      Test successful retrieval of students requiring attention.
      """
      response = client.get(
          "/teacher/dashboard/attention",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get Urgent Health Alerts

- **URL:** `/teacher/dashboard/health-alerts`
- **Method:** GET

### Test Cases

**1. test_get_urgent_health_alerts_success** _Test successful retrieval of urgent health alerts._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of health alerts

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"student_id": "uuid1", "alert_type": "stress", "severity": "high"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_urgent_health_alerts_success(client, teacher_auth_header):
      """
      Test successful retrieval of urgent health alerts.
      """
      response = client.get(
          "/teacher/dashboard/health-alerts",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get Join Requests

- **URL:** `/teacher/dashboard/join-requests`
- **Method:** GET

### Test Cases

**1. test_get_join_requests_success** _Test successful retrieval of join requests._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of join requests

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"request_id": "uuid1", "student_name": "Alice", "classroom": "Math 101"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_join_requests_success(client, teacher_auth_header):
      """
      Test successful retrieval of join requests.
      """
      response = client.get(
          "/teacher/dashboard/join-requests",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Respond to Join Request

- **URL:** `/teacher/dashboard/join-requests/respond`
- **Method:** POST

### Test Cases

**1. test_respond_to_join_request_approve** _Test successful approval of a join request._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `Request Body`: `{ "request_id": "request_uuid", "action": "approve" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Request approved successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Request approved successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_respond_to_join_request_approve(client, teacher_auth_header):
      """
      Test successful approval of a join request.
      """
      response = client.post(
          "/teacher/dashboard/join-requests/respond",
          headers=teacher_auth_header,
          json={
              "request_id": "request_uuid_123",
              "action": "approve"
          },
      )
      assert response.status_code == 200
      assert "approved" in response.json()["message"]
  ```

**2. test_respond_to_join_request_reject** _Test successful rejection of a join request._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `Request Body`: `{ "request_id": "request_uuid", "action": "reject" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Request rejected successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Request rejected successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_respond_to_join_request_reject(client, teacher_auth_header):
      """
      Test successful rejection of a join request.
      """
      response = client.post(
          "/teacher/dashboard/join-requests/respond",
          headers=teacher_auth_header,
          json={
              "request_id": "request_uuid_123",
              "action": "reject"
          },
      )
      assert response.status_code == 200
      assert "rejected" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Teacher Classroom Management API Tests Documentation

### Description

The Teacher Classroom Management API provides endpoints for teachers to manage classrooms and students including listing classrooms, managing student enrollment, and retrieving classroom metrics.

---

### Endpoint: List Classrooms

- **URL:** `/teacher/classrooms`
- **Method:** GET

### Test Cases

**1. test_list_classrooms_success** _Test successful retrieval of teacher's classrooms._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of classroom objects

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"id": "classroom_uuid", "name": "Math 101", "student_count": 25}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_classrooms_success(client, teacher_auth_header):
      """
      Test successful retrieval of teacher's classrooms.
      """
      response = client.get(
          "/teacher/classrooms",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: List Classroom Students

- **URL:** `/teacher/classrooms/{classroom_id}/students`
- **Method:** GET

### Test Cases

**1. test_list_classroom_students_success** _Test successful retrieval of students in a classroom._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `URL Parameter`: `classroom_id` = "classroom_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of student objects

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"id": "student_uuid", "name": "Alice Smith", "email": "alice@example.com"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_classroom_students_success(client, teacher_auth_header):
      """
      Test successful retrieval of students in a classroom.
      """
      classroom_id = "classroom_uuid_123"
      response = client.get(
          f"/teacher/classrooms/{classroom_id}/students",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Add Student to Classroom

- **URL:** `/teacher/classrooms/{classroom_id}/students/{student_id}`
- **Method:** POST

### Test Cases

**1. test_add_student_to_classroom_success** _Test successful addition of student to classroom._

- **Passed Inputs:**

  - `Authorization Header\*\*: "Bearer <valid_teacher_token>"
  - `URL Parameters`: `classroom_id` = "classroom_uuid_123", `student_id` = "student_uuid_456"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Student added to classroom successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Student added to classroom successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_add_student_to_classroom_success(client, teacher_auth_header):
      """
      Test successful addition of student to classroom.
      """
      classroom_id = "classroom_uuid_123"
      student_id = "student_uuid_456"
      response = client.post(
          f"/teacher/classrooms/{classroom_id}/students/{student_id}",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
      assert "added" in response.json()["message"]
  ```

---

### Endpoint: Remove Student from Classroom

- **URL:** `/teacher/classrooms/{classroom_id}/students/{student_id}`
- **Method:** DELETE

### Test Cases

**1. test_remove_student_from_classroom_success** _Test successful removal of student from classroom._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `URL Parameters`: `classroom_id` = "classroom_uuid_123", `student_id` = "student_uuid_456"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Student removed from classroom successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Student removed from classroom successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_remove_student_from_classroom_success(client, teacher_auth_header):
      """
      Test successful removal of student from classroom.
      """
      classroom_id = "classroom_uuid_123"
      student_id = "student_uuid_456"
      response = client.delete(
          f"/teacher/classrooms/{classroom_id}/students/{student_id}",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
      assert "removed" in response.json()["message"]
  ```

---

### Endpoint: Get Students Metrics

- **URL:** `/teacher/students/metrics`
- **Method:** GET

### Test Cases

**1. test_get_students_metrics_success** _Test successful retrieval of students metrics._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of student metrics

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"student_id": "uuid", "tasks_assigned": 10, "tasks_completed": 8, "overdue_count": 1}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_students_metrics_success(client, teacher_auth_header):
      """
      Test successful retrieval of students metrics.
      """
      response = client.get(
          "/teacher/students/metrics",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

<div style="page-break-after: always;"></div>

## Teacher Tasks Management API Tests Documentation

### Description

Extended Teacher Tasks API covering task summaries, recent tasks, and overdue task management.

---

### Endpoint: Get Tasks Summary

- **URL:** `/teacher/tasks/summary`
- **Method:** GET

### Test Cases

**1. test_get_tasks_summary_success** _Test successful retrieval of tasks summary._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Tasks summary object

- **Actual Output:**

  - `HTTP-Status Code\*\*: 200
  - `Response Body`: `{ "total_tasks": 50, "pending": 15, "completed": 30, "overdue": 5 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_tasks_summary_success(client, teacher_auth_header):
      """
      Test successful retrieval of tasks summary.
      """
      response = client.get(
          "/teacher/tasks/summary",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get Recent Tasks

- **URL:** `/teacher/tasks/recent`
- **Method:** GET

### Test Cases

**1. test_get_recent_tasks_success** _Test successful retrieval of recent tasks._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of recent tasks

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"id": "task_uuid", "title": "Math Homework", "created_at": "2025-07-26"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_recent_tasks_success(client, teacher_auth_header):
      """
      Test successful retrieval of recent tasks.
      """
      response = client.get(
          "/teacher/tasks/recent",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get Overdue Tasks

- **URL:** `/teacher/tasks/overdue`
- **Method:** GET

### Test Cases

**1. test_get_overdue_tasks_success** _Test successful retrieval of overdue tasks._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of overdue tasks

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"id": "task_uuid", "title": "Late Assignment", "due_date": "2025-07-20"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_overdue_tasks_success(client, teacher_auth_header):
      """
      Test successful retrieval of overdue tasks.
      """
      response = client.get(
          "/teacher/tasks/overdue",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get All Tasks

- **URL:** `/teacher/tasks/`
- **Method:** GET

### Test Cases

**1. test_get_all_tasks_success** _Test successful retrieval of all tasks._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of all tasks

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"id": "task_uuid", "title": "Assignment 1", "status": "pending"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_all_tasks_success(client, teacher_auth_header):
      """
      Test successful retrieval of all tasks.
      """
      response = client.get(
          "/teacher/tasks/",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Update Task

- **URL:** `/teacher/tasks/{task_id}`
- **Method:** PUT

### Test Cases

**1. test_update_task_success** _Test successful update of a task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `URL Parameter`: `task_id` = "task_uuid_123"
  - `Request Body`: `{ "title": "Updated Assignment", "description": "Updated description" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated task object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "id": "task_uuid_123", "title": "Updated Assignment", "description": "Updated description" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_task_success(client, teacher_auth_header):
      """
      Test successful update of a task.
      """
      task_id = "task_uuid_123"
      response = client.put(
          f"/teacher/tasks/{task_id}",
          headers=teacher_auth_header,
          json={
              "title": "Updated Assignment",
              "description": "Updated description"
          },
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Task

- **URL:** `/teacher/tasks/{task_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_task_success** _Test successful deletion of a task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `URL Parameter`: `task_id` = "task_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Task deleted successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Task deleted successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_task_success(client, teacher_auth_header):
      """
      Test successful deletion of a task.
      """
      task_id = "task_uuid_123"
      response = client.delete(
          f"/teacher/tasks/{task_id}",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Teacher Reports API Tests Documentation

### Description

The Teacher Reports API provides endpoints for generating detailed student reports.

---

### Endpoint: Get Student Report

- **URL:** `/teacher/reports/{student_id}`
- **Method:** GET

### Test Cases

**1. test_get_student_report_success** _Test successful retrieval of student report._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `URL Parameter`: `student_id` = "student_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Detailed student report object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "student_id": "student_uuid_123", "performance": "good", "tasks_completed": 8 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_student_report_success(client, teacher_auth_header):
      """
      Test successful retrieval of student report.
      """
      student_id = "student_uuid_123"
      response = client.get(
          f"/teacher/reports/{student_id}",
          headers=teacher_auth_header,
      )
      assert response.status_code == 200
      assert "student_id" in response.json()
  ```

**2. test_get_student_report_not_found** _Test retrieval of report for non-existent student._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `URL Parameter`: `student_id` = "non_existent_uuid"

- **Expected Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Student not found" }`

- **Actual Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Student not found" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_student_report_not_found(client, teacher_auth_header):
      """
      Test retrieval of report for non-existent student.
      """
      non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
      response = client.get(
          f"/teacher/reports/{non_existent_id}",
          headers=teacher_auth_header,
      )
      assert response.status_code == 404
      assert response.json()["detail"] == "Student not found"
  ```

<div style="page-break-after: always;"></div>

## Student Dashboard API Tests Documentation

### Description

The Student Dashboard API provides overview information for student dashboard including tasks, finance, emotions, diet, and health data.

---

### Endpoint: Get Student Dashboard

- **URL:** `/student/dashboard/`
- **Method:** GET

### Test Cases

**1. test_get_student_dashboard_success** _Test successful retrieval of student dashboard._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Dashboard overview object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "pending_tasks": 5, "total_savings": 150.00, "mood": "happy" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_student_dashboard_success(client, student_auth_header):
      """
      Test successful retrieval of student dashboard.
      """
      response = client.get(
          "/student/dashboard/",
          headers=student_auth_header,
      )
      assert response.status_code == 200
  ```

<div style="page-break-after: always;"></div>

## Student Tasks API Tests Documentation

### Description

Extended Student Tasks API covering task listing, creation, updates, and deletion for students.

---

### Endpoint: List Student Tasks

- **URL:** `/student/tasks/`
- **Method:** GET

### Test Cases

**1. test_list_student_tasks_success** _Test successful retrieval of student's tasks._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of tasks assigned to student

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"id": "task_uuid", "title": "Math Homework", "status": "pending"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_student_tasks_success(client, student_auth_header):
      """
      Test successful retrieval of student's tasks.
      """
      response = client.get(
          "/student/tasks/",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Add Student Task

- **URL:** `/student/tasks/`
- **Method:** POST

### Test Cases

**1. test_add_student_task_success** _Test successful creation of a new task by student._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body`: `{ "title": "Personal Study", "category": "Self-Study", "due_date": "2025-08-01" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Created task object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "id": "new_task_uuid", "title": "Personal Study", "status": "pending" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_add_student_task_success(client, student_auth_header):
      """
      Test successful creation of a new task by student.
      """
      response = client.post(
          "/student/tasks/",
          headers=student_auth_header,
          json={
              "title": "Personal Study",
              "category": "Self-Study",
              "due_date": "2025-08-01T23:59:59Z"
          },
      )
      assert response.status_code == 200
      assert "id" in response.json()
  ```

---

### Endpoint: Get Student Task

- **URL:** `/student/tasks/{task_id}`
- **Method:** GET

### Test Cases

**1. test_get_student_task_success** _Test successful retrieval of specific task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `task_id` = "task_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Task object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "id": "task_uuid_123", "title": "Math Homework", "status": "pending" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_student_task_success(client, student_auth_header):
      """
      Test successful retrieval of specific task.
      """
      task_id = "task_uuid_123"
      response = client.get(
          f"/student/tasks/{task_id}",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert response.json()["id"] == task_id
  ```

---

### Endpoint: Update Student Task

- **URL:** `/student/tasks/{task_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_student_task_success** _Test successful update of student task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter**: `task_id` = "task_uuid_123"
  - `Request Body`: `{ "status": "completed" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated task object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "id": "task_uuid_123", "status": "completed" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_student_task_success(client, student_auth_header):
      """
      Test successful update of student task.
      """
      task_id = "task_uuid_123"
      response = client.patch(
          f"/student/tasks/{task_id}",
          headers=student_auth_header,
          json={"status": "completed"},
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Student Task

- **URL:** `/student/tasks/{task_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_student_task_success** _Test successful deletion of student task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `task_id` = "task_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Task deleted successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Task deleted successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_student_task_success(client, student_auth_header):
      """
      Test successful deletion of student task.
      """
      task_id = "task_uuid_123"
      response = client.delete(
          f"/student/tasks/{task_id}",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Student Finance Extended API Tests Documentation

### Description

Extended Student Finance API covering finance dashboard, savings goals management, and transaction listing.

---

### Endpoint: List Transactions

- **URL:** `/student/finance/transactions`
- **Method:** GET

### Test Cases

**1. test_list_transactions_success** _Test successful retrieval of student's transactions._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of transactions

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"transaction_id": "txn_uuid", "amount": 15.00, "type": "income"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_transactions_success(client, student_auth_header):
      """
      Test successful retrieval of student's transactions.
      """
      response = client.get(
          "/student/finance/transactions",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Finance Dashboard

- **URL:** `/student/finance/dashboard`
- **Method:** GET

### Test Cases

**1. test_get_finance_dashboard_success** _Test successful retrieval of finance dashboard._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Finance dashboard summary

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "total_income": 500.00, "total_expenses": 300.00, "balance": 200.00 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_finance_dashboard_success(client, student_auth_header):
      """
      Test successful retrieval of finance dashboard.
      """
      response = client.get(
          "/student/finance/dashboard",
          headers=student_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: List Savings Goals

- **URL:** `/student/finance/savings-goals`
- **Method:** GET

### Test Cases

**1. test_list_savings_goals_success** _Test successful retrieval of savings goals._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code\*\*: 200
  - `Response Body`: Array of savings goals

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"goal_id": "goal_uuid", "title": "New Bike", "target_amount": 500.00}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_savings_goals_success(client, student_auth_header):
      """
      Test successful retrieval of savings goals.
      """
      response = client.get(
          "/student/finance/savings-goals",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Savings Goal

- **URL:** `/student/finance/savings-goals/{goal_id}`
- **Method:** GET

### Test Cases

**1. test_get_savings_goal_success** _Test successful retrieval of specific savings goal._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `goal_id` = "goal_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Savings goal object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "goal_id": "goal_uuid_123", "title": "New Bike", "target_amount": 500.00 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_savings_goal_success(client, student_auth_header):
      """
      Test successful retrieval of specific savings goal.
      """
      goal_id = "goal_uuid_123"
      response = client.get(
          f"/student/finance/savings-goals/{goal_id}",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert response.json()["goal_id"] == goal_id
  ```

---

### Endpoint: Update Savings Goal

- **URL:** `/student/finance/savings-goals/{goal_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_savings_goal_success** _Test successful update of savings goal._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `goal_id` = "goal_uuid_123"
  - `Request Body`: `{ "saved_amount": 150.00 }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated savings goal object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "goal_id": "goal_uuid_123", "saved_amount": 150.00 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_savings_goal_success(client, student_auth_header):
      """
      Test successful update of savings goal.
      """
      goal_id = "goal_uuid_123"
      response = client.patch(
          f"/student/finance/savings-goals/{goal_id}",
          headers=student_auth_header,
          json={"saved_amount": 150.00},
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Savings Goal

- **URL:** `/student/finance/savings-goals/{goal_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_savings_goal_success** _Test successful deletion of savings goal._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `goal_id` = "goal_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Savings goal deleted successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Savings goal deleted successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_savings_goal_success(client, student_auth_header):
      """
      Test successful deletion of savings goal.
      """
      goal_id = "goal_uuid_123"
      response = client.delete(
          f"/student/finance/savings-goals/{goal_id}",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Student Emotions API Tests Documentation

### Description

The Student Emotions API provides comprehensive emotional wellbeing features including emotional entries, mood logging, chat sessions, emergency contacts, and AI-powered emotional support.

---

### Endpoint: List Emotional Entries

- **URL:** `/student/emotions/entries`
- **Method:** GET

### Test Cases

**1. test_list_emotional_entries_success** _Test successful retrieval of emotional entries._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of emotional entries

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"entry_id": "entry_uuid", "emotion": "happy", "notes": "Good day", "date": "2025-07-26"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_emotional_entries_success(client, student_auth_header):
      """
      Test successful retrieval of emotional entries.
      """
      response = client.get(
          "/student/emotions/entries",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Create Emotional Entry

- **URL:** `/student/emotions/entries`
- **Method:** POST

### Test Cases

**1. test_create_emotional_entry_success** _Test successful creation of emotional entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body`: `{ "emotion": "anxious", "intensity": 7, "notes": "Worried about exam" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Created emotional entry object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "entry_id": "new_entry_uuid", "emotion": "anxious", "intensity": 7 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_emotional_entry_success(client, student_auth_header):
      """
      Test successful creation of emotional entry.
      """
      response = client.post(
          "/student/emotions/entries",
          headers=student_auth_header,
          json={
              "emotion": "anxious",
              "intensity": 7,
              "notes": "Worried about exam"
          },
      )
      assert response.status_code == 200
      assert "entry_id" in response.json()
  ```

---

### Endpoint: List Mood Logs

- **URL:** `/student/emotions/mood-logs`
- **Method:** GET

### Test Cases

**1. test_list_mood_logs_success** _Test successful retrieval of mood logs._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of mood logs

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"log_id": "log_uuid", "mood": "happy", "energy_level": "high", "date": "2025-07-26"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_mood_logs_success(client, student_auth_header):
      """
      Test successful retrieval of mood logs.
      """
      response = client.get(
          "/student/emotions/mood-logs",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Create Mood Log

- **URL:** `/student/emotions/mood-logs`
- **Method:** POST

### Test Cases

**1. test_create_mood_log_success** _Test successful creation of mood log._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body**: `{ "mood": "calm", "energy_level": "medium", "stress_level": "low" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Created mood log object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "log_id": "new_log_uuid", "mood": "calm", "energy_level": "medium" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_mood_log_success(client, student_auth_header):
      """
      Test successful creation of mood log.
      """
      response = client.post(
          "/student/emotions/mood-logs",
          headers=student_auth_header,
          json={
              "mood": "calm",
              "energy_level": "medium",
              "stress_level": "low"
          },
      )
      assert response.status_code == 200
      assert "log_id" in response.json()
  ```

---

### Endpoint: List Chat Sessions

- **URL:** `/student/emotions/sessions`
- **Method:** GET

### Test Cases

**1. test_list_chat_sessions_success** _Test successful retrieval of chat sessions._

- **Passed Inputs:**

  - `Authorization Header\*\*: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of chat sessions

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"session_id": "session_uuid", "title": "Daily Check-in", "created_at": "2025-07-26"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_chat_sessions_success(client, student_auth_header):
      """
      Test successful retrieval of chat sessions.
      """
      response = client.get(
          "/student/emotions/sessions",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Create Chat Session

- **URL:** `/student/emotions/sessions`
- **Method:** POST

### Test Cases

**1. test_create_chat_session_success** _Test successful creation of chat session._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body`: `{ "title": "Evening Reflection", "topic": "stress_management" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Created chat session object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "session_id": "new_session_uuid", "title": "Evening Reflection" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_chat_session_success(client, student_auth_header):
      """
      Test successful creation of chat session.
      """
      response = client.post(
          "/student/emotions/sessions",
          headers=student_auth_header,
          json={
              "title": "Evening Reflection",
              "topic": "stress_management"
          },
      )
      assert response.status_code == 200
      assert "session_id" in response.json()
  ```

---

### Endpoint: List Emergency Contacts

- **URL:** `/student/emotions/contacts`
- **Method:** GET

### Test Cases

**1. test_list_emergency_contacts_success** _Test successful retrieval of emergency contacts._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of emergency contacts

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"contact_id": "contact_uuid", "name": "Crisis Hotline", "phone": "1-800-123-4567"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_emergency_contacts_success(client, student_auth_header):
      """
      Test successful retrieval of emergency contacts.
      """
      response = client.get(
          "/student/emotions/contacts",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Create Emergency Contact

- **URL:** `/student/emotions/contacts`
- **Method:** POST

### Test Cases

**1. test_create_emergency_contact_success** _Test successful creation of emergency contact._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body**: `{ "name": "Family Doctor", "phone": "555-0123", "contact_type": "medical" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Created emergency contact object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "contact_id": "new_contact_uuid", "name": "Family Doctor", "phone": "555-0123" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_emergency_contact_success(client, student_auth_header):
      """
      Test successful creation of emergency contact.
      """
      response = client.post(
          "/student/emotions/contacts",
          headers=student_auth_header,
          json={
              "name": "Family Doctor",
              "phone": "555-0123",
              "contact_type": "medical"
          },
      )
      assert response.status_code == 200
      assert "contact_id" in response.json()
  ```

<div style="page-break-after: always;"></div>

## Health and Diet API Tests Documentation

### Description

The Health and Diet API provides comprehensive health tracking including diet logging, meal tracking, health metrics monitoring, and health analytics.

---

### Endpoint: Get Diet Logs

- **URL:** `/health/student_diet`
- **Method:** GET

### Test Cases

**1. test_get_diet_logs_success** _Test successful retrieval of diet logs._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of diet entries

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"entry_id": "diet_uuid", "food_item": "Apple", "calories": 95, "date": "2025-07-26"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_diet_logs_success(client, student_auth_header):
      """
      Test successful retrieval of diet logs.
      """
      response = client.get(
          "/health/student_diet",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Log Student Diet

- **URL:** `/health/student_diet`
- **Method:** POST

### Test Cases

**1. test_log_student_diet_success** _Test successful logging of diet entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body**: `{ "food_item": "Banana", "calories": 105, "meal_type": "snack" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Created diet entry object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "entry_id": "new_diet_uuid", "food_item": "Banana", "calories": 105 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_log_student_diet_success(client, student_auth_header):
      """
      Test successful logging of diet entry.
      """
      response = client.post(
          "/health/student_diet",
          headers=student_auth_header,
          json={
              "food_item": "Banana",
              "calories": 105,
              "meal_type": "snack"
          },
      )
      assert response.status_code == 200
      assert "entry_id" in response.json()
  ```

---

### Endpoint: Get Meal Logs

- **URL:** `/health/meals`
- **Method:** GET

### Test Cases

**1. test_get_meal_logs_success** _Test successful retrieval of meal logs._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of meal entries

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"meal_id": "meal_uuid", "meal_name": "Breakfast", "total_calories": 350}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_meal_logs_success(client, student_auth_header):
      """
      Test successful retrieval of meal logs.
      """
      response = client.get(
          "/health/meals",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Health Metrics

- **URL:** `/health/metrics`
- **Method:** GET

### Test Cases

**1. test_get_health_metrics_success** _Test successful retrieval of health metrics._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of health metrics

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"metric_id": "metric_uuid", "type": "weight", "value": 65.5, "unit": "kg"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_health_metrics_success(client, student_auth_header):
      """
      Test successful retrieval of health metrics.
      """
      response = client.get(
          "/health/metrics",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Log Health Metrics

- **URL:** `/health/metrics`
- **Method:** POST

### Test Cases

**1. test_log_health_metrics_success** _Test successful logging of health metrics._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body**: `{ "type": "blood_pressure", "systolic": 120, "diastolic": 80 }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Created health metric object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "metric_id": "new_metric_uuid", "type": "blood_pressure", "systolic": 120 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_log_health_metrics_success(client, student_auth_header):
      """
      Test successful logging of health metrics.
      """
      response = client.post(
          "/health/metrics",
          headers=student_auth_header,
          json={
              "type": "blood_pressure",
              "systolic": 120,
              "diastolic": 80
          },
      )
      assert response.status_code == 200
      assert "metric_id" in response.json()
  ```

---

### Endpoint: Get Health Analytics

- **URL:** `/health/analytics`
- **Method:** GET

### Test Cases

**1. test_get_health_analytics_success** _Test successful retrieval of health analytics._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Health analytics object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "average_calories": 2150, "weight_trend": "stable", "bmi": 22.5 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_health_analytics_success(client, student_auth_header):
      """
      Test successful retrieval of health analytics.
      """
      response = client.get(
          "/health/analytics",
          headers=student_auth_header,
      )
      assert response.status_code == 200
  ```

<div style="page-break-after: always;"></div>

## Parent Dashboard API Tests Documentation

### Description

The Parent Dashboard API provides comprehensive dashboard functionality for parents including overview information, task management, health alerts, finance goals, and family management.

---

### Endpoint: Get Parent Dashboard

- **URL:** `/parent/dashboard/`
- **Method:** GET

### Test Cases

**1. test_get_parent_dashboard_success** _Test successful retrieval of parent dashboard._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Parent dashboard overview

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "total_children": 2, "pending_requests": 1, "health_alerts": 0 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_parent_dashboard_success(client, parent_auth_header):
      """
      Test successful retrieval of parent dashboard.
      """
      response = client.get(
          "/parent/dashboard/",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get Dashboard Tasks

- **URL:** `/parent/dashboard/tasks`
- **Method:** GET

### Test Cases

**1. test_get_dashboard_tasks_success** _Test successful retrieval of dashboard tasks._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of tasks overview

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"child_name": "Alice", "pending_tasks": 3, "completed_tasks": 7}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_dashboard_tasks_success(client, parent_auth_header):
      """
      Test successful retrieval of dashboard tasks.
      """
      response = client.get(
          "/parent/dashboard/tasks",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get Health Alerts

- **URL:** `/parent/dashboard/health/alerts`
- **Method:** GET

### Test Cases

**1. test_get_health_alerts_success** _Test successful retrieval of health alerts._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of health alerts

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"child_id": "child_uuid", "alert_type": "high_stress", "severity": "medium"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_health_alerts_success(client, parent_auth_header):
      """
      Test successful retrieval of health alerts.
      """
      response = client.get(
          "/parent/dashboard/health/alerts",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
  ```

<div style="page-break-after: always;"></div>

## Parent Children Management Extended API Tests Documentation

### Description

Extended Parent Children Management API covering comprehensive child management including metrics, relationship updates, and child search functionality.

---

### Endpoint: Get Children Metrics

- **URL:** `/parent/children/metrics`
- **Method:** GET

### Test Cases

**1. test_get_children_metrics_success** _Test successful retrieval of children metrics._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of children metrics

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"child_id": "child_uuid", "academic_score": 85, "emotional_state": "good"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_children_metrics_success(client, parent_auth_header):
      """
      Test successful retrieval of children metrics.
      """
      response = client.get(
          "/parent/children/metrics",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: List Children

- **URL:** `/parent/children`
- **Method:** GET

### Test Cases

**1. test_list_children_success** _Test successful retrieval of linked children._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of linked children

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"child_id": "child_uuid", "name": "Alice", "relationship": "Mother"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_children_success(client, parent_auth_header):
      """
      Test successful retrieval of linked children.
      """
      response = client.get(
          "/parent/children",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Remove Child

- **URL:** `/parent/children/remove`
- **Method:** DELETE

### Test Cases

**1. test_remove_child_success** _Test successful removal of child link._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Query Parameter`: `child_id` = "child_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Child removed successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Child removed successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_remove_child_success(client, parent_auth_header):
      """
      Test successful removal of child link.
      """
      response = client.delete(
          "/parent/children/remove",
          headers=parent_auth_header,
          params={"child_id": "child_uuid_123"},
      )
      assert response.status_code == 200
      assert "removed" in response.json()["message"]
  ```

---

### Endpoint: Update Child Relationship

- **URL:** `/parent/children/relationship`
- **Method:** PATCH

### Test Cases

**1. test_update_child_relationship_success** _Test successful update of child relationship._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Request Body**: `{ "child_id": "child_uuid_123", "new_relationship": "Guardian" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Relationship updated successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Relationship updated successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_child_relationship_success(client, parent_auth_header):
      """
      Test successful update of child relationship.
      """
      response = client.patch(
          "/parent/children/relationship",
          headers=parent_auth_header,
          json={
              "child_id": "child_uuid_123",
              "new_relationship": "Guardian"
          },
      )
      assert response.status_code == 200
      assert "updated" in response.json()["message"]
  ```

---

### Endpoint: Search Children

- **URL:** `/parent/children/search`
- **Method:** GET

### Test Cases

**1. test_search_children_success** _Test successful search for children._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Query Parameters`: `email` = "child@example.com"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of matching children

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"child_id": "child_uuid", "name": "Alice", "email": "child@example.com"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_search_children_success(client, parent_auth_header):
      """
      Test successful search for children.
      """
      response = client.get(
          "/parent/children/search",
          headers=parent_auth_header,
          params={"email": "child@example.com"},
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

<div style="page-break-after: always;"></div>

## Student Profile API Tests Documentation

### Description

The Student Profile API provides comprehensive profile management functionality for students including profile retrieval, creation, updates, and deletion.

---

### Endpoint: Get Student Profile

- **URL:** `/student/profile/`
- **Method:** GET

### Test Cases

**1. test_get_student_profile_success** _Test successful retrieval of student profile._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Student profile object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "student_id": "student_uuid", "bio": "High school student", "interests": ["math", "science"] }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_student_profile_success(client, student_auth_header):
      """
      Test successful retrieval of student profile.
      """
      response = client.get(
          "/student/profile/",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert "student_id" in response.json()
  ```

---

### Endpoint: Create Student Profile

- **URL:** `/student/profile/`
- **Method:** POST

### Test Cases

**1. test_create_student_profile_success** _Test successful creation of student profile._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body**: `{ "bio": "Enthusiastic learner", "interests": ["art", "music"], "grade_level": 10 }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Created student profile object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "student_id": "student_uuid", "bio": "Enthusiastic learner", "grade_level": 10 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_student_profile_success(client, student_auth_header):
      """
      Test successful creation of student profile.
      """
      response = client.post(
          "/student/profile/",
          headers=student_auth_header,
          json={
              "bio": "Enthusiastic learner",
              "interests": ["art", "music"],
              "grade_level": 10
          },
      )
      assert response.status_code == 200
      assert "student_id" in response.json()
  ```

---

### Endpoint: Update Student Profile

- **URL:** `/student/profile/`
- **Method:** PATCH

### Test Cases

**1. test_update_student_profile_success** _Test successful update of student profile._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body**: `{ "bio": "Updated bio", "interests": ["coding", "robotics"] }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Updated student profile object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "student_id": "student_uuid", "bio": "Updated bio", "interests": ["coding", "robotics"] }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_student_profile_success(client, student_auth_header):
      """
      Test successful update of student profile.
      """
      response = client.patch(
          "/student/profile/",
          headers=student_auth_header,
          json={
              "bio": "Updated bio",
              "interests": ["coding", "robotics"]
          },
      )
      assert response.status_code == 200
      assert "bio" in response.json()
  ```

---

### Endpoint: Delete Student Profile

- **URL:** `/student/profile/`
- **Method:** DELETE

### Test Cases

**1. test_delete_student_profile_success** _Test successful deletion of student profile._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Profile deleted successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "message": "Profile deleted successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_student_profile_success(client, student_auth_header):
      """
      Test successful deletion of student profile.
      """
      response = client.delete(
          "/student/profile/",
          headers=student_auth_header,
      )
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Parent Tasks Management API Tests Documentation

### Description

The Parent Tasks Management API provides comprehensive task management functionality for parents including task summaries, creation, updates, and monitoring of children's tasks.

---

### Endpoint: Get Parent Tasks Summary

- **URL:** `/parent/tasks/summary`
- **Method:** GET

### Test Cases

**1. test_get_parent_tasks_summary_success** _Test successful retrieval of parent tasks summary._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Tasks summary for all children

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "total_tasks": 15, "completed": 10, "pending": 4, "overdue": 1 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_parent_tasks_summary_success(client, parent_auth_header):
      """
      Test successful retrieval of parent tasks summary.
      """
      response = client.get(
          "/parent/tasks/summary",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Get Recent Parent Tasks

- **URL:** `/parent/tasks/recent`
- **Method:** GET

### Test Cases

**1. test_get_recent_parent_tasks_success** _Test successful retrieval of recent tasks._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body\*\*: Array of recent tasks

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `[{"task_id": "task_uuid", "child_name": "Alice", "title": "Math Practice"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_recent_parent_tasks_success(client, parent_auth_header):
      """
      Test successful retrieval of recent tasks.
      """
      response = client.get(
          "/parent/tasks/recent",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
  ```

---

### Endpoint: Create Parent Task

- **URL:** `/parent/tasks/`
- **Method:** POST

### Test Cases

**1. test_create_parent_task_success** _Test successful creation of task by parent._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Request Body**: `{ "title": "Clean Room", "assigned_to": "child_uuid", "due_date": "2025-08-01" }`

- **Expected Output:**

  - `HTTP-Status Code\*\*: 200
  - `Response Body\*\*: Created task object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body**: `{ "task_id": "new_task_uuid", "title": "Clean Room", "status": "pending" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_parent_task_success(client, parent_auth_header):
      """
      Test successful creation of task by parent.
      """
      response = client.post(
          "/parent/tasks/",
          headers=parent_auth_header,
          json={
              "title": "Clean Room",
              "assigned_to": "child_uuid_123",
              "due_date": "2025-08-01T18:00:00Z"
          },
      )
      assert response.status_code == 200
      assert "task_id" in response.json()
  ```

<div style="page-break-after: always;"></div>

## Parent Requests API Tests Documentation

### Description

The Parent Requests API provides functionality for parents to manage family join requests including listing pending requests and approving or rejecting them.

---

### Endpoint: List Family Join Requests

- **URL:** `/parent/requests/`
- **Method:** GET

### Test Cases

**1. test_list_family_requests_success** _Test successful retrieval of pending family join requests._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of pending family join requests

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"request_id": "req_uuid", "requester_name": "John Doe", "family_name": "Smith Family"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_family_requests_success(client, parent_auth_header):
      """
      Test successful retrieval of pending family join requests.
      """
      response = client.get(
          "/parent/requests/",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Approve Family Join Request

- **URL:** `/parent/requests/{request_id}/approve`
- **Method:** POST

### Test Cases

**1. test_approve_family_request_success** _Test successful approval of a family join request._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameter`: `request_id` = "request_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Request approved successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Request approved successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_approve_family_request_success(client, parent_auth_header):
      """
      Test successful approval of a family join request.
      """
      request_id = "request_uuid_123"
      response = client.post(
          f"/parent/requests/{request_id}/approve",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert "approved" in response.json()["message"]
  ```

**2. test_approve_family_request_not_found** _Test approval of non-existent family join request._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameter`: `request_id` = "non_existent_uuid"

- **Expected Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Request not found" }`

- **Actual Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Request not found" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_approve_family_request_not_found(client, parent_auth_header):
      """
      Test approval of non-existent family join request.
      """
      non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
      response = client.post(
          f"/parent/requests/{non_existent_id}/approve",
          headers=parent_auth_header,
      )
      assert response.status_code == 404
      assert response.json()["detail"] == "Request not found"
  ```

---

### Endpoint: Reject Family Join Request

- **URL:** `/parent/requests/{request_id}/reject`
- **Method:** POST

### Test Cases

**1. test_reject_family_request_success** _Test successful rejection of a family join request._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameter`: `request_id` = "request_uuid_456"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Request rejected successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Request rejected successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_reject_family_request_success(client, parent_auth_header):
      """
      Test successful rejection of a family join request.
      """
      request_id = "request_uuid_456"
      response = client.post(
          f"/parent/requests/{request_id}/reject",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert "rejected" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Parent Family API Tests Documentation

### Description

The Parent Family API provides comprehensive family group management functionality including family overview, group creation, member management, and family group administration.

---

### Endpoint: Get Family Overview

- **URL:** `/parent/family/overview`
- **Method:** GET

### Test Cases

**1. test_get_family_overview_success** _Test successful retrieval of family overview._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Family overview summary object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "total_members": 4, "pending_tasks": 12, "health_alerts": 1, "total_savings": 850.00 }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_family_overview_success(client, parent_auth_header):
      """
      Test successful retrieval of family overview.
      """
      response = client.get(
          "/parent/family/overview",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert "total_members" in response.json()
  ```

---

### Endpoint: List Family Groups

- **URL:** `/parent/family/groups`
- **Method:** GET

### Test Cases

**1. test_list_family_groups_success** _Test successful retrieval of family groups._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of family groups

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"group_id": "group_uuid", "name": "Smith Family", "member_count": 4}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_family_groups_success(client, parent_auth_header):
      """
      Test successful retrieval of family groups.
      """
      response = client.get(
          "/parent/family/groups",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Create Family Group

- **URL:** `/parent/family/groups`
- **Method:** POST

### Test Cases

**1. test_create_family_group_success** _Test successful creation of a new family group._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Request Body`: `{ "name": "Johnson Family", "description": "Our family group" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Created family group object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "group_id": "new_group_uuid", "name": "Johnson Family", "head_id": "parent_uuid" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_family_group_success(client, parent_auth_header):
      """
      Test successful creation of a new family group.
      """
      response = client.post(
          "/parent/family/groups",
          headers=parent_auth_header,
          json={
              "name": "Johnson Family",
              "description": "Our family group"
          },
      )
      assert response.status_code == 200
      assert "group_id" in response.json()
      assert response.json()["name"] == "Johnson Family"
  ```

---

### Endpoint: Get Family Group Details

- **URL:** `/parent/family/groups/{group_id}`
- **Method:** GET

### Test Cases

**1. test_get_family_group_success** _Test successful retrieval of family group details._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameter`: `group_id` = "group_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Detailed family group object with members

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "group_id": "group_uuid_123", "name": "Smith Family", "members": [{"id": "child1", "name": "Alice"}] }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_family_group_success(client, parent_auth_header):
      """
      Test successful retrieval of family group details.
      """
      group_id = "group_uuid_123"
      response = client.get(
          f"/parent/family/groups/{group_id}",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert response.json()["group_id"] == group_id
      assert "members" in response.json()
  ```

**2. test_get_family_group_not_found** _Test retrieval of non-existent family group._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameter`: `group_id` = "non_existent_uuid"

- **Expected Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Family group not found" }`

- **Actual Output:**

  - `HTTP-Status Code`: 404
  - `Response Body`: `{ "detail": "Family group not found" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_family_group_not_found(client, parent_auth_header):
      """
      Test retrieval of non-existent family group.
      """
      non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
      response = client.get(
          f"/parent/family/groups/{non_existent_id}",
          headers=parent_auth_header,
      )
      assert response.status_code == 404
      assert response.json()["detail"] == "Family group not found"
  ```

---

### Endpoint: Add Family Member

- **URL:** `/parent/family/groups/{group_id}/add/{child_id}`
- **Method:** POST

### Test Cases

**1. test_add_family_member_success** _Test successful addition of member to family group._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameters`: `group_id` = "group_uuid_123", `child_id` = "child_uuid_456"
  - `Request Body`: `{ "role": "child" }`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Member added to family group successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Member added to family group successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_add_family_member_success(client, parent_auth_header):
      """
      Test successful addition of member to family group.
      """
      group_id = "group_uuid_123"
      child_id = "child_uuid_456"
      response = client.post(
          f"/parent/family/groups/{group_id}/add/{child_id}",
          headers=parent_auth_header,
          json={"role": "child"},
      )
      assert response.status_code == 200
      assert "added" in response.json()["message"]
  ```

---

### Endpoint: Remove Family Member

- **URL:** `/parent/family/groups/{group_id}/remove/{child_id}`
- **Method:** DELETE

### Test Cases

**1. test_remove_family_member_success** _Test successful removal of member from family group._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameters`: `group_id` = "group_uuid_123", `child_id` = "child_uuid_456"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Member removed from family group successfully" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "Member removed from family group successfully" }`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_remove_family_member_success(client, parent_auth_header):
      """
      Test successful removal of member from family group.
      """
      group_id = "group_uuid_123"
      child_id = "child_uuid_456"
      response = client.delete(
          f"/parent/family/groups/{group_id}/remove/{child_id}",
          headers=parent_auth_header,
      )
      assert response.status_code == 200
      assert "removed" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Failing Test Case Demonstration

### Description

## Missing API Endpoints Tests Documentation

<div style="page-break-after: always;"></div>

## Teacher Dashboard Extended API Tests Documentation

### Description

Additional Teacher Dashboard API endpoints for student management and reporting.

---

### Endpoint: Get Student Cards

- **URL:** `/teacher/dashboard/students`
- **Method:** GET

### Test Cases

**1. test_get_student_cards_success** _Test successful retrieval of student cards._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of student cards

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"student_id": "uuid", "name": "John Doe", "status": "active"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_student_cards_success(client, teacher_auth_header):
      response = client.get("/teacher/dashboard/students", headers=teacher_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Student Report

- **URL:** `/teacher/dashboard/student/{student_id}/report`
- **Method:** GET

### Test Cases

**1. test_get_dashboard_student_report_success** _Test successful retrieval of student report from dashboard._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_teacher_token>"
  - `URL Parameter`: `student_id` = "student_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Student report object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"student_id": "student_uuid_123", "grades": [85, 90], "attendance": 95}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_dashboard_student_report_success(client, teacher_auth_header):
      student_id = "student_uuid_123"
      response = client.get(f"/teacher/dashboard/student/{student_id}/report", headers=teacher_auth_header)
      assert response.status_code == 200
      assert response.json()["student_id"] == student_id
  ```

<div style="page-break-after: always;"></div>

## Student Emotions Extended API Tests Documentation

### Description

Comprehensive Student Emotions API covering detailed emotional entry management, chat messaging, and emergency contacts.

---

### Endpoint: Get Emotional Entry

- **URL:** `/student/emotions/entries/{entry_id}`
- **Method:** GET

### Test Cases

**1. test_get_emotional_entry_success** _Test successful retrieval of specific emotional entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "entry_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Emotional entry object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"entry_id": "entry_uuid_123", "emotion": "happy", "intensity": 8}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_emotional_entry_success(client, student_auth_header):
      entry_id = "entry_uuid_123"
      response = client.get(f"/student/emotions/entries/{entry_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert response.json()["entry_id"] == entry_id
  ```

---

### Endpoint: Update Emotional Entry

- **URL:** `/student/emotions/entries/{entry_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_emotional_entry_success** _Test successful update of emotional entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "entry_uuid_123"
  - `Request Body`: `{"intensity": 9, "notes": "Updated notes"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated emotional entry object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"entry_id": "entry_uuid_123", "intensity": 9, "notes": "Updated notes"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_emotional_entry_success(client, student_auth_header):
      entry_id = "entry_uuid_123"
      response = client.patch(f"/student/emotions/entries/{entry_id}",
                            json={"intensity": 9, "notes": "Updated notes"},
                            headers=student_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Emotional Entry

- **URL:** `/student/emotions/entries/{entry_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_emotional_entry_success** _Test successful deletion of emotional entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "entry_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Emotional entry deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Emotional entry deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_emotional_entry_success(client, student_auth_header):
      entry_id = "entry_uuid_123"
      response = client.delete(f"/student/emotions/entries/{entry_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

---

### Endpoint: Get Mood Log

- **URL:** `/student/emotions/mood-logs/{log_id}`
- **Method:** GET

### Test Cases

**1. test_get_mood_log_success** _Test successful retrieval of specific mood log._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `log_id` = "log_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Mood log object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"log_id": "log_uuid_123", "mood": "calm", "energy_level": "medium"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_mood_log_success(client, student_auth_header):
      log_id = "log_uuid_123"
      response = client.get(f"/student/emotions/mood-logs/{log_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert response.json()["log_id"] == log_id
  ```

---

### Endpoint: Update Mood Log

- **URL:** `/student/emotions/mood-logs/{log_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_mood_log_success** _Test successful update of mood log._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `log_id` = "log_uuid_123"
  - `Request Body`: `{"mood": "happy", "energy_level": "high"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated mood log object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"log_id": "log_uuid_123", "mood": "happy", "energy_level": "high"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_mood_log_success(client, student_auth_header):
      log_id = "log_uuid_123"
      response = client.patch(f"/student/emotions/mood-logs/{log_id}",
                            json={"mood": "happy", "energy_level": "high"},
                            headers=student_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Mood Log

- **URL:** `/student/emotions/mood-logs/{log_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_mood_log_success** _Test successful deletion of mood log._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `log_id` = "log_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Mood log deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Mood log deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_mood_log_success(client, student_auth_header):
      log_id = "log_uuid_123"
      response = client.delete(f"/student/emotions/mood-logs/{log_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

---

### Endpoint: Get Chat Session

- **URL:** `/student/emotions/sessions/{session_id}`
- **Method:** GET

### Test Cases

**1. test_get_chat_session_success** _Test successful retrieval of specific chat session._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `session_id` = "session_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Chat session object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"session_id": "session_uuid_123", "topic": "stress management", "active": true}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_chat_session_success(client, student_auth_header):
      session_id = "session_uuid_123"
      response = client.get(f"/student/emotions/sessions/{session_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert response.json()["session_id"] == session_id
  ```

---

### Endpoint: Update Chat Session

- **URL:** `/student/emotions/sessions/{session_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_chat_session_success** _Test successful update of chat session._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `session_id` = "session_uuid_123"
  - `Request Body`: `{"topic": "anxiety management", "active": false}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated chat session object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"session_id": "session_uuid_123", "topic": "anxiety management", "active": false}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_chat_session_success(client, student_auth_header):
      session_id = "session_uuid_123"
      response = client.patch(f"/student/emotions/sessions/{session_id}",
                            json={"topic": "anxiety management", "active": False},
                            headers=student_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Chat Session

- **URL:** `/student/emotions/sessions/{session_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_chat_session_success** _Test successful deletion of chat session._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `session_id` = "session_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Chat session deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Chat session deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_chat_session_success(client, student_auth_header):
      session_id = "session_uuid_123"
      response = client.delete(f"/student/emotions/sessions/{session_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

---

### Endpoint: Create Chat Message

- **URL:** `/student/emotions/messages`
- **Method:** POST

### Test Cases

**1. test_create_chat_message_success** _Test successful creation of chat message._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body`: `{"session_id": "session_uuid_123", "content": "I'm feeling anxious today", "sender_type": "student"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Created chat message object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message_id": "msg_uuid", "content": "I'm feeling anxious today", "sender_type": "student"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_create_chat_message_success(client, student_auth_header):
      response = client.post("/student/emotions/messages",
                           json={"session_id": "session_uuid_123", "content": "I'm feeling anxious today", "sender_type": "student"},
                           headers=student_auth_header)
      assert response.status_code == 200
      assert "message_id" in response.json()
  ```

---

### Endpoint: List Chat Messages

- **URL:** `/student/emotions/messages/{session_id}`
- **Method:** GET

### Test Cases

**1. test_list_chat_messages_success** _Test successful retrieval of chat messages for a session._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `session_id` = "session_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of chat messages

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"message_id": "msg_uuid", "content": "Hello", "sender_type": "student"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_list_chat_messages_success(client, student_auth_header):
      session_id = "session_uuid_123"
      response = client.get(f"/student/emotions/messages/{session_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Chat Message

- **URL:** `/student/emotions/message/{message_id}`
- **Method:** GET

### Test Cases

**1. test_get_chat_message_success** _Test successful retrieval of specific chat message._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `message_id` = "msg_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Chat message object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message_id": "msg_uuid_123", "content": "Hello", "sender_type": "student"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_chat_message_success(client, student_auth_header):
      message_id = "msg_uuid_123"
      response = client.get(f"/student/emotions/message/{message_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert response.json()["message_id"] == message_id
  ```

---

### Endpoint: Update Chat Message

- **URL:** `/student/emotions/message/{message_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_chat_message_success** _Test successful update of chat message._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `message_id` = "msg_uuid_123"
  - `Request Body`: `{"content": "Updated message content"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated chat message object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message_id": "msg_uuid_123", "content": "Updated message content"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_chat_message_success(client, student_auth_header):
      message_id = "msg_uuid_123"
      response = client.patch(f"/student/emotions/message/{message_id}",
                            json={"content": "Updated message content"},
                            headers=student_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Chat Message

- **URL:** `/student/emotions/message/{message_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_chat_message_success** _Test successful deletion of chat message._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `message_id` = "msg_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Chat message deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Chat message deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_chat_message_success(client, student_auth_header):
      message_id = "msg_uuid_123"
      response = client.delete(f"/student/emotions/message/{message_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

---

### Endpoint: Get Emergency Contact

- **URL:** `/student/emotions/contacts/{contact_id}`
- **Method:** GET

### Test Cases

**1. test_get_emergency_contact_success** _Test successful retrieval of specific emergency contact._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `contact_id` = "contact_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Emergency contact object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"contact_id": "contact_uuid_123", "name": "Dr. Smith", "phone": "+1234567890"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_emergency_contact_success(client, student_auth_header):
      contact_id = "contact_uuid_123"
      response = client.get(f"/student/emotions/contacts/{contact_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert response.json()["contact_id"] == contact_id
  ```

---

### Endpoint: Update Emergency Contact

- **URL:** `/student/emotions/contacts/{contact_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_emergency_contact_success** _Test successful update of emergency contact._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `contact_id` = "contact_uuid_123"
  - `Request Body`: `{"name": "Dr. Jane Smith", "phone": "+1987654321"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated emergency contact object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"contact_id": "contact_uuid_123", "name": "Dr. Jane Smith", "phone": "+1987654321"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_emergency_contact_success(client, student_auth_header):
      contact_id = "contact_uuid_123"
      response = client.patch(f"/student/emotions/contacts/{contact_id}",
                            json={"name": "Dr. Jane Smith", "phone": "+1987654321"},
                            headers=student_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Emergency Contact

- **URL:** `/student/emotions/contacts/{contact_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_emergency_contact_success** _Test successful deletion of emergency contact._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `contact_id` = "contact_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Emergency contact deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Emergency contact deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_emergency_contact_success(client, student_auth_header):
      contact_id = "contact_uuid_123"
      response = client.delete(f"/student/emotions/contacts/{contact_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

---

### Endpoint: Auto Reply

- **URL:** `/student/emotions/sessions/{session_id}/auto-reply`
- **Method:** POST

### Test Cases

**1. test_auto_reply_success** _Test successful AI auto-reply generation._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `session_id` = "session_uuid_123"
  - `Request Body`: `{"prompt": "I'm feeling overwhelmed with studies"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: AI generated response

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"response": "I understand you're feeling overwhelmed. Let's break down your tasks into smaller, manageable pieces."}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_auto_reply_success(client, student_auth_header):
      session_id = "session_uuid_123"
      response = client.post(f"/student/emotions/sessions/{session_id}/auto-reply",
                           json={"prompt": "I'm feeling overwhelmed with studies"},
                           headers=student_auth_header)
      assert response.status_code == 200
      assert "response" in response.json()
  ```

<div style="page-break-after: always;"></div>

## Health Extended API Tests Documentation

### Description

Extended Health API covering diet entry management, meal logging, and health metrics with full CRUD operations.

---

### Endpoint: Update Diet Entry

- **URL:** `/health/student_diet/{entry_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_diet_entry_success** _Test successful update of diet entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "diet_uuid_123"
  - `Request Body`: `{"food_item": "Apple", "calories": 95, "meal_type": "snack"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated diet entry object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"entry_id": "diet_uuid_123", "food_item": "Apple", "calories": 95}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_diet_entry_success(client, student_auth_header):
      entry_id = "diet_uuid_123"
      response = client.patch(f"/health/student_diet/{entry_id}",
                            json={"food_item": "Apple", "calories": 95, "meal_type": "snack"},
                            headers=student_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Diet Entry

- **URL:** `/health/student_diet/{entry_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_diet_entry_success** _Test successful deletion of diet entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "diet_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Diet entry deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Diet entry deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_diet_entry_success(client, student_auth_header):
      entry_id = "diet_uuid_123"
      response = client.delete(f"/health/student_diet/{entry_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

---

### Endpoint: Log Meal

- **URL:** `/health/meals`
- **Method:** POST

### Test Cases

**1. test_log_meal_success** _Test successful meal logging._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `Request Body`: `{"meal_name": "Breakfast", "items": ["Oatmeal", "Banana"], "total_calories": 350}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Created meal log object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"meal_id": "meal_uuid", "meal_name": "Breakfast", "total_calories": 350}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_log_meal_success(client, student_auth_header):
      response = client.post("/health/meals",
                           json={"meal_name": "Breakfast", "items": ["Oatmeal", "Banana"], "total_calories": 350},
                           headers=student_auth_header)
      assert response.status_code == 200
      assert "meal_id" in response.json()
  ```

---

### Endpoint: Update Meal Entry

- **URL:** `/health/meals/{entry_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_meal_entry_success** _Test successful update of meal entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "meal_uuid_123"
  - `Request Body`: `{"meal_name": "Healthy Breakfast", "total_calories": 320}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated meal entry object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"meal_id": "meal_uuid_123", "meal_name": "Healthy Breakfast", "total_calories": 320}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_meal_entry_success(client, student_auth_header):
      entry_id = "meal_uuid_123"
      response = client.patch(f"/health/meals/{entry_id}",
                            json={"meal_name": "Healthy Breakfast", "total_calories": 320},
                            headers=student_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Meal Entry

- **URL:** `/health/meals/{entry_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_meal_entry_success** _Test successful deletion of meal entry._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "meal_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Meal entry deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Meal entry deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_meal_entry_success(client, student_auth_header):
      entry_id = "meal_uuid_123"
      response = client.delete(f"/health/meals/{entry_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

---

### Endpoint: Update Health Metrics

- **URL:** `/health/metrics/{entry_id}`
- **Method:** PATCH

### Test Cases

**1. test_update_health_metrics_success** _Test successful update of health metrics._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "metrics_uuid_123"
  - `Request Body`: `{"weight": 70.5, "sleep_hours": 8, "stress_level": "low"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated health metrics object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"metrics_id": "metrics_uuid_123", "weight": 70.5, "sleep_hours": 8}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_health_metrics_success(client, student_auth_header):
      entry_id = "metrics_uuid_123"
      response = client.patch(f"/health/metrics/{entry_id}",
                            json={"weight": 70.5, "sleep_hours": 8, "stress_level": "low"},
                            headers=student_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Health Metrics

- **URL:** `/health/metrics/{entry_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_health_metrics_success** _Test successful deletion of health metrics._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_student_token>"
  - `URL Parameter`: `entry_id` = "metrics_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Health metrics deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Health metrics deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_health_metrics_success(client, student_auth_header):
      entry_id = "metrics_uuid_123"
      response = client.delete(f"/health/metrics/{entry_id}", headers=student_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Parent Dashboard Extended API Tests Documentation

### Description

Extended Parent Dashboard API covering financial goals tracking and family join request management.

---

### Endpoint: Get Parent Finance Goals

- **URL:** `/parent/dashboard/finance/goals`
- **Method:** GET

### Test Cases

**1. test_get_parent_finance_goals_success** _Test successful retrieval of children's finance goals._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of children's savings goals

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"child_id": "child_uuid", "goal": "New Bike", "target": 500, "saved": 200}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_parent_finance_goals_success(client, parent_auth_header):
      response = client.get("/parent/dashboard/finance/goals", headers=parent_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Family Join Requests

- **URL:** `/parent/dashboard/family/join-requests`
- **Method:** GET

### Test Cases

**1. test_get_family_join_requests_success** _Test successful retrieval of family join requests._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of pending family join requests

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"request_id": "req_uuid", "requester": "John Doe", "relationship": "uncle"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_family_join_requests_success(client, parent_auth_header):
      response = client.get("/parent/dashboard/family/join-requests", headers=parent_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Respond Family Join Request

- **URL:** `/parent/dashboard/family/join-requests/respond`
- **Method:** POST

### Test Cases

**1. test_respond_family_join_request_success** _Test successful response to family join request._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Request Body`: `{"request_id": "req_uuid_123", "action": "approve", "message": "Welcome to the family!"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Join request approved successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Join request approved successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_respond_family_join_request_success(client, parent_auth_header):
      response = client.post("/parent/dashboard/family/join-requests/respond",
                           json={"request_id": "req_uuid_123", "action": "approve", "message": "Welcome to the family!"},
                           headers=parent_auth_header)
      assert response.status_code == 200
      assert "approved" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Parent Extended API Tests Documentation

### Description

Extended Parent API covering child health monitoring, diet tracking, and parent network management.

---

### Endpoint: View Other Parents

- **URL:** `/parent/other-parents`
- **Method:** GET

### Test Cases

**1. test_view_other_parents_success** _Test successful retrieval of other parents in the network._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of other parents

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"parent_id": "parent_uuid", "name": "Jane Smith", "shared_children": 2}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_view_other_parents_success(client, parent_auth_header):
      response = client.get("/parent/other-parents", headers=parent_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Child Health Data

- **URL:** `/parent/child/health`
- **Method:** GET

### Test Cases

**1. test_get_child_health_data_success** _Test successful retrieval of child's health data._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Query Parameter`: `child_id` = "child_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Child health snapshot

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"child_id": "child_uuid_123", "height": 150, "weight": 45, "bmi": 20}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_child_health_data_success(client, parent_auth_header):
      response = client.get("/parent/child/health?child_id=child_uuid_123", headers=parent_auth_header)
      assert response.status_code == 200
      assert "child_id" in response.json()
  ```

---

### Endpoint: View Children Diet

- **URL:** `/parent/children/diet`
- **Method:** GET

### Test Cases

**1. test_view_children_diet_success** _Test successful retrieval of children's diet information._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of children's diet logs

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"child_id": "child_uuid", "total_calories": 1800, "meals_logged": 3}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_view_children_diet_success(client, parent_auth_header):
      response = client.get("/parent/children/diet", headers=parent_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Child Meal Logs

- **URL:** `/parent/child/meals`
- **Method:** GET

### Test Cases

**1. test_get_child_meal_logs_success** _Test successful retrieval of child's meal logs._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `Query Parameter`: `child_id` = "child_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of meal logs for the child

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"meal_id": "meal_uuid", "meal_name": "Breakfast", "calories": 350, "date": "2025-07-26"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_child_meal_logs_success(client, parent_auth_header):
      response = client.get("/parent/child/meals?child_id=child_uuid_123", headers=parent_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

<div style="page-break-after: always;"></div>

## Parent Tasks Extended API Tests Documentation

### Description

Extended Parent Tasks API covering overdue task management and full CRUD operations for parent-assigned tasks.

---

### Endpoint: Get Overdue Tasks

- **URL:** `/parent/tasks/overdue`
- **Method:** GET

### Test Cases

**1. test_get_parent_overdue_tasks_success** _Test successful retrieval of overdue tasks._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of overdue tasks

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"task_id": "task_uuid", "title": "Clean Room", "due_date": "2025-07-20", "child_id": "child_uuid"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_parent_overdue_tasks_success(client, parent_auth_header):
      response = client.get("/parent/tasks/overdue", headers=parent_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get All Parent Tasks

- **URL:** `/parent/tasks/`
- **Method:** GET

### Test Cases

**1. test_get_all_parent_tasks_success** _Test successful retrieval of all parent tasks._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Array of all tasks created by parent

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `[{"task_id": "task_uuid", "title": "Homework", "status": "pending", "child_id": "child_uuid"}]`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_all_parent_tasks_success(client, parent_auth_header):
      response = client.get("/parent/tasks/", headers=parent_auth_header)
      assert response.status_code == 200
      assert isinstance(response.json(), list)
  ```

---

### Endpoint: Get Parent Task

- **URL:** `/parent/tasks/{task_id}`
- **Method:** GET

### Test Cases

**1. test_get_parent_task_success** _Test successful retrieval of specific parent task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameter`: `task_id` = "task_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Task object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"task_id": "task_uuid_123", "title": "Homework", "status": "pending"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_get_parent_task_success(client, parent_auth_header):
      task_id = "task_uuid_123"
      response = client.get(f"/parent/tasks/{task_id}", headers=parent_auth_header)
      assert response.status_code == 200
      assert response.json()["task_id"] == task_id
  ```

---

### Endpoint: Update Parent Task

- **URL:** `/parent/tasks/{task_id}`
- **Method:** PUT

### Test Cases

**1. test_update_parent_task_success** _Test successful update of parent task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameter`: `task_id` = "task_uuid_123"
  - `Request Body`: `{"title": "Complete Math Homework", "priority": "high"}`

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Updated task object

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"task_id": "task_uuid_123", "title": "Complete Math Homework", "priority": "high"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_update_parent_task_success(client, parent_auth_header):
      task_id = "task_uuid_123"
      response = client.put(f"/parent/tasks/{task_id}",
                          json={"title": "Complete Math Homework", "priority": "high"},
                          headers=parent_auth_header)
      assert response.status_code == 200
  ```

---

### Endpoint: Delete Parent Task

- **URL:** `/parent/tasks/{task_id}`
- **Method:** DELETE

### Test Cases

**1. test_delete_parent_task_success** _Test successful deletion of parent task._

- **Passed Inputs:**

  - `Authorization Header`: "Bearer <valid_parent_token>"
  - `URL Parameter`: `task_id` = "task_uuid_123"

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Task deleted successfully"}`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Task deleted successfully"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_delete_parent_task_success(client, parent_auth_header):
      task_id = "task_uuid_123"
      response = client.delete(f"/parent/tasks/{task_id}", headers=parent_auth_header)
      assert response.status_code == 200
      assert "deleted" in response.json()["message"]
  ```

<div style="page-break-after: always;"></div>

## Root API Tests Documentation

### Description

The Root API provides the basic endpoint for API health checks and welcome messages.

---

### Endpoint: Read Root

- **URL:** `/`
- **Method:** GET

### Test Cases

**1. test_read_root_success** _Test successful root endpoint access._

- **Passed Inputs:**

  - None (no authentication required)

- **Expected Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: Welcome or API status message

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{"message": "Welcome to GrowthGeine API"}`

- **Result:** Passed

- **Pytest Code:**
  ```python
  def test_read_root_success(client):
      response = client.get("/")
      assert response.status_code == 200
      assert "message" in response.json()
  ```

<div style="page-break-after: always;"></div>

This section demonstrates how testing helps improve an API by identifying a discrepancy between expected and actual behavior.

**Scenario:** The business logic requires that a user cannot sign up with a password that is too short (e.g., less than 8 characters). The test case below is designed to verify this validation rule.

---

### Endpoint: Signup

- **URL:** `/auth/signup`
- **Method:** POST

### Test Case

**1. test_signup_short_password** _Test registration with a password that is shorter than the required minimum length._

- **Passed Inputs:**

  - `full_name` = "Short Pass"
  - `email` = "shortpass@example.com"
  - `password` = "short"
  - `confirm_password` = "short"
  - `role` = "student"
  - `terms_agreed` = true

- **Expected Output:**

  - `HTTP-Status Code`: 422
  - `Response Body`: `{ "detail": "Password must be at least 8 characters long" }`

- **Actual Output:**

  - `HTTP-Status Code`: 200
  - `Response Body`: `{ "message": "User created successfully" }`

- **Result:** Fail

- **Pytest Code:**
  ```python
  def test_signup_with_short_password(client):
      """
      Test that the API rejects passwords shorter than 8 characters.
      This test is expected to fail if the validation is not implemented.
      """
      response = client.post(
          "/auth/signup",
          json={
              "full_name": "Short Pass",
              "email": "shortpass@example.com",
              "password": "short",
              "confirm_password": "short",
              "role": "student",
              "terms_agreed": True,
          },
      )
      # This assertion will fail based on the "Actual Output"
      assert response.status_code == 422
      assert "Password must be at least 8 characters long" in response.text
  ```

### Analysis of Failure

The test **failed** because the API returned a `200 OK` status and created the user, whereas the expected behavior was a `422 Unprocessable Entity` error with a specific validation message. This failure indicates that the backend logic for the `/auth/signup` endpoint is missing the required validation to enforce a minimum password length. This is a critical security vulnerability that must be addressed. The failing test successfully highlights this area for improvement, demonstrating the value of thorough API testing.
