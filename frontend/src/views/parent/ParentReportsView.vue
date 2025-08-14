<template>
  <div class="p-6 space-y-6">
    <div class="flex items-end gap-3">
      <div class="flex-1">
        <label class="block text-sm text-gray-600 mb-1">Select Child</label>
        <select v-model="selectedId" @change="loadReport" class="w-full border rounded px-3 py-2">
          <option disabled value="">Choose a student…</option>
          <option v-for="s in students" :key="s.student_id" :value="s.student_id">
            {{ s.full_name || s.email }}
          </option>
        </select>
      </div>
      <button class="px-4 py-2 bg-blue-600 text-white rounded" :disabled="!selectedId || loading.report" @click="loadReport">
        {{ loading.report ? 'Loading…' : 'Refresh' }}
      </button>
    </div>

    <div v-if="loading.students" class="text-sm text-gray-500">Loading children…</div>
    <div v-else-if="!students.length" class="text-sm text-gray-500">No student children found.</div>

    <div v-if="selectedId" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Medical Conditions -->
      <div class="bg-white rounded shadow p-4">
        <h2 class="font-semibold mb-2">Medical Conditions</h2>
        <div v-if="loading.report" class="text-sm text-gray-500">Loading…</div>
        <template v-else>
          <ul class="space-y-2" v-if="report.medical?.conditions?.length">
            <li v-for="c in report.medical.conditions" :key="c.condition_id" class="border rounded p-2">
              <div class="font-medium">{{ c.condition_name }} <span class="text-xs text-gray-500">({{ c.severity }})</span></div>
              <div class="text-xs text-gray-500" v-if="c.diagnosed_date">Diagnosed: {{ c.diagnosed_date }}</div>
              <div class="text-xs" v-if="c.dietary_restrictions">Restrictions: {{ c.dietary_restrictions }}</div>
            </li>
          </ul>
          <div v-else class="text-sm text-gray-500">No active conditions.</div>
        </template>
      </div>

      <!-- Medications & Logs (7d) -->
      <div class="bg-white rounded shadow p-4">
        <h2 class="font-semibold mb-2">Medications & Logs (7d)</h2>
        <div v-if="loading.report" class="text-sm text-gray-500">Loading…</div>
        <div v-else>
          <div>
            <div class="text-sm text-gray-700 mb-1">Medications</div>
            <ul class="space-y-2" v-if="report.medical?.medications?.length">
              <li v-for="m in report.medical.medications" :key="m.medication_id" class="border rounded p-2">
                <div class="font-medium">{{ m.medication_name }} — {{ m.dosage }} ({{ m.frequency }})</div>
                <div class="text-xs text-gray-500">{{ m.start_date }} <span v-if="m.end_date">→ {{ m.end_date }}</span></div>
              </li>
            </ul>
            <div v-else class="text-sm text-gray-500">No medications.</div>
          </div>
          <div class="mt-3">
            <div class="text-sm text-gray-700 mb-1">Recent Logs</div>
            <ul class="space-y-2 max-h-44 overflow-auto" v-if="report.medical?.medication_logs?.length">
              <li v-for="l in report.medical.medication_logs" :key="l.log_id" class="border rounded p-2">
                <div class="text-sm">Taken: {{ l.taken_at }}</div>
                <div class="text-xs text-gray-500">Qty: {{ l.quantity_taken }} • {{ l.notes }}</div>
              </li>
            </ul>
            <div v-else class="text-sm text-gray-500">No logs in last 7 days.</div>
          </div>
        </div>
      </div>

      <!-- Water Intake (Today) -->
      <div class="bg-white rounded shadow p-4">
        <h2 class="font-semibold mb-2">Water Intake (Today)</h2>
        <div v-if="loading.report" class="text-sm text-gray-500">Loading…</div>
        <div v-else>
          <div class="text-sm">Total: <span class="font-semibold">{{ report.water?.today_total_ml || 0 }} ml</span></div>
          <ul class="space-y-1 mt-2 max-h-44 overflow-auto" v-if="report.water?.logs?.length">
            <li v-for="w in report.water.logs" :key="w.intake_id" class="text-xs text-gray-700">
              {{ w.intake_time }} — {{ w.amount_ml }} ml ({{ w.container_type }})
            </li>
          </ul>
          <div v-else class="text-sm text-gray-500">No entries today.</div>
        </div>
      </div>

      <!-- Meals (Today) -->
      <div class="bg-white rounded shadow p-4">
        <h2 class="font-semibold mb-2">Meals (Today)</h2>
        <div v-if="loading.report" class="text-sm text-gray-500">Loading…</div>
        <template v-else>
          <ul class="space-y-2" v-if="report.meals?.length">
            <li v-for="m in report.meals" :key="m.id" class="border rounded p-2">
              <div class="font-medium">{{ m.mealtype }} — {{ m.description }}</div>
              <div class="text-xs text-gray-500">{{ m.time }}</div>
              <div class="text-xs">Calories: {{ m.calories }} • Sodium: {{ m.sodium }} • Sugar: {{ m.sugar }}</div>
            </li>
          </ul>
          <div v-else class="text-sm text-gray-500">No meals logged today.</div>
        </template>
      </div>

      <!-- Latest Health Metrics -->
      <div class="bg-white rounded shadow p-4">
        <h2 class="font-semibold mb-2">Latest Health Metrics</h2>
        <div v-if="loading.report" class="text-sm text-gray-500">Loading…</div>
        <div v-else-if="report.health_metrics_latest" class="grid grid-cols-2 gap-2 text-sm">
          <div>Weight: <span class="font-semibold">{{ report.health_metrics_latest.weight }}</span></div>
          <div>Height: <span class="font-semibold">{{ report.health_metrics_latest.height }}</span></div>
          <div>BMI: <span class="font-semibold">{{ report.health_metrics_latest.bmi }}</span></div>
          <div>BP: <span class="font-semibold">{{ report.health_metrics_latest.systolic }}/{{ report.health_metrics_latest.diastolic }}</span></div>
          <div>Sugar: <span class="font-semibold">{{ report.health_metrics_latest.blood_sugar }}</span></div>
          <div>HR: <span class="font-semibold">{{ report.health_metrics_latest.heart_rate }}</span></div>
          <div class="col-span-2 text-xs text-gray-500">{{ report.health_metrics_latest.created_at }}</div>
        </div>
        <div v-else class="text-sm text-gray-500">No metrics yet.</div>
      </div>

      <!-- Latest Nutrition Suggestion -->
      <div class="bg-white rounded shadow p-4 md:col-span-2">
        <h2 class="font-semibold mb-2">Latest Nutrition Suggestion</h2>
        <div v-if="loading.report" class="text-sm text-gray-500">Loading…</div>
        <div v-else-if="report.nutrition_suggestion_latest" class="space-y-2 text-sm">
          <div class="text-xs text-gray-500">Generated: {{ report.nutrition_suggestion_latest.generated_at }} ({{ report.nutrition_suggestion_latest.range_key }})</div>
          <div v-if="report.nutrition_suggestion_latest.suggestions?.overview">
            <span class="font-medium">Overview:</span> {{ report.nutrition_suggestion_latest.suggestions.overview }}
          </div>
          <div v-if="report.nutrition_suggestion_latest.suggestions?.macro_targets" class="grid grid-cols-3 gap-2">
            <div>Calories: {{ report.nutrition_suggestion_latest.suggestions.macro_targets.calories }}</div>
            <div>Proteins: {{ report.nutrition_suggestion_latest.suggestions.macro_targets.proteins }}</div>
            <div>Carbs: {{ report.nutrition_suggestion_latest.suggestions.macro_targets.carbs }}</div>
            <div>Fat: {{ report.nutrition_suggestion_latest.suggestions.macro_targets.fat }}</div>
            <div>Sodium: {{ report.nutrition_suggestion_latest.suggestions.macro_targets.sodium }}</div>
            <div>Sugar: {{ report.nutrition_suggestion_latest.suggestions.macro_targets.sugar }}</div>
          </div>
          <div v-if="report.nutrition_suggestion_latest.suggestions?.hydration_advice">
            <span class="font-medium">Hydration:</span> {{ report.nutrition_suggestion_latest.suggestions.hydration_advice }}
          </div>
          <div v-if="report.nutrition_suggestion_latest.suggestions?.alerts?.length">
            <div class="font-medium">Alerts</div>
            <ul class="list-disc ml-5 space-y-1">
              <li v-for="(a, i) in report.nutrition_suggestion_latest.suggestions.alerts" :key="i">{{ a }}</li>
            </ul>
          </div>
          <div v-if="report.nutrition_suggestion_latest.suggestions?.risks?.length">
            <div class="font-medium">Risks</div>
            <ul class="list-disc ml-5 space-y-1">
              <li v-for="(r, i) in report.nutrition_suggestion_latest.suggestions.risks" :key="i">{{ r }}</li>
            </ul>
          </div>
          <div v-if="report.nutrition_suggestion_latest.suggestions?.meal_plan?.length">
            <div class="font-medium">Meal Plan</div>
            <ul class="list-disc ml-5 space-y-2">
              <li v-for="(m, i) in report.nutrition_suggestion_latest.suggestions.meal_plan" :key="i">
                <div>{{ m.item || m.name }}</div>
                <div class="text-xs text-gray-500" v-if="m.time || m.timing">{{ m.time || m.timing }}</div>
                <div class="text-xs" v-if="m.notes">{{ m.notes }}</div>
              </li>
            </ul>
          </div>
          <div v-if="report.nutrition_suggestion_latest.suggestions?.notes">
            <div class="font-medium">Notes</div>
            <div>{{ report.nutrition_suggestion_latest.suggestions.notes }}</div>
          </div>
        </div>
        <div v-else class="text-sm text-gray-500">No suggestions yet.</div>
      </div>
    </div>
  </div>
</template>

<script>
import { parentReportsService } from '@/services/parentReportsService'

export default {
  name: 'ParentReportsView',
  data() {
    return {
      students: [],
      selectedId: '',
      report: {},
      loading: { students: false, report: false },
      error: '',
    }
  },
  computed: {
    token() {
      return this.$store.getters['auth/token']
    },
  },
  methods: {
    async loadStudents() {
      this.loading.students = true
      try {
        const data = await parentReportsService.listStudents(this.token)
        // Filter to ensure only children with student rows (defensive)
        this.students = (data || []).filter(x => x)
        if (!this.selectedId && this.students.length) {
          this.selectedId = this.students[0].student_id
          await this.loadReport()
        }
      } finally {
        this.loading.students = false
      }
    },
    async loadReport() {
      if (!this.selectedId) return
      this.loading.report = true
      try {
        this.report = await parentReportsService.getStudentReport(this.token, this.selectedId)
      } finally {
        this.loading.report = false
      }
    },
  },
  mounted() {
    this.loadStudents()
  }
}
</script>
