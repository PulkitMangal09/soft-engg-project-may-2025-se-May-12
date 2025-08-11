<template>
    <div class="grid grid-cols-4 gap-4 mt-8">
        <router-link to="/student/food-log"
            class="bg-white rounded-xl p-6 flex flex-col items-center shadow hover:border-indigo-500 border-2 border-transparent transition">
            <span class="text-3xl mb-1">📊</span>
            <span class="font-semibold text-sm text-gray-800">View Today's Meals</span>
            <span class="text-xs text-gray-400">Food Log</span>
        </router-link>
        <!-- <router-link to="/student/health-analytics"
            class="bg-white rounded-xl p-6 flex flex-col items-center shadow hover:border-indigo-500 border-2 border-transparent transition">
            <span class="text-3xl mb-1">📈</span>
            <span class="font-semibold text-sm text-gray-800">Analytics</span>
            <span class="text-xs text-gray-400">Health insights</span>
        </router-link> -->
        <router-link to="/student/medical-conditions"
            class="bg-white rounded-xl p-6 flex flex-col items-center shadow hover:border-indigo-500 border-2 border-transparent transition">
            <span class="text-3xl mb-1">🏥</span>
            <span class="font-semibold text-sm text-gray-800">Medical</span>
            <span class="text-xs text-gray-400">Conditions & meds</span>
        </router-link>
        <router-link to="/student/diet-chatbot"
            class="bg-white rounded-xl p-6 flex flex-col items-center shadow hover:border-indigo-500 border-2 border-transparent transition">
            <span class="text-3xl mb-1">🤖</span>
            <span class="font-semibold text-sm text-gray-800">AI Assistant</span>
            <span class="text-xs text-gray-400">Get dietary advice</span>
        </router-link>
        <router-link to="/student/water"
            class="bg-white rounded-xl p-6 flex flex-col items-center shadow hover:border-indigo-500 border-2 border-transparent transition">
            <span class="text-3xl mb-1">💧</span>
            <span class="font-semibold text-sm text-gray-800">Water Tracker</span>
            <span class="text-xs text-gray-400">Track hydration</span>
        </router-link>
        <!-- <router-link to="/student/medical-reports"
            class="bg-white rounded-xl p-6 flex flex-col items-center shadow hover:border-indigo-500 border-2 border-transparent transition">
            <span class="text-3xl mb-1">📄</span>
            <span class="font-semibold text-sm text-gray-800">Reports</span>
            <span class="text-xs text-gray-400">Medical reports</span>
        </router-link> -->
        <router-link to="/student/nutrition-suggestions"
            class="bg-white rounded-xl p-6 flex flex-col items-center shadow hover:border-indigo-500 border-2 border-transparent transition">
            <span class="text-3xl mb-1">🥗</span>
            <span class="font-semibold text-sm text-gray-800">Suggestions</span>
            <span class="text-xs text-gray-400">AI nutrition tips</span>
        </router-link>
        <router-link to="/student/health-metrics"
            class="bg-white rounded-xl p-6 flex flex-col items-center shadow hover:border-indigo-500 border-2 border-transparent transition">
            <span class="text-3xl mb-1">📏</span>
            <span class="font-semibold text-sm text-gray-800">Metrics</span>
            <span class="text-xs text-gray-400">Update health data</span>
        </router-link>
    </div>
</template>