import { createRouter, createWebHistory } from 'vue-router'
import { useStore } from 'vuex'

// Auth Views
import WelcomeView from '@/views/auth/WelcomeView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import SignupView from '@/views/auth/SignupView.vue'
import ProfileCompletionView from '@/views/auth/ProfileCompletionView.vue'


// Student Views
import StudentDashboard from '@/views/student/DashboardView.vue'
import StudentFinView from '@/views/student/StudentFinView.vue'
import EmotionView from '@/views/student/EmotionView.vue'
import NewEmotionEntryView from '@/views/student/NewEmotionEntryView.vue'
import AllEmotionEntriesView from '@/views/student/AllEmotionEntriesView.vue'
import BreathingExerciseView from '@/views/student/BreathingExerciseView.vue'
import ChatSupportView from '@/views/student/ChatSupportView.vue'
import EmergencyHelpView from '@/views/student/EmergencyHelpView.vue'
import EditEmotionEntryView from '@/views/student/EditEmotionEntryView.vue'
import DiaryView from '@/views/student/DiaryView.vue'
import NewDiaryEntryView from '@/views/student/NewDiaryEntryView.vue'
import EditDiaryEntryView from '@/views/student/EditDiaryEntryView.vue'
import AddTransactions from '@/views/student/AddTransactions.vue'
import TaskManagementView from '@/views/student/TaskManagementView.vue'
import FinanceView from '@/views/student/FinanceView.vue'
import DietView from '@/views/student/DietView.vue'
import WaterTrackerView from '@/views/student/WaterTrackerView.vue'
import MedicalConditionsView from '@/views/student/MedicalConditionsView.vue'
import MedicalReportsView from '@/views/student/MedicalReportsView.vue'
import HealthAnalyticsView from '@/views/student/HealthAnalyticsView.vue'
import NutritionSuggestionsView from '@/views/student/NutritionSuggestionsView.vue'
import HealthMetricsUpdateView from '@/views/student/HealthMetricsUpdateView.vue'
import DietChatBotView from '@/views/student/DietChatBotView.vue'
import FoodLogView from '@/views/student/FoodLogView.vue'
import StudentConnectionsView from '@/views/student/StudentConnectionsView.vue'
import JoinConnectionView from '@/views/student/JoinConnectionView.vue'
import EditTransaction from '@/views/student/EditTransaction.vue'
import AddSavingGoal from '@/views/student/AddSavingGoal.vue'
import EditGoal from '@/views/student/EditGoal.vue'

// Insights Views
import MoodInsights from '@/views/student/insights/MoodInsights.vue'
import ActivityPatterns from '@/views/student/insights/ActivityPatterns.vue'
import WeeklyReports from '@/views/student/insights/WeeklyReports.vue'

// Settings Views
import AccountSettings from '@/views/student/settings/AccountSettings.vue'
import PrivacySettings from '@/views/student/settings/PrivacySettings.vue'
import NotificationSettings from '@/views/student/settings/NotificationSettings.vue'

// Support Views
import HelpCenter from '@/views/student/support/HelpCenter.vue'
import ContactSupport from '@/views/student/support/ContactSupport.vue'

// Parent Views
import ParentLayout from '@/components/layout/ParentLayout.vue'
import ParentDashboard from '@/views/parent/DashboardView.vue'
import ParentFamilyGroupView from '@/views/parent/FamilyGroupView.vue'
import ParentAnalyticsView from '@/views/parent/AnalyticsView.vue'
import ParentChildAnalyticsView from '@/views/parent/ChildAnalyticsView.vue'
import ParentTasksView from '@/views/parent/TasksView.vue'
import ParentAssignTaskView from '@/views/parent/AssignTaskView.vue'
import ParentReportsView from '@/views/parent/ParentReportsView.vue'
import JoinFamilyView from '@/views/parent/JoinFamilyView.vue'

// Teacher Views  
import TeacherLayout from '@/components/layout/TeacherLayout.vue'
import TeacherDashboard from '@/views/teacher/DashboardView.vue'
import MyStudentsView from '@/views/teacher/MyStudentsView.vue'
import ClassTasksView from '@/views/teacher/ClassTasksView.vue'
import ReportsView from '@/views/teacher/ReportsView.vue'
import components from '@/components/index'

// Placeholder component for missing views
const PlaceholderView = {
  template: `
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">Coming Soon</h1>
        <p class="text-gray-600 mb-4">This feature is under development.</p>
        <router-link to="/" class="text-blue-500 hover:underline">Go back to home</router-link>
      </div>
    </div>
  `
}

const routes = [
  // Auth Routes
  { path: '/', name: 'Welcome', component: WelcomeView },
  { path: '/login/:role?', name: 'Login', component: LoginView, props: true },
  { path: '/signup/:role?', name: 'Signup', component: SignupView, props: true },
  { path: '/:role?/profile', name: 'ProfileCompletion', component: ProfileCompletionView, props: true },

  // // Student Routes
  // {
  //     path: '/student',
  //     name: 'StudentLayout',
  //     meta: { requiresAuth: true, role: 'student' },
  //     children: [
  //         { path: '', name: 'StudentDashboard', component: StudentDashboard },
  //         { path: 'tasks', name: 'StudentTasks', component: PlaceholderView },
  //         { path: 'finance', name: 'StudentFinance', component: PlaceholderView },
  //         { path: 'emotion', name: 'StudentEmotion', component: PlaceholderView },
  //         { path: 'health', name: 'StudentHealth', component: PlaceholderView },
  //     ]
  // },

  // Student Routes
  {
    path: '/student',
    name: 'StudentLayout',
    meta: { requiresAuth: false, role: 'student' },
    children: [
      { path: '', name: 'StudentDashboard', component: StudentDashboard },
      {
        path: 'tasks',
        name: 'TaskManagement',
        component: TaskManagementView,
        meta: { title: 'Task Management' }
      },
      {
        path: 'finance',
        name: 'Finance',
        component: FinanceView,
        meta: { title: 'Finance Management' }
      },
      {
        path: 'health',
        name: 'Diet',
        component: DietView,
        meta: { title: 'Diet & Nutrition' }
      },
      {
        path: "Addtransaction",
        name: "addtransaction",
        component: AddTransactions
      },
      {
        path: "EditTransaction/:id",
        name: "edittransaction",
        component: EditTransaction
      },
      {
        path: 'add-goal',
        name: 'AddGoal',
        component: AddSavingGoal // lazy-load
      },
      {
        path: 'add-goal/:id',
        name: 'EditGoal',
        component: EditGoal// lazy-load
      },
      { path: 'my-connections', name: 'StudentConnections', component: StudentConnectionsView },
      { path: 'connections', name: 'JoinConnection', component: JoinConnectionView },
      { path: 'emotion', name: 'StudentEmotion', component: EmotionView },
      { path: 'emotion/new', name: 'NewEmotionEntry', component: NewEmotionEntryView },
      { path: 'emotion/all', name: 'AllEmotionEntries', component: AllEmotionEntriesView },
      { path: 'emotion/exercise', name: 'BreathingExercise', component: BreathingExerciseView },
      { path: 'emotion/chat', name: 'ChatSupport', component: ChatSupportView },
      { path: 'emotion/edit/:id', name: 'EditEmotionEntry', component: EditEmotionEntryView, props: true },
      { path: 'emotion/emergency', name: 'EmergencyHelp', component: EmergencyHelpView },

      // Diary routes
      { path: 'diary', name: 'DiaryView', component: DiaryView },
      { path: 'diary/new', name: 'NewDiaryEntry', component: NewDiaryEntryView },
      { path: 'diary/edit/:id', name: 'EditDiaryEntry', component: EditDiaryEntryView, props: true },

      // Insights routes
      { path: 'insights', redirect: '/student/insights/mood' },
      { path: 'insights/mood', name: 'MoodInsights', component: MoodInsights },
      { path: 'insights/patterns', name: 'ActivityPatterns', component: ActivityPatterns },
      { path: 'insights/reports', name: 'WeeklyReports', component: WeeklyReports },

      // Settings routes
      { path: 'settings/account', name: 'AccountSettings', component: AccountSettings },
      { path: 'settings/privacy', name: 'PrivacySettings', component: PrivacySettings },
      { path: 'settings/notifications', name: 'NotificationSettings', component: NotificationSettings },

      // Support routes
      { path: 'support/help', name: 'HelpCenter', component: HelpCenter },
      { path: 'support/contact', name: 'ContactSupport', component: ContactSupport },
      { path: 'water', name: 'WaterTracker', component: WaterTrackerView },
      { path: 'medical-conditions', name: 'MedicalConditions', component: MedicalConditionsView },
      { path: 'medical-reports', name: 'MedicalReports', component: MedicalReportsView },
      { path: 'health-analytics', name: 'HealthAnalytics', component: HealthAnalyticsView },
      { path: 'nutrition-suggestions', name: 'NutritionSuggestions', component: NutritionSuggestionsView },
      { path: 'health-metrics', name: 'HealthMetricsUpdate', component: HealthMetricsUpdateView },
      { path: 'diet-chatbot', name: 'DietChatBot', component: DietChatBotView },
      { path: 'food-log', name: 'FoodLog', component: FoodLogView },
    ]
  },


  // Parent Routes
  {
    path: '/parent',
    component: ParentLayout,
    meta: { requiresAuth: true, role: 'parent' },
    children: [
      { path: '', redirect: '/parent/dashboard' },
      { path: 'dashboard', name: 'ParentDashboard', component: ParentDashboard },
      { path: 'family', name: 'ParentFamilyGroup', component: ParentFamilyGroupView },
      { path: 'analytics', name: 'ParentAnalytics', component: ParentAnalyticsView },
      { path: 'analytics/:childId', name: 'ParentChildAnalytics', component: ParentChildAnalyticsView, props: true },
      { path: 'tasks', name: 'ParentTasks', component: ParentTasksView },
      { path: 'tasks/assign', name: 'ParentAssignTask', component: ParentAssignTaskView },
      { path: 'reports', name: 'ParentReports', component: ParentReportsView },
      { path: 'join-family', name: 'JoinFamily', component: JoinFamilyView },
    ]
  },

  // Teacher Routes
  {
    path: '/teacher',
    component: TeacherLayout,
    meta: { requiresAuth: true, role: 'teacher' },
    children: [
      { path: '', name: 'Dashboard', component: TeacherDashboard },
      { path: 'students', name: 'My Students', component: MyStudentsView },
      { path: 'tasks', name: 'Tasks', component: ClassTasksView },
      { path: 'reports', name: 'Reports', component: ReportsView },
    ]
  },

  // Fallback route for 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: {
      template: `
        <div class="min-h-screen bg-gray-50 flex items-center justify-center">
          <div class="text-center">
            <h1 class="text-4xl font-bold text-gray-900 mb-4">404</h1>
            <p class="text-gray-600 mb-4">Page not found</p>
            <router-link to="/" class="text-blue-500 hover:underline">Go back to home</router-link>
          </div>
        </div>
      `
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  // Skip auth check if store is not available yet
  try {
    const store = useStore()
    const isAuthenticated = store.getters['auth/isAuthenticated']
    const userRole = store.getters['auth/userRole']

    if (to.meta.requiresAuth && !isAuthenticated) {
      next('/login')
    } else if (to.meta.role && userRole !== to.meta.role) {
      next(`/${userRole}`)
    } else {
      next()
    }
  } catch (error) {
    // If store is not available, allow navigation (will be handled by components)
    next()
  }
})

export default router