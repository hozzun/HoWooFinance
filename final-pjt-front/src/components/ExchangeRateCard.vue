<template>
  <div class="card shadow-sm mb-4">
    <div class="card-body">
      <ul class="list-unstyled">
        <li class="mb-3 text-center">
          <strong>{{ rate.cur_nm }}</strong><br>
          <span class="deal-bas-rate h4">{{ rate.deal_bas_r }}</span>
          <span :style="percentChangeStyle">
            전일대비 {{ percentChangeSymbol }} {{ percentChange.toFixed(2) }}%
          </span>
        </li>
        <hr>
        <li class="mb-2">
          <strong>(송금)보내실 때: </strong>
            <span :style="{ color: riseFallColor, 'font-weight': 'bold' }">
              {{ rate.tts }}
            </span>
          <div><strong>(송금)받으실 때:</strong> {{ rate.ttb }}</div>
        </li>
        <li class="text-muted large">2024.05.24. 차트</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExchangeRateCard',
  props: {
    rate: Object,
    previousRate: Number, // 전일 환율을 prop으로 전달받음
  },
  computed: {
    riseFallColor() {
      return this.percentChange < 0 ? '#3498db' : '#e74c3c'; // Blue for decrease, Red for increase
    },
    percentChange() {
      const currentRate = parseFloat(this.rate.deal_bas_r.replace(/,/g, ''));
      if (isNaN(currentRate) || !this.previousRate) return 0;
      return ((currentRate - this.previousRate) / this.previousRate) * 100;
    },
    percentChangeSymbol() {
      return this.percentChange >= 0 ? '▲' : '▼';
    },
    percentChangeStyle() {
      return {
        color: this.riseFallColor,
        fontWeight: 'bold',
        fontSize: '18pt', // Increase font size
      };
    }
  },
};
</script>

<style scoped>
.card {
  width: 100%;
  max-width: 240px; /* Adjusted max-width for smaller cards */
  border-radius: 12px;
  margin: 16px auto;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.deal-bas-rate {
  font-size: 26pt; /* Increase font size */
  display: block;
  margin: 12px 0;
}

.text-muted {
  color: #6c757d;
  text-align: center;
  margin-top: 30px;
}
</style>


