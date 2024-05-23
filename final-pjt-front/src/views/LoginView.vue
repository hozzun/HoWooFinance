<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="text-center">로그인</h1>
      <form @submit.prevent="logIn">
        <div class="form-group">
          <label for="username" class="login-label">이메일</label>
          <input class="form-control" type="text" id="username" v-model="username" placeholder="이메일을 입력하세요" />
        </div>
        <div class="form-group">
          <label for="password" class="login-label">비밀번호</label>
          <input class="form-control" type="password" id="password" v-model="password" placeholder="비밀번호를 입력하세요" />
        </div>
        <button class="btn btn-primary btn-block" type="submit">로그인</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();

const username = ref('');
const password = ref('');

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};
</script>

<style scoped>
/* @import url('https://fonts.googleapis.com/css?family=Raleway:300,400,600'); */

body {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 400;
  line-height: 1.6;
  color: #212529;
  text-align: left;
  /* background-color: #f5f8fa; */
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 92.5vh;
  background: linear-gradient(to bottom, white,  rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5));
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.text-center {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.login-label {
  font-weight: bold;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.btn-block {
  width: 100%;
}
</style>
