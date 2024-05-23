<template>
  <div class="articles-container">
    <h3>게시글 목록</h3>
    <hr>
    <div class="articles-table">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>글번호</th>
            <th>제목</th>
            <th>작성자</th>
            <th>작성일</th>
            <th>상세조회</th>
          </tr>
        </thead>
        <tbody>
          <ArticlesListItem 
            v-for="article in filteredArticles"
            :key="article.id"
            :article="article"
          />
        </tbody>
      </table>
      <div v-if="filteredArticles.length === 0" class="no-articles">
        해당 섹션에 게시글이 없습니다.
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useCounterStore } from '@/stores/counter';
import ArticlesListItem from '@/components/ArticlesListItem.vue';

const store = useCounterStore();
const props = defineProps(['section']);

const filteredArticles = computed(() => {
  console.log('Current section:', props.section);
  console.log('Articles:', store.articles);
  if (props.section === 'all') {
    return store.articles;
  }
  const filtered = store.articles.filter(article => article.category === props.section);
  console.log('Filtered Articles:', filtered);
  return filtered;
});
</script>

<style scoped>
/* @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap'); */

.articles-container {
  padding: 20px;
  /* font-family: 'Noto Sans', sans-serif; */
  max-width: 900px;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h3 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
  font-size: 2rem;
}

.articles-table {
  width: 100%;
  margin-bottom: 20px;
}

.table {
  width: 100%;
  margin-bottom: 20px;
  border-collapse: separate;
  border-spacing: 0 15px;
}

th, td {
  padding: 12px;
  text-align: left;
  vertical-align: middle;
}

th {
  background-color: #f4f4f4;
  font-weight: bold;
  border-bottom: 2px solid #ddd;
}

tbody tr {
  background-color: #fff;
  transition: background-color 0.3s;
}

tbody tr:hover {
  background-color: #f1f1f1;
}

.no-articles {
  text-align: center;
  margin-top: 20px;
  color: #999;
  font-size: 1rem;
}

.detail-link {
  display: inline-block;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.detail-link:hover {
  background-color: #0056b3;
}

.table-hover tbody tr:hover {
  background-color: #f1f1f1;
}
</style>
