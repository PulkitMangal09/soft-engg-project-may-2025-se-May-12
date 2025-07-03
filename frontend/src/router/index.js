import { createRouter, createWebHistory } from 'vue-router'
import { useStore } from 'vuex'

// Auth Views
import WelcomeView from '@/views/auth/WelcomeView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import SignupView from '@/views/auth/SignupView.vue'

// Student Views
import StudentDashboard from '@/views/student/DashboardView.vue'

// Parent Views
import ParentLayout from '@/components/layout/ParentLayout.vue'
import ParentDashboard from '@/views/parent/DashboardView.vue'
import ParentFamilyGroupView from '@/views/parent/FamilyGroupView.vue'
import ParentAnalyticsView from '@/views/parent/AnalyticsView.vue'
import ParentChildAnalyticsView from '@/views/parent/ChildAnalyticsView.vue'
import ParentTasksView from '@/views/parent/TasksView.vue'
import ParentAssignTaskView from '@/views/parent/AssignTaskView.vue'
import ParentSettingsView from '@/views/parent/SettingsView.vue'

// Teacher Views
import TeacherLayout from '@/components/layout/TeacherLayout.vue'
import TeacherDashboard from '@/views/teacher/DashboardView.vue'
import MyStudentsView from '@/views/teacher/MyStudentsView.vue'
import ClassTasksView from '@/views/teacher/ClassTasksView.vue'
import ReportsView from '@/views/teacher/ReportsView.vue'

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

    // Student Routes
    {
        path: '/student',
        name: 'StudentLayout',
        meta: { requiresAuth: true, role: 'student' },
        children: [
            { path: '', name: 'StudentDashboard', component: StudentDashboard },
            { path: 'tasks', name: 'StudentTasks', component: PlaceholderView },
            { path: 'finance', name: 'StudentFinance', component: PlaceholderView },
            { path: 'emotion', name: 'StudentEmotion', component: PlaceholderView },
            { path: 'health', name: 'StudentHealth', component: PlaceholderView },
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
            { path: 'settings', name: 'ParentSettings', component: ParentSettingsView },
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