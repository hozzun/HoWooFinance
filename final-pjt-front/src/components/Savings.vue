<template>
  <div style="background: linear-gradient(to bottom,  white, rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5)), rgba(29, 63, 85, 0.5); min-height: 92.5vh;">
  <div>
    <h1>적금 상품 목록</h1>
    <hr>
    <p></p>
    <!-- 필터링 폼 -->
    <div class="filters">
      <div class="filter-group">
        <label for="bank-filter">은행 선택:</label>
        <select id="bank-filter" v-model="selectedBank" @change="applyFilters">
          <option value="">전체</option>
          <option v-for="bank in bankList" :key="bank" :value="bank">{{ bank }}</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="term-filter">희망 개월 상품:</label>
        <select id="term-filter" v-model="selectedMaxTerm" @change="applyFilters">
          <option value="">전체</option>
          <option v-for="term in termList" :key="term" :value="term">{{ term }}개월</option>
        </select>
      </div>
    </div>

    <div v-if="filteredSavings.length" class="cards-container">
      <div class="card" v-for="saving in filteredSavings" :key="saving.id">
        <img :src="getImage(saving.kor_co_nm)" :alt="saving.name" class="bank-image" />
        <div class="card-content">
          <h2 class="product-name">{{ saving.kor_co_nm }}</h2>
          <p class="highlight">상품 이름: {{ saving.fin_prdt_nm }}</p>
          <p>옵션 개수: {{ saving.saving_options.length }}개</p>
          <p>최소: {{ getMinTerm(saving.saving_options) }}개월</p>
          <p>최대: {{ getMaxTerm(saving.saving_options) }}개월</p>
          <p class="highlight">최고 우대금리: {{ getMaxBenefitRate(saving.saving_options) }}%</p>
          <button @click="goToDetail(saving.fin_prdt_cd, 'saving')" class="detail-button">상세 정보 바로가기</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>적금 상품을 불러오는 중입니다...</p>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const router = useRouter()
const savings = ref([])

const selectedBank = ref('')
const selectedMaxTerm = ref('')

// 은행 목록과 기간 목록 설정
const bankList = ref([])
const termList = ref(['1', '3', '6', '12', '24', '36', '48', '60'])

const fetchSavings = async () => {
  axios({
    method: 'get',
    url: `${store.baseURL}/savings/products/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((response) => {
    savings.value = response.data
    // 은행 목록 설정
    bankList.value = [...new Set(response.data.map(product => product.kor_co_nm))]
  })
  .catch((error) => {
    console.error('적금 상품을 불러오는 중 에러가 발생했습니다:', error)
    window.alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
  })
}

const goToDetail = (finPrdtCd, type) => {
  router.push({ name: 'productdetail', params: { fin_prdt_cd: finPrdtCd, type: type } })
}

onMounted(() => {
  fetchSavings()
})

const getImage = (bankName) => {
  return `/images/${bankName}.png`
}

const getMinTerm = (options) => {
  if (options.length === 0) return 0
  return options.reduce((min, option) => option.save_trm < min ? option.save_trm : min, options[0].save_trm)
}

const getMaxTerm = (options) => {
  if (options.length === 0) return 0
  return options.reduce((max, option) => option.save_trm > max ? option.save_trm : max, options[0].save_trm)
}

const getMaxBenefitRate = (options) => {
  if (options.length === 0) return 0
  return options.reduce((maxRate, option) => option.intr_rate2 > maxRate ? option.intr_rate2 : maxRate, options[0].intr_rate2)
}

const sortedSavings = computed(() => {
  return savings.value.slice().sort((a, b) => getMaxBenefitRate(b.saving_options) - getMaxBenefitRate(a.saving_options))
})

const filteredSavings = computed(() => {
  return sortedSavings.value.filter(product => {
    const matchBank = selectedBank.value === '' || product.kor_co_nm === selectedBank.value
    const matchMaxTerm = selectedMaxTerm.value === '' || product.saving_options.some(option => option.save_trm <= parseInt(selectedMaxTerm.value))
    return matchBank && matchMaxTerm
  })
})

const applyFilters = () => {
  // 필터 적용 로직은 자동으로 반응형 computed 필드에서 처리됨
}
</script>

<style scoped>
.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  margin-bottom: 5px;
  font-weight: bold;
}

.filter-group select {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
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
  padding: 16px;
}

h2.product-name {
  margin: 0 0 8px;
  font-size: 1.5em;
  font-weight: bold;
  color: #007bff;
}

p {
  margin: 4px 0;
  font-size: 1em;
}

.highlight {
  font-weight: bold;
  color: #ff4500;
}

.detail-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: rgba(236, 28, 36, 0.8);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  margin-top: 16px;
  transition: background-color 0.3s;
}

.detail-button:hover {
  background-color: #b3001e;
}
</style>
