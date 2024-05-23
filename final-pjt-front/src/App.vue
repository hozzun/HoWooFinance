<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top main-nav">
      <div class="container">
        <a class="navbar-brand" href="/">
          <img src="/public/images/Howoologo.png" alt="Howoo Finance" class="logo-img" />
        </a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'productlist'}">상품 조회</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'exchangerate'}">환율 계산기</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'closebank'}">주변 은행</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'articles'}">게시판</RouterLink>
            </li>
            <template v-if="store.isAuthenticated">
              <li class="nav-item">
                <RouterLink class="nav-link" :to="{ name: 'mypage'}">마이 페이지</RouterLink>
              </li>
              <li class="nav-item">
                <button @click="logOut" class="nav-link btn btn-link"><span style="color: red;">로그아웃</span></button>
              </li>
            </template>
            <template v-else>
              <li class="nav-item">
                <RouterLink class="nav-link" :to="{ name: 'login'}">로그인</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" :to="{ name: 'signup'}">회원가입</RouterLink>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>

    <!-- 퀵 메뉴 토글 버튼 -->
    <button class="quickmenu-toggle-button" @click="toggleQuickMenu">
      <span v-if="quickmenuOpen">✖</span>
      <span v-else>☰</span>
    </button>

    <div v-if="quickmenuOpen" class="quickmenu-overlay" @click="closeQuickMenu">
      <div class="quickmenu" @click.stop>
        <QuickMenu @close="toggleQuickMenu" />
      </div>
    </div>
    <RouterView />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';
import QuickMenu from '@/components/QuickMenu.vue';

const store = useCounterStore();

onMounted(() => {
  if (store.token) {
    store.getUserDetails();
  }
});

const logOut = () => {
  store.logOut();
};

const user = computed(() => store.user);

const quickmenuOpen = ref(false);

const toggleQuickMenu = () => {
  quickmenuOpen.value = !quickmenuOpen.value;
};

const closeQuickMenu = () => {
  quickmenuOpen.value = false;
};
</script>

<style scoped>
/* @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap'); */

/* #app {
  font-family: 'Noto Sans', sans-serif;
} */

.welcome-message {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.main-nav {
  padding: 10px;
  position: relative;
  z-index: 1000;
}

.navbar-brand img {
  height: 40px;
}

.nav-link {
  color: #555;
  font-weight: bold;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #0056b3;
}

.quickmenu-toggle-button {
  position: fixed;
  width: 60px;
  height: 60px;
  bottom: 20px;
  right: 20px;
  background-color: #0056b3;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  z-index: 9999;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.quickmenu-toggle-button:hover {
  background-color: #0056b3;
  transform: scale(1.1);
}

.quickmenu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 9998;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
}

.quickmenu {
  /* background-color: white; */
  padding: 20px;
  border-radius: 10px;
  width: 100%;
  max-width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.5s ease;
}

@keyframes slideIn {
  0% {
    transform: translateY(100%);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.mainpage-gradient {
  background: linear-gradient(to top, rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5), rgba(60, 120, 140, 0.5));
}
</style>
