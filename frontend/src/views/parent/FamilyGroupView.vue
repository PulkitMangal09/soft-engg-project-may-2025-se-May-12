<!-- src/views/parent/FamilyGroupView.vue -->
<template>
  <div class="bg-gray-100 font-sans p-4 md:p-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:justify-between md:items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">Family Groups</h1>
        <p class="text-sm text-gray-500">Create a family before generating invitation codes</p>
      </div>
      <div class="mt-4 md:mt-0 flex space-x-3">
        <AppButton
          v-if="selectedGroup"
          label="Generate Invitation Code"
          icon="🔑"
          variant="secondary"
          @click="openGenerateCode()"
        />
        <AppButton label="Create Family" icon="➕" variant="primary" @click="openCreate()" />
      </div>
    </div>

    <!-- Groups list -->
    <div class="mb-6">
      <div v-if="loading" class="text-gray-500">Loading families…</div>

      <div v-else-if="groups.length === 0" class="bg-white rounded-xl shadow p-6 text-center">
        <p class="text-gray-600 mb-4">No family groups yet.</p>
        <AppButton label="Create your first family" variant="primary" @click="openCreate()" />
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="g in groups"
          :key="g.family_id"
          class="bg-white rounded-xl shadow p-5 border"
          :class="selectedGroup?.family_id === g.family_id ? 'ring-2 ring-indigo-500' : ''"
        >
          <div class="flex items-start justify-between">
            <div class="mr-4">
              <h3 class="text-lg font-semibold text-gray-800">{{ g.family_name }}</h3>
              <p class="text-sm text-gray-500">{{ g.description || '—' }}</p>
              <p class="mt-1 text-xs text-gray-400">ID: {{ g.family_id }}</p>
              <p v-if="g.family_code" class="mt-1 text-xs text-indigo-600">Code: {{ g.family_code }}</p>
            </div>
            <div class="flex gap-2">
              <AppButton size="sm" variant="secondary" label="Select" @click="selectGroup(g)" />
              <AppButton size="sm" variant="secondary" label="Edit" @click="openEdit(g)" />
              <AppButton size="sm" variant="error" label="Delete" @click="confirmDelete(g)" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Active codes + requests (optional summary) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <AppCard title="🔑 Active Invitation Codes">
        <div v-if="codesLoading" class="text-gray-500">Loading codes…</div>
        <div v-else-if="activeInvitations.length === 0" class="text-gray-500">No active codes</div>
        <div v-else class="space-y-2">
          <div v-for="c in activeInvitations" :key="c.code_id" class="p-3 bg-gray-50 rounded-lg">
            <div class="flex items-center justify-between">
              <code class="font-mono text-indigo-600 font-semibold">{{ c.code }}</code>
              <span class="text-sm text-gray-600">{{ c.usage_count || 0 }}/{{ c.max_uses ?? '∞' }}</span>
            </div>
            <div class="text-xs text-gray-500">Expires: {{ c.expires_at ? formatDate(c.expires_at) : 'Never' }}</div>
          </div>
        </div>
      </AppCard>

      <AppCard title="🔔 Pending Join Requests">
        <div v-if="requestsLoading" class="text-gray-500">Loading requests…</div>
        <div v-else-if="pendingRequests.length === 0" class="text-gray-500">No pending requests</div>
        <div v-else class="space-y-2">
          <div v-for="r in pendingRequests" :key="r.request_id" class="p-3 bg-amber-50 rounded-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-semibold text-amber-800">{{ r.requester_name }}</p>
                <p class="text-xs text-amber-700">{{ r.relationship_type }} • {{ formatDate(r.created_at) }}</p>
              </div>
              <div class="flex gap-2">
                <AppButton size="sm" variant="success" label="Accept" @click="approve(r.request_id)" />
                <AppButton size="sm" variant="error" label="Reject" @click="reject(r.request_id)" />
              </div>
            </div>
          </div>
        </div>
      </AppCard>
    </div>

    <!-- Create/Edit Modal -->
    <AppModal :is-open="isEditOpen" @close="isEditOpen=false" :title="editId ? 'Edit Family' : 'Create Family'">
      <form @submit.prevent="submitEdit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Family Name</label>
          <input v-model.trim="form.name" type="text" required class="w-full rounded-md border px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea v-model.trim="form.description" rows="3" class="w-full rounded-md border px-3 py-2" />
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <AppButton type="button" label="Cancel" variant="secondary" @click="isEditOpen=false" />
          <AppButton type="submit" :label="editId ? 'Save' : 'Create'" variant="primary" :disabled="saving" />
        </div>
      </form>
    </AppModal>

    <!-- Generate Code Modal -->
    <AppModal :is-open="isCodeOpen" @close="isCodeOpen=false" title="Generate Family Invitation Code">
      <form @submit.prevent="submitCode" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Expires In</label>
          <select v-model="codeForm.expiresIn" class="w-full rounded-md border px-3 py-2">
            <option :value="24">24 hours</option>
            <option :value="48">48 hours</option>
            <option :value="168">1 week</option>
            <option :value="0">No expiry</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Max Uses</label>
          <input v-model.number="codeForm.maxUses" type="number" min="1" class="w-full rounded-md border px-3 py-2" />
        </div>
        <div class="flex justify-end gap-2 pt-2">
          <AppButton type="button" label="Cancel" variant="secondary" @click="isCodeOpen=false" />
          <AppButton type="submit" label="Generate" variant="primary" :disabled="codeSaving" />
        </div>
      </form>
    </AppModal>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppBadge from '@/components/ui/AppBadge.vue' // if you use it elsewhere
import { familyGroupsService } from '@/services/familyGroupsService'
import { familyCodesService } from '@/services/familyCodesService'
import { parentRequestsService } from '@/services/parentRequestsService' // list/approve/reject

export default {
  name: 'FamilyGroupView',
  components: { AppCard, AppButton, AppModal, AppBadge },
  setup() {
    const store = useStore()
    const token = computed(() => store.getters['auth/token'] || store.state.auth?.token || '')

    // groups
    const loading = ref(false)
    const groups = ref([])
    const selectedGroup = ref(null)

    // edit/create
    const isEditOpen = ref(false)
    const editId = ref(null)
    const form = ref({ name: '', description: '' })
    const saving = ref(false)

    // codes
    const isCodeOpen = ref(false)
    const codeForm = ref({ expiresIn: 24, maxUses: 1 })
    const codeSaving = ref(false)
    const activeInvitations = ref([])
    const codesLoading = ref(false)

    // requests
    const pendingRequests = ref([])
    const requestsLoading = ref(false)

    const loadGroups = async () => {
      loading.value = true
      try {
        groups.value = token.value ? await familyGroupsService.list(token.value) : []
        if (!selectedGroup.value && groups.value.length) {
          selectedGroup.value = groups.value[0]
        }
      } catch (e) {
        console.error(e)
        groups.value = []
      } finally {
        loading.value = false
      }
    }

    const loadCodes = async () => {
      if (!token.value) return
      codesLoading.value = true
      try {
        activeInvitations.value = await familyCodesService.list(token.value)
      } catch (e) {
        console.error(e)
        activeInvitations.value = []
      } finally {
        codesLoading.value = false
      }
    }

    const loadRequests = async () => {
      if (!token.value) return
      requestsLoading.value = true
      try {
        pendingRequests.value = await parentRequestsService.list(token.value) // GET /parent/requests/
      } catch (e) {
        console.error(e)
        pendingRequests.value = []
      } finally {
        requestsLoading.value = false
      }
    }

    // CRUD
    const openCreate = () => {
      editId.value = null
      form.value = { name: '', description: '' }
      isEditOpen.value = true
    }
    const openEdit = (g) => {
      editId.value = g.family_id
      form.value = { name: g.family_name || '', description: g.description || '' }
      isEditOpen.value = true
    }
    const submitEdit = async () => {
      if (!token.value) return
      try {
        saving.value = true
        if (editId.value) {
          await familyGroupsService.update(editId.value, { ...form.value }, token.value)
        } else {
          const created = await familyGroupsService.create({ ...form.value }, token.value)
          selectedGroup.value = created
        }
        isEditOpen.value = false
        await loadGroups()
        await loadCodes()
      } catch (e) {
        console.error(e)
      } finally {
        saving.value = false
      }
    }
    const confirmDelete = async (g) => {
      if (!token.value) return
      const ok = window.confirm(`Delete family "${g.family_name}"? This removes codes and requests.`)
      if (!ok) return
      try {
        await familyGroupsService.remove(g.family_id, token.value)
        if (selectedGroup.value?.family_id === g.family_id) {
          selectedGroup.value = null
        }
        await loadGroups()
        await loadCodes()
      } catch (e) {
        console.error(e)
      }
    }
    const selectGroup = (g) => { selectedGroup.value = g }

    // Codes
    const openGenerateCode = () => {
      if (!selectedGroup.value) {
        store.dispatch('ui/showToast', { title: 'Create a family first', message: 'Select or create a family, then generate a code.', type: 'error' })
        return
      }
      isCodeOpen.value = true
    }
    const submitCode = async () => {
      if (!token.value || !selectedGroup.value) return
      try {
        codeSaving.value = true
        let expires_at = null
        if (Number(codeForm.value.expiresIn) > 0) {
          const d = new Date()
          d.setHours(d.getHours() + Number(codeForm.value.expiresIn))
          expires_at = d.toISOString()
        }
        await familyCodesService.create({
          target_id: selectedGroup.value.family_id,
          expires_at,
          max_uses: Number(codeForm.value.maxUses) || null,
        }, token.value)
        isCodeOpen.value = false
        await loadCodes()
        store.dispatch('ui/showToast', { title: 'Code created', message: 'Invitation code ready to share.', type: 'success' })
      } catch (e) {
        console.error(e)
        store.dispatch('ui/showToast', { title: 'Error', message: 'Failed to create code', type: 'error' })
      } finally {
        codeSaving.value = false
      }
    }

    // Requests actions
    const approve = async (requestId) => {
      try {
        await parentRequestsService.approve(requestId, token.value) // POST /parent/requests/{id}/approve
        pendingRequests.value = pendingRequests.value.filter(r => r.request_id !== requestId)
        await loadGroups() // membership may change metrics later
        store.dispatch('ui/showToast', { title: 'Approved', message: 'Request approved', type: 'success' })
      } catch (e) {
        console.error(e)
      }
    }
    const reject = async (requestId) => {
      try {
        await parentRequestsService.reject(requestId, token.value)
        pendingRequests.value = pendingRequests.value.filter(r => r.request_id !== requestId)
        store.dispatch('ui/showToast', { title: 'Rejected', message: 'Request rejected', type: 'success' })
      } catch (e) {
        console.error(e)
      }
    }

    const formatDate = (v) => {
      try { if (!v) return '—'; const d = new Date(v); return d.toLocaleString() } catch { return String(v) }

    }

    onMounted(async () => {
      await Promise.all([loadGroups(), loadCodes(), loadRequests()])
    })

    return {
      // state
      loading, groups, selectedGroup,
      isEditOpen, editId, form, saving,
      isCodeOpen, codeForm, codeSaving, activeInvitations, codesLoading,
      pendingRequests, requestsLoading,
      // actions
      openCreate, openEdit, submitEdit, confirmDelete, selectGroup,
      openGenerateCode, submitCode,
      approve, reject,
      // utils
      formatDate,
    }
  },
}
</script>
