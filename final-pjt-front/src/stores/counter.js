// stores/counter.js
import { ref } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import axios from 'axios';

export const useCounterStore = defineStore('counter', () => {
  const baseURL = 'http://127.0.0.1:8000';
  const router = useRouter();
  const token = ref(localStorage.getItem('token') || null);
  const isAuthenticated = ref(!!token.value);
  const user = ref(null);

  const signUp = async function (payload) {
    try {
      const { username, password1, password2, name, age, gender, salary, wealth, period } = payload;
      await axios.post(`${baseURL}/accounts/signup/`, { username, password1, password2, name, age, gender, salary, wealth, period });
      await logIn({ username: payload.username, password: payload.password1 });
      console.log('회원가입이 완료되었습니다.');
    } catch (error) {
      if (error.response && error.response.data) {
        console.error('Signup error response data:', error.response.data);
        throw error.response.data;
      } else {
        console.error('There was an error with the signup request:', error.message);
        throw new Error('회원가입에 실패했습니다.');
      }
    }
  }

  const logIn = async function (payload) {
    try {
      const { username, password } = payload;
      const response = await axios.post(`${baseURL}/accounts/login/`, { username, password });
      const userToken = response.data.key;
      localStorage.setItem('token', userToken);
      token.value = userToken;
      await getUserDetails();
      isAuthenticated.value = true;
      router.push({ name: 'home' });
      console.log('로그인이 완료되었습니다.');
    } catch (error) {
      console.error('로그인 에러:', error);
      window.alert('아이디 또는 비밀번호가 틀렸습니다.')
    }
  }

  const logOut = async function () {
    try {
      await axios.post(`${baseURL}/accounts/logout/`, null, {
        headers: { 'Authorization': `Token ${localStorage.getItem('token')}` }
      });
      localStorage.removeItem('token');
      token.value = null;
      user.value = null;
      isAuthenticated.value = false;
      console.log('로그아웃이 완료되었습니다.');
      router.push({ name: 'home' });
    } catch (error) {
      console.error('로그아웃 에러:', error);
    }
  }

  const getUserDetails = async function () {
    try {
      const response = await axios.get(`${baseURL}/accounts/user_info/`, {
        headers: { 'Authorization': `Token ${localStorage.getItem('token')}` }
      });
      user.value = response.data;
      console.log('User details fetched:', response.data);
    } catch (error) {
      console.error('사용자 정보를 가져오는 중 에러가 발생했습니다:', error);
    }
  }

  const articles = ref([]);

  const getArticles = async function () {
    try {
      const response = await axios.get(`${baseURL}/articles/`, {
        headers: { Authorization: `Token ${token.value}` }
      });
      articles.value = response.data;
    } catch (error) {
      if (error.response && error.response.status === 401) {
        alert('로그인이 필요합니다.');
        router.push('/login'); // 로그인 페이지로 리디렉션
      } else {
        console.error('게시글을 가져오는 중 에러가 발생했습니다:', error);
      }
    }
  }

  return { baseURL, user, token, signUp, logIn, logOut, isAuthenticated, getUserDetails, articles, getArticles };
});