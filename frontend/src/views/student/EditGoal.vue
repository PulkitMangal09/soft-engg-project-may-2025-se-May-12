<template>
  <div class="max-w-md mx-auto p-4 bg-white rounded-lg shadow">
    <h2 class="text-xl font-bold mb-4">Edit Goal</h2>
    <form @submit.prevent="submitForm">
      <div class="mb-4">
        <label class="block text-gray-700">Title</label>
        <input
          v-model="form.title"
          type="text"
          class="w-full px-3 py-2 border rounded"
          :placeholder="originalGoal.title || 'Goal Title'"
        />
      </div>

      <div class="mb-4">
        <label class="block text-gray-700">Target Amount</label>
        <input
          v-model="form.target_amount"
          type="number"
          step="0.01"
          class="w-full px-3 py-2 border rounded"
          :placeholder="originalGoal.target_amount || 'Target Amount'"
        />
      </div>

      <div class="mb-4">
        <label class="block text-gray-700">Saved Amount</label>
        <input
          v-model="form.saved_amount"
          type="number"
          step="0.01"
          class="w-full px-3 py-2 border rounded"
          :placeholder="originalGoal.saved_amount || 'Saved Amount'"
         required/>
      </div>

      <button
        type="submit"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Save Changes
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { updateGoal } from "@/services/finservice";
import { useRoute } from "vue-router";

export default {
  name: "EditGoal",
  data() {
    return {
      form: {
        title: "",
        target_amount: "",
        saved_amount: ""
      },
      originalGoal: {},
      goalId: null
    };
  },
  async mounted() {
    const route = useRoute(); // ✅ Get route object
    this.goalId = route.params.id;

    try {
      const { data } = await axios.get(`/student/finance/goal/${this.goalId}`);
      this.originalGoal = data;
      this.form = {
        title: data.title || "",
        target_amount: data.target_amount || "",
        saved_amount: data.saved_amount || ""
      };
    } catch (err) {
      console.error("Failed to fetch goal:", err);
    }
  },
  methods: {
    
async submitForm() {
  try {
    await updateGoal(this.goalId, this.form);
    this.$emit("goal-updated");
    this.$router.push('/student/finance'); // ✅ use this.$router
  } catch (err) {
    console.error("Failed to update goal:", err);
  }
}
  }
};
</script>
