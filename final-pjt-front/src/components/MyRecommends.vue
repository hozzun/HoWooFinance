<template>
  * HoWoo Bot은 AI기반 예/적금 상품추천 서비스입니다.
  <div class="chat_window">
    <div class="top_menu">
      <div class="buttons">
        <div class="button close"></div>
        <div class="button minimize"></div>
        <div class="button maximize"></div>
      </div>
      <div class="title">HoWoo Bot</div>
    </div>
    <ul class="messages">
      <li v-for="(message, index) in sortedMessages" :key="index" :class="['message', 'appeared', message.role === 'user' ? 'right' : 'left']">
        <div class="avatar"></div>
        <div class="text_wrapper">
          <div class="text" v-html="message.content"></div>
        </div>
        <span class="time_date">{{ formatDate(message.timestamp) }}</span>
      </li>
    </ul>
    <div class="bottom_wrapper clearfix">
      <div class="message_input_wrapper">
        <input v-model="userInput" @keyup.enter="sendMessage" class="message_input" placeholder="메시지를 입력하세요..." />
      </div>
      <div class="send_message" @click="sendMessage">
        <div class="text">전송</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';

const messages = ref([]);
const userInput = ref('');
const store = useCounterStore();

const sendMessage = async () => {
  if (userInput.value.trim() === '') return;

  const timestamp = new Date();
  messages.value.push({ role: 'user', content: userInput.value, timestamp });

  try {
    const response = await fetch(`${store.baseURL}/chatbot/recommend/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userInput.value })
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const data = await response.json();

    if (data.error) {
      messages.value.push({ role: 'bot', content: `Error: ${data.error}`, timestamp: new Date() });
    } else {
      const formattedRecommendation = formatRecommendation(data.recommendation);
      messages.value.push({ role: 'bot', content: formattedRecommendation, timestamp: new Date() });
    }
  } catch (error) {
    console.error('Error fetching recommendation:', error);
    messages.value.push({ role: 'bot', content: `Error: ${error.message}`, timestamp: new Date() });
  } finally {
    userInput.value = '';
  }
};

const formatRecommendation = (recommendation) => {
  return recommendation.split('<br>').map(line => {
    if (line.includes('**')) {
      return `<p><strong>${line.replace(/\*\*/g, '')}</strong></p>`;
    }
    return `<p>${line}</p>`;
  }).join('');
};

const formatDate = (timestamp) => {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).format(timestamp);
};

const sortedMessages = computed(() => {
  return messages.value.slice().sort((a, b) => a.timestamp - b.timestamp);
});
</script>


<style scoped>
/* @import url('https://fonts.googleapis.com/css?family=Raleway:300,400,600'); */

body {
  background-color: #edeff2;
  /* font-family: "Raleway", "Roboto", sans-serif; */
}

.chat_window {
  position: absolute;
  width: calc(100% - 20px);
  max-width: 1000px;
  height: 550px;
  border-radius: 10px;
  background-color: #fff;
  left: 50%;
  top: 58%;
  transform: translateX(-50%) translateY(-50%);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  background-color: #f8f8f8;
  overflow: hidden;
}

.top_menu {
  background-color: #fff;
  width: 100%;
  padding: 20px 0 15px;
  box-shadow: 0 1px 30px rgba(0, 0, 0, 0.1);
}

.top_menu .buttons {
  margin: 3px 0 0 20px;
  position: absolute;
}

.top_menu .buttons .button {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 10px;
  position: relative;
}

.top_menu .buttons .button.close {
  background-color: #f5886e;
  margin-top: 2.5px;
  margin-left: 1.5px;
}

.top_menu .buttons .button.minimize {
  background-color: #fdbf68;
}

.top_menu .buttons .button.maximize {
  background-color: #a3d063;
}

.top_menu .title {
  text-align: center;
  color: #bcbdc0;
  font-size: 20px;
}

.messages {
  position: relative;
  list-style: none;
  padding: 20px 10px 0 10px;
  margin: 0;
  height: 347px;
  overflow-y: scroll;
  height: 500px;
}

.messages .message {
  clear: both;
  overflow: hidden;
  margin-bottom: 20px;
  transition: all 0.5s linear;
  opacity: 0;
}

.messages .message.left .avatar {
  background-color: #f5886e;
  float: left;
}

.messages .message.left .text_wrapper {
  background-color: #ffe6cb;
  margin-left: 20px;
}

.messages .message.left .text_wrapper::after, .messages .message.left .text_wrapper::before {
  right: 100%;
  border-right-color: #ffe6cb;
}

.messages .message.left .text {
  color: #c48843;
  color: black;
}

.messages .message.right .avatar {
  background-color: #fdbf68;
  float: right;
}

.messages .message.right .text_wrapper {
  background-color: #c7eafc;
  margin-right: 20px;
  float: right;
}

.messages .message.right .text_wrapper::after, .messages .message.right .text_wrapper::before {
  left: 100%;
  border-left-color: #c7eafc;
}

.messages .message.right .text {
  color: #45829b;
  color: black;
}

.messages .message.appeared {
  opacity: 1;
}

.messages .message .avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: inline-block;
}

.messages .message .text_wrapper {
  display: inline-block;
  padding: 15px;
  border-radius: 6px;
  width: calc(100% - 70px);
  min-width: 100px;
  position: relative;
}

.messages .message .text_wrapper::after, .messages .message .text_wrapper:before {
  top: 18px;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}

.messages .message .text_wrapper::after {
  border-width: 10px;
  margin-top: 0px;
}

.messages .message .text_wrapper::before {
  border-width: 12px;
  margin-top: -2px;
}

.messages .message .text_wrapper .text {
  font-size: 14px;
  font-weight: 300;
}

.bottom_wrapper {
  position: relative;
  width: 100%;
  background-color: #fff;
  padding: 20px 20px;
  position: absolute;
  bottom: 0;
}

.bottom_wrapper .message_input_wrapper {
  display: inline-block;
  height: 50px;
  border-radius: 25px;
  border: 1px solid #bcbdc0;
  width: calc(100% - 160px);
  position: relative;
  padding: 0 20px;
}

.bottom_wrapper .message_input_wrapper .message_input {
  border: none;
  height: 100%;
  box-sizing: border-box;
  width: calc(100% - 40px);
  position: absolute;
  outline-width: 0;
  color: gray;
}

.bottom_wrapper .send_message {
  width: 140px;
  height: 50px;
  display: inline-block;
  border-radius: 50px;
  background-color: rgba(24, 204, 144, 0.8);
  border: 2px solid rgba(24, 204, 144, 0.8);
  color: #fff;
  cursor: pointer;
  transition: all 0.2s linear;
  text-align: center;
  float: right;
}

.bottom_wrapper .send_message:hover {
  color: #f2f3f1;
  background-color: #097e39;
  border-color: white;
}

.bottom_wrapper .send_message .text {
  font-size: 18px;
  font-weight: 300;
  display: inline-block;
  line-height: 48px;
}

.message_template {
  display: none;
}

.time_date {
  display: block;
  font-size: 12px;
  margin: 8px 0 0;
  color: #747474;
  text-align: right;
}
</style>
