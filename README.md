# Growth Genie

Growth Genie is a comprehensive life skills application designed for school-aged children. This full-stack web application, built with a Python backend and a Vue.js frontend, empowers students, parents, and teachers to collaborate on developing essential life skills in areas such as financial literacy, health and wellness, and personal responsibility.

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database & Auth**: Supabase
- **Data Validation**: Pydantic
- **Testing**: Pytest

### Frontend
- **Framework**: Vue.js
- **Build Tool**: Vite
- **Routing**: Vue Router
- **State Management**: Vuex
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

## Features

### Student Features

*   **Dashboard**: Provides a centralized overview and quick access to all key modules.
*   **Task Management**: Allows students to manage their responsibilities efficiently.
    *   Create, update, and delete personal tasks.
    *   View tasks assigned by parents and teachers.
    *   Filter tasks by type (personal, parent-assigned, teacher-assigned) and status.
*   **Financial Literacy**: Equips students with tools for money management.
    *   Track income, expenses, and view current balance.
    *   Set, manage, and contribute to savings goals.
    *   Log financial transactions.
*   **Emotional Well-being**: Supports students' mental health with private and secure tools.
    *   Log daily moods and maintain a personal diary.
    *   Access a chat support system and an emergency help feature.
    *   View mood history and summaries.
*   **Health and Nutrition**: Helps students monitor and manage their physical health with comprehensive tools.
    *   **Medical Records**: Log and manage health conditions, medications, and medication intake schedules.
    *   **AI Dietitian Chat**: Get personalized dietary advice and meal ideas through an interactive AI chatbot.
    *   **AI Nutrition Suggestions**: Generate detailed nutrition reports based on health data (including meal logs, water intake, health metrics, and medical conditions). The report provides an overview, macro-nutrient targets, hydration advice, risk alerts, and meal recommendations.
    *   Track daily calorie and water intake, and log meals and physical metrics (e.g., weight, BMI).
*   **Connections**: Manage connections with parents and teachers to share progress and information securely.
    *   View connected parents and teachers.
    *   Manage pending connection requests.
    *   Understand data sharing and privacy settings for each connection.

### Parent Features

*   **Family Management**:
    *   Create, edit, and manage multiple family groups.
    *   Generate unique invitation codes for children and other parents to join a family group.
    *   Review and manage join requests from other users.
    *   View all members within a family group and their respective roles.
    *   Join other family groups using an invitation code.

*   **Dashboard & Child Monitoring**:
    *   View a centralized dashboard with key metrics for all connected children, including active tasks and pending requests.
    *   Select a specific child to view their detailed analytics.
    *   **Financial Oversight**: Monitor a child's financial savings goals and view a detailed, filterable history of their transactions (income/expense).

*   **Health & Nutrition Reporting**:
    *   Select a child to view a comprehensive health report.
    *   Monitor medical conditions, medications, and recent medication logs.
    *   Track daily water and meal intake, including nutritional details.
    *   View the latest recorded health metrics (e.g., weight, BMI, blood pressure).
    *   Review the latest AI-generated nutrition suggestions, including dietary advice, meal plans, and health alerts.

*   **Task Assignment & Tracking**:
    *   Assign tasks to children with specific details, including a title, description, due date, category, priority, and reward points.
    *   Track the status of all assigned tasks (e.g., Pending, Overdue, Completed).
    *   Edit assigned tasks and mark them as complete.

### Teacher Features

*   **Dashboard & Overview**:
    *   A centralized dashboard displaying key metrics like total students, total classrooms, and urgent alerts for overdue tasks and student health conditions.
    *   View a list of all created classrooms with their status.
    *   See a breakdown of students by grade level.

*   **Classroom & Student Management**:
    *   Create, edit, and delete classrooms with details like name, subject, and grade level.
    *   View connected students and parents within classrooms.
    *   Manage connection requests from students and parents.
    *   Generate unique invitation codes to invite students and parents to specific classrooms.

*   **Task Management**:
    *   Assign tasks to individual students or entire classes with details like title, due date, and priority.
    *   Track class-wide task statistics, including active, overdue, and completion rates.
    *   View recent and overdue tasks for the entire class.

*   **Student Reporting & Monitoring**:
    *   Select a student to view their comprehensive individual report.
    *   Monitor academic performance, including task completion rates and trends.
    *   Access a student's health summary, including medical conditions.
    *   Review detailed AI-generated nutrition reports and alerts for students.
    *   Access a parent's emergency contact number to make a call.

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- `pip` and `npm`

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the `backend` directory and add your Supabase URL and key.
    ```
    NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
    NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
    GOOGLE_API_KEY=your_google_api_key
    NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
    ```

5.  **Run the backend server:**
    ```bash
    python main.py
    ```
    The server will be running at `http://127.0.0.1:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

4.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:5173`.