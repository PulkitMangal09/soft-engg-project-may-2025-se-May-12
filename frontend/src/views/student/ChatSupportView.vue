<template>
  <div class="flex flex-col h-screen bg-gray-50">

    <!-- Header -->
    <div class="px-4 py-3 border-b border-gray-200 flex items-center justify-between bg-white">
      <button class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100" @click="$router.go(-1)">
        ←
      </button>
      <h1 class="text-lg font-semibold">Mood Buddy</h1>
      <div class="w-8"></div> <!-- Spacer for alignment -->
    </div>

    <!-- Chat Container -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <!-- System Message -->
      <div class="flex justify-start">
        <div class="max-w-xs bg-blue-100 text-blue-800 rounded-2xl p-3 text-sm">
          🤖 AI Support - This conversation is private and confidential
        </div>
      </div>

      <!-- History -->
      <div v-for="m in messages" :key="m.message_id || m.id"
        :class="m.sender_type === 'user' ? 'flex justify-end' : 'flex justify-start'">
        <div :class="[
          m.sender_type === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-800',
          'rounded-2xl p-3 text-sm',
          m.sender_type === 'user' ? 'max-w-xs' : 'max-w-[75%]'
        ]">
          {{ m.message_content }}
        </div>
      </div>

      <!-- Typing Indicator -->
      <div v-if="isTyping" class="flex justify-start">
        <div class="bg-gray-100 rounded-full p-2">
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div class="border-t border-gray-200 bg-white p-3">
      <div class="relative flex items-center">
        <!-- Emoji picker popover -->
        <div v-if="showEmoji"
          class="absolute bottom-12 left-2 bg-white border border-gray-200 shadow-lg rounded-lg p-2 flex space-x-1 z-10">
          <button v-for="e in emojis" :key="e" @click="pickEmoji(e)"
            class="text-xl leading-none hover:scale-110 transition-transform">
            {{ e }}
          </button>
        </div>

        <button class="p-2 text-gray-500 hover:text-gray-700" @click="toggleEmoji">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
        <!-- Chat history button + dropdown -->
        <div class="relative">
          <button ref="historyButtonEl" class="p-2 text-gray-500 hover:text-gray-700" @click="toggleHistory"
            title="Chat history">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
          <div v-if="showHistory" ref="historyDropdownEl"
            class="absolute bottom-12 left-0 w-72 max-h-80 overflow-y-auto bg-white border border-gray-200 shadow-lg rounded-lg p-2 z-10">
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
        <input type="text" v-model="message" placeholder="Type a message..."
          class="flex-1 border border-gray-300 rounded-full py-2 px-4 mx-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          @keyup.enter="sendMessage">
        <button class="p-2 text-blue-500 hover:text-blue-700" @click="sendMessage">
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
import { ensureSession, getMessages, autoReply, closeSession, listSessions, reopenSession } from '@/services/chatService'

const message = ref('')
const session = ref(null)
const messages = ref([])
const isTyping = ref(false)
const showEmoji = ref(false)
const emojis = ['🙂', '😊', '😢', '😡', '😴', '👍', '❤️', '👏', '🙌']
const showHistory = ref(false)
const sessions = ref([])
const historyButtonEl = ref(null)
const historyDropdownEl = ref(null)

onMounted(async () => {
  // Ensure an emotion chat session exists
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
  if (!message.value.trim()) return
  const text = message.value
  message.value = ''
  isTyping.value = true

  const sessionId = session.value.session_id || session.value.id || session.value.sessionId
  // optimistic user message
  const tempId = `tmp_${Date.now().toString(36)}_${Math.random().toString(36).slice(2)}`
  messages.value.push({ message_id: tempId, sender_type: 'user', message_content: text, __optimistic: true })
  try {
    const { bot_reply } = await autoReply(sessionId, text)
    // Reload history after auto-reply stored both messages
    messages.value = await getMessages(sessionId)
  } finally {
    isTyping.value = false
  }
}

function toggleEmoji() {
  showEmoji.value = !showEmoji.value
}

async function pickEmoji(e) {
  showEmoji.value = false
  // send emoji immediately
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
  // attach/detach outside-click listener
  if (showHistory.value) {
    // use capture phase to get early
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
  // Render in IST (Asia/Kolkata)
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
</script>

<style scoped>
.animate-bounce {
  animation: bounce 1.5s infinite;
}

@keyframes bounce {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-5px);
  }
}
</style>
