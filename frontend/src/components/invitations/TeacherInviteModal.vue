<!-- src/components/invitations/TeacherInviteModal.vue -->
<template>
  <teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center">
      <!-- backdrop -->
      <div class="absolute inset-0 bg-black/40" @click="handleClose"></div>

      <!-- modal -->
      <div class="relative z-10 w-full max-w-lg rounded-xl bg-white p-6 shadow-xl">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold">Generate Invitation Code</h3>
          <button class="text-gray-500 hover:text-gray-700" @click="handleClose">✕</button>
        </div>

        <form @submit.prevent="generate" class="space-y-4">
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Invite Type</label>
            <select v-model="type" class="w-full rounded-md border px-3 py-2">
              <option value="teacher_student">Student Invitation</option>
              <option value="parent_student">Parent Invitation</option>
            </select>
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Classroom</label>
            <select v-model="classroomId" class="w-full rounded-md border px-3 py-2">
              <option disabled value="">Select a classroom…</option>
              <option
                v-for="c in classrooms"
                :key="c.classroom_id"
                :value="c.classroom_id"
              >
                {{ c.classroom_name || c.name }} ({{ c.classroom_key }})
              </option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-sm font-medium text-gray-700">Expires in (hours)</label>
              <select v-model.number="expiresIn" class="w-full rounded-md border px-3 py-2">
                <option :value="24">24</option>
                <option :value="48">48</option>
                <option :value="168">168 (1 week)</option>
              </select>
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium text-gray-700">Max Uses</label>
              <input v-model.number="maxUses" type="number" min="1" class="w-full rounded-md border px-3 py-2" />
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-2">
            <button type="button" class="rounded-md bg-gray-100 px-3 py-2 hover:bg-gray-200" @click="handleClose">
              Cancel
            </button>
            <button type="submit" class="rounded-md bg-blue-600 px-3 py-2 text-white hover:bg-blue-700" :disabled="loading">
              {{ loading ? 'Generating…' : 'Generate Code' }}
            </button>
          </div>
        </form>

        <!-- Result -->
        <div v-if="generatedCode" class="mt-6 rounded-lg bg-gray-50 p-4">
          <p class="mb-2 text-sm text-gray-600">Share this code:</p>
          <div class="flex items-center gap-2">
            <code class="rounded border bg-white px-3 py-2 text-lg font-mono">{{ generatedCode }}</code>
            <button class="rounded-md bg-gray-200 px-2 py-1 text-sm hover:bg-gray-300" @click="copy">
              Copy
            </button>
          </div>
          <p class="mt-2 text-xs text-gray-500">Expires in {{ expiresIn }} hours · Max uses: {{ maxUses || 1 }}</p>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useStore } from 'vuex'
import { invitationService } from '@/services/invitationService'

const props = defineProps({
  isOpen: { type: Boolean, required: true },
  classrooms: { type: Array, default: () => [] },
  defaultType: { type: String, default: 'teacher_student' },
  preselectedClassroomId: { type: String, default: '' },
})
const emit = defineEmits(['close', 'generated'])

const store = useStore()
const token = computed(() => store.getters['auth/token'] || store.state.auth?.token || '')

const type = ref(props.defaultType)
const classroomId = ref(props.preselectedClassroomId || '')
const expiresIn = ref(24)
const maxUses = ref(1)
const loading = ref(false)
const generatedCode = ref('')

watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      // reset each time we open
      type.value = props.defaultType
      classroomId.value = props.preselectedClassroomId || ''
      expiresIn.value = 24
      maxUses.value = 1
      generatedCode.value = ''
    }
  }
)

const handleClose = () => emit('close')

const generate = async () => {
  if (!token.value || !classroomId.value) return
  loading.value = true
  try {
    const exp = new Date()
    exp.setHours(exp.getHours() + Number(expiresIn.value))
    const payload = {
      target_type: 'classroom',
      target_id: classroomId.value,
      relation_type: type.value,       // teacher_student | parent_student
      max_uses: maxUses.value || 1,
      expires_at: exp.toISOString(),
    }
    const res = await invitationService.generateCode(payload, token.value)
    generatedCode.value = res.code
    emit('generated', res)
  } catch (e) {
    console.error('Generate code error:', e)
    store.dispatch('ui/showToast', {
      title: 'Error',
      message: e?.response?.data?.detail || 'Failed to generate code',
      type: 'error',
    })
  } finally {
    loading.value = false
  }
}

const copy = async () => {
  try {
    await navigator.clipboard.writeText(generatedCode.value)
    store.dispatch('ui/showToast', { title: 'Copied', message: 'Code copied to clipboard', type: 'success' })
  } catch {}
}
</script>
