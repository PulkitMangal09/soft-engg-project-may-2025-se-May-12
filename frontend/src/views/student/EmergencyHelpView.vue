<template>
  <div class="flex flex-col h-screen bg-gray-50">
    <!-- Header -->
    <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between bg-white">
      <button class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100" @click="$router.go(-1)">
        ←
      </button>
      <h1 class="text-lg font-semibold">Emergency Help</h1>
      <div class="w-8"></div> <!-- Spacer for alignment -->
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-y-auto p-6 text-center">
      <div class="bg-white rounded-2xl p-6 shadow-sm mb-6">
        <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-800 mb-2">Emergency Support</h2>
        <p class="text-gray-600 mb-6">If you're in immediate danger or need urgent help, please contact emergency
          services in your area.</p>

        <button
          class="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-4 rounded-xl mb-4 flex items-center justify-center"
          @click="callEmergency">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
          Call Emergency Services (100)
        </button>
      </div>

      <div class="bg-white rounded-2xl p-6 shadow-sm mb-6 text-left">
        <h3 class="font-semibold text-gray-800 mb-3">Crisis Hotlines</h3>

        <div class="space-y-3">
          <div class="p-3 bg-blue-50 rounded-lg">
            <div class="font-medium">National Suicide Prevention Lifeline</div>
            <div class="text-blue-600">+91 9152987821</div>
          </div>

          <div class="p-3 bg-blue-50 rounded-lg">
            <div class="font-medium">Crisis Text Line</div>
            <div class="text-blue-600">Text HOME to 741741</div>
          </div>

          <div class="p-3 bg-blue-50 rounded-lg">
            <div class="font-medium">Childhelp National Child Abuse Hotline</div>
            <div class="text-blue-600">1098</div>
          </div>
          <div class="p-3 bg-blue-50 rounded-lg">
            <div class="font-medium">Ambulance</div>
            <div class="text-blue-600">108</div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-6 shadow-sm text-left">
        <h3 class="font-semibold text-gray-800 mb-4">Your Trusted Contacts</h3>

        <!-- Add Contact Form -->
        <form @submit.prevent="addContact" class="grid grid-cols-1 md:grid-cols-5 gap-3 mb-5">
          <input v-model="form.name" type="text" placeholder="Name"
            class="col-span-1 md:col-span-1 border rounded-lg px-3 py-2" required>
          <input v-model="form.phone_number" type="tel" placeholder="Phone"
            class="col-span-1 md:col-span-1 border rounded-lg px-3 py-2" required>
          <input v-model="form.description" type="text" placeholder="Description (optional)"
            class="col-span-1 md:col-span-2 border rounded-lg px-3 py-2">
          <select v-model="form.contact_type" class="col-span-1 md:col-span-1 border rounded-lg px-3 py-2" required>
            <option disabled value="">Type…</option>
            <!-- Backend enum allowed values -->
            <option value="crisis">Crisis</option>
            <option value="teen_support">Teen Support</option>
            <option value="text_line">Text Line</option>
            <option value="bullying">Bullying</option>
            <option value="family_crisis">Family Crisis</option>
            <option value="local_emergency">Local Emergency</option>
          </select>
          <label class="inline-flex items-center text-sm">
            <input type="checkbox" v-model="form.is_available_24_7" class="mr-2"> 24/7
          </label>
          <button type="submit" class="md:col-span-5 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Add
            Contact</button>
        </form>

        <div v-if="loading" class="text-gray-500 text-sm">Loading…</div>
        <div v-if="!loading && studentEmergency && studentEmergency.phone"
          class="p-3 border border-amber-200 bg-amber-50 text-amber-800 rounded-lg mb-4">
          <div class="flex items-center">
            <div class="font-semibold mr-2">Primary Emergency:</div>
            <div class="mr-2">{{ studentEmergency.label }}</div>
            <a :href="'tel:' + studentEmergency.phone" class="underline">{{ studentEmergency.phone }}</a>
          </div>
        </div>
        <div v-if="!loading" class="space-y-3">
          <div v-for="contact in contacts" :key="contact.contact_id || contact.id"
            class="p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
            <div class="flex items-center">
              <div
                class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-semibold mr-3">
                {{ (contact.name || '').charAt(0) }}
              </div>
              <div class="flex-1">
                <div class="font-medium">{{ contact.name }}</div>
                <div class="text-sm text-gray-500">{{ contact.description || '—' }}</div>
                <div class="text-xs text-gray-400">{{ contact.contact_type }} <span v-if="contact.is_available_24_7">•
                    24/7</span></div>
              </div>
              <a :href="'tel:' + contact.phone_number" class="text-blue-500 p-2" title="Call">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
              </a>
              <button @click="startEdit(contact)" class="text-gray-500 p-2 hover:text-gray-700" title="Edit">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    d="M13.586 3.586a2 2 0 112.828 2.828l-8.5 8.5a1 1 0 01-.293.195l-3 1a1 1 0 01-1.272-1.272l1-3a1 1 0 01.195-.293l8.5-8.5z" />
                </svg>
              </button>
              <button @click="removeContact(contact)" class="text-red-500 p-2 hover:text-red-600" title="Delete">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clip-rule="evenodd" />
                </svg>
              </button>
            </div>

            <!-- Inline Edit -->
            <div v-if="editing && editing.contact_id === (contact.contact_id || contact.id)"
              class="mt-3 grid grid-cols-1 md:grid-cols-4 gap-3">
              <input v-model="editing.name" type="text" class="border rounded-lg px-3 py-2" placeholder="Name">
              <input v-model="editing.phone_number" type="tel" class="border rounded-lg px-3 py-2" placeholder="Phone">
              <input v-model="editing.description" type="text" class="border rounded-lg px-3 py-2"
                placeholder="Description">
              <select v-model="editing.contact_type" class="border rounded-lg px-3 py-2">
                <option value="crisis">Crisis</option>
                <option value="teen_support">Teen Support</option>
                <option value="text_line">Text Line</option>
                <option value="bullying">Bullying</option>
                <option value="family_crisis">Family Crisis</option>
                <option value="local_emergency">Local Emergency</option>
              </select>
              <label class="inline-flex items-center text-sm">
                <input type="checkbox" v-model="editing.is_available_24_7" class="mr-2"> 24/7
              </label>
              <div class="md:col-span-4 flex gap-2">
                <button @click="saveEdit()"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Save</button>
                <button @click="cancelEdit()" class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300">Cancel</button>
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
    // fetch student's primary emergency from profile if available
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
