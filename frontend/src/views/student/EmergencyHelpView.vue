<template>
  <div class="flex flex-col min-h-screen bg-gray-100">
    <div class="flex items-center justify-between p-4 bg-white shadow-md">
      <button
        @click="$router.go(-1)"
        class="w-10 h-10 flex items-center justify-center rounded-full text-gray-600 hover:bg-gray-100 transition-colors"
        aria-label="Go Back"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <h1 class="text-xl font-bold text-gray-800">Emergency Help 🚨</h1>
      <div class="w-10"></div>
    </div>

    <div class="flex-1 overflow-y-auto p-6 md:p-10 space-y-8 max-w-5xl mx-auto w-full">

      <div class="bg-gradient-to-br from-red-600 to-red-800 text-white rounded-3xl p-8 text-center shadow-2xl">
        <div class="w-20 h-20 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-5 border-4 border-red-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h2 class="text-3xl font-extrabold mb-2">Immediate Danger?</h2>
        <p class="text-lg font-light mb-6">If you're in immediate danger, please use the button below to call for help.</p>
        <button
          class="w-full bg-white text-red-600 hover:bg-gray-100 font-bold py-4 px-4 rounded-xl flex items-center justify-center text-xl shadow-lg transition-all"
          @click="callEmergency">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-3" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
          Call Emergency Services (100)
        </button>
      </div>

      <div class="bg-white rounded-2xl p-6 shadow-lg text-left">
        <h3 class="text-2xl font-bold text-gray-800 mb-4">Crisis Hotlines</h3>
        <p class="text-gray-600 mb-6 text-sm">These resources offer confidential support from trained professionals.</p>

        <div class="space-y-4">
          <div class="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
            <div class="font-bold text-gray-800">National Suicide Prevention Lifeline</div>
            <a href="tel:+919152987821" class="text-blue-600 font-medium text-lg">+91 9152987821</a>
          </div>

          <div class="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
            <div class="font-bold text-gray-800">Crisis Text Line</div>
            <div class="text-blue-600 font-medium text-lg">Text HOME to 741741</div>
          </div>

          <div class="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
            <div class="font-bold text-gray-800">Ambulance</div>
            <a href="tel:108" class="text-blue-600 font-medium text-lg">108</a>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-6 shadow-lg text-left">
        <h3 class="text-2xl font-bold text-gray-800 mb-4">Your Trusted Contacts</h3>
        <p class="text-gray-600 mb-6 text-sm">Add personal contacts, like family members or a local therapist, for easy access.</p>

        <form @submit.prevent="addContact" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <input v-model="form.name" type="text" placeholder="Name" class="input-field" required>
          <input v-model="form.phone_number" type="tel" placeholder="Phone" class="input-field" required>
          <select v-model="form.contact_type" class="input-field" required>
            <option disabled value="">Type…</option>
            <option value="crisis">Crisis</option>
            <option value="teen_support">Teen Support</option>
            <option value="text_line">Text Line</option>
            <option value="bullying">Bullying</option>
            <option value="family_crisis">Family Crisis</option>
            <option value="local_emergency">Local Emergency</option>
          </select>
          <div class="flex items-center gap-2">
            <input type="checkbox" v-model="form.is_available_24_7" class="form-checkbox h-5 w-5 text-blue-600 rounded-full transition duration-150 ease-in-out">
            <label class="text-sm font-medium text-gray-700">24/7</label>
          </div>
          <input v-model="form.description" type="text" placeholder="Description (optional)" class="input-field col-span-full">
          <button type="submit" class="btn-primary col-span-full">Add Contact</button>
        </form>

        <div v-if="loading" class="text-gray-500 text-sm py-4 text-center">Loading...</div>
        <div v-if="!loading && studentEmergency && studentEmergency.phone"
          class="p-4 border border-amber-300 bg-amber-100 text-amber-800 rounded-lg mb-4 flex items-center justify-between">
          <div>
            <div class="font-bold">Primary Emergency: {{ studentEmergency.label }}</div>
            <a :href="'tel:' + studentEmergency.phone" class="underline font-medium">{{ studentEmergency.phone }}</a>
          </div>
        </div>
        <div v-if="!loading" class="space-y-4">
          <div v-for="contact in contacts" :key="contact.contact_id || contact.id"
            class="p-4 border border-gray-200 rounded-lg bg-gray-50 hover:bg-white transition-colors">
            <div class="flex items-center">
              <div
                class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-lg mr-4 flex-shrink-0">
                {{ (contact.name || '').charAt(0) }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="font-bold text-gray-800 truncate">{{ contact.name }}</div>
                <div class="text-sm text-gray-500 truncate">{{ contact.description || '—' }}</div>
                <div class="text-xs text-gray-400 mt-1">
                  {{ contact.contact_type }} <span v-if="contact.is_available_24_7">• 24/7</span>
                </div>
              </div>
              <div class="flex gap-2 ml-4">
                <a :href="'tel:' + contact.phone_number" class="text-blue-500 p-2 rounded-full hover:bg-blue-50" title="Call">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </a>
                <button @click="startEdit(contact)" class="text-gray-500 p-2 rounded-full hover:bg-gray-200" title="Edit">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-8.5 8.5a1 1 0 01-.293.195l-3 1a1 1 0 01-1.272-1.272l1-3a1 1 0 01.195-.293l8.5-8.5z" />
                  </svg>
                </button>
                <button @click="removeContact(contact)" class="text-red-500 p-2 rounded-full hover:bg-red-100" title="Delete">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>

            <div v-if="editing && editing.contact_id === (contact.contact_id || contact.id)"
              class="mt-4 pt-4 border-t border-gray-200">
              <h4 class="font-bold text-sm mb-3">Edit Contact</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <input v-model="editing.name" type="text" class="input-field" placeholder="Name">
                <input v-model="editing.phone_number" type="tel" class="input-field" placeholder="Phone">
                <input v-model="editing.description" type="text" class="input-field" placeholder="Description">
                <select v-model="editing.contact_type" class="input-field">
                  <option value="crisis">Crisis</option>
                  <option value="teen_support">Teen Support</option>
                  <option value="text_line">Text Line</option>
                  <option value="bullying">Bullying</option>
                  <option value="family_crisis">Family Crisis</option>
                  <option value="local_emergency">Local Emergency</option>
                </select>
                <div class="flex items-center gap-2">
                  <input type="checkbox" v-model="editing.is_available_24_7" class="form-checkbox h-4 w-4 text-blue-600">
                  <label class="text-sm font-medium text-gray-700">24/7</label>
                </div>
              </div>
              <div class="mt-4 flex gap-2">
                <button @click="saveEdit()" class="btn-primary">Save</button>
                <button @click="cancelEdit()" class="btn-tertiary">Cancel</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listContacts, createContact, updateContact, deleteContact } from '@/services/emergencyContactsService'
import axios from 'axios'

const contacts = ref([])
const loading = ref(false)
const form = ref({ name: '', phone_number: '', description: '', contact_type: '', is_available_24_7: true })
const editing = ref(null)
const studentEmergency = ref(null)

onMounted(loadContacts)

async function loadContacts() {
  loading.value = true
  try {
    contacts.value = await listContacts()
    const { data } = await axios.get('/student/profile')
    const phone = data?.emergency_contact_phone || data?.profile_data?.emergency_contact_phone
    if (phone) studentEmergency.value = { label: 'From Profile', phone }
  } finally {
    loading.value = false
  }
}

async function addContact() {
  try {
    const newContact = await createContact({ ...form.value })
    contacts.value.unshift(newContact)
    form.value = { name: '', phone_number: '', description: '', contact_type: '', is_available_24_7: true }
  } catch (e) {
    // noop or show toast
  }
}

function startEdit(contact) {
  editing.value = { ...contact }
}

function cancelEdit() {
  editing.value = null
}

async function saveEdit() {
  if (!editing.value) return
  const id = editing.value.contact_id || editing.value.id
  try {
    const updated = await updateContact(id, { ...editing.value })
    const idx = contacts.value.findIndex(c => (c.contact_id || c.id) === id)
    if (idx !== -1) contacts.value[idx] = updated
    editing.value = null
  } catch (e) {
    // noop or show toast
  }
}

async function removeContact(contact) {
  const id = contact.contact_id || contact.id
  try {
    await deleteContact(id)
    contacts.value = contacts.value.filter(c => (c.contact_id || c.id) !== id)
  } catch (e) {
    // noop or show toast
  }
}

function callEmergency() {
  alert('Calling emergency services...')
}
</script>

<style scoped>
.input-field {
  @apply w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-sm;
}
.btn-primary {
  @apply bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-blue-700 transition-all text-sm;
}
.btn-tertiary {
  @apply bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition-all text-sm;
}
</style>