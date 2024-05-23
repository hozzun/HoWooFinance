<template>
  <div class="chart-container">
    <div class="chart-column">
      <div class="chart-card">
        <h2 class="chart-title">예금별 금리 비교</h2>
        <hr>
        <div class="chart">
          <canvas ref="depositChartCanvas"></canvas>
        </div>
      </div>
    </div>
    <div class="chart-column">
      <div class="chart-card">
        <h2 class="chart-title">적금별 금리 비교</h2>
        <hr>
        <div class="chart">
          <canvas ref="savingChartCanvas"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: {
    totalProducts: {
      type: Array,
      required: true,
    },
  },
  computed: {
    depositProducts() {
      return this.totalProducts.filter(product => product.deposit_options && product.deposit_options.length > 0);
    },
    savingProducts() {
      return this.totalProducts.filter(product => product.saving_options && product.saving_options.length > 0);
    },
  },
  mounted() {
    if (this.depositProducts.length > 0) {
      this.$refs.depositChartCanvas.height = 600; // 원하는 높이로 설정
      this.renderChart('depositChartCanvas', this.depositProducts);
    }
    if (this.savingProducts.length > 0) {
      this.$refs.savingChartCanvas.height = 600; // 원하는 높이로 설정
      this.renderChart('savingChartCanvas', this.savingProducts);
    }
  },
  methods: {
    renderChart(canvasRef, products) {
      const ctx = this.$refs[canvasRef].getContext('2d');

      const productData = products.map(product => {
        return {
          label: `${product.kor_co_nm} (${product.fin_prdt_cd})`,
          data: product.deposit_options ? product.deposit_options.map(option => ({ x: option.save_trm, y: option.intr_rate2 })) : product.saving_options.map(option => ({ x: option.save_trm, y: option.intr_rate2 })),
          backgroundColor: this.getRandomColor(),
          borderColor: this.getRandomColor(),
          fill: false,
          tension: 0.1,
          pointRadius: 5,
          bankName: product.kor_co_nm,
          productCode: product.fin_prdt_cd,
        };
      });

      new Chart(ctx, {
        type: 'line',
        data: {
          datasets: productData,
        },
        options: {
          scales: {
            x: {
              type: 'linear',
              title: {
                display: true,
                text: '희망 기간 (개월)',
              },
              ticks: {
                stepSize: 6,
                min: 0,
                max: 60,
              },
            },
            y: {
              title: {
                display: true,
                text: '금리 (%)',
              },
              ticks: {
                stepSize: 0.1,
                min: 0,
                max: 10,
              },
            },
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function (context) {
                  const data = context.raw;
                  return `${context.dataset.label}: ${data.y}%`;
                },
                title: function (tooltipItem) {
                  const bankName = tooltipItem[0].dataset.bankName;
                  const productCode = tooltipItem[0].dataset.productCode;
                  return `${bankName} (${productCode})`;
                },
              },
            },
          },
        },
      });
    },
    getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
}

.chart-column {
  flex: 1;
  min-width: 400px;
  display: flex;
  justify-content: center;
}

.chart-card {
  background-color: #fff;
  padding: 10px; /* Reduced padding */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.chart-title {
  text-align: center;
  margin-bottom: 10px; /* Reduced margin */
}

.chart {
  height: 400px; /* Increased height */
}

canvas {
  width: 600px;
  height: 400px; /* Set canvas height */
}
</style>
