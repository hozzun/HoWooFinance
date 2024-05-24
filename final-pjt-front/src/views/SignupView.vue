<template>
  <div style="background: linear-gradient(to bottom, white,  rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5)); min-height:92.5vh;">
  <div class="signup-container">
    <div class="card bg-light mx-auto" style="max-width: 600px;">
      <article class="card-body">
        <h4 class="card-title mt-3 text-center">회원가입</h4>
        <br>
        <form @submit.prevent="signUp">
          <div class="form-group input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"> <i class="fa fa-envelope"></i> </span>
            </div>
            <input class="form-control" placeholder="이메일" type="email" v-model="username" @blur="validateEmail">
          </div>
          <div v-if="errors.username || !isEmailValid" class="form-group">
            <span v-if="errors.username" class="signup-warning-message">{{ errors.username[0] }}</span>
            <span v-if="!isEmailValid" class="signup-warning-message">유효한 이메일 주소를 입력하세요.</span>
          </div>

          <div class="form-group input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"> <i class="fa fa-lock"></i> </span>
            </div>
            <input class="form-control" placeholder="비밀번호" type="password" v-model="password1">
          </div>
          <div v-if="password1.length < 8" class="form-group">
            <span class="signup-warning-message">비밀번호는 8자리 이상 입력해야 합니다.</span>
          </div>

          <div class="form-group input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"> <i class="fa fa-lock"></i> </span>
            </div>
            <input class="form-control" placeholder="비밀번호 확인" type="password" v-model="password2">
          </div>
          <div v-if="password1 !== password2" class="form-group">
            <span class="signup-warning-message">비밀번호가 일치하지 않습니다.</span>
          </div>

          <div class="form-group input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"> <i class="fa fa-user"></i> </span>
            </div>
            <input class="form-control" placeholder="이름" type="text" v-model="name">
          </div>

          <div class="form-group input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"> <i class="fa fa-info"></i> </span>
            </div>
            <input class="form-control" placeholder="나이" type="number" v-model="age" min="1" max="100">
          </div>

          <div class="form-group input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"> <i class="fa fa-info"></i> </span>
            </div>
            <input class="form-control" placeholder="연봉 (단위: 만원)" type="number" v-model="salary" min="0" step="100">
          </div>
          <div class="form-group">
            <span class="text-muted" v-show="!salary">직업이 없다면 0을 입력하세요.</span>
          </div>

          <div class="form-group input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"> <i class="fa fa-info"></i> </span>
            </div>
            <input class="form-control" placeholder="가용 자산 (단위: 만원)" type="number" v-model="wealth" min="0" step="100">
          </div>

          <div class="form-group input-group">
            <div class="input-group-prepend">
              <span class="input-group-text"> <i class="fa fa-calendar"></i> </span>
            </div>
            <input class="form-control" placeholder="희망 기간 (단위: 개월)" type="number" v-model="period" min="6" max="60" step="6">
          </div>
          <div class="form-group">
            <span class="text-muted" v-show="!period">최소 6개월, 최대 60개월입니다.</span>
            <span v-if="period && (period > 60 || period < 6)" class="signup-warning-message">희망 기간을 다시 설정해주세요.</span>
          </div>

          <div class="form-group">
            <button type="submit" class="btn btn-primary btn-block" :disabled="!isFormValid">회원가입</button>
          </div>
          <div v-if="errorMessage" class="signup-warning-message">{{ errorMessage }}</div>
          <p class="text-center">이미 계정이 있으신가요? <RouterLink to="/login">로그인</RouterLink></p>
        </form>
      </article>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const name = ref('')
const age = ref(null)
const gender = ref(null)
const salary = ref(null)
const wealth = ref(null)
const period = ref(null)

const errorMessage = ref('')
const errors = ref({})
const isEmailValid = ref(true)

const validateEmail = () => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  isEmailValid.value = emailPattern.test(username.value)
}

const isFormValid = computed(() => {
  return username.value && isEmailValid.value && password1.value && password2.value && password1.value === password2.value
})

const signUp = async function () {
  if (!isEmailValid.value) {
    alert('유효한 이메일 주소를 입력하세요.')
    return
  }

  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    name: name.value,
    age: age.value,
    gender: gender.value,
    salary: salary.value,
    wealth: wealth.value,
    period: period.value,
  }

  try {
    await store.signUp(payload)
    router.push('/') // 회원가입 후 메인페이지로 이동
  } catch (error) {
    if (typeof error === 'object' && error !== null) {
      console.log('Signup error:', error)  // 에러 메시지 디버깅

      errors.value = error

      if (error.username && error.username[0] === 'User with this username already exists.') {
        window.alert('ID가 이미 존재합니다. 다른 ID를 선택해주세요.')
      } else {
        errorMessage.value = error.non_field_errors ? error.non_field_errors[0] : '회원가입에 실패했습니다.'
      }
    } else {
      errorMessage.value = error
    }
  }
}
</script>

<style scoped>
@import url('https://use.fontawesome.com/releases/v5.0.8/css/all.css');

.signup-container {
  max-width: 550px; /* 폼 컨테이너의 최대 너비 설정 */
  margin: 75px auto; /* 폼 컨테이너를 가운데로 정렬 */
}

.form-group.input-group {
  margin-bottom: 20px; /* 각 폼 그룹 사이의 간격 조정 */
}

.input-group-prepend .input-group-text {
  background-color: #f8f9fa; /* 아이콘 배경색 */
}

.signup-warning-message {
  color: red; /* 경고 메시지의 글자색을 빨간색으로 설정 */
  display: block; /* 경고 메시지를 블록 요소로 설정하여 줄바꿈 적용 */
  margin-top: 5px; /* 경고 메시지를 입력 필드 바로 아래에 위치시키기 위해 위쪽 여백 제거 */
  margin-bottom: 10px; /* 경고 메시지와 다음 필드 사이의 간격 조정 */
}

.btn-primary {
  background-color: #007bff; /* 배경색 설정 */
  color: white; /* 글자색 설정 */
  border: none; /* 테두리 없애기 */
}

.btn-primary:hover {
  background-color: #0056b3; /* 호버 시 배경색 변경 */
}

.btn-primary:disabled {
  background-color: #ccc; /* 비활성화 시 배경색 변경 */
  cursor: not-allowed; /* 비활성화 시 커서 변경 */
}
</style>
