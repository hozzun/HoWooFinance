<template>
  <div class="mainpage-image-gradient">
    <div class="image-container">
      <img class="mainpage-image" src="/images/mainpage.png" alt="#" />
      <img class="mainpage-image-introduce" src="/images/mainintroduce.png" alt="#" />
    </div>
  </div>
  <!-- 여기부터 -->
  <div class="mainpage-content">
    <div class="container">
      <div class="row">
        <div class="col-md-4">
          <div class="our-team-main">
            <div class="team-front">
              <img src="/icons/icon1.png" class="img-fluid" />
              <h3>Howoo Finance 소개</h3>
              <p></p>
            </div>
            <div class="team-back" style="font-style: italic;">
              <p>Howoo Finance는 여러분의 금융 여정을 혁신적으로 안내하는 프리미엄 재테크 플랫폼입니다.</p><br>
              <p>다양한 예금 및 적금 상품을 손쉽게 검색하고 비교하며, 당신에게 딱 맞는 금융 상품으로 최적의 재테크 전략을 세워보세요.</p> 
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="our-team-main">
            <div class="team-front">
              <img src="/icons/icon2.png" class="img-fluid" />
              <h3>Howoo Finance 주요 기능</h3>
              <p></p>
            </div>
            <div class="team-back">
              <span>
                1. 예금/적금 상품 조회 <br />
                2. 실시간 환율 계산 <br />
                3. 주변 은행 찾기 <br />
                4. 자유 게시판 <br />
                5. 나에게 맞는 상품 추천
              </span>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="our-team-main">
            <div class="team-front">
              <img src="/icons/icon3.png" class="img-fluid" />
              <h3>Howoo Finance 이용 방법</h3>
              <p></p>
            </div>
            <div class="team-back">
              <span>
                1. 간단한 절차로 회원가입 하세요. <br/><br/>
                2. 로그인 하세요. <br/><br/>
                3. 다양한 기능을 누리세요 <br/>
              </span>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="our-team-main">
            <div style="height: 180px;">
              <img src="/icons/icon4.png"/>
              <h3>주요 기능 1</h3>
              <p>예금/적금 상품 조회</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="our-team-main">
            <div style="height: 180px;">
              <img src="/icons/icon5.png"/>
              <h3>주요 기능 2</h3>
              <p>실시간 환율 계산기</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="our-team-main">
            <div style="height: 180px;">
              <img src="/icons/icon6.png"/>
              <h3>주요 기능 3</h3>
              <p>주변 은행 찾기</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="copyright">
    <div class="container text-center">
      <p>본 사이트의 콘텐츠는 저작권법의 보호를 받는 바 무단 전재, 복사, 배포 등을 금합니다.</p>
      <p>Copyright © SAMSUNG All Rights Reserved.</p>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.mainpage-image-gradient {
  background: linear-gradient(to top, rgba(60, 120, 140, 0.5), rgba(135, 206, 250, 0.5), rgba(190, 225, 230, 0.5));
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 20px 0;
}

.image-container {
  position: relative;
  width: 80%;
  max-width: 1000px;
  margin-bottom: 20px;
}

.mainpage-image {
  width: 127%;
  height: auto;
  margin-left: -15%;
}

.mainpage-image-introduce {
  position: absolute;
  top: 20%;
  left: 15%;
  transform: translate(-50%, -50%);
  width: 60%;
  height: auto;
}

.mainpage-content {
  padding: 40px 0;
  background-color: rgba(60, 120, 140, 0.1);
}

.our-team-main {
  width: 100%;
  height: auto;
  border-bottom: 5px rgba(29, 63, 85, 0.5) solid;
  background: #fff;
  text-align: center;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  transition: 0.5s;
  margin-bottom: 28px;
}

.our-team-main img {
  margin-bottom: 20px;
  width: 90px;
}

.our-team-main h3 {
  font-size: 20px;
  font-weight: 700;
}

.our-team-main p {
  margin-bottom: 0;
}

.team-back {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  padding: 15px;
  text-align: left;
  background: #fff;

  /* Flexbox를 사용하여 수직 중앙 정렬 추가 */
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.team-front {
  width: 100%;
  height: 180px;
  position: relative;
  z-index: 10;
  background: #fff;
  padding: 15px;
  bottom: 0px;
  transition: all 0.5s ease;
}

.our-team-main:hover .team-front {
  bottom: -200px;
  transition: all 0.5s ease;
}

.our-team-main:hover {
  border-color: rgba(60, 120, 140, 0.5);
  transition: 0.5s;
}

.card {
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.copyright {
  background: linear-gradient(to bottom, rgba(60, 120, 140, 0.5), rgba(29, 63, 85, 0.5), #1e3663);
  padding: 20px 0 10px 0;
  color: #e0e0e0;
}
</style>
