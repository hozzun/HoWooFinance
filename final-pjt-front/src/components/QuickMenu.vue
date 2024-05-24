<template>
  <div class="quickmenu-style">
    <div class="number-pad">
      <button v-for="(label, index) in labels" :key="index" @click="handleClick(index + 1)" :class="{ 'home-button': index === 4 }">
        {{ label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import axios from 'axios'; // axios를 import 합니다.

const router = useRouter();
const store = useCounterStore();

const labels = ['예금', '적금', '추천', '환율', '홈', '게시판', '프로필', '지도', '데이터'];

const handleClick = (num) => {
  const userInput = num.toString();
  const options = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];
  
  if (options.includes(userInput)) {
    switch (userInput) {
      case '1':
        router.push({ name: 'productlist', query: { section: 'deposits' } });
        break;
      case '2':
        router.push({ name: 'productlist', query: { section: 'savings' } });
        break;
      case '3':
        router.push({ name: 'productlist', query: { section: 'recommends' } });
        break;
      case '4':
        router.push({ name: 'exchangerate' });
        break;
      case '5':
        router.push({ name: 'home' });
        break;
      case '6':
        router.push({ name: 'articles' });
        break;
      case '7':
        router.push({ name: 'mypage' });
        break;
      case '8':
        router.push({ name: 'closebank' });
        break;
      case '9':
        uploadData();
        break;    
    }
  }
}

const uploadData = async () => {
  const urls = [
    `${store.baseURL}/deposits/save_products/`,
    `${store.baseURL}/deposits/save_options/`,
    `${store.baseURL}/savings/save_products/`,
    `${store.baseURL}/savings/save_options/`
  ];

  try {
    await Promise.all(
      urls.map(url => 
        axios({
          method: 'get',
          url: url,
          headers: {
            Authorization: `Token ${store.token}`
          }
        })
      )
    );
    console.log('save success');
    window.alert('예적금 상품 데이터가 저장되었습니다.');
  } catch (error) {
    console.error('save fail', error);
    window.alert('예적금 상품 데이터 저장에 실패하였습니다.');
  }
}
</script>

<style scoped>
.quickmenu-style {
  width: 260px;
  height: auto;
  border: none;
  position: fixed;
  bottom: 80px;
  right: 20px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  animation: slideUp 0.3s ease-out;
}

.number-pad {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.number-pad button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  height: 60px;
  width: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: background-color 0.3s, transform 0.3s;
}

.number-pad button:hover {
  background-color: #0056b3;
  transform: scale(1.1);
}

.number-pad .home-button {
  background-color: #ff4500;
}

.number-pad .home-button:hover {
  background-color: #e03e00;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
