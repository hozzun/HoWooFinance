<template>
  <div class="container">
    <div class="form-container">
      <div class="panel panel-primary">
        <div class="panel-heading">
          <h4 class="panel-title">
            <span class="glyphicon glyphicon-pencil">게시글 수정</span> 
          </h4>
        </div>
        <div class="panel-body">
          <div v-if="article">
            <form @submit.prevent="updateArticle" class="article-form">
              <div class="form-group">
                <br>
                <label for="title">[ 게시글 제목 ]</label>
                <input type="text" id="title" v-model.trim="article.title" class="form-control" placeholder="제목을 입력하세요" required>
              </div>
              <div class="form-group">
                <label for="content">[ 게시글 내용 ]</label>
                <textarea id="content" v-model.trim="article.content" class="form-control" placeholder="내용을 입력하세요" rows="5" required></textarea>
              </div>
              <div class="form-group">
                <label for="category">[ 카테고리 ]</label>
                <select id="category" v-model="article.category" class="form-control" required>
                  <option value="notice">공지사항</option>
                  <option value="question">질문게시판</option>
                  <option value="review">리뷰게시판</option>
                  <option value="all">전체</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary btn-block">
                <span class="glyphicon glyphicon-ok"></span> 수정 완료
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const article = ref(null)

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.baseURL}/articles/${route.params.id}`,
    headers: {
    Authorization: `Token ${store.token}`
    }
  })
  .then((response) => {
    article.value = response.data
  })
  .catch((error) => {
    console.error('에러 발생:', error)
  })
})

const updateArticle = async () => {
  try {
    await axios.put(`${store.baseURL}/articles/${route.params.id}/`, {
      title: article.value.title,
      content: article.value.content,
      category: article.value.category // Include category in the request
    }, {
      headers: { Authorization: `Token ${store.token}` }
    });
    router.push({ name: 'articlesdetail', params: { id: route.params.id } })
  } catch (error) {
    window.alert('작성자가 아닙니다!')
    router.push({ name: 'articles' }) // 게시판 페이지로 이동
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh; /* 컨테이너를 세로로 중앙에 배치 */
}

.form-container {
  width: 100%;
  max-width: 600px; /* 폼의 최대 너비를 제한 */
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.panel-primary {
  border-color: #337ab7;
}

.panel-primary > .panel-heading {
  color: #fff;
  background-color: #3bb18d;
  border-color: #337ab7;
  height: 30px;
  border-radius: 10px;
}

.panel-title {
  font-size: 24px;
  text-align: center;
}

.article-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.form-control {
  padding: 5px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
}

textarea.form-control {
  resize: vertical;
  min-height: 150px;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  color: #fff;
  background-color: #3bb18d;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #286090;
}

.glyphicon {
  margin-right: 5px;
}
</style>
