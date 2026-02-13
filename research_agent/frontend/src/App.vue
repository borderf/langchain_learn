<template>
  <div class="app-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>Research Agent</h2>
        <button class="new-chat-btn" @click="createNewSession">+ 新建会话</button>
      </div>
      <div class="session-list">
        <div
          v-for="session in sessions"
          :key="session.id"
          :class="['session-item', { active: currentSession?.id === session.id }]"
          @click="selectSession(session.id)"
        >
          <span class="session-title">{{ session.title }}</span>
          <button class="delete-btn" @click.stop="deleteSession(session.id)">删除</button>
        </div>
      </div>
    </aside>

    <main class="chat-main">
      <div v-if="!currentSession" class="empty-state">
        <h2>欢迎使用 Research Agent</h2>
        <p>点击左侧"新建会话"开始对话</p>
      </div>

      <template v-else>
        <div class="chat-header">
          <h3>{{ currentSession.title }}</h3>
        </div>

        <div class="messages-container" ref="messagesContainer">
          <div
            v-for="msg in messages"
            :key="msg.id"
            :class="['message', msg.role]"
          >
            <div class="message-role">{{ msg.role === 'user' ? '用户' : '助手' }}</div>
            <div class="message-content">{{ msg.content }}</div>
          </div>
        </div>

        <div class="input-area">
          <textarea
            v-model="inputMessage"
            placeholder="输入消息..."
            @keydown.enter.exact.prevent="sendMessage"
            :disabled="loading"
          ></textarea>
          <button @click="sendMessage" :disabled="loading || !inputMessage.trim()">
            {{ loading ? '发送中...' : '发送' }}
          </button>
        </div>
      </template>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue'
import { sessionApi } from './api'

export default {
  name: 'App',
  setup() {
    const sessions = ref([])
    const currentSession = ref(null)
    const messages = ref([])
    const inputMessage = ref('')
    const loading = ref(false)
    const messagesContainer = ref(null)

    const loadSessions = async () => {
      try {
        const res = await sessionApi.list()
        sessions.value = res.data
      } catch (error) {
        console.error('加载会话列表失败:', error)
      }
    }

    const createNewSession = async () => {
      try {
        const res = await sessionApi.create()
        sessions.value.unshift(res.data)
        selectSession(res.data.id)
      } catch (error) {
        console.error('创建会话失败:', error)
      }
    }

    const selectSession = async (sessionId) => {
      try {
        const res = await sessionApi.get(sessionId)
        currentSession.value = res.data
        messages.value = res.data.messages || []
        scrollToBottom()
      } catch (error) {
        console.error('获取会话详情失败:', error)
      }
    }

    const deleteSession = async (sessionId) => {
      if (!confirm('确定删除此会话?')) return
      try {
        await sessionApi.delete(sessionId)
        sessions.value = sessions.value.filter(s => s.id !== sessionId)
        if (currentSession.value?.id === sessionId) {
          currentSession.value = null
          messages.value = []
        }
      } catch (error) {
        console.error('删除会话失败:', error)
      }
    }

    const sendMessage = async () => {
      if (!inputMessage.value.trim() || loading.value) return

      const content = inputMessage.value.trim()
      inputMessage.value = ''
      loading.value = true

      messages.value.push({
        id: Date.now(),
        role: 'user',
        content: content,
        session_id: currentSession.value.id
      })
      scrollToBottom()

      try {
        const res = await sessionApi.get(currentSession.value.id)
        messages.value = res.data.messages || []
        scrollToBottom()
      } catch (error) {
        console.error('发送消息失败:', error)
      } finally {
        loading.value = false
      }
    }

    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }

    onMounted(() => {
      loadSessions()
    })

    return {
      sessions,
      currentSession,
      messages,
      inputMessage,
      loading,
      messagesContainer,
      loadSessions,
      createNewSession,
      selectSession,
      deleteSession,
      sendMessage
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
}

.app-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 260px;
  background: #202123;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #4d4d4f;
}

.sidebar-header h2 {
  font-size: 18px;
  margin-bottom: 12px;
}

.new-chat-btn {
  width: 100%;
  padding: 10px;
  background: transparent;
  border: 1px solid #4d4d4f;
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.new-chat-btn:hover {
  background: #2a2b32;
}

.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.session-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 4px;
}

.session-item:hover {
  background: #2a2b32;
}

.session-item.active {
  background: #343541;
}

.session-title {
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.delete-btn {
  background: transparent;
  border: none;
  color: #999;
  font-size: 12px;
  cursor: pointer;
  opacity: 0;
  padding: 4px 8px;
}

.session-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: #ff6b6b;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #666;
}

.empty-state h2 {
  margin-bottom: 12px;
}

.chat-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e5e5e5;
}

.chat-header h3 {
  font-size: 16px;
  font-weight: 500;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 16px;
  padding: 12px 16px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background: #e3f2fd;
  margin-left: auto;
  text-align: right;
}

.message.assistant {
  background: #f5f5f5;
}

.message-role {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}

.message-content {
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.input-area {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #e5e5e5;
  background: #fafafa;
}

.input-area textarea {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  font-size: 14px;
  font-family: inherit;
  min-height: 48px;
  max-height: 120px;
}

.input-area textarea:focus {
  outline: none;
  border-color: #10a37f;
}

.input-area button {
  padding: 12px 24px;
  background: #10a37f;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.input-area button:hover:not(:disabled) {
  background: #0d8a6a;
}

.input-area button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
