<template>
  <div class="bg-gray-100 font-sans p-4 md:p-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:justify-between md:items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">👨‍👩‍👧‍👦 Family Groups</h1>
        <p class="text-sm text-gray-500">
          Manage your families, handle join requests, and share invite codes
        </p>
      </div>
      <div class="mt-4 md:mt-0 flex gap-2">
        <AppButton label="Create Family" icon="➕" variant="primary" @click="openCreate" />
        <AppButton
          v-if="selectedGroupId"
          label="Generate Invite Code"
          icon="🔑"
          variant="info"
          @click="isInviteModalOpen = true"
        />
        <AppButton
          v-if="selectedGroupId"
          label="Edit Family"
          variant="info"
          size="sm"
          @click="openEdit"
        />
        <AppButton
          v-if="selectedGroupId"
          label="Delete Family"
          variant="error"
          size="sm"
          @click="isDeleteOpen = true"
        />
      </div>
    </div>

    <!-- Top Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white p-4 rounded-lg shadow-sm text-center">
        <p class="text-2xl font-bold text-blue-600">{{ headedGroups.length }}</p>
        <p class="text-xs text-gray-500">Groups You Head</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm text-center">
        <p class="text-2xl font-bold text-purple-600">{{ memberships.length }}</p>
        <p class="text-xs text-gray-500">Groups You Joined</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm text-center">
        <p class="text-2xl font-bold text-amber-500">{{ requests.length }}</p>
        <p class="text-xs text-gray-500">Pending Requests</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm text-center">
        <p class="text-2xl font-bold text-green-600">{{ activeCodesCount }}</p>
        <p class="text-xs text-gray-500">Active Codes (selected)</p>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- LEFT: Groups you head + memberships -->
      <div class="space-y-6">
        <!-- Groups you head -->
        <div class="bg-white rounded-xl shadow p-6">
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-lg font-semibold text-gray-800">Your Families (Head)</h2>
            <span class="text-sm text-gray-500">{{ headedGroups.length }}</span>
          </div>

          <div v-if="loadingHeaded" class="text-gray-500 text-sm">Loading…</div>
          <div v-else-if="headedGroups.length === 0" class="text-sm text-gray-500">
            You don't head any families yet. Create one to get started.
          </div>

          <ul v-else class="space-y-2">
            <li
              v-for="g in headedGroups"
              :key="g.family_id"
              class="flex items-center justify-between rounded-lg border p-3 cursor-pointer"
              :class="selectedGroupId === g.family_id ? 'ring-2 ring-indigo-500 border-transparent' : ''"
              @click="selectGroup(g.family_id)"
            >
              <div>
                <div class="font-medium text-gray-800">{{ g.family_name }}</div>
                <div class="text-xs text-gray-500">
                  Created: {{ fmtDate(g.created_at) }}
                </div>
              </div>
              <AppBadge :variant="selectedGroupId === g.family_id ? 'success' : 'secondary'">
                {{ selectedGroupId === g.family_id ? 'Selected' : 'Select' }}
              </AppBadge>
            </li>
          </ul>
        </div>

        <!-- Groups you joined -->
        <div class="bg-white rounded-xl shadow p-6">
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-lg font-semibold text-gray-800">Your Memberships</h2>
            <span class="text-sm text-gray-500">{{ memberships.length }} joined</span>
          </div>

          <div v-if="loadingMemberships" class="text-gray-500 text-sm">Loading…</div>
          <div v-else-if="memberships.length === 0" class="text-sm text-gray-500">
            You haven’t joined any other family yet.
          </div>

          <ul v-else class="space-y-2">
            <li
              v-for="m in memberships"
              :key="m.family_id"
              class="flex items-center justify-between rounded-lg border p-3"
            >
              <div>
                <div class="font-medium text-gray-800">{{ m.family_name }}</div>
                <div class="text-xs text-gray-500">
                  Role: {{ m.role || 'Member' }}
                  <span v-if="m.head_name"> • Head: {{ m.head_name }}</span>
                  <span v-if="m.joined_at"> • Joined: {{ fmtDate(m.joined_at) }}</span>
                </div>
              </div>
              <AppBadge variant="info">Member</AppBadge>
            </li>
          </ul>
        </div>
      </div>

      <!-- RIGHT (2 cols): Selected family details -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Selected family summary -->
        <div class="bg-white rounded-xl shadow p-6">
          <div class="flex items-center justify-between mb-1">
            <h2 class="text-lg font-semibold text-gray-800">
              {{ currentGroup?.family_name || 'Select a family' }}
            </h2>
            <div v-if="currentGroup" class="text-xs text-gray-500">Family ID: {{ currentGroup.family_id }}</div>
          </div>
          <p class="text-sm text-gray-500" v-if="currentGroup?.description">
            {{ currentGroup.description }}
          </p>
        </div>

        <!-- Codes + Requests + Members -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Active Invitation Codes -->
          <div class="bg-white rounded-xl shadow p-6">
            <div class="flex items-center justify-between mb-3">
              <h3 class="font-semibold text-gray-800">🔑 Active Invitation Codes</h3>
              <AppButton
                v-if="selectedGroupId"
                label="Generate"
                size="sm"
                variant="primary"
                @click="isInviteModalOpen = true"
              />
            </div>

            <div v-if="loadingCodes" class="text-gray-500 text-sm">Loading…</div>
            <div v-else-if="codesForSelected.length === 0" class="text-sm text-gray-500">
              No active codes for this family.
            </div>

            <div v-else class="space-y-3">
              <div
                v-for="code in codesForSelected"
                :key="code.code_id"
                class="p-3 rounded-lg bg-gray-50"
              >
                <div class="flex items-center justify-between mb-2">
                  <code class="font-mono font-bold text-indigo-600">{{ code.code }}</code>
                  <AppBadge variant="success">Active</AppBadge>
                </div>
                <div class="grid grid-cols-2 gap-3 text-xs text-gray-600">
                  <div>
                    <div><strong>Uses:</strong> {{ code.usage_count || 0 }}/{{ code.max_uses ?? '∞' }}</div>
                    <div><strong>Type:</strong> {{ code.target_type }}</div>
                  </div>
                  <div>
                    <div><strong>Expires:</strong> {{ code.expires_at ? fmtDate(code.expires_at) : 'Never' }}</div>
                    <div><strong>Created:</strong> {{ fmtDate(code.created_at) }}</div>
                  </div>
                </div>
                <div class="mt-3 flex gap-2 justify-end">
                  <AppButton label="Copy" size="sm" variant="info" @click="copy(code.code)" />
                  <AppButton label="Revoke" size="sm" variant="error" @click="revoke(code)" />
                </div>
              </div>
            </div>
          </div>

          <!-- Join Requests -->
          <div class="bg-white rounded-xl shadow p-6">
            <div class="flex items-center justify-between mb-3">
              <h3 class="font-semibold text-gray-800">🔔 Join Requests</h3>
              <AppButton
                v-if="requests.length"
                label="Accept All"
                size="sm"
                variant="primary"
                :disabled="bulkBusy"
                @click="approveAll"
              />
            </div>

            <div v-if="loadingRequests" class="text-gray-500 text-sm">Loading…</div>
            <div v-else-if="requests.length === 0" class="text-sm text-gray-500">
              No pending join requests.
            </div>

            <div v-else class="space-y-3">
              <div v-for="r in filteredRequests" :key="r.request_id" class="p-3 rounded-lg bg-amber-50">
                <div class="flex items-center justify-between mb-1">
                  <div class="font-medium text-amber-900">{{ r.requester_name || 'Unknown' }}</div>
                  <AppBadge variant="warning">Pending</AppBadge>
                </div>
                <div class="text-xs text-amber-700">
                  {{ r.requester_type || 'member' }}
                  <span v-if="r.relationship_type"> • {{ r.relationship_type }}</span>
                  <span v-if="r.created_at"> • Requested: {{ fmtDate(r.created_at) }}</span>
                </div>
                <p v-if="r.message" class="mt-2 text-xs bg-amber-100 p-2 rounded">
                  “{{ r.message }}”
                </p>
                <div class="mt-3 flex gap-2 justify-end">
                  <AppButton
                    size="sm"
                    label="✓ Approve"
                    variant="success"
                    :disabled="r._busy"
                    @click="approve(r)"
                  />
                  <AppButton
                    size="sm"
                    label="✗ Reject"
                    variant="error"
                    :disabled="r._busy"
                    @click="reject(r)"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Members -->
          <div class="md:col-span-2 bg-white rounded-xl shadow p-6">
            <div class="flex items-center justify-between mb-3">
              <h3 class="font-semibold text-gray-800">👥 Members</h3>
              <span class="text-sm text-gray-500">{{ currentGroupMembers.length }}</span>
            </div>

            <div v-if="loadingGroup" class="text-gray-500 text-sm">Loading…</div>
            <div v-else-if="!currentGroup" class="text-sm text-gray-500">Select a family to see members.</div>
            <div v-else-if="currentGroupMembers.length === 0" class="text-sm text-gray-500">
              No members found.
            </div>

            <ul v-else class="divide-y divide-gray-200">
              <li v-for="m in currentGroupMembers" :key="m.user_id" class="py-3 flex items-center justify-between">
                <div>
                  <div class="font-medium text-gray-800">
                    {{ m.full_name || m.name || m.email || shortId(m.user_id) }}
                  </div>
                  <div class="text-xs text-gray-500">
                    {{ m.display_role || m.role || 'Member' }}
                    <span v-if="m.joined_at"> • Joined: {{ fmtDate(m.joined_at) }}</span>
                    <span v-if="m.connectionType"> • {{ m.connectionType }}</span>
                  </div>
                </div>
                <AppBadge :variant="(m.display_role || m.role) === 'head' ? 'success' : ((m.display_role === 'parent' || m.display_role === 'teacher') ? 'info' : 'secondary')">
                  {{ (m.display_role || m.role) === 'head' ? 'Head' : (m.display_role === 'parent' ? 'Parent' : (m.display_role === 'teacher' ? 'Teacher' : 'Member')) }}
                </AppBadge>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Family Modal -->
    <AppModal :is-open="isEditOpen" @close="closeEdit" :title="editId ? 'Edit Family' : 'Create Family'">
      <form @submit.prevent="submitEdit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Family Name</label>
          <input v-model.trim="form.name" type="text" required class="w-full rounded-md border px-3 py-2" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea v-model.trim="form.description" rows="3" class="w-full rounded-md border px-3 py-2"></textarea>
        </div>
        <div class="pt-2 flex justify-end gap-2">
          <AppButton label="Cancel" variant="info" type="button" @click="closeEdit" />
          <AppButton :label="editId ? 'Save' : 'Create'" variant="primary" type="submit" :disabled="savingEdit" />
        </div>
      </form>
    </AppModal>

    <!-- Delete confirm -->
    <AppModal :is-open="isDeleteOpen" @close="isDeleteOpen=false" title="Delete Family">
      <p class="text-gray-700">Are you sure you want to delete this family?</p>
      <div class="mt-6 flex justify-end gap-3">
        <AppButton label="Cancel" variant="info" @click="isDeleteOpen=false" />
        <AppButton label="Delete" variant="error" @click="confirmDelete" :disabled="deleting" />
      </div>
    </AppModal>

    <!-- Generate Invite Modal -->
    <AppModal :is-open="isInviteModalOpen" @close="isInviteModalOpen=false" title="Generate Family Invitation Code">
      <div class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Expires In</label>
          <select v-model="inviteForm.expiresInHours" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
            <option :value="24">24 hours</option>
            <option :value="48">48 hours</option>
            <option :value="168">1 week</option>
            <option :value="0">No expiry</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Max Uses</label>
          <input v-model.number="inviteForm.maxUses" type="number" min="1" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" placeholder="e.g., 1" />
          <p class="text-xs text-gray-500 mt-1">Leave blank for unlimited</p>
        </div>

        <div class="flex justify-end gap-2">
          <AppButton label="Cancel" variant="info" @click="isInviteModalOpen=false" />
          <AppButton label="Generate Code" variant="primary" @click="generateCode" :disabled="generating" />
        </div>
      </div>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppBadge from '@/components/ui/AppBadge.vue'

import { familyGroupsService } from '@/services/familyGroupsService'
import { familyCodesService } from '@/services/familyCodesService'
import { parentRequestsService } from '@/services/parentRequestsService'

const store = useStore()
const token = () => store.getters['auth/token']

/** ---------- State ---------- */
const headedGroups = ref([])
const memberships = ref([])
const selectedGroupId = ref(null)
const currentGroup = ref(null)
const currentGroupMembers = ref([])

const codes = ref([])
const requests = ref([])

const loadingHeaded = ref(false)
const loadingMemberships = ref(false)
const loadingGroup = ref(false)
const loadingCodes = ref(false)
const loadingRequests = ref(false)

const bulkBusy = ref(false)

/** Create/Edit/Delete family */
const isEditOpen = ref(false)
const editId = ref(null)
const form = ref({ name: '', description: '' })
const savingEdit = ref(false)
const isDeleteOpen = ref(false)
const deleting = ref(false)

/** Generate invite code */
const isInviteModalOpen = ref(false)
const inviteForm = ref({ expiresInHours: 24, maxUses: null })
const generating = ref(false)

/** ---------- Loaders ---------- */
const loadHeaded = async () => {
  loadingHeaded.value = true
  try {
    headedGroups.value = await familyGroupsService.listHeaded(token())
    // select first by default
    if (!selectedGroupId.value && headedGroups.value.length) {
      selectedGroupId.value = headedGroups.value[0].family_id
    }
  } catch (e) {
    headedGroups.value = []
  } finally {
    loadingHeaded.value = false
  }
}

const loadMemberships = async () => {
  loadingMemberships.value = true
  try {
    memberships.value = await familyGroupsService.listMemberships(token())
  } catch (e) {
    memberships.value = []
  } finally {
    loadingMemberships.value = false
  }
}

const loadGroupDetail = async () => {
  if (!selectedGroupId.value) { currentGroup.value = null; currentGroupMembers.value = []; return }
  loadingGroup.value = true
  try {
    const data = await familyGroupsService.get(selectedGroupId.value, token())
    currentGroup.value = data
    // members from API (for heads only)
    currentGroupMembers.value = (data.members || []).map(m => ({
      ...m,
      connectionType: m.role === 'head' ? 'Family Head' : 'Connected via invitation'
    }))
  } catch (e) {
    currentGroup.value = null
    currentGroupMembers.value = []
  } finally {
    loadingGroup.value = false
  }
}

const loadCodes = async () => {
  loadingCodes.value = true
  try {
    const all = await familyCodesService.list(token())
    codes.value = Array.isArray(all) ? all : []
  } catch (e) {
    codes.value = []
  } finally {
    loadingCodes.value = false
  }
}

const loadRequests = async () => {
  loadingRequests.value = true
  try {
    const rows = await parentRequestsService.list(token())
    // mark all not busy
    requests.value = (rows || []).map(r => ({ ...r, _busy: false }))
  } catch (e) {
    requests.value = []
  } finally {
    loadingRequests.value = false
  }
}

/** ---------- Derived ---------- */
const codesForSelected = computed(() =>
  codes.value.filter(c => c.target_type === 'family' && c.target_id === selectedGroupId.value)
)
const activeCodesCount = computed(() => codesForSelected.value.length)

const filteredRequests = computed(() => {
  // only requests directed to the currently selected family group
  if (!selectedGroupId.value) return requests.value
  return requests.value.filter(r => r.target_id === selectedGroupId.value)
})

/** ---------- Actions ---------- */
const selectGroup = (id) => {
  if (selectedGroupId.value === id) return
  selectedGroupId.value = id
}

watch(selectedGroupId, async () => {
  await Promise.all([loadGroupDetail(), loadCodes(), loadRequests()])
})

const openCreate = () => {
  editId.value = null
  form.value = { name: '', description: '' }
  isEditOpen.value = true
}
const openEdit = () => {
  if (!currentGroup.value) return
  editId.value = currentGroup.value.family_id
  form.value = {
    name: currentGroup.value.family_name || '',
    description: currentGroup.value.description || ''
  }
  isEditOpen.value = true
}
const closeEdit = () => { isEditOpen.value = false; savingEdit.value = false }

const submitEdit = async () => {
  try {
    savingEdit.value = true
    if (editId.value) {
      await familyGroupsService.update(editId.value, { name: form.value.name, description: form.value.description }, token())
    } else {
      const created = await familyGroupsService.create({ name: form.value.name, description: form.value.description }, token())
      // select the newly created
      selectedGroupId.value = created?.family_id || selectedGroupId.value
    }
    closeEdit()
    await Promise.all([loadHeaded(), loadGroupDetail()])
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to save family'
    store.dispatch('ui/showToast', { title: 'Error', message: msg, type: 'error' })
  } finally {
    savingEdit.value = false
  }
}

const confirmDelete = async () => {
  if (!selectedGroupId.value) return
  try {
    deleting.value = true
    await familyGroupsService.remove(selectedGroupId.value, token())
    isDeleteOpen.value = false
    // refresh and clear selection
    await loadHeaded()
    selectedGroupId.value = headedGroups.value[0]?.family_id || null
    await loadGroupDetail()
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to delete family'
    store.dispatch('ui/showToast', { title: 'Error', message: msg, type: 'error' })
  } finally {
    deleting.value = false
  }
}

/** Codes */
const generateCode = async () => {
  if (!selectedGroupId.value) return
  try {
    generating.value = true
    let expires_at = null
    if (inviteForm.value.expiresInHours && inviteForm.value.expiresInHours > 0) {
      const d = new Date()
      d.setHours(d.getHours() + Number(inviteForm.value.expiresInHours))
      expires_at = d.toISOString()
    }
    const payload = {
      target_id: selectedGroupId.value,
      expires_at,
      max_uses: inviteForm.value.maxUses || null,
    }
    await familyCodesService.create(payload, token())
    isInviteModalOpen.value = false
    inviteForm.value = { expiresInHours: 24, maxUses: null }
    await loadCodes()
    store.dispatch('ui/showToast', { title: 'Code generated', message: 'Share it with family members', type: 'success' })
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to generate code'
    store.dispatch('ui/showToast', { title: 'Error', message: msg, type: 'error' })
  } finally {
    generating.value = false
  }
}

const copy = (txt) => {
  navigator.clipboard?.writeText(txt)
  store.dispatch('ui/showToast', { title: 'Copied', message: 'Code copied to clipboard', type: 'success' })
}
const revoke = async (code) => {
  try {
    await familyCodesService.revoke(code.code_id, token())
    await loadCodes()
    store.dispatch('ui/showToast', { title: 'Revoked', message: 'Invitation code revoked', type: 'success' })
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to revoke code'
    store.dispatch('ui/showToast', { title: 'Error', message: msg, type: 'error' })
  }
}

/** Requests */
const approve = async (r) => {
  try {
    r._busy = true
    await parentRequestsService.approve(r.request_id, token())
    requests.value = requests.value.filter(x => x.request_id !== r.request_id)
    await loadGroupDetail() // refresh members
    store.dispatch('ui/showToast', { title: 'Approved', message: r.requester_name || '', type: 'success' })
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to approve'
    store.dispatch('ui/showToast', { title: 'Error', message: msg, type: 'error' })
    r._busy = false
  }
}
const reject = async (r) => {
  try {
    r._busy = true
    await parentRequestsService.reject(r.request_id, token())
    requests.value = requests.value.filter(x => x.request_id !== r.request_id)
    store.dispatch('ui/showToast', { title: 'Rejected', message: r.requester_name || '', type: 'success' })
  } catch (e) {
    const msg = e?.response?.data?.detail || 'Failed to reject'
    store.dispatch('ui/showToast', { title: 'Error', message: msg, type: 'error' })
    r._busy = false
  }
}
const approveAll = async () => {
  if (!requests.value.length) return
  bulkBusy.value = true
  try {
    const copies = [...filteredRequests.value]
    for (const r of copies) {
      try { await parentRequestsService.approve(r.request_id, token()) } catch {}
    }
    await Promise.all([loadRequests(), loadGroupDetail()])
    store.dispatch('ui/showToast', { title: 'All Approved', message: 'All pending requests approved', type: 'success' })
  } finally {
    bulkBusy.value = false
  }
}

/** ---------- Utils ---------- */
const fmtDate = (v) => {
  try { if (!v) return '-'; const d = new Date(v); return Number.isNaN(d.getTime()) ? String(v) : d.toLocaleDateString() }
  catch { return String(v) }
}
const shortId = (id) => (id ? String(id).slice(0, 8) : '—')

/** ---------- Mount ---------- */
const refreshAll = async () => {
  await Promise.all([loadHeaded(), loadMemberships()])
  await Promise.all([loadGroupDetail(), loadCodes(), loadRequests()])
}
onMounted(refreshAll)
</script>
