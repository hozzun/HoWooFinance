<template>
  <div style="background: linear-gradient(to bottom, white,  rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5)); min-height: 92.5vh">
  <div class="mypage-container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Category || </a>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="#" @click="showSection('profile')">프로필</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="showSection('products')">가입한 상품들</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="showSection('chart')">상품 비교</a>
          </li>
        </ul>
      </div>
    </nav> 
    <hr>
    <br>
    <div v-if="user">
      <div v-show="activeSection === 'profile'" class="profile-section">
        <div class="user-info-container">
          <h1 class="profile-title">{{ user.name }}님의 회원정보</h1>
          <form @submit.prevent="checkAndUpdateUserInfo">
            <div class="form-area">
              <div class="form-group">
                <label for="username">이메일</label>
                <input type="text" class="form-control" id="username" :value="user.username" disabled>
              </div>
              <div class="form-group">
                <label for="name">이름</label>
                <input type="text" class="form-control" id="name" v-model="editableUser.name" disabled>
              </div>
              <div class="form-group">
                <label for="age">나이</label>
                <input type="number" class="form-control" id="age" v-model="editableUser.age" disabled>
              </div>
              <div class="form-group">
                <label for="salary">연봉 (단위: 만원)</label>
                <input type="text" class="form-control" id="salary" v-model="formattedSalary" @input="updateSalary">
              </div>
              <div class="form-group">
                <label for="wealth">가용 자산 (단위: 만원)</label>
                <input type="text" class="form-control" id="wealth" v-model="formattedWealth" @input="updateWealth">
              </div>
              <div class="form-group">
                <label for="period">희망 상품 가입기간 (단위: 개월)</label>
                <input type="number" class="form-control" id="period" v-model="editableUser.period" step="6" min="6" max="60">
              </div>
              <button type="submit" class="btn btn-primary pull-right save-button">회원정보 변경</button>
              <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            </div>
          </form>
        </div>
      </div>
      <div v-show="activeSection === 'products'" class="products-section">
        <h1 class="section-title">가입한 상품들 [총 {{ totalProducts.length }}개]</h1>
        <hr>
        <div v-if="totalProducts.length" class="cards-container">
          <div v-for="product in totalProducts" :key="product.fin_prdt_cd" class="product-card">
            <div class="product-details">
              <h2>{{ product.fin_prdt_nm }}</h2>
              <hr>
              <p>은행: {{ product.kor_co_nm }}</p>
              <p>상품 코드: {{ product.fin_prdt_cd }}</p>
              <hr>
              <div v-for="option in product.deposit_options || product.saving_options" :key="option.id">
                <p>저축 기간: {{ option.save_trm }}개월</p>
                <p>기본 금리: {{ option.intr_rate }}%</p>
                <p class="redcol">우대 금리: {{ option.intr_rate2 }}%</p>
              </div>
            </div>
            <button @click="confirmCancellation(product.fin_prdt_cd, productType(product))" class="cancel-button">가입취소</button>
          </div>
        </div>
      </div>
      <div v-show="activeSection === 'chart'" class="chart-section">
        <h1 class="section-title">내가 가입한 상품 비교</h1>
        <hr>
        <br>
        <ProductChart v-if="totalProducts.length !== 0" :totalProducts="totalProducts" />
      </div>
    </div>
    <div v-else>
      <p>사용자 정보를 불러오는 중입니다...</p>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter';
import ProductChart from '@/components/ProductChart.vue';
import axios from 'axios';

const store = useCounterStore()
const user = computed(() => store.user)
const editableUser = ref({})
const errorMessage = ref('')
const lastUpdateTimeKey = 'lastUpdateTime';
const updateInterval = 10 * 60 * 1000; // 10분

const activeSection = ref('profile');

const showSection = (section) => {
  activeSection.value = section;
};

const totalProducts = ref([])

const productType = (product) => {
  return product.type === 'deposit' ? 'deposit' : 'saving';
};

const confirmCancellation = (productCode, type) => {
  if (confirm("가입을 취소하시겠습니까 ?")) {
    cancelSubscription(productCode, type);
  }
}

const cancelSubscription = async (productCode, type) => {
  const url = type === 'deposit' 
    ? `${store.baseURL}/accounts/deposit/remove/`
    : `${store.baseURL}/accounts/saving/remove/`;
  try {
    await axios.post(url, { product_code: productCode }, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    alert('가입이 취소되었습니다.');
    await fetchUserProducts(); // 데이터를 다시 가져옴
  } catch (error) {
    console.error('가입 취소 중 에러가 발생했습니다:', error);
    alert('오류가 발생했습니다.');
  }
}

const checkAndUpdateUserInfo = async () => {
  const lastUpdateTime = localStorage.getItem(lastUpdateTimeKey);
  const now = new Date().getTime();

  if (lastUpdateTime && now - lastUpdateTime < updateInterval) {
    const minutesLeft = Math.ceil((updateInterval - (now - lastUpdateTime)) / (60 * 1000));
    alert(`회원 정보를 수정하려면 ${minutesLeft}분이 지나야 합니다.`);
    return;
  }

  await updateUserInfo();
}

const updateUserInfo = async () => {
  if (editableUser.value.period < 6 || editableUser.value.period > 60) {
    alert('희망 상품 가입기간은 6개월에서 60개월 사이여야 합니다.');
    return;
  }
  if (editableUser.value.salary < 0) {
    alert('연봉은 0 이상이어야 합니다.');
    return;
  }
  if (editableUser.value.wealth < 0) {
    alert('가용 자산은 0 이상이어야 합니다.');
    return;
  }
  try {
    await axios.put(`${store.baseURL}/accounts/update/`, editableUser.value, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    alert('회원 정보가 업데이트되었습니다.');
    localStorage.setItem(lastUpdateTimeKey, new Date().getTime().toString());
    await store.getUserDetails();
  } catch (error) {
    console.error('회원 정보 업데이트 중 에러가 발생했습니다:', error);
    if (error.response && error.response.data) {
      errorMessage.value = JSON.stringify(error.response.data);
    } else {
      errorMessage.value = '오류가 발생했습니다.';
    }
  }
}

const fetchUserProducts = async () => {
  try {
    const response = await axios.get(`${store.baseURL}/accounts/user_info/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    const userData = response.data;
    totalProducts.value = [
      ...userData.deposit.map(item => ({
        ...item,
        type: 'deposit',
        deposit_options: item.deposit_options.filter(option => option.users.includes(userData.pk))
      })),
      ...userData.saving.map(item => ({
        ...item,
        type: 'saving',
        saving_options: item.saving_options.filter(option => option.users.includes(userData.pk))
      }))
    ];
  } catch (error) {
    console.error('가입한 상품을 불러오는 중 에러가 발생했습니다:', error);
  }
}

const formatNumber = (value) => {
  if (typeof value !== 'number' || isNaN(value)) return value;
  return value.toLocaleString('en-US');
}

const parseNumber = (value) => {
  const parsed = parseInt(value.replace(/,/g, ''), 10);
  return isNaN(parsed) ? 0 : parsed;
}

const formattedSalary = computed({
  get() {
    return formatNumber(editableUser.value.salary);
  },
  set(value) {
    editableUser.value.salary = parseNumber(value);
  }
});

const formattedWealth = computed({
  get() {
    return formatNumber(editableUser.value.wealth);
  },
  set(value) {
    editableUser.value.wealth = parseNumber(value);
  }
});

const updateSalary = (event) => {
  const value = event.target.value;
  editableUser.value.salary = parseNumber(value);
  event.target.value = formatNumber(editableUser.value.salary);
}

const updateWealth = (event) => {
  const value = event.target.value;
  editableUser.value.wealth = parseNumber(value);
  event.target.value = formatNumber(editableUser.value.wealth);
}

onMounted(async () => {
  if (!user.value) {
    await store.getUserDetails()
  }
  editableUser.value = { ...user.value }
  await fetchUserProducts()
});
</script>

<style scoped>
.mypage-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-title {
  text-align: center;
  margin-bottom: 20px;
}

.navbar {
  margin-bottom: 20px;
}

.user-info-container,
.products-section,
.chart-section {
  background-color: #FAFAFA;
  padding: 20px;
  border: 1px solid grey;
  border-radius: 10px;
  margin-bottom: 20px;
}

.form-area {
  padding: 10px 40px 60px;
  border: 1px solid grey;
  border-radius: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
}

.form-control {
  border-radius: 5px;
}

.save-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.product-card {
  border: 1px solid #ccc;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-details {
  margin-bottom: 16px;
}

.cancel-button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #cc0000;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.redcol {
  color: #ff4d4d;
}

</style>
