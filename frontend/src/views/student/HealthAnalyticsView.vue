<template>
    <div class="min-h-screen bg-gray-50">
        <StudentNavBar />
        <div class="flex flex-col items-center py-6 px-2 md:px-0">
            <div class="bg-white rounded-xl shadow p-6 w-full max-w-md mb-4">
                <div class="mb-4">
                    <select class="form-select w-full">
                        <option>This Week</option>
                        <option>This Month</option>
                        <option>Last 3 Months</option>
                    </select>
                </div>
                <div class="bg-green-50 border-l-4 border-green-400 rounded-lg p-4 mb-4">
                    <div class="font-semibold mb-2">Nutritional Summary</div>
                    <div class="text-xs text-gray-700">
                        <strong>Average Daily Intake:</strong><br>
                        Calories: 1,850 (Target: 2,000)<br>
                        Sugar: 45g (⚠️ Above 35g limit)<br>
                        Sodium: 2,800mg (⚠️ Above 2,300mg limit)
                    </div>
                </div>
                <div class="bg-orange-50 border-l-4 border-orange-400 rounded-lg p-4 mb-4">
                    <div class="font-semibold mb-2">AI Recommendations</div>
                    <div class="text-xs text-gray-700">
                        🚫 <strong>Reduce:</strong> Spicy foods, processed snacks<br>
                        ❌ <strong>Avoid:</strong> Sweets, high-sodium foods<br>
                        ✅ <strong>Increase:</strong> Fresh fruits, vegetables, water<br>
                        💊 <strong>Remember:</strong> Take insulin before meals
                    </div>
                </div>
                <div class="bg-gray-50 rounded-lg p-4 mb-4">
                    <div class="font-semibold mb-2">Weight Trends</div>
                    <div class="flex justify-between items-center mb-2 text-xs">
                        <span>Current: 65.2kg</span>
                        <span class="text-green-600">↓ -0.8kg this month</span>
                    </div>
                    <div class="w-full h-2 bg-gray-200 rounded">
                        <div class="h-2 bg-green-500 rounded" style="width: 65%"></div>
                    </div>
                    <div class="text-[10px] text-gray-500 mt-1">Target range: 60-70kg</div>
                </div>
                <div class="bg-gray-50 rounded-lg p-4 mb-2">
                    <div class="font-semibold mb-2">Blood Sugar Levels</div>
                    <div class="text-xs text-gray-700 mb-1">
                        Last reading: 128 mg/dL (2 hours ago)<br>
                        <span class="text-orange-500">Slightly elevated</span>
                    </div>
                    <div class="text-[10px] text-gray-500">Target: 80-130 mg/dL before meals</div>
                </div>
            </div>
            <div class="text-xs text-gray-400 mt-4">Health Analytics</div>
        </div>
    </div>
</template>

<script setup>
import StudentNavBar from '@/components/layout/StudentNavBar.vue'
// Placeholder logic for select and analytics
</script>