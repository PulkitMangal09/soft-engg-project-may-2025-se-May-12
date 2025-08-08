<template>
    <div class="min-h-screen bg-gray-50 flex flex-col items-center py-6 px-2 md:px-0">
        <div class="bg-white rounded-xl shadow p-6 w-full max-w-md flex flex-col h-[600px]">
            <div class="bg-gray-50 rounded-lg p-3 text-xs text-center text-gray-600 mb-2">
                AI Assistant trained on your health conditions and dietary needs
            </div>
            <div class="flex-1 overflow-y-auto mb-2">
                <div v-for="m in messages" :key="m.message_id || m.id"
                    :class="m.sender_type === 'user' ? 'mb-2 flex justify-end' : 'mb-2 flex justify-start'">
                    <div :class="m.sender_type === 'user' ? 'bg-emerald-500 text-white' : 'bg-gray-200 text-gray-800'"
                        class="rounded-lg p-2 max-w-[70%]">
                        {{ m.message_content }}
                    </div>
                </div>
                <div v-if="isTyping" class="mb-2 flex justify-start">
                    <div class="bg-gray-200 rounded-lg p-2 max-w-[70%]">Typing…</div>
                </div>
            </div>
            <div class="flex gap-2 mt-2">
                <input v-model="message" type="text" class="form-input flex-1"
                    placeholder="Ask about foods, recipes, or nutrition..." @keyup.enter="send">
                <button class="btn-primary px-4" @click="send">➤</button>
            </div>
        </div>
        <div class="text-xs text-gray-400 mt-4">Diet Chat Bot</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ensureSession, getMessages, autoReply } from '@/services/chatService'

const message = ref('')
const session = ref(null)
const messages = ref([])
const isTyping = ref(false)

onMounted(async () => {
    const s = await ensureSession(session, 'diet', 'Diet Assistant Session')
    messages.value = await getMessages(s.session_id || s.id || s.sessionId)
})

async function send() {
    if (!message.value.trim()) return
    const text = message.value
    message.value = ''
    isTyping.value = true
    const sessionId = session.value.session_id || session.value.id || session.value.sessionId
    // optimistic user message
    const tempId = `tmp_${Date.now().toString(36)}_${Math.random().toString(36).slice(2)}`
    messages.value.push({ message_id: tempId, sender_type: 'user', message_content: text, __optimistic: true })
    try {
        await autoReply(sessionId, text)
        messages.value = await getMessages(sessionId)
    } finally {
        isTyping.value = false
    }
}
</script>