<template>
  <div style="background: linear-gradient(to bottom, white,  rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5)); min-height:92.5vh;">
  <div class="product-page-container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light custom-navbar">
      <a class="navbar-brand" href="#">Category || </a>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mx-auto">
          <li class="nav-item" :class="{ active: selected === 'deposits' }">
            <a class="nav-link" href="#" @click.prevent="showSection('deposits')">정기예금</a>
          </li>
          <li class="nav-item" :class="{ active: selected === 'savings' }">
            <a class="nav-link" href="#" @click.prevent="showSection('savings')">적금</a>
          </li>
          <li class="nav-item" :class="{ active: selected === 'recommends' }">
            <a class="nav-link" href="#" @click.prevent="showSection('recommends')">AI 상품추천</a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="content-container">
      <div v-show="selected === 'deposits'">
        <Deposits />
      </div>
      <div v-show="selected === 'savings'">
        <Savings />
      </div>
      <div v-show="selected === 'recommends'">
        <MyRecommends />
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Deposits from '@/components/Deposits.vue';
import Savings from '@/components/Savings.vue';
import MyRecommends from '@/components/MyRecommends.vue';

const route = useRoute();
const router = useRouter();
const selected = ref('deposits');

const showSection = (section) => {
  selected.value = section;
  router.push({ name: 'productlist', query: { section } });
};

const updateSectionFromQuery = () => {
  const section = route.query.section;
  if (section && ['deposits', 'savings', 'recommends'].includes(section)) {
    selected.value = section;
  }
};

onMounted(() => {
  updateSectionFromQuery();
});

watch(() => route.query.section, () => {
  updateSectionFromQuery();
});
</script>

<style scoped>
.product-page-container {
  padding: 20px;
  /* font-family: 'Helvetica Neue', Arial, sans-serif; */
  color: #2c3e50;
}

.navbar {
  margin-bottom: 20px;
  margin-top: 20px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  border-radius: 10px;
}

.navbar-brand {
  font-size: 18px;
}

.navbar-nav {
  width: 100%;
  display: flex;
  justify-content: space-around;
  gap: 20px;
}

.nav-item {
  flex-grow: 1;
  text-align: center;
}

.nav-link {
  font-size: 18px;
  color: #000;
  transition: color 0.3s, background-color 0.3s;
}

.nav-item.active:nth-child(1) .nav-link,
.nav-item:nth-child(1) .nav-link:hover {
  color: #fff;
  background-color: rgba(1, 17, 236, 0.8);
  border-radius: 5px;
}

.nav-item.active:nth-child(2) .nav-link,
.nav-item:nth-child(2) .nav-link:hover {
  color: #fff;
  background-color: rgba(236, 28, 36, 0.8);
  border-radius: 5px;
}

.nav-item.active:nth-child(3) .nav-link,
.nav-item:nth-child(3) .nav-link:hover {
  color: #fff;
  background-color: rgba(24, 204, 144, 0.8);
  border-radius: 5px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fafafa;
  border: 1px solid #ddd;
  border-radius: 10px;
  margin-top: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

.card-wrapper {
  flex: 1 1 calc(25% - 15px);
  display: flex;
  justify-content: center;
  max-width: calc(25% - 15px);
}
</style>