<template>
  <div style="background: linear-gradient(to bottom, white,  rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5)); min-height:92.5vh;">
    <div class="board-container">
      <nav class="navbar navbar-expand-lg navbar-light bg-light custom-navbar">
        <a class="navbar-brand" href="#">Category || </a>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="#" @click="showSection('all')">전체</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="showSection('notice')">공지사항</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="showSection('question')">질문게시판</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click="showSection('review')">리뷰게시판</a>
            </li>
          </ul>
        </div>
      </nav>
      <hr>
      <div class="action-bar">
        <RouterLink :to="{ name: 'create'}" class="create-link btn btn-primary">
          게시글 작성하기
        </RouterLink>
      </div>
      <ArticlesList :section="activeSection" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { RouterLink } from 'vue-router';
import ArticlesList from '@/components/ArticlesList.vue';

const store = useCounterStore();
const activeSection = ref('all');

onMounted(async () => {
  try {
    await store.getArticles();
  } catch (error) {
    console.log(error);
  }
});

const showSection = (section) => {
  activeSection.value = section;
};
</script>

<style scoped>
/* @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap'); */

.board-container {
  padding: 20px;
  /* font-family: 'Noto Sans', sans-serif; */
  max-width: 900px;
  margin: 0 auto;
}

.navbar {
  margin-bottom: 20px;
  margin-top: 20px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.action-bar {
  text-align: right;
  margin-bottom: 20px;
}

.create-link {
  display: inline-block;
  padding: 10px 20px;
  background-color: #3bb18d;
  border-color: white;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.create-link:hover {
  background-color: #0056b3;
}
</style>
