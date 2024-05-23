<template>
  <div style="background: linear-gradient(to bottom, white,  rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5)); min-height:92.5vh;">
    <div class="container">
      <div class="form-container">
        <div class="panel panel-primary">
          <div class="panel-heading">
            <h4 class="panel-title">
              <span class="glyphicon glyphicon-pencil">게시글 작성</span> 
            </h4>
          </div>
          <div class="panel-body">
            <form @submit.prevent="createArticle" class="article-form">
              <div class="form-group">
                <br>
                <label for="title">[ 게시글 제목 ]</label>
                <input type="text" id="title" v-model.trim="title" class="form-control" placeholder="제목을 입력하세요" required>
              </div>
              <div class="form-group">
                <label for="content">[ 게시글 내용 ]</label>
                <textarea id="content" v-model.trim="content" class="form-control" placeholder="내용을 입력하세요" rows="5" required></textarea>
              </div>
              <div class="form-group">
                <label for="category">[ 카테고리 ]</label>
                <select id="category" v-model="category" class="form-control" required>
                  <option value="notice">공지사항</option>
                  <option value="question">질문게시판</option>
                  <option value="review">리뷰게시판</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary btn-block">
                <span class="glyphicon glyphicon-ok"></span> 작성하기
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useCounterStore } from '@/stores/counter';
  import { useRouter } from 'vue-router';
  import axios from 'axios'
  
  const store = useCounterStore()
  const router = useRouter()
  
  const title = ref('')
  const content = ref('')
  const category = ref('all') // Default value for category
  
  const createArticle = async () => {
    if (!store.isAuthenticated) {
      console.error('사용자가 로그인되어 있지 않습니다.')
      window.alert('로그인이 필요합니다.')
      router.push({ name: 'login' })
      return
    }
  
    try {
      await axios.post('http://127.0.0.1:8000/articles/', {
        title: title.value,
        content: content.value,
        category: category.value // Include category in the request
      }, {
        headers: { Authorization: `Token ${store.token}` }
      });
      router.push({ name: 'articles' });
    } catch (error) {
      console.error('게시글 작성 중 오류 발생:', error);
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
  