<template>
  <AppModal :is-open="isOpen" @close="handleClose" title="Generate Invitation Code">
    <div class="space-y-6" v-if="!generatedCode">
      <!-- Invite For -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Invitation For</label>
        <select
          v-model="form.inviteFor"
          class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option v-if="canInviteStudents" value="student">Student (Join Classroom)</option>
          <option v-if="canInviteParents" value="parent">Parent (Join Family)</option>
        </select>
        <p v-if="!canInviteStudents && !canInviteParents" class="text-sm text-red-600 mt-2">
          No available targets. Add a classroom or a family group first.
        </p>
      </div>

      <!-- Classroom select (for student) -->
      <div v-if="form.inviteFor === 'student'">
        <label class="block text-sm font-medium text-gray-700 mb-2">Classroom</label>
        <select
          v-model="form.classroom_id"
          class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option disabled value="">Select a classroom</option>
          <option
            v-for="c in classrooms"
            :key="c.classroom_id || c.id"
            :value="c.classroom_id || c.id"
          >
            {{ c.classroom_name || c.name }} • {{ c.subject || 'No subject' }}
          </option>
        </select>
      </div>

      <!-- Family select (for parent) -->
      <div v-if="form.inviteFor === 'parent'">
        <label class="block text-sm font-medium text-gray-700 mb-2">Family Group</label>
        <select
          v-model="form.family_id"
          class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
        >
          <option disabled value="">Select a family group</option>
          <option
            v-for="f in families"
            :key="f.family_id"
            :value="f.family_id"
          >
            {{ f.family_name }} • {{ f.description || 'No description' }}
          </option>
        </select>
      </div>

      <!-- Expiration + max uses -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Expires In</label>
          <select v-model.number="form.expiresIn" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
            <option :value="24">24 hours</option>
            <option :value="48">48 hours</option>
            <option :value="168">1 week</option>
            <option :value="0">No expiry</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Max Uses</label>
          <input
            v-model.number="form.maxUses"
            type="number"
            min="1"
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            placeholder="1"
          />
        </div>
      </div>

      <div class="flex justify-end space-x-3">
        <AppButton label="Cancel" variant="secondary" @click="handleClose" />
        <AppButton
          label="Generate Code"
          variant="primary"
          :disabled="disableGenerate"
          :loading="submitting"
          @click="generate"
        />
      </div>
    </div>

    <!-- Generated -->
    <div v-else class="space-y-6">
      <div class="text-center">
        <div class="bg-gray-100 p-6 rounded-lg">
          <p class="text-sm text-gray-600 mb-2">Share this code:</p>
          <div class="flex items-center justify-center space-x-2">
            <code class="text-2xl font-mono font-bold text-indigo-600 bg-white px-4 py-2 rounded border">
              {{ generatedCode }}
            </code>
            <AppButton label="Copy" icon="📋" size="sm" variant="secondary" @click="copy" />
          </div>
          <p class="mt-3 text-xs text-gray-500">
            {{ summaryText }}
          </p>
        </div>
      </div>

      <div class="flex justify-end">
        <AppButton label="Done" variant="primary" @click="handleClose(true)" />
      </div>
    </div>
  </AppModal>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useStore } from 'vuex'
import AppModal from '@/components/ui/AppModal.vue'
import AppButton from '@/components/ui/AppButton.vue'
import { invitationService } from '@/services/invitationService'

// PROPS
const props = defineProps({
  isOpen: { type: Boolean, default: false },
  // For teacher flow (student invite)
  classrooms: { type: Array, default: () => [] },
  // For parent flow (parent invite)
  families: { type: Array, default: () => [] },
})

const emit = defineEmits(['close', 'generated'])

const store = useStore()
const token = computed(() => store.getters['auth/token'] || store.state.auth?.token || '')

const canInviteStudents = computed(() => (props.classrooms || []).length > 0)
const canInviteParents  = computed(() => (props.families || []).length > 0)

// form state
const form = ref({
  inviteFor: 'student',   // 'student' | 'parent'
  classroom_id: '',
  family_id: '',
  expiresIn: 24,          // hours; 0 = no expiry
  maxUses: 1,
})

watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      // default inviteFor to whatever we can actually invite
      if (canInviteStudents.value) form.value.inviteFor = 'student'
      else if (canInviteParents.value) form.value.inviteFor = 'parent'
      // reset
      form.value.classroom_id = ''
      form.value.family_id = ''
      form.value.expiresIn = 24
      form.value.maxUses = 1
      generatedCode.value = ''
      submitting.value = false
    }
  }
)

const submitting = ref(false)
const generatedCode = ref('')

const disableGenerate = computed(() => {
  if (!token.value) return true
  if (form.value.inviteFor === 'student') return !form.value.classroom_id
  if (form.value.inviteFor === 'parent') return !form.value.family_id
  return true
})

const summaryText = computed(() => {
  if (form.value.inviteFor === 'student') {
    return `Student invite • Classroom ${form.value.classroom_id} • Expires in ${form.value.expiresIn || '∞'}h • Max uses ${form.value.maxUses || '∞'}`
  }
  return `Parent invite • Family ${form.value.family_id} • Expires in ${form.value.expiresIn || '∞'}h • Max uses ${form.value.maxUses || '∞'}`
})

const generate = async () => {
  try {
    submitting.value = true
    if (!token.value) throw new Error('Not authenticated')

    // Build payload for /codes
    const expiresAtISO = (() => {
      if (!form.value.expiresIn || form.value.expiresIn === 0) return null
      const d = new Date()
      d.setHours(d.getHours() + Number(form.value.expiresIn))
      return d.toISOString()
    })()

    const payload =
      form.value.inviteFor === 'student'
        ? {
            target_type: 'classroom',
            target_id: form.value.classroom_id,
            expires_at: expiresAtISO,
            max_uses: form.value.maxUses || null,
          }
        : {
            target_type: 'family',
            target_id: form.value.family_id,
            expires_at: expiresAtISO,
            max_uses: form.value.maxUses || null,
          }

    const res = await invitationService.generateCode(payload, token.value)
    generatedCode.value = res?.code || ''
    emit('generated', res)
    store.dispatch('ui/showToast', {
      title: 'Success',
      message: 'Invitation code generated',
      type: 'success',
    })
  } catch (e) {
    console.error('Generate code error:', e)
    store.dispatch('ui/showToast', {
      title: 'Error',
      message: e?.response?.data?.detail || 'Failed to generate code',
      type: 'error',
    })
  } finally {
    submitting.value = false
  }
}

const copy = () => {
  if (!generatedCode.value) return
  navigator.clipboard.writeText(generatedCode.value)
  store.dispatch('ui/showToast', {
    title: 'Copied',
    message: 'Code copied to clipboard',
    type: 'success',
  })
}

const handleClose = (wasDone = false) => {
  emit('close', wasDone)
}
</script>
