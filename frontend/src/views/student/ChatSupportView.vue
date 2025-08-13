<template>
  <div class="flex flex-col h-screen bg-gray-100">
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

      <h1 class="text-xl font-bold text-gray-800">Mood Buddy 😊</h1>

      <div class="w-10"></div>
    </div>

    <div class="flex-1 overflow-y-auto p-6 space-y-4">
      <div class="flex justify-start">
        <div class="max-w-md bg-blue-100 text-blue-800 rounded-2xl rounded-bl-none p-4 text-sm font-medium shadow-sm">
          <p>
            Hello! I'm your Mood Buddy, an AI assistant here to listen and provide support. This conversation is private and confidential. You can talk about your day, your feelings, or anything on your mind.
          </p>
        </div>
      </div>

      <div v-for="m in messages" :key="m.message_id || m.id"
        :class="m.sender_type === 'user' ? 'flex justify-end' : 'flex justify-start'">
        <div :class="[
          m.sender_type === 'user' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-white text-gray-800 rounded-bl-none',
          'rounded-2xl p-4 text-sm shadow-md',
          m.sender_type === 'user' ? 'max-w-md' : 'max-w-[75%]'
        ]">
          <template v-if="m.message_content">
            {{ m.message_content }}
          </template>
          <template v-if="m.image_preview">
            <img :src="m.image_preview" alt="uploaded" class="rounded-lg max-h-56 object-contain mt-2" />
          </template>
        </div>
      </div>

      <div v-if="isTyping" class="flex justify-start">
        <div class="bg-white rounded-2xl rounded-bl-none p-4 shadow-md">
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0.4s"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t border-gray-200 bg-white p-4">
      <div class="relative flex items-center bg-white rounded-full shadow-lg">
        <div v-if="showEmoji"
          class="absolute bottom-full left-0 mb-2 bg-white border border-gray-200 shadow-lg rounded-lg p-2 flex space-x-1 z-10">
          <button v-for="e in emojis" :key="e" @click="pickEmoji(e)"
            class="text-xl leading-none hover:scale-110 transition-transform">
            {{ e }}
          </button>
        </div>
        
        <button class="p-3 text-gray-500 hover:text-gray-700 transition-colors" @click="toggleEmoji">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>

        <div class="relative">
          <button ref="historyButtonEl" class="p-3 text-gray-500 hover:text-gray-700 transition-colors" @click="toggleHistory"
            title="Chat history">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
          <div v-if="showHistory" ref="historyDropdownEl"
            class="absolute bottom-full left-0 mb-2 w-72 max-h-80 overflow-y-auto bg-white border border-gray-200 shadow-lg rounded-lg p-2 z-10">
            <div class="font-semibold text-sm px-2 py-1 text-gray-700">Chat Sessions</div>
            <div v-if="!sessions.length" class="text-xs text-gray-400 px-2 py-2">No sessions yet</div>
            <button v-for="s in sessions" :key="s.session_id || s.id" @click="openSession(s)"
              class="w-full text-left px-2 py-2 hover:bg-gray-50 rounded">
              <div class="text-sm text-gray-800 truncate">{{ s.session_title || 'Session' }}</div>
              <div class="text-xs text-gray-500">
                {{ formatDateTime(s.started_at || s.created_at) }}
                <span v-if="s.ended_at" class="ml-1">→ {{ formatDateTime(s.ended_at) }}</span>
              </div>
              <div class="text-xs" :class="s.is_active ? 'text-green-600' : 'text-gray-400'">
                {{ s.is_active ? 'Active' : 'Closed' }}
              </div>
            </button>
          </div>
        </div>

        <label class="p-3 text-gray-500 hover:text-gray-700 transition-colors cursor-pointer" title="Upload image">
          <input ref="fileInputEl" type="file" accept="image/png,image/jpeg" class="hidden" @change="onFileChange" />
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5-5m0 0l5 5m-5-5v12" />
          </svg>
        </label>

        <input type="text" v-model="message" placeholder="Type a message..."
          class="flex-1 rounded-full py-3 px-4 mx-2 focus:outline-none focus:ring-0 focus:border-transparent text-gray-700"
          @keyup.enter="sendMessage">

        <button class="p-3 text-blue-500 hover:text-blue-700 transition-colors" @click="sendMessage">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ensureSession, getMessages, autoReply, autoReplyWithImage, closeSession, listSessions, reopenSession } from '@/services/chatService'

const message = ref('')
const session = ref(null)
const messages = ref([])
const isTyping = ref(false)
const showEmoji = ref(false)
const emojis = ['🙂', '😊', '😢', '😡', '😴', '👍', '❤️', '👏', '🙌']
const showHistory = ref(false)
const sessions = ref([])
const pendingFile = ref(null)
const fileInputEl = ref(null)
const historyButtonEl = ref(null)
const historyDropdownEl = ref(null)

onMounted(async () => {
  const s = await ensureSession(session, 'emotion', 'Mood Buddy Session')
  messages.value = await getMessages(s.session_id || s.id || s.sessionId)
  sessions.value = await listSessions()
})

onBeforeUnmount(async () => {
  const sessionId = session.value?.session_id || session.value?.id || session.value?.sessionId
  if (sessionId) {
    await closeSession(sessionId)
  }
  document.removeEventListener('click', onOutsideClick, true)
})

async function sendMessage() {
  if (!message.value.trim() && !pendingFile.value) return
  const text = message.value
  message.value = ''
  isTyping.value = true

  const sessionId = session.value.session_id || session.value.id || session.value.sessionId
  const tempId = `tmp_${Date.now().toString(36)}_${Math.random().toString(36).slice(2)}`
  const optimisticText = text || ''
  let image_preview = null
  if (pendingFile.value) {
    image_preview = URL.createObjectURL(pendingFile.value)
  }
  messages.value.push({ message_id: tempId, sender_type: 'user', message_content: optimisticText, image_preview, __optimistic: true })
  try {
    if (pendingFile.value) {
      await autoReplyWithImage(sessionId, text, pendingFile.value)
    } else {
      await autoReply(sessionId, text)
    }
    messages.value = await getMessages(sessionId)
  } finally {
    isTyping.value = false
    if (pendingFile.value && image_preview) URL.revokeObjectURL(image_preview)
    pendingFile.value = null
    if (fileInputEl.value) fileInputEl.value.value = ''
  }
}

function toggleEmoji() {
  showEmoji.value = !showEmoji.value
}

async function pickEmoji(e) {
  showEmoji.value = false
  const sessionId = session.value.session_id || session.value.id || session.value.sessionId
  const tempId = `tmp_${Date.now().toString(36)}_${Math.random().toString(36).slice(2)}`
  messages.value.push({ message_id: tempId, sender_type: 'user', message_content: e, __optimistic: true })
  isTyping.value = true
  try {
    await autoReply(sessionId, e)
    messages.value = await getMessages(sessionId)
  } finally {
    isTyping.value = false
  }
}

function toggleHistory() {
  showHistory.value = !showHistory.value
  if (showHistory.value) {
    document.addEventListener('click', onOutsideClick, true)
  } else {
    document.removeEventListener('click', onOutsideClick, true)
  }
}

async function openSession(s) {
  showHistory.value = false
  document.removeEventListener('click', onOutsideClick, true)
  const sid = s.session_id || s.id || s.sessionId
  try {
    await reopenSession(sid)
  } catch { }
  session.value = { ...s, is_active: true }
  messages.value = await getMessages(sid)
}

function formatDateTime(iso) {
  const d = new Date(iso)
  if (!iso || isNaN(d.getTime())) return '—'
  return d.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function onOutsideClick(e) {
  const btn = historyButtonEl.value
  const dd = historyDropdownEl.value
  if (!btn || !dd) return
  const target = e.target
  if (dd.contains(target) || btn.contains(target)) {
    return
  }
  showHistory.value = false
  document.removeEventListener('click', onOutsideClick, true)
}

function onFileChange(e) {
  const file = e.target.files && e.target.files[0]
  if (!file) return
  if (!['image/png', 'image/jpeg'].includes(file.type)) return
  pendingFile.value = file
}
</script>

<style scoped>
.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}
</style>