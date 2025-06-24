<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
        <div class="text-center p-8">
            <div class="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center text-4xl mb-6 mx-auto">
                🚧
            </div>
            <h1 class="text-3xl font-bold text-gray-900 mb-4">Coming Soon</h1>
            <p class="text-gray-600 mb-6">This feature is under development and will be available soon.</p>
            <div class="space-y-2">
                <router-link :to="goBackRoute"
                    class="inline-block bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors">
                    Go Back
                </router-link>
                <div>
                    <router-link to="/" class="text-blue-500 hover:underline text-sm">
                        Return to Home
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PlaceholderView',
    computed: {
        goBackRoute() {
            const path = this.$route.path
            if (path.includes('/student')) return '/student'
            if (path.includes('/parent')) return '/parent'
            if (path.includes('/teacher')) return '/teacher'
            return '/'
        }
    }
}
</script>