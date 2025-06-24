# Views Documentation

This document outlines all the views (pages) in the GrowthGeine application, organized by user role and functionality.

## 🔐 Authentication Views

### WelcomeView
**Path**: `/`  
**File**: `src/views/auth/WelcomeView.vue`

**Purpose**: Landing page with role selection for new users.

**Features**:
- Role selection (Student, Teacher, Parent)
- App branding and introduction
- Navigation to login/signup

**User Flow**:
1. User visits the application
2. Selects their role (Student/Teacher/Parent)
3. Clicks "Get Started" to go to signup
4. Can navigate to login if they already have an account

### LoginView  
**Path**: `/login/:role?`  
**File**: `src/views/auth/LoginView.vue`

**Purpose**: User authentication for all roles.

**Features**:
- Role-specific login forms
- Email/password authentication
- Social login options (Google, Apple)
- "Forgot Password" functionality
- Error handling and validation

**Props**:
- `role` (String): User role from URL parameter

**Role Variations**:
- **Student**: Basic email/password login
- **Teacher**: School email + district selection
- **Parent**: Standard login with phone number option

### SignupView
**Path**: `/signup/:role?`  
**File**: `src/views/auth/SignupView.vue`

**Purpose**: User registration for all roles.

**Features**:
- Role-specific registration forms
- Form validation
- Terms of service acceptance
- Email verification process

**Props**:
- `role` (String): User role from URL parameter

**Role-Specific Fields**:
- **Student**: Name, email, password, date of birth
- **Teacher**: Name, school email, employee ID, subject/grade
- **Parent**: Name, email, phone, relationship to child

## 👨‍🎓 Student Views

### Student Dashboard
**Path**: `/student`  
**File**: `src/views/student/DashboardView.vue`

**Purpose**: Central hub for student activities and overview.

**Features**:
- Quick action buttons
- Recent activity summary
- Health alerts and notifications
- Progress indicators
- Navigation to other modules

**Components Used**:
- AppCard for information display
- AppButton for quick actions
- Progress bars and statistics
- Health alert banners

### Student Tasks (Coming Soon)
**Path**: `/student/tasks`  
**File**: `src/views/student/TasksView.vue`

**Purpose**: Task management for students.

**Planned Features**:
- Create, edit, delete tasks
- Task categorization
- Due date management
- Progress tracking
- Reminders and notifications
- Priority levels

### Student Finance (Coming Soon)
**Path**: `/student/finance`  
**File**: `src/views/student/FinanceView.vue`

**Purpose**: Financial literacy and money management.

**Planned Features**:
- Expense tracking
- Budget categories
- Savings goals
- Transaction history
- Financial analytics
- Goal progress tracking

### Student Emotion (Coming Soon)
**Path**: `/student/emotion`  
**File**: `src/views/student/EmotionView.vue`

**Purpose**: Emotional wellbeing and mood tracking.

**Planned Features**:
- Mood diary entries
- Emotion analytics
- AI chat support
- Crisis helpline access
- Privacy controls
- Trend analysis

### Student Health (Coming Soon)
**Path**: `/student/health`  
**File**: `src/views/student/HealthView.vue`

**Purpose**: Health monitoring and diet tracking.

**Planned Features**:
- Food intake logging
- Water consumption tracking
- Medical condition management
- Medication reminders
- Health metrics (BMI, blood pressure)
- Parent-visible health alerts

## 👨‍👩‍👧‍👦 Parent Views

### Parent Dashboard
**Path**: `/parent`  
**File**: `src/views/parent/DashboardView.vue`

**Purpose**: Overview of all children's activities and health.

**Features**:
- Multi-child selector
- Health alerts and critical notifications
- Achievement summaries
- Quick action buttons
- Family group management

**Planned Enhancements**:
- Real-time health monitoring
- Task completion statistics
- Financial oversight
- Communication tools

### Parent Analytics (Coming Soon)
**Path**: `/parent/analytics`  
**File**: `src/views/parent/AnalyticsView.vue`

**Purpose**: Detailed analytics and reports for children.

**Planned Features**:
- Performance comparisons
- Trend analysis
- Health reports
- Academic progress
- Behavioral insights
- Downloadable reports

### Parent Tasks (Coming Soon)
**Path**: `/parent/tasks`  
**File**: `src/views/parent/TasksView.vue`

**Purpose**: Task assignment and monitoring for children.

**Planned Features**:
- Assign tasks to children
- Monitor completion rates
- Set rewards and consequences
- Create recurring tasks
- Template management

### Parent Family (Coming Soon)
**Path**: `/parent/family`  
**File**: `src/views/parent/FamilyView.vue`

**Purpose**: Family group management and settings.

**Planned Features**:
- Add/remove family members
- Manage join requests
- Set permissions
- Family settings
- Invite other parents/guardians

## 👨‍🏫 Teacher Views

### Teacher Dashboard
**Path**: `/teacher`  
**File**: `src/views/teacher/DashboardView.vue`

**Purpose**: Classroom overview and student monitoring.

**Features**:
- Classroom statistics
- Student health alerts
- Task completion overview
- Quick access to student profiles

**Planned Enhancements**:
- Real-time classroom status
- Urgent health notifications
- Performance analytics
- Communication tools

### Teacher Students (Coming Soon)
**Path**: `/teacher/students`  
**File**: `src/views/teacher/StudentsView.vue`

**Purpose**: Student list and individual monitoring.

**Planned Features**:
- Student roster
- Individual student profiles
- Health status indicators
- Academic performance tracking
- Communication with parents
- Filter and search capabilities

### Teacher Tasks (Coming Soon)
**Path**: `/teacher/tasks`  
**File**: `src/views/teacher/TasksView.vue`

**Purpose**: Classroom task management.

**Planned Features**:
- Assign tasks to entire class
- Individual task assignments
- Completion tracking
- Grade management
- Template creation
- Due date management

### Teacher Reports (Coming Soon)
**Path**: `/teacher/reports`  
**File**: `src/views/teacher/ReportsView.vue`

**Purpose**: Classroom analytics and reporting.

**Planned Features**:
- Class performance reports
- Individual student reports
- Health summary reports
- Export capabilities
- Trend analysis
- Parent communication tools

## 🔧 Utility Views

### PlaceholderView
**File**: `src/views/PlaceholderView.vue`

**Purpose**: Temporary view for features under development.

**Features**:
- "Coming Soon" message
- Navigation back to appropriate dashboard
- Role-aware routing

### NotFoundView (404)
**Purpose**: Handle invalid routes.

**Features**:
- 404 error message
- Navigation back to home
- Clean error presentation

## 🗂 View Structure Patterns

### Standard Layout
Most views follow this structure:

```vue
<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header (if needed) -->
    <AppHeader :title="pageTitle" />
    
    <!-- Main content -->
    <main class="pb-20 pt-4">
      <div class="max-w-7xl mx-auto px-4">
        <!-- Page content -->
      </div>
    </main>
    
    <!-- Bottom navigation (mobile) -->
    <AppBottomNav />
  </div>
</template>
```

### Data Patterns
Views typically include:

```javascript
export default {
  name: 'ViewName',
  data() {
    return {
      loading: false,
      error: null,
      // View-specific data
    }
  },
  
  computed: {
    // Vuex state/getters
    ...mapState('module', ['data']),
    ...mapGetters('auth', ['userRole'])
  },
  
  methods: {
    // Vuex actions
    ...mapActions('module', ['fetchData']),
    
    // View-specific methods
  },
  
  async created() {
    // Initialize data
    await this.fetchData()
  }
}
```

## 🔄 Navigation Flow

### Authentication Flow
```
WelcomeView → LoginView/SignupView → Role-specific Dashboard
```

### Student Flow
```
Student Dashboard → Tasks/Finance/Emotion/Health → Back to Dashboard
```

### Parent Flow  
```
Parent Dashboard → Analytics/Tasks/Family → Child-specific views
```

### Teacher Flow
```
Teacher Dashboard → Students/Tasks/Reports → Individual student views
```

## 📱 Responsive Design

All views are designed with mobile-first approach:

- **Mobile**: Single column, bottom navigation
- **Tablet**: Optimized spacing, side navigation option
- **Desktop**: Multi-column layouts, full navigation

## 🔐 Route Protection

Views include meta properties for access control:

```javascript
meta: { 
  requiresAuth: true,    // Requires login
  role: 'student'        // Requires specific role
}