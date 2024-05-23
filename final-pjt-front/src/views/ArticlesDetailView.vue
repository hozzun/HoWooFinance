<template>
  <div class="background">
    <div class="container my-5">
      <div class="header mb-4">
        <button @click="goBack" class="btn btn-secondary"><i class="fa fa-arrow-left"></i> 뒤로가기</button>
      </div>
      <div v-if="article" class="card">
        <div class="card-body">
          <p class="card-title"><i class="fa fa-user"></i> 작성자: {{ usernameWithoutDomain(article.username) }}</p>
          <p class="card-text"><i class="fa fa-hashtag"></i> {{ article.id }}번 게시글</p>
          <br>
          <h3 class="card-title">{{ article.title }}</h3>
          <hr>
          <br>
          <h5 class="card-text">{{ article.content }}</h5>
          <br>
          <br>
          <hr>
          <p class="text-muted"><i class="fa fa-clock"></i> 작성시간: {{ formattedCreatedAt }}</p>
          <p class="text-muted"><i class="fa fa-edit"></i> 수정시간: {{ formattedUpdatedAt }}</p>
          <div v-if="isAuthor" class="action-buttons">
            <button @click="updateArticle" class="btn btn-primary"><i class="fa fa-edit"></i> 게시글 수정</button>
            <button @click="confirmDeleteArticle(article.id)" class="btn btn-danger"><i class="fa fa-trash"></i> 게시글 삭제</button>
          </div>
        </div>
      </div>
      <div class="card mt-4">
        <div class="card-body">
          <h4 class="card-title"><i class="fa fa-comments"></i> 댓글</h4>
          <textarea v-model.trim="commentContent" class="form-control" rows="3" placeholder="댓글을 입력해주세요"></textarea>
          <button @click="postComment" class="btn btn-primary mt-2"><i class="fa fa-reply"></i> 댓글 작성</button>
          <hr>
          <div v-if="filteredComments.length">
            <div v-for="comment in filteredComments" :key="comment.id" class="border rounded p-2 mb-2">
              <p><strong>{{ comment.content }}</strong> - {{ usernameWithoutDomain(comment.username) }}</p>
              <hr>
              <p class="text-muted"><i class="fa fa-clock"></i> 작성시간: {{ formatDateTime(comment.created_at) }}</p>
              <div v-if="isCommentAuthor(comment)" class="text-right">
                <button @click="confirmDeleteComment(comment.id)" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i> 댓글 삭제</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const article = ref(null)
const commentContent = ref('')
const comments = ref([])

onMounted(() => {
  fetchArticle()
})

const formatDateTime = (dateTime) => {
  const date = new Date(dateTime)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).replace('T', ' ')
}

const formattedCreatedAt = computed(() => {
  return article.value ? formatDateTime(article.value.created_at) : ''
})

const formattedUpdatedAt = computed(() => {
  return article.value ? formatDateTime(article.value.updated_at) : ''
})

const usernameWithoutDomain = (email) => {
  return email.split('@')[0];
};

const fetchArticle = () => {
  axios({
    method: 'get',
    url: `${store.baseURL}/articles/${route.params.id}`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((response) => {
    console.log('Fetched article:', response.data)
    article.value = response.data
    fetchComments()
  })
  .catch((error) => {
    console.error('게시글을 불러오는 중 에러가 발생했습니다:', error)
    window.alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
  })
}

const fetchComments = () => {
  const url = `${store.baseURL}/articles/comments/`
  console.log('Fetching comments from URL:', url)
  
  axios({
    method: 'get',
    url: url,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((response) => {
    console.log('Comments response:', response.data)
    comments.value = response.data
  })
  .catch((error) => {
    console.error('댓글을 불러오는 중 에러가 발생했습니다:', error)
    window.alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
  })
}

const postComment = () => {
  if (!commentContent.value.trim()) {
    window.alert('댓글 내용을 입력해주세요.')
    return
  }

  axios({
    method: 'post',
    url: `${store.baseURL}/articles/${route.params.id}/create/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      content: commentContent.value.trim()
    }
  })
  .then((response) => {
    comments.value.push(response.data)
    commentContent.value = ''
  })
  .catch((error) => {
    console.error('댓글을 작성하는 중 에러가 발생했습니다:', error)
    window.alert('댓글을 작성하는 중 에러가 발생했습니다.')
  })
}

const isAuthor = computed(() => {
  console.log('Article username:', article.value?.username)
  console.log('Current username:', store.user?.username)
  return article.value && store.user && article.value.username === store.user.username
})

const isCommentAuthor = (comment) => {
  console.log('Comment username:', comment.username)
  console.log('Current username:', store.user?.username)
  return comment.username === store.user.username
}

const updateArticle = () => {
  router.push({ name: 'articlesupdate', params: { id: article.value.id } })
}

const confirmDeleteArticle = (id) => {
  if (confirm("정말 삭제하시겠습니까?")) {
    deleteArticle(id)
  }
}

const confirmDeleteComment = (id) => {
  if (confirm("정말 삭제하시겠습니까?")) {
    deleteComment(id)
  }
}

const deleteArticle = function (id) {
  axios({
    method: 'delete',
    url: `${store.baseURL}/articles/${id}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then(() => {
    window.alert('게시글이 성공적으로 삭제되었습니다.')
    router.push({ name: 'articles' })  // 게시글 목록 페이지로 이동
  })
  .catch((error) => {
    console.error('게시글 삭제 실패:', error)
    window.alert('권한이 없습니다.')
  })
}

const deleteComment = (commentId) => {
  axios({
    method: 'delete',
    url: `${store.baseURL}/articles/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then(() => {
    comments.value = comments.value.filter(comment => comment.id !== commentId)
  })
  .catch((error) => {
    console.error('댓글을 삭제하는 중 에러가 발생했습니다:', error)
    window.alert('권한이 없습니다.')
  })
}

const filteredComments = computed(() => {
  return comments.value.filter(comment => comment.article_id === article.value.id)
})

// 뒤로가기 함수
const goBack = () => {
  router.push({ name: 'articles' }) // 게시판 페이지로 이동
}
</script>

<style scoped>
.background {
  background: linear-gradient(to bottom, white, rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5)), rgba(29, 63, 85, 0.5);
  min-height: 92.5vh;
  padding: 20px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-body {
  padding: 20px;
}

.card-body h3, .card-body h5, .card-body p {
  margin-bottom: 20px;
}

.card-body h3 {
  font-size: 1.75rem;
  font-weight: bold;
}

.card-body h5 {
  font-size: 1.25rem;
  font-weight: normal;
}

.btn-primary {
  margin-right: 10px;
  background-color: #3bb18d;
  border-color: white;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #2e865c;
}

.btn-danger {
  transition: background-color 0.3s;
}

.btn-danger:hover {
  background-color: #c9302c;
}

textarea.form-control {
  resize: vertical;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: flex-end;
}
</style>
