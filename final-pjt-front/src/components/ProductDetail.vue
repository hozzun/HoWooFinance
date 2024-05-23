<template>
  <div style="background: linear-gradient(to bottom,  white, rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5)), rgba(29, 63, 85, 0.5), ; min-height: 92.5vh;">
  <div class="product-detail-container">
    <button @click="goBack" class="back-button">뒤로가기</button>
    <h2 class="title">[ {{ optionName }} ] 상세조회</h2>
    <hr>
    <div v-if="options.length" class="cards-container">
      <div class="card" v-for="option in options" :key="option.save_trm">
        <img :src="getImage(bankName)" :alt="bankName" class="bank-image" />
        <div class="card-content">
          <h3 class="product-name">{{ optionName }}</h3>
          <p class="bank-name">{{ bankName }}</p>
          <p>저축 기간: <strong>{{ option.save_trm }}개월</strong></p>
          <p>기본 금리: <strong>{{ option.intr_rate }}%</strong></p>
          <p class="highlight">우대 금리: <strong>{{ option.intr_rate2 }}%</strong></p>
          <p v-if="preferCondition.length">우대 조건:</p>
          <ul v-for="(condition, index) in preferCondition" :key="index" class="conditions-list">
            <li>{{ condition }}</li>
          </ul>
          <button @click="confirmSubscription(option)" class="subscribe-button">가입하기</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>옵션을 불러오는 중입니다...</p>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const optionName = ref('')
const bankName = ref('')
const options = ref([])
const preferCondition = ref([])
const userProducts = ref([])

onMounted(() => {
    const type = route.params.type;
    const baseURL = type === 'deposit' ? `${store.baseURL}/deposits/products/${route.params.fin_prdt_cd}` : `${store.baseURL}/savings/products/${route.params.fin_prdt_cd}`;
    axios({
        method: 'get',
        url: baseURL,
        headers: {
            Authorization: `Token ${store.token}`
        }
    })
    .then((response) => {
        fetchProducts()
        options.value = response.data
    })
    .catch((error) => {
        console.error('에러 발생:', error)
    })

    fetchUserProducts()
})

const fetchProducts = async () => {
    const type = route.params.type;
    const productsURL = type === 'deposit' ? `${store.baseURL}/deposits/products/` : `${store.baseURL}/savings/products/`;
    axios({
        method: 'get',
        url: productsURL,
        headers: {
            Authorization: `Token ${store.token}`
        }
    })
    .then((response) => {
        const product = response.data.find(item => item.fin_prdt_cd === route.params.fin_prdt_cd);
        optionName.value = product ? product.fin_prdt_nm : '상품 이름을 찾을 수 없습니다.';
        bankName.value = product ? product.kor_co_nm : '은행 이름을 찾을 수 없습니다.';
        preferCondition.value = product ? product.spcl_cnd.split('\n') : ['우대 조건을 찾을 수 없습니다.'];
    })
    .catch((error) => {
        console.error('예금 상품을 불러오는 중 에러가 발생했습니다:', error)
    })
}

const fetchUserProducts = async () => {
    axios({
        method: 'get',
        url: `${store.baseURL}/accounts/user_info/`,
        headers: {
            Authorization: `Token ${store.token}`
        }
    })
    .then((response) => {
        userProducts.value = [
            ...response.data.deposit,
            ...response.data.saving
        ];
    })
    .catch((error) => {
        console.error('유저 가입 상품을 불러오는 중 에러가 발생했습니다:', error)
    })
}

const confirmSubscription = (option) => {
    if (isProductAlreadySubscribed(route.params.fin_prdt_cd)) {
        alert('해당 상품은 이미 가입되어 있습니다.');
    } else {
        if (confirm("상품을 가입 하시겠습니까?")) {
            subscribeProduct(option);
        }
    }
}

const isProductAlreadySubscribed = (productCode) => {
    return userProducts.value.some(product => product.fin_prdt_cd === productCode);
}

const subscribeProduct = async (option) => {
    try {
        const type = route.params.type;
        const url = type === 'deposit' 
            ? `${store.baseURL}/accounts/deposit/add/`
            : `${store.baseURL}/accounts/saving/add/`;
        
        await axios.post(url, {
            product_code: route.params.fin_prdt_cd,
            product_trm: option.save_trm,
            product_intr: option.intr_rate,
            product_intr2: option.intr_rate2,
        }, {
            headers: {
                Authorization: `Token ${store.token}`
            }
        });
        alert('해당 상품이 가입되었습니다.');
        await store.getUserDetails();
        if (confirm("마이페이지에서 가입한 상품을 확인하시겠습니까?")) {
            router.push('/mypage');
        }
    } catch (error) {
        console.error('상품을 추가하는 중 에러가 발생했습니다:', error);
        alert('오류가 발생했습니다.');
    }
}

const getImage = (bankName) => {
  return `/images/${bankName}.png`
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.product-detail-container {
  padding: 20px;
  /* font-family: 'Helvetica Neue', Arial, sans-serif; */
  color: #2c3e50;
}

.back-button {
  display: block;
  margin-bottom: 20px;
  padding: 10px 20px;
  background-color: #41484e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #9c9ea1;
}

.title {
  text-align: center;
  font-size: 1.8em;
  margin-bottom: 20px;
  color: #333;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.card {
  border: 1px solid #ccc;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: #fff;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.bank-image {
  width: 100%;
  height: auto;
}

.card-content {
  padding: 20px;
}

.product-name {
  font-size: 1.4em;
  font-weight: bold;
  color: #007bff;
  margin-bottom: 10px;
}

.bank-name {
  font-size: 1.1em;
  margin-bottom: 10px;
  color: #555;
}

p {
  margin: 5px 0;
  font-size: 1em;
  color: #555;
}

.highlight {
  font-weight: bold;
  color: #ff4500;
}

.conditions-list {
  margin: 0;
  padding-left: 20px;
  color: #777;
}

.subscribe-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #303130;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  margin-top: 16px;
  transition: background-color 0.3s;
}

.subscribe-button:hover {
  background-color: #9a9e9b;
}
</style>
