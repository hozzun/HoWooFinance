<template>
  <div class="exchange-page-container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light custom-navbar">
      <a class="navbar-brand" href="#">Category || </a>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="#" @click="showSection('calculator')">환율 계산기</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="showSection('rates')">실시간 환율 정보</a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="content-container">
      <div v-show="activeSection === 'calculator'">
        <h2>환율 계산기</h2>
        <div class="exchange-container">
          <div class="contact-image">
            <img src="/public/images/Howoologo.png" alt="exchange_calculator"/>
          </div>
          <form @submit.prevent="calculateExchange">
            <div class="form-group">
              <label for="amount" class="input-label">금액 입력:</label>
              <div class="input-wrapper">
                <input v-model.number="amountInKRW" class="form-control input-large" placeholder="금액을 입력하세요" id="INKRW" />
                <span>원</span>
              </div>
            </div>
            <div class="form-group">
              <label for="currency" class="input-label">통화 선택:</label>
              <select class="form-select input-large" aria-label="Default select example" v-model="selectedCurrency" id="currency">
                <option disabled selected>나라를 선택해 주세요</option>
                <option v-for="(rate, index) in exchangeRates" :value="rate" :key="index">{{ rate.cur_nm }} ({{ rate.cur_unit }}) {{ rate.deal_bas_r || 'N/A' }}</option>
              </select>
            </div>
            <div class="result-container">
              <h3>계산 금액</h3>
              <div class="result-box">
                <span>{{ calculatedAmount.toFixed(2) }} {{ selectedCurrency ? selectedCurrency.cur_unit : '' }}</span>
              </div>
            </div>
          </form>
        </div>
      </div>
      <div v-show="activeSection === 'rates'">
        <h2>실시간 환율 정보</h2>
        <div class="cards-container">
          <div class="card-wrapper" v-for="rate in exchangeRates" :key="rate.cur_unit">
            <ExchangeRateCard :rate="rate" :previousRate="getPreviousRate(rate.cur_unit)" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ExchangeRateCard from '@/components/ExchangeRateCard.vue';

export default {
  name: 'ExchangeRateView',
  components: {
    ExchangeRateCard,
  },
  data() {
    return {
      exchangeRates: [],
      previousExchangeRates: [],
      selectedCurrency: null,
      amountInKRW: null,
      activeSection: 'calculator'
    };
  },
  computed: {
    calculatedAmount() {
      if (!this.selectedCurrency || !this.selectedCurrency.deal_bas_r) return 0;
      const dealBasRate = parseFloat(this.selectedCurrency.deal_bas_r.replace(/,/g, '')); // 천 단위 구분 쉼표 제거
      const result = this.amountInKRW / dealBasRate;
      return isNaN(result) ? 0 : result;
    },
  },
  methods: {
    async fetchExchangeRates() {
      try {
        const currentResponse = await axios.get(`/api/site/program/financial/exchangeJSON`, {
          params: {
            authkey: '', // APIKEY
            searchdate: '20240524', // 현재 날짜
            data: 'AP01'
          }
        });

        const previousResponse = await axios.get(`/api/site/program/financial/exchangeJSON`, {
          params: {
            authkey: '', // APIKEY
            searchdate: '20240524', // 전일 날짜
            data: 'AP01'
          }
        });

        console.log('현재 환율 데이터:', currentResponse.data);
        console.log('전일 환율 데이터:', previousResponse.data);

        this.exchangeRates = currentResponse.data;
        this.previousExchangeRates = previousResponse.data;

        // 기본 통화를 USD로 설정
        this.selectedCurrency = this.exchangeRates.find(rate => rate.cur_unit === 'USD') || null;
      } catch (error) {
        console.error('Error fetching exchange rates:', error);
      }
    },
    getPreviousRate(cur_unit) {
      const previousRate = this.previousExchangeRates.find(rate => rate.cur_unit === cur_unit);
      return previousRate ? parseFloat(previousRate.deal_bas_r.replace(/,/g, '')) : null;
    },
    showSection(section) {
      this.activeSection = section;
    },
    calculateExchange() {
      // 추가적인 계산 로직을 추가할 수 있습니다.
      alert("계산이 완료되었습니다.");
    }
  },
  created() {
    this.fetchExchangeRates();
  },
};
</script>

<style scoped>
body {
  background: -webkit-linear-gradient(left, #0072ff, #00c6ff);
}

.exchange-page-container {
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: #2c3e50;
}

.navbar {
  margin-bottom: 20px;
  margin-top: 20px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.exchange-container {
  background: #fff;
  margin: 0 auto;
  width: 70%;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.contact-image {
  text-align: center;
}

.contact-image img {
  width: 15%;
  margin-top: -3%;
}

.input-section {
  padding: 0 10%;
}

.input-group {
  margin-bottom: 20px;
}

.input-label {
  font-weight: bold;
  font-size: 1.2rem;
  color: #34495e;
  margin-bottom: 10px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-large {
  font-size: 1.2rem;
  padding: 10px;
  width: calc(100% - 40px);
  text-align: left;
  border: 1px solid #ced4da;
  border-radius: 5px;
  transition: border-color 0.3s;
}

.input-large:focus {
  border-color: #007bff;
  outline: none;
}

.result-container {
  text-align: center;
  margin-top: 20px;
  width: 100%;
}

.result-box {
  font-size: 2rem;
  font-weight: bold;
  background-color: #f8f9fa;
  border: 1px solid #ced4da;
  border-radius: 5px;
  padding: 20px;
  display: inline-block;
  margin-top: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  text-align: center;
}

.form-group.text-center {
  margin-top: 20px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fafafa;
  border: 1px solid #ddd;
  border-radius: 10px;
  margin-top: 20px;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

.card-wrapper {
  flex: 1 1 calc(25% - 15px);
  display: flex;
  justify-content: center;
  max-width: calc(25% - 15px);
}

h3 {
  margin-bottom: 10px;
}

.exchange-page-container {
  background: linear-gradient(to bottom, white,  rgba(190, 225, 230, 0.5), rgba(135, 206, 250, 0.5));
  min-height: 92.5vh;
}
</style>
