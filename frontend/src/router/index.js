import { createRouter, createWebHistory } from 'vue-router'
import { useStore } from 'vuex'

// Auth Views
import WelcomeView from '@/views/auth/WelcomeView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import SignupView from '@/views/auth/SignupView.vue'

// Student Views
import StudentDashboard from '@/views/student/DashboardView.vue'
import StudentFinView from '@/views/student/StudentFinView.vue'
import AddTransactions from '@/views/student/AddTransactions.vue'

// Parent Views
import ParentDashboard from '@/views/parent/DashboardView.vue'

// Teacher Views
import TeacherDashboard from '@/views/teacher/DashboardView.vue'

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
    { path: '/', name: 'Welcome', component: AddTransactions }, //WelcomeView
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
        name: 'ParentLayout',
        meta: { requiresAuth: true, role: 'parent' },
        children: [
            { path: '', name: 'ParentDashboard', component: ParentDashboard },
            { path: 'analytics', name: 'ParentAnalytics', component: PlaceholderView },
            { path: 'tasks', name: 'ParentTasks', component: PlaceholderView },
            { path: 'family', name: 'ParentFamily', component: PlaceholderView },
        ]
    },

    // Teacher Routes
    {
        path: '/teacher',
        name: 'TeacherLayout',
        meta: { requiresAuth: true, role: 'teacher' },
        children: [
            { path: '', name: 'TeacherDashboard', component: TeacherDashboard },
            { path: 'students', name: 'TeacherStudents', component: PlaceholderView },
            { path: 'tasks', name: 'TeacherTasks', component: PlaceholderView },
            { path: 'reports', name: 'TeacherReports', component: PlaceholderView },
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