<template>
  <div class="background">
    <div class="container my-5">
      <div class="header">
        <h1>주변 은행 검색</h1>
      </div>
      <hr>
      <div class="content-map">
        <div class="left-panel">
          <form class="search-form" @submit.prevent="search">
            <select
              class="form-select form-control mb-3"
              name="location1"
              id="location1"
              v-model="mainRegion"
              @change="updateSubRegion"
            >
              <option :value="null" selected hidden>시 / 도</option>
              <option v-for="locate1 in store.sectionList" :value="locate1" :key="locate1">
                {{ locate1 }}
              </option>
            </select>
            <select
              class="form-select form-control mb-3"
              name="location2"
              id="location2"
              v-model="subRegion"
            >
              <option :value="null" selected hidden>
                시 / 군 / 구
              </option>
              <option v-for="locate2 in store.detailList[mainRegion]" :value="locate2" :key="locate2">
                {{ locate2 }}
              </option>
            </select>
            <select class="form-select form-control mb-3" name="bank" id="bank" v-model="selectedBank">
              <option :value="null" selected hidden>은행</option>
              <option v-for="bank in store.banks" :value="bank" :key="bank">
                {{ bank }}
              </option>
            </select>
            <button class="btn btn-primary btn-block search-button" type="submit">검색</button>
          </form>
          <button class="btn btn-success btn-block current-location-button mt-3" @click="getCurrentLocation">현재 위치에서 찾기</button>
        </div>
        <div class="map-container">
          <div id="map" class="map"></div>
          <br>
          <h4>내 주변 [ {{ banks.length }}곳 ]의 은행을 찾았습니다.</h4>
          <div class="bank-list">
            <ul>
              <li v-for="(bank, index) in banks" :key="bank.id" @click="highlightMarker(index)">
                {{ bank.place_name }} - {{ bank.address_name }}
                <button @click.stop="toggleFavorite(bank)" :class="['btn', isFavorite(bank) ? 'btn-warning' : 'btn-outline-warning']">
                  ★
                </button>
              </li>
            </ul>
          </div>
        </div>
        <div class="favorite-container">
          <h2>즐겨찾기</h2>
          <ul class="favorite-list">
            <li v-for="(bank, index) in favoriteBanks" :key="bank.id" @click="highlightFavorite(index)">
              {{ bank.place_name }} - {{ bank.address_name }}
              <button @click.stop="removeFavorite(bank)" class="btn btn-outline-danger">×</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { usePlacesStore } from "@/stores/places";

const store = usePlacesStore();
const mainRegion = ref(null);
const subRegion = ref(null);
const selectedBank = ref(null);
const searchword = ref(null);
const banks = ref([]);
const markers = ref([]);
const favoriteBanks = ref([]);
const API_KEY = '0dc68af8ca4800ae7aabae06673dca3a';

const search = () => {
  searchword.value = `${mainRegion.value || ''} ${subRegion.value || ''} ${selectedBank.value || ''}`.trim();
  if (searchword.value.length === 0) {
    alert("지역과 은행을 선택해주세요.");
    return;
  }

  loadKakaoMapScript(() => initMap(searchword.value));
};

const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      const { latitude, longitude } = position.coords;
      const coords = new kakao.maps.LatLng(latitude, longitude);
      loadKakaoMapScript(() => initMap(coords, true));
    }, error => {
      console.error("Error getting location: ", error);
      alert("위치 정보를 가져오는 데 실패했습니다.");
    });
  } else {
    alert("Geolocation is not supported by this browser.");
  }
};

const loadKakaoMapScript = (callback) => {
  if (window.kakao && window.kakao.maps) {
    // Kakao Maps API가 이미 로드된 경우
    callback();
  } else {
    // Kakao Maps API 스크립트 로드
    const script = document.createElement("script");
    script.onload = () => {
      if (window.kakao && window.kakao.maps) {
        callback();
      } else {
        console.error('Kakao 지도 API가 로드되지 않았습니다.');
      }
    };
    script.onerror = () => {
      console.error('Kakao 지도 API 스크립트 로드에 실패했습니다.');
    };
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${API_KEY}&libraries=services`;
    document.head.appendChild(script);
  }
};

const initMap = (keywordOrCoords, isCoords = false) => {
  // kakao가 정의되어 있는지 확인
  if (typeof kakao === 'undefined' || !kakao.maps) {
    console.error('Kakao 지도 API가 로드되지 않았습니다.');
    return;
  }

  kakao.maps.load(() => {
    var infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    var mapContainer = document.getElementById("map"),
      mapOption = {
        center: new kakao.maps.LatLng(36.2683, 127.6358), // 대한민국 중심 좌표
        level: 3, // 확대 레벨
      };

    var map = new kakao.maps.Map(mapContainer, mapOption);
    map.setMapTypeId(kakao.maps.MapTypeId.ROADMAP);
    var ps = new kakao.maps.services.Places();

    // 기존 마커 초기화
    markers.value.forEach(marker => marker.setMap(null));
    markers.value = [];

    if (isCoords) {
      const coords = keywordOrCoords;
      map.setCenter(coords);
      const marker = new kakao.maps.Marker({
        map: map,
        position: coords
      });

      // 주변 은행 검색
      const places = new kakao.maps.services.Places();
      places.categorySearch('BK9', placesSearchCB, { location: coords, radius: 500 });

    } else {
      ps.keywordSearch(keywordOrCoords, placesSearchCB);
    }

    function placesSearchCB(data, status, pagination) {
      if (status === kakao.maps.services.Status.OK) {
        var bounds = new kakao.maps.LatLngBounds();
        banks.value = data;
        for (var i = 0; i < data.length; i++) {
          displayMarker(data[i]);
          bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
        }
        map.setBounds(bounds);
      }
    }

    function displayMarker(place) {
      var marker = new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(place.y, place.x),
      });
      markers.value.push(marker);

      kakao.maps.event.addListener(marker, "click", function () {
        infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + "</div>");
        infowindow.open(map, marker);
      });
    }
  });
};

const highlightMarker = (index) => {
  const marker = markers.value[index];
  const map = marker.getMap();
  map.setCenter(marker.getPosition());
  kakao.maps.event.trigger(marker, 'click');
};

const highlightFavorite = (index) => {
  const bank = favoriteBanks.value[index];
  const bankIndex = banks.value.findIndex(b => b.id === bank.id);
  if (bankIndex !== -1) {
    highlightMarker(bankIndex);
  } else {
    // 즐겨찾기 항목이 현재 검색 결과에 없는 경우
    const coords = new kakao.maps.LatLng(bank.y, bank.x);
    loadKakaoMapScript(() => initMap(coords, true));
  }
};

const toggleFavorite = (bank) => {
  const index = favoriteBanks.value.findIndex(fav => fav.id === bank.id);
  if (index === -1) {
    favoriteBanks.value.push(bank);
  } else {
    favoriteBanks.value.splice(index, 1);
  }
};

const isFavorite = (bank) => {
  return favoriteBanks.value.some(fav => fav.id === bank.id);
};

const removeFavorite = (bank) => {
  const index = favoriteBanks.value.findIndex(fav => fav.id === bank.id);
  if (index !== -1) {
    favoriteBanks.value.splice(index, 1);
  }
};

// subRegion 업데이트 함수 추가
const updateSubRegion = () => {
  subRegion.value = null;
};

// 페이지 로드 시 기본 키워드로 지도 초기화
onMounted(() => {
  loadKakaoMapScript(() => initMap("은행"));
});
</script>

<style scoped>
/* @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap'); */

.container {
  padding: 20px;
  /* font-family: 'Noto Sans', sans-serif; */
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 2rem;
  color: #34495e;
}

.content-map {
  display: flex;
  gap: 20px;
}

.left-panel {
  width: 20%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-select {
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ced4da;
  border-radius: 5px;
  transition: border-color 0.3s;
  height: auto;
  min-height: 50px;
}

.form-select option {
  padding: 10px;
  height: auto;
  line-height: 1.5;
}

.form-select:focus {
  border-color: #007bff;
  outline: none;
}

.map-container {
  display: flex;
  flex-direction: column;
  width: 60%;
  position: relative;
}

.map {
  width: 100%;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
}

.map::before {
  content: '주변 은행 검색';
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1rem;
  font-weight: bold;
  color: #eff1f3;
  z-index: 10;
  background: rgba(1, 17, 236, 0.8);
  padding: 10px;
  border-radius: 5px;
}

.bank-list {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  height: 300px;
  overflow-y: scroll;
}

.bank-list h4 {
  margin-top: 0;
  text-align: center;
  font-size: 1.2rem;
  color: #34495e;
}

.bank-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.bank-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  transition: background-color 0.3s;
}

.bank-list li:hover {
  background-color: #e9ecef;
}

.btn-info {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-info:hover {
  background-color: #0056b3;
}

.search-button {
  margin-top: 10px;
}

.current-location-button {
  margin-top: 20px;
  background-color: #3bb18d;
}

.btn-outline-warning {
  color: #ffc107;
  border-color: #ffc107;
}

.btn-outline-warning:hover {
  background-color: #ffc107;
  color: #fff;
}

.btn-warning {
  background-color: #ffc107;
  color: #fff;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
  padding: 2px 6px;
  font-size: 0.9rem;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: #fff;
}

.favorite-container {
  width: 20%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.favorite-container h2 {
  font-size: 1.5rem;
  color: #34495e;
}

.favorite-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.favorite-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  transition: background-color 0.3s;
}

.favorite-list li:hover {
  background-color: #e9ecef;
}
</style>
