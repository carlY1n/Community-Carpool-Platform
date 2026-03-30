@carpool_schema.sql <template>
  <view class="search-trip-container">
    <view class="search-card">
      <view class="input-group">
        <input v-model="startLocation" placeholder="请选择起点" readonly @click="choosePoint('start')" class="input-box" />
        <input v-model="endLocation" placeholder="请选择终点" readonly @click="choosePoint('end')" class="input-box" />
        <picker mode="date" v-model="departureDate" @change="onDateChange">
          <view class="picker-label">出发日期: <text class="picker-value">{{ departureDate || '请选择' }}</text></view>
        </picker>
      </view>
      <button class="search-btn" @click="searchTrips">查找行程</button>
    </view>
    <!-- #ifdef H5 -->
    <view id="bmap-container" class="trip-map"></view>
    <!-- #endif -->
    <!-- #ifndef H5 -->
    <map
      :longitude="longitude"
      :latitude="latitude"
      :markers="markers"
      :polyline="polyline"
      scale="14"
      class="trip-map"
      @tap="onMapTap"
      @markertap="onMarkerTap"
      show-location
    ></map>
    <!-- #endif -->
    <view v-if="hasSearched && trips.length === 0" class="no-result">暂无符合条件的行程</view>
    <view v-for="trip in trips" :key="trip.id" class="trip-card">
      <view class="trip-route">
        <text class="trip-point">{{ trip.startLocation }}</text>
        <text class="trip-arrow">→</text>
        <text class="trip-point">{{ trip.endLocation }}</text>
      </view>
      <view class="trip-info">
        <text>出发时间：{{ trip.departureTime }}</text>
        <text>价格：￥{{ trip.price }}</text>
        <text>剩余座位：{{ trip.seatAvailable }}</text>
      </view>
      <button class="apply-btn" @click="applyForTrip(trip.id)">报名此行程</button>
    </view>
    <uni-popup ref="orderPopup" type="center">
      <view class="add-car-popup">
        <view class="popup-title">订单确认</view>
        <view class="form-list">
          <view class="form-item">
            <text>订单号：</text>
            <text>{{ pendingOrder ? pendingOrder.id : '' }}</text>
          </view>
          <view class="form-item">
            <text>行程ID：</text>
            <text>{{ pendingOrder ? pendingOrder.tripId : '' }}</text>
          </view>
          <view class="form-item">
            <text>乘客ID：</text>
            <text>{{ pendingOrder ? pendingOrder.passengerId : '' }}</text>
          </view>
          <view class="form-item">
            <text>座位数：</text>
            <text>{{ pendingOrder ? pendingOrder.seatCount : '' }}</text>
          </view>
          <view class="form-item">
            <text>金额：</text>
            <text>￥{{ pendingOrder ? pendingOrder.amount : '' }}</text>
          </view>
          <view class="form-item">
            <text>下单时间：</text>
            <text>{{ pendingOrder && pendingOrder.orderTime ? formatOrderTime(pendingOrder.orderTime) : '' }}</text>
          </view>
          <view class="form-item">
            <text>订单状态：</text>
            <text>{{ pendingOrder ? orderStatusText(pendingOrder.orderStatus) : '' }}</text>
          </view>
          <view class="form-item">
            <text>支付状态：</text>
            <text>{{ pendingOrder ? payStatusText(pendingOrder.payStatus) : '' }}</text>
          </view>
        </view>
        <view class="popup-actions">
          <button class="main-btn" @click="confirmOrder">确认</button>
          <button class="cancel-btn" @click="cancelOrder">取消</button>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
import { searchTripApi, applyOrder, confirmOrder, cancelOrder } from '@/common/api.js';
import uniPopup from '@dcloudio/uni-ui/lib/uni-popup/uni-popup.vue';
import uniTransition from '@dcloudio/uni-ui/lib/uni-transition/uni-transition.vue';
export default {
  components: { uniPopup, uniTransition },
  data() {
    return {
      longitude: 116.397428,
      latitude: 39.90923,
      startLocation: '',
      endLocation: '',
      startLng: null,
      startLat: null,
      endLng: null,
      endLat: null,
      departureDate: '',
      trips: [],
      markers: [],
      polyline: [],
      hasSearched: false,
      selectType: '', // 'start' or 'end'
      bmap: null, // H5端百度地图实例
      showOrderPopup: false,
      pendingOrder: null,
      isGeocoding: false
    }
  },
  onShow() {
  	// 每次页面显示时，如果已经搜索过，就刷新一下列表
  	if (this.hasSearched) {
  		this.searchTrips(true); // 传入true表示是静默刷新
  	}
  },
  methods: {
    choosePoint(type) {
      this.selectType = type;
      uni.showToast({ title: '请在地图上点击选择', icon: 'none' });
    },
    // #ifdef H5
    initBMap() {
      if (!window.BMapGL) {
        uni.showToast({ title: '百度地图JS API未加载', icon: 'none' });
        return;
      }
      this.bmap = new window.BMapGL.Map('bmap-container');
      const point = new window.BMapGL.Point(this.longitude, this.latitude);
      this.bmap.centerAndZoom(point, 14);
      this.bmap.enableScrollWheelZoom(true);

      this.bmap.on('click', (e) => {
        this.onBMapClick(e.latlng.lng, e.latlng.lat);
      });

      const geolocation = new window.BMapGL.Geolocation();
      geolocation.getCurrentPosition((result) => {
        if (geolocation.getStatus() === 0) { // BMAP_STATUS_SUCCESS
          this.longitude = result.point.lng;
          this.latitude = result.point.lat;
          this.bmap.panTo(result.point);
        } else {
          console.error('Baidu Geolocation failed:', geolocation.getStatus());
        }
      });
    },
    onBMapClick(longitude, latitude) {
      if (!this.selectType) {
        uni.showToast({ title: '请先选择起点或终点', icon: 'none' });
        return;
      }
      if (this.isGeocoding) {
        uni.showToast({ title: '正在处理上一个位置请求', icon: 'none' });
        return;
      }
      this.isGeocoding = true;
      uni.showLoading({ title: '正在获取地址...' });

      const geocoder = new window.BMapGL.Geocoder();
      const point = new window.BMapGL.Point(longitude, latitude);

      geocoder.getLocation(point, (result) => {
        uni.hideLoading();
        this.isGeocoding = false;
        let address;
        if (result && result.address) {
          address = result.address;
        } else {
          address = `经度:${longitude.toFixed(6)}, 纬度:${latitude.toFixed(6)}`;
          uni.showToast({ title: '地址解析失败,将使用经纬度', icon: 'none' });
        }
        
        if (this.selectType === 'start') {
          this.startLocation = address;
          this.startLng = longitude;
          this.startLat = latitude;
        } else if (this.selectType === 'end') {
          this.endLocation = address;
          this.endLng = longitude;
          this.endLat = latitude;
        }

        this.updateMapMarkers(); 
        this.bmap.setCenter(point);

        this.bmap.clearOverlays();
        if (this.markers.length > 0) {
          this.markers.forEach(markerInfo => {
            const markerPoint = new window.BMapGL.Point(markerInfo.longitude, markerInfo.latitude);
            const marker = new window.BMapGL.Marker(markerPoint);
            this.bmap.addOverlay(marker);
          });
        }
        if (this.polyline.length > 0 && this.polyline[0].points.length > 1) {
          const path = this.polyline[0].points.map(p => new window.BMapGL.Point(p.longitude, p.latitude));
          const poly = new window.BMapGL.Polyline(path, {
            strokeColor: this.polyline[0].color,
            strokeWeight: this.polyline[0].width,
            strokeStyle: 'solid'
          });
          this.bmap.addOverlay(poly);
        }
      });
    },
    // #endif
    // #ifndef H5
    onMapTap(e) {
      if (this.isGeocoding) {
        uni.showToast({ title: '正在处理上一个位置请求', icon: 'none' });
        return;
      }
      const { longitude, latitude } = e.detail;
      if (!this.selectType) {
        uni.showToast({ title: '请先选择起点或终点', icon: 'none' });
        return;
      }
      
      this.isGeocoding = true;
      uni.showLoading({ title: '正在获取地址...' });

      if (this.selectType === 'start') {
        this.startLng = longitude;
        this.startLat = latitude;
      } else if (this.selectType === 'end') {
        this.endLng = longitude;
        this.endLat = latitude;
      }

      uni.request({
        url: 'https://api.map.baidu.com/reverse_geocoding/v3/',
        data: {
          ak: 'bc5jB0qU7svV3dWgqfNn5ivZZ7P75SVq',
          output: 'json',
          coordtype: 'gcj02ll',
          location: `${latitude},${longitude}`
        },
        success: (res) => {
          let address;
          if (res.statusCode === 200 && res.data.status === 0) {
            address = res.data.result.formatted_address;
          } else {
            address = `经度:${longitude.toFixed(6)}, 纬度:${latitude.toFixed(6)}`;
            const errorInfo = (res.data && res.data.message) || '请求失败';
            console.error('Baidu native geocoding error:', res);
            uni.showToast({ title: `地址解析失败(${errorInfo})`, icon: 'none', duration: 3000 });
          }

          if (this.selectType === 'start') {
            this.startLocation = address;
          } else if (this.selectType === 'end') {
            this.endLocation = address;
          }
        },
        fail: () => {
          const address = `经度:${longitude.toFixed(6)}, 纬度:${latitude.toFixed(6)}`;
          if (this.selectType === 'start') {
            this.startLocation = address;
          } else if (this.selectType === 'end') {
            this.endLocation = address;
          }
          uni.showToast({ title: '地址解析请求失败', icon: 'none' });
        },
        complete: () => {
          this.isGeocoding = false;
          uni.hideLoading();
          this.updateMapMarkers();
        }
      });
    },
    // #endif
    onMarkerTap(e) {
      uni.showToast({ title: '点击了标记点' + e.markerId, icon: 'none' });
    },
    onDateChange(e) {
      this.departureDate = e.detail.value;
    },
    async searchTrips(isRefresh = false) {
      if (!this.startLng || !this.endLng) {
        if (!isRefresh) { // 如果是用户点击的搜索，则提示
        	uni.showToast({ title: '请选择起点和终点', icon: 'none' });
        }
        return;
      }
      if (!this.departureDate) {
        uni.showToast({ title: '请选择出发日期', icon: 'none' });
        return;
      }
      uni.showLoading({ title: '正在查找行程...' });
      try {
        const params = {
          startLng: this.startLng,
          startLat: this.startLat,
          endLng: this.endLng,
          endLat: this.endLat,
          departureTime: this.departureDate
        };
        const res = await searchTripApi(params);
        uni.hideLoading();
        if (Array.isArray(res)) {
          this.trips = res;
        } else {
          this.trips = [];
          console.error("返回的行程数据格式不正确:", res);
        }
        this.hasSearched = true;
      } catch (error) {
        uni.hideLoading();
        this.trips = [];
        this.hasSearched = true;
        uni.showToast({ title: '查找失败，请稍后再试', icon: 'none' });
      }
    },
    async applyForTrip(tripId) {
      const userInfo = uni.getStorageSync('userInfo');
      if (!userInfo) {
        uni.showToast({ title: '请先登录', icon: 'none' });
        return;
      }
      // 假设每次只预订1个座位，金额为trip.price
      const trip = this.trips.find(t => t.id === tripId);
      if (!trip) return;
      uni.showLoading({ title: '正在生成订单...' });
      try {
        const order = await applyOrder({
          tripId: tripId,
          passengerId: userInfo.id,
          seatCount: 1,
          amount: trip.price
        });
        uni.hideLoading();
        this.pendingOrder = order;
        this.markers = [];
        this.polyline = [];
        this.$refs.orderPopup.open();
      } catch (e) {
        uni.hideLoading();
        uni.showToast({ title: '下单失败', icon: 'none' });
      }
    },
    async confirmOrder() {
      if (!this.pendingOrder) return;
      uni.showLoading({ title: '正在确认...' });
      try {
        const res = await confirmOrder(this.pendingOrder.id);
        if (res.code === 200) {
          console.log('订单确认成功', res);
          this.pendingOrder = null;
          this.$refs.orderPopup.close();
          uni.showToast({ title: '订单已确认', icon: 'success' });
          // 确认订单后刷新行程列表
          this.searchTrips(true); 
        } else {
          uni.showToast({ title: res.msg || '订单确认失败', icon: 'none' });
        }
      } catch (e) {
        uni.hideLoading();
        uni.showToast({ title: '确认失败', icon: 'none' });
      }
    },
    async cancelOrder() {
      if (!this.pendingOrder) return;
      uni.showLoading({ title: '正在取消...' });
      try {
        await cancelOrder(this.pendingOrder.id);
        uni.hideLoading();
        uni.showToast({ title: '已取消', icon: 'none' });
        this.$refs.orderPopup.close();
        this.pendingOrder = null;
        this.updateMapMarkers();
      } catch (e) {
        uni.hideLoading();
        uni.showToast({ title: '取消失败', icon: 'none' });
      }
    },
    formatOrderTime(time) {
      if (!time) return '';
      const date = new Date(time);
      return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`;
    },
    orderStatusText(status) {
      switch(status) {
        case 0: return '待确认';
        case 1: return '已确认';
        case 3: return '已取消';
        default: return '未知';
      }
    },
    payStatusText(status) {
      switch(status) {
        case 0: return '未支付';
        case 1: return '已支付';
        default: return '未知';
      }
    },
    updateMapMarkers() {
      this.markers = [];
      this.polyline = [];
      if (this.startLng && this.startLat) {
        this.markers.push({
          id: 1,
          longitude: this.startLng,
          latitude: this.startLat,
          title: '起点',
          iconPath: '/static/marker.png',
          width: 32,
          height: 32
        });
      }
      if (this.endLng && this.endLat) {
        this.markers.push({
          id: 2,
          longitude: this.endLng,
          latitude: this.endLat,
          title: '终点',
          iconPath: '/static/marker.png',
          width: 32,
          height: 32
        });
      }
      if (this.startLng && this.startLat && this.endLng && this.endLat) {
        this.polyline = [{
          points: [
            { longitude: this.startLng, latitude: this.startLat },
            { longitude: this.endLng, latitude: this.endLat }
          ],
          color: '#007AFF',
          width: 6
        }];
      }
    }
  },
  mounted() {
    // #ifdef H5
    const BAIDU_MAP_AK = 'bc5jB0qU7svV3dWgqfNn5ivZZ7P75SVq';
    if (!window.BMapGL) {
      window.initBaiduMapCallback = () => {
        this.initBMap();
      };
      const script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = `https://api.map.baidu.com/api?v=1.0&type=webgl&ak=${BAIDU_MAP_AK}&callback=initBaiduMapCallback`;
      document.head.appendChild(script);
    } else {
      this.initBMap();
    }
    // #endif
    // #ifndef H5
    uni.getLocation({
      type: 'gcj02',
      success: (res) => {
        this.longitude = res.longitude;
        this.latitude = res.latitude;
      }
    });
    // #endif
  },
  onReady() {
  }
}
</script>

<style>
.search-trip-container {
  padding: 32rpx 20rpx 20rpx 20rpx;
  background: #f6f8fa;
  min-height: 100vh;
}
.search-card {
  background: #fff;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
  padding: 32rpx 24rpx 24rpx 24rpx;
  margin-bottom: 32rpx;
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  margin-bottom: 24rpx;
}
.input-box {
  border: 1rpx solid #e0e0e0;
  border-radius: 12rpx;
  padding: 18rpx 24rpx;
  font-size: 30rpx;
  background: #f9f9f9;
  margin-bottom: 0;
}
.picker-label {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 0;
}
.picker-value {
  color: #007AFF;
  margin-left: 12rpx;
}
.search-btn {
  width: 100%;
  background: linear-gradient(90deg, #007AFF 0%, #00c6ff 100%);
  color: #fff;
  border-radius: 16rpx;
  font-size: 32rpx;
  font-weight: bold;
  padding: 20rpx 0;
  margin-top: 10rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,122,255,0.08);
}
.trip-map {
  width: 100%;
  height: 320rpx;
  border-radius: 18rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
}
.result-title {
  font-size: 30rpx;
  color: #333;
  font-weight: bold;
  margin-bottom: 18rpx;
  margin-left: 8rpx;
}
.trip-card {
  background: #fff;
  border-radius: 18rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.06);
  padding: 24rpx 20rpx 18rpx 20rpx;
  margin-bottom: 22rpx;
}
.trip-route {
  display: flex;
  align-items: center;
  font-size: 30rpx;
  color: #007AFF;
  margin-bottom: 10rpx;
}
.trip-point {
  font-weight: bold;
}
.trip-arrow {
  margin: 0 16rpx;
  color: #888;
}
.trip-info {
  font-size: 26rpx;
  color: #666;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}
.no-result {
  text-align: center;
  color: #bbb;
  font-size: 28rpx;
  margin-top: 40rpx;
}
.apply-btn {
  width: 100%;
  background: linear-gradient(90deg, #00c6ff 0%, #007AFF 100%);
  color: #fff;
  border-radius: 12rpx;
  font-size: 28rpx;
  font-weight: bold;
  padding: 16rpx 0;
  margin-top: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,122,255,0.08);
}
.add-car-popup {
  background: #fff;
  border-radius: 24rpx;
  padding: 48rpx 36rpx 60rpx 36rpx;
  width: 90vw;
  max-width: 600rpx;
  box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.12);
  animation: popupIn .3s;
  max-height: 80vh;
  overflow-y: auto;
}
.popup-title {
  font-size: 36rpx;
  font-weight: 700;
  margin-bottom: 36rpx;
  text-align: center;
  color: #222;
  letter-spacing: 2rpx;
}
.form-list {
  margin-bottom: 32rpx;
}
.form-item {
  display: flex;
  align-items: center;
  border-bottom: 1rpx solid #eee;
  margin-bottom: 18rpx;
  padding-bottom: 8rpx;
  font-size: 28rpx;
}
.popup-actions {
  display: flex;
  justify-content: space-between;
  gap: 24rpx;
  margin-top: 24rpx;
}
.main-btn {
  flex: 1;
  background: linear-gradient(90deg, #007aff 60%, #00c6fb 100%);
  color: #fff;
  border-radius: 32rpx;
  font-size: 30rpx;
  font-weight: 600;
  box-shadow: 0 2rpx 8rpx rgba(0,122,255,0.08);
}
.cancel-btn {
  flex: 1;
  background: #f5f5f5;
  color: #888;
  border-radius: 32rpx;
  font-size: 30rpx;
  font-weight: 600;
}
</style>

<!-- 百度地图AK集成：H5端请在index.html引入 -->
<!-- <script type="text/javascript" src="https://api.map.baidu.com/api?v=3.0&ak=YDe8yIOAuKF66bXg68Timl6qZylATSaJ"></script> --> 