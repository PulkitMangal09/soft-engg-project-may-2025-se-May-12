<template>
    <!-- Dummy Navigation Bar -->
<nav class="bg-white shadow-md px-6 py-4 flex items-center justify-between mb-6 rounded-xl">
  <!-- Logo / Brand -->
  <div class="text-xl font-bold text-blue-600">
    💼 GrowthGenie
  </div>

  <!-- Menu Items -->
  <ul class="hidden md:flex gap-6 text-gray-700 font-medium">
    <li><a href="#" class="hover:text-blue-600">Dashboard</a></li>
    <li><a href="#" class="hover:text-blue-600">Transactions</a></li>
    <li><a href="#" class="hover:text-blue-600">Savings</a></li>
    <li><a href="#" class="hover:text-blue-600">Learn</a></li>
  </ul>

  <!-- User / Settings -->
  <div class="text-sm text-gray-600">
    Hello, Student 👋
  </div>
</nav>
<div class="max-w-7xl mx-auto px-4">

    <!-- Summary Boxes -->
<div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
  <!-- Balance -->
  <div class="bg-blue-100 text-blue-900 p-4 rounded-xl shadow">
    <div class="text-sm font-medium">Balance</div>
    <div class="text-xl font-bold">₹660</div>
  </div>

  <!-- Income -->
  <div class="bg-green-100 text-green-900 p-4 rounded-xl shadow">
    <div class="text-sm font-medium">Income</div>
    <div class="text-xl font-bold">₹700</div>
  </div>

  <!-- Expenses -->
  <div class="bg-red-100 text-red-900 p-4 rounded-xl shadow">
    <div class="text-sm font-medium">Expenses</div>
    <div class="text-xl font-bold">₹40</div>
  </div>

  <!-- Savings -->
  <div class="bg-yellow-100 text-yellow-900 p-4 rounded-xl shadow">
    <div class="text-sm font-medium">Savings</div>
    <div class="text-xl font-bold">₹850</div>
  </div>

  <!-- Add Transaction Button -->
  <div class="flex items-center justify-center">
    <button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg w-full">
      + Add Transaction
    </button>
  </div>
</div>
</div>
<!-- Lower Section: Chart + Savings -->
<div class="grid grid-cols-1 md:grid-cols-12 gap-6">

  <!-- 📈 Money Flow Chart -->
  <div class="col-span-12 md:col-span-8 bg-white p-4 rounded-xl shadow">
    <h2 class="text-lg font-bold mb-4">Money Flow</h2>
    <!-- Chart placeholder -->
    <div class="h-64 flex items-center justify-center text-gray-400 bg-gray-50 rounded-lg">
      [Line Chart Placeholder]
       <!-- <Line :data="moneyFlowData" :options="chartOptions" /> -->

    </div>
  </div>

  <!-- 🐷 Savings Goals Box -->
  <div class="col-span-12 md:col-span-4 bg-white p-4 rounded-xl shadow flex flex-col">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold">My Savings</h2>
      <button class="text-sm text-blue-600 hover:underline">See All</button>
    </div>

    <div v-for="goal in savingsGoals" :key="goal.id" class="mb-4">
      <div class="flex justify-between text-sm font-medium mb-1">
        <span>{{ goal.title }}</span>
        <span>₹{{ goal.saved }}/₹{{ goal.target }}</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-3">
        <div
          class="bg-green-500 h-3 rounded-full"
          :style="{ width: (goal.saved / goal.target * 100) + '%' }"
        ></div>
      </div>
    </div>
  </div>

</div>

<!-- Bottom Row: Pie Chart + Transaction History -->
<div class="grid grid-cols-1 md:grid-cols-12 gap-6 mt-6">

  <!-- 📊 Expenses Overview (70%) -->
  <div class="col-span-12 md:col-span-8 bg-white p-4 rounded-xl shadow relative">
    
    <!-- Slicer -->
    <div class="absolute top-4 right-4">
      <select class="border border-gray-300 rounded px-2 py-1 text-sm">
        <option>1 Month</option>
        <option>3 Months</option>
        <option>6 Months</option>
      </select>
    </div>

    <h2 class="text-lg font-bold mb-4">Expense Breakdown</h2>

    <div class="grid grid-cols-12 items-center">
      
      <!-- Summary -->
      <div class="col-span-4 text-sm space-y-2">
        <div>
          <div class="font-semibold">Today</div>
          <div class="text-gray-600">₹80</div>
        </div>
        <div>
          <div class="font-semibold">This Week</div>
          <div class="text-gray-600">₹450</div>
        </div>
        <div>
          <div class="font-semibold">This Month</div>
          <div class="text-gray-600">₹1100</div>
        </div>
      </div>

      <!-- Pie Chart Placeholder -->
      <div class="col-span-8">
        <div class="h-56 flex items-center justify-center bg-gray-50 rounded-lg text-gray-400">
          [Pie Chart Placeholder]
        </div>
      </div>

    </div>
  </div>

  <!-- 📄 Transaction History (30%) -->
  <div class="col-span-12 md:col-span-4 bg-white p-4 rounded-xl shadow overflow-y-auto max-h-80">
    <h2 class="text-lg font-bold mb-4">Transaction History</h2>
    <ul class="divide-y">
      <li v-for="tx in transactions" :key="tx.id" class="py-3 flex justify-between text-sm">
        <div>
          <div class="font-medium">{{ tx.category }}</div>
          <div class="text-gray-500">{{ tx.note }} · {{ tx.date }}</div>
        </div>
        <div :class="tx.type === 'income' ? 'text-green-600' : 'text-red-500'">
          {{ tx.type === 'income' ? '+' : '-' }}₹{{ tx.amount }}
        </div>
      </li>
    </ul>
  </div>

</div>
</template>

<script setup>



const transactions = [
  { id: 1, type: 'income', category: 'Pocket Money', note: 'From Dad', amount: 200, date: '2025-06-24' },
  { id: 2, type: 'expense', category: 'Snacks', note: 'Ice cream', amount: 40, date: '2025-06-25' },
  { id: 3, type: 'income', category: 'Gift', note: 'Birthday', amount: 500, date: '2025-06-20' },
  { id: 4, type: 'expense', category: 'Toys', note: 'Puzzle', amount: 100, date: '2025-06-22' },
  { id: 5, type: 'expense', category: 'Stationery', note: 'Notebooks', amount: 80, date: '2025-06-23' },
];

const moneyFlowData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Income',
      data: [500, 700, 650, 800, 600, 750],
      borderColor: '#22c55e', // green
      backgroundColor: 'rgba(34,197,94,0.2)',
      tension: 0.3,
      fill: true,
    },
    {
      label: 'Expenses',
      data: [300, 450, 400, 550, 380, 500],
      borderColor: '#ef4444', // red
      backgroundColor: 'rgba(239,68,68,0.2)',
      tension: 0.3,
      fill: true,
    },
  ]
};
const savingsGoals = [
  {
    id: 1,
    title: 'Gaming PC',
    target: 5000,
    saved: 2300
  },
  {
    id: 2,
    title: 'Football',
    target: 1200,
    saved: 950
  },
  {
    id: 3,
    title: 'Wireless Headphones',
    target: 3000,
    saved: 800
  },
  {
    id: 4,
    title: 'Field Trip Fund',
    target: 2000,
    saved: 1400
  },
  {
    id: 5,
    title: 'LEGO Set',
    target: 1800,
    saved: 1000
  }
];


</script>
<script>
export default {
    name: 'StudentFinView'
}
</script>

<style scoped>
/* Optional custom styles here */
</style>
