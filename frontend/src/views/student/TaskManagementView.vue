<template>
  <div class="min-h-screen bg-gray-50 p-4">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-1">Task Management</h1>
      <p class="text-gray-600">Organize your tasks and stay on top of your work</p>
    </div>

    <!-- Add New Task -->
    <div class="bg-white rounded-xl shadow-sm p-4 mb-6">
      <div class="flex items-center">
        <input 
          type="text" 
          v-model="newTask"
          @keyup.enter="addTask"
          placeholder="Add a new task..."
          class="flex-1 border-0 focus:ring-0 focus:outline-none text-gray-700"
        >
        <button 
          @click="addTask"
          class="ml-2 p-2 bg-blue-100 text-blue-600 rounded-full hover:bg-blue-200 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Task List -->
    <div class="space-y-3">
      <div 
        v-for="(task, index) in tasks" 
        :key="index"
        class="bg-white rounded-xl shadow-sm p-4 flex items-center"
      >
        <button 
          @click="toggleTask(index)"
          class="mr-3 flex-shrink-0 h-5 w-5 rounded-full border-2 flex items-center justify-center"
          :class="task.completed ? 'bg-green-100 border-green-500' : 'border-gray-300'"
        >
          <svg v-if="task.completed" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-green-600" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        <span 
          class="flex-1"
          :class="{ 'line-through text-gray-400': task.completed }"
        >
          {{ task.text }}
        </span>
        <button 
          @click="deleteTask(index)"
          class="text-gray-400 hover:text-red-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="tasks.length === 0" class="text-center py-8">
        <div class="text-gray-400 mb-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <p class="text-gray-500">No tasks yet. Add one above!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newTask = ref('');
const tasks = ref(JSON.parse(localStorage.getItem('tasks')) || []);

const addTask = () => {
  if (newTask.value.trim() === '') return;
  
  tasks.value.push({
    text: newTask.value,
    completed: false,
    createdAt: new Date().toISOString()
  });
  
  saveTasks();
  newTask.value = '';
};

const toggleTask = (index) => {
  tasks.value[index].completed = !tasks.value[index].completed;
  saveTasks();
};

const deleteTask = (index) => {
  tasks.value.splice(index, 1);
  saveTasks();
};

const saveTasks = () => {
  localStorage.setItem('tasks', JSON.stringify(tasks.value));
};
</script>
