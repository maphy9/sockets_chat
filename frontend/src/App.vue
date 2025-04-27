<script setup>
import { ref } from 'vue'

const room = ref('')
const message = ref('')
const messages = ref([])
let socket = null
const connected = ref(false)

const connect = () => {
  socket = new WebSocket(`ws://localhost:8000/ws/${room.value}`)

  socket.onopen = () => {
    connected.value = true
  }

  socket.onmessage = (event) => {
    messages.value.push(event.data)
  }

  socket.onclose = () => {
    connected.value = false
    socket = null
  }
}

const sendMessage = () => {
  if (message.value.trim() !== '' && socket) {
    socket.send(message.value)
    messages.value.push(`You: ${message.value}`)
    message.value = ''
  }
}
</script>

<template>
  <div class="chat-container">
    <h1>Simple Chat</h1>

    <div v-if="!connected">
      <input v-model="room" placeholder="Room name" />
      <button @click="connect">Join Room</button>
    </div>

    <div v-else>
      <div class="messages">
        <div v-for="(msg, index) in messages" :key="index" class="message">
          {{ msg }}
        </div>
      </div>

      <input v-model="message" @keyup.enter="sendMessage" placeholder="Type your message..." />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  max-width: 500px;
  margin: 50px auto;
  text-align: center;
}
.messages {
  border: 1px solid #ccc;
  height: 300px;
  overflow-y: scroll;
  padding: 10px;
  margin-bottom: 10px;
}
.message {
  margin-bottom: 5px;
}
input {
  width: 70%;
  padding: 8px;
  margin-right: 5px;
}
button {
  padding: 8px 12px;
}
</style>
