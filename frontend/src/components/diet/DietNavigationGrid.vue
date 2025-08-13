<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 mt-8">
    <router-link 
      v-for="(card, index) in cardData"
      :key="index"
      :to="card.to"
      class="bg-white rounded-2xl p-4 md:p-6 flex flex-col items-center justify-center text-center shadow-md transition-all duration-300 ease-in-out transform hover:-translate-y-1 hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-indigo-200"
    >
      <div 
        class="w-14 h-14 md:w-16 md:h-16 rounded-full flex items-center justify-center mb-2 md:mb-3 text-3xl md:text-4xl"
        :class="card.colorClass"
      >
        {{ card.icon }}
      </div>
      <span class="font-bold text-sm md:text-base text-gray-800">{{ card.title }}</span>
      <span class="text-xs text-gray-500 mt-1">{{ card.subtitle }}</span>
    </router-link>
  </div>
</template>

<script setup>
import { reactive } from 'vue';

const cardData = reactive([
  {
    to: "/student/food-log",
    icon: "📊",
    title: "Food Log",
    subtitle: "View Today's Meals",
    colorClass: "bg-blue-100 text-blue-600"
  },
  {
    to: "/student/medical-conditions",
    icon: "🏥",
    title: "Medical",
    subtitle: "Conditions & meds",
    colorClass: "bg-green-100 text-green-600"
  },
  {
    to: "/student/diet-chatbot",
    icon: "🤖",
    title: "AI Assistant",
    subtitle: "Get dietary advice",
    colorClass: "bg-purple-100 text-purple-600"
  },
  {
    to: "/student/water",
    icon: "💧",
    title: "Water Tracker",
    subtitle: "Track hydration",
    colorClass: "bg-cyan-100 text-cyan-600"
  },
  {
    to: "/student/nutrition-suggestions",
    icon: "🥗",
    title: "Suggestions",
    subtitle: "AI nutrition tips",
    colorClass: "bg-orange-100 text-orange-600"
  },
  {
    to: "/student/health-metrics",
    icon: "📏",
    title: "Metrics",
    subtitle: "Update health data",
    colorClass: "bg-yellow-100 text-yellow-600"
  }
]);
</script>

<style scoped>
/* Scoped styles are not strictly necessary with Tailwind, but can be used for custom overrides */
</style>