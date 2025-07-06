<template>
  <div class="p-6 md:p-8 bg-gray-100 min-h-screen">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Class Tasks</h1>
        <p class="text-lg text-gray-600 mt-1">Manage and track all class assignments.</p>
      </div>
    </div>

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <AppCard title="Active Tasks">
        <p class="text-3xl font-bold text-indigo-600">15</p>
      </AppCard>
      <AppCard title="Overdue" variant="error">
        <p class="text-3xl font-bold text-red-500">5</p>
      </AppCard>
      <AppCard title="Completion Rate" variant="success">
        <p class="text-3xl font-bold text-emerald-500">85%</p>
      </AppCard>
      <AppCard title="Total This Month">
        <p class="text-3xl font-bold text-gray-800">156</p>
      </AppCard>
    </div>

    <!-- Main Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left Column: Recent Tasks -->
      <div class="lg:col-span-2 space-y-8">
        <AppCard title="Recent Tasks" icon="📋">
           <template #action>
            <AppButton label="View All" variant="secondary" size="sm" />
          </template>
          <ul class="space-y-4">
            <li class="p-4 border rounded-lg bg-white">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-bold text-gray-800">Budget Analysis Project</h4>
                  <p class="text-sm text-gray-500">Due: Tomorrow • Assigned to: All students</p>
                </div>
                <AppBadge variant="success">23/28 completed</AppBadge>
              </div>
              <div class="mt-3 h-2 bg-gray-200 rounded-full">
                <div class="h-2 bg-emerald-500 rounded-full" style="width: 82%;"></div>
              </div>
            </li>
            <li class="p-4 border rounded-lg bg-white">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-bold text-gray-800">Financial Planning Quiz</h4>
                  <p class="text-sm text-gray-500">Due: Today • Assigned to: All students</p>
                </div>
                <AppBadge variant="warning">15/28 completed</AppBadge>
              </div>
              <div class="mt-3 h-2 bg-gray-200 rounded-full">
                <div class="h-2 bg-amber-500 rounded-full" style="width: 54%;"></div>
              </div>
            </li>
            <li class="p-4 border rounded-lg bg-white">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-bold text-gray-800">Investment Portfolio Analysis</h4>
                  <p class="text-sm text-gray-500">Due: Next Week • Assigned to: Advanced Group</p>
                </div>
                <AppBadge>8/12 completed</AppBadge>
              </div>
              <div class="mt-3 h-2 bg-gray-200 rounded-full">
                <div class="h-2 bg-indigo-500 rounded-full" style="width: 67%;"></div>
              </div>
            </li>
          </ul>
        </AppCard>
      </div>

      <!-- Right Column: Overdue & Actions -->
      <div class="space-y-8">
        <AppCard title="Overdue Tasks (5)" icon="⚠️" variant="error">
          <p class="text-sm text-gray-600 mb-3">Financial Planning Project (3 students)</p>
          <p class="text-sm text-gray-600 mb-4">Budget Analysis Assignment (2 students)</p>
          <p class="text-xs text-gray-500">Due: 2-3 days ago • Affected: Michael R., Alex T., others</p>
          <template #footer>
            <div class="flex justify-end">
              <AppButton label="Send Reminders" variant="primary" />
            </div>
          </template>
        </AppCard>
        
        <AppCard title="Actions">
            <div class="grid grid-cols-1 gap-3">
                <AppButton label="New Task" icon="📝" variant="secondary" />
                <AppButton label="Analytics" icon="📊" variant="secondary" />
                <AppButton label="Templates" icon="📋" variant="secondary" />
            </div>
        </AppCard>
      </div>
    </div>
  </div>
</template>

<script>
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

export default {
  name: 'ClassTasksView',
  components: { AppCard, AppButton, AppBadge },
}
</script>
