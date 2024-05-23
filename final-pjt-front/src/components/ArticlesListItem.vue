<template>
  <tr class="article-row">
    <td>{{ article.id }}</td>
    <td>
      <div class="article-details">
        <span class="title">{{ article.title }}</span>
      </div>
    </td>
    <td>{{ usernameWithoutDomain(article.username) }}</td>
    <td class="date">{{ formatDateTime(article.created_at) }}</td>
    <td>
      <RouterLink :to="{name: 'articlesdetail', params: { id: article.id }}" class="detail-link btn btn-info">
        상세 조회
      </RouterLink>
    </td>
  </tr>
</template>

<script setup>
defineProps({
  article: Object,
})

import { RouterLink } from 'vue-router';

const usernameWithoutDomain = (email) => {
  return email.split('@')[0];
};

const formatDateTime = (dateTime) => {
  const date = new Date(dateTime);
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).replace('T', ' ');
}
</script>

<style scoped>
.article-row {
  cursor: pointer;
  transition: background-color 0.3s;
}

.article-row:hover {
  background-color: #f1f1f1;
}

.article-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 1rem;
  font-weight: bold;
  margin-right: 10px;
  color: #333;
}

.date {
  font-size: 0.9rem;
  color: #888;
}

.detail-link {
  padding: 5px 10px;
  background-color: #3bb18d;
  border-color: white;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.detail-link:hover {
  background-color: #0056b3;
}
</style>
