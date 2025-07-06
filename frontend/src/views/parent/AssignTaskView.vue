<template>
  <div class="bg-gray-100 font-sans p-4 md:p-6">
    <div class="max-w-2xl mx-auto">
      <AppCard title="Assign Task" icon="💾">
        <form @submit.prevent="assignTask" class="space-y-6">
          <!-- Assign To -->
          <div>
            <label for="assignTo" class="block text-sm font-medium text-gray-700">Assign To</label>
            <select id="assignTo" v-model="task.assignee" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
              <option disabled value="">Select a child</option>
              <option v-for="child in children" :key="child.id" :value="child.id">{{ child.name }}</option>
            </select>
          </div>

          <!-- Task Title -->
          <div>
            <label for="taskTitle" class="block text-sm font-medium text-gray-700">Task Title</label>
            <input type="text" id="taskTitle" v-model="task.title" placeholder="Enter task title" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
          </div>

          <!-- Category, Due Date, Priority -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label for="category" class="block text-sm font-medium text-gray-700">Category</label>
              <select id="category" v-model="task.category" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option>Academic</option>
                <option>Chores</option>
                <option>Health</option>
                <option>Creative</option>
              </select>
            </div>
            <div>
              <label for="dueDate" class="block text-sm font-medium text-gray-700">Due Date</label>
              <input type="date" id="dueDate" v-model="task.dueDate" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
            </div>
            <div>
              <label for="priority" class="block text-sm font-medium text-gray-700">Priority</label>
              <select id="priority" v-model="task.priority" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
              </select>
            </div>
          </div>

          <!-- Description -->
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
            <textarea id="description" v-model="task.description" rows="4" placeholder="Enter task description and instructions" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"></textarea>
          </div>

          <!-- Reward Points -->
          <div>
            <label for="rewardPoints" class="block text-sm font-medium text-gray-700">Reward Points</label>
            <input type="number" id="rewardPoints" v-model.number="task.rewardPoints" placeholder="Enter points value" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
          </div>

          <!-- Attachments -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Attachments</label>
            <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
              <div class="space-y-1 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true"><path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
                <div class="flex text-sm text-gray-600">
                  <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                    <span>📎 Add Files</span>
                    <input id="file-upload" name="file-upload" type="file" class="sr-only">
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Reminders -->
          <div class="flex items-center">
            <input id="reminders" v-model="task.reminders" type="checkbox" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
            <label for="reminders" class="ml-2 block text-sm text-gray-900">Enable daily reminders</label>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end space-x-4">
            <AppButton type="button" label="Save as Template" variant="secondary" />
            <AppButton type="submit" label="Assign Task" variant="primary" />
          </div>
        </form>
      </AppCard>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'

export default {
  name: 'ParentAssignTaskView',
  components: {
    AppCard,
    AppButton,
  },
  setup() {
    const children = ref([
      { id: 1, name: 'John Jr.' },
      { id: 2, name: 'Emma' },
      { id: 3, name: 'Sophie' },
    ])

    const task = ref({
      assignee: '',
      title: '',
      category: 'Academic',
      dueDate: '',
      priority: 'Low',
      description: '',
      rewardPoints: null,
      reminders: false,
    })

    function assignTask() {
      // Here you would typically dispatch an action to a Vuex store
      // or send the data to an API.
      console.log('Assigning task:', task.value)
      alert('Task assigned successfully!')
    }

    return {
      children,
      task,
      assignTask,
    }
  },
}
</script>
