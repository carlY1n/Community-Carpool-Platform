<template>
  <view class="publish-trip-container">
    <view class="form-card">
      <view class="form-group">
        <input v-model="startLocation" placeholder="请选择起点" readonly @click="choosePoint('start')" class="input-box" />
        <input v-model="endLocation" placeholder="请选择终点" readonly @click="choosePoint('end')" class="input-box" />
        <picker mode="date" v-model="departureDate" @change="onDateChange">
          <view class="picker-label">出发日期: <text class="picker-value">{{ departureDate || '请选择' }}</text></view>
        </picker>
        <input v-model="price" type="number" placeholder="请输入拼车价格" class="input-box" />
        <input v-model="seatAvailable" type="number" placeholder="请输入可用座位数" class="input-box" />
        <picker :range="carList" range-key="plateNumber" v-model="carIndex" @change="onCarChange">
          <view class="picker-label">选择车辆: <text class="picker-value">{{ carList[carIndex] && carList[carIndex].plateNumber ? carList[carIndex].plateNumber : '请选择' }}</text></view>
        </picker>
      </view>
      <button class="publish-btn" @click="publishTrip">发布行程</button>
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
      show-location
    ></map>
    <!-- #endif -->
    
    <!-- #ifndef H5 -->
    <view v-if="isGeocoding" class="loading-mask">
      <view class="loading-text">正在获取地址...</view>
    </view>
    <!-- #endif -->
  </view>
</template>

<script>
import { getMyCars, publishTripApi, getMyApprovedCars } from '@/common/api.js';
export default {
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
      price: '',
      seatAvailable: '',
      carList: [],
      carIndex: 0,
      markers: [],
      polyline: [],
      selectType: '',
      bmap: null,
      isGeocoding: false
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

      /*
      const geolocation = new window.BMapGL.Geolocation();
      geolocation.getCurrentPosition((result) => {
        if (geolocation.getStatus() === 0) { // BMAP_STATUS_SUCCESS
          this.longitude = result.point.lng;
          this.latitude = result.point.lat;
          this.bmap.panTo(result.point);
        } else {
          console.error('Baidu Geolocation failed:', geolocation.getStatus());
          const status = geolocation.getStatus();
          if (status === 6) { // BMAP_STATUS_PERMISSION_DENIED
            this.handleLocationPermissionDenied();
          } else {
            let errorMsg = '定位失败';
             if (status === 2) {
              errorMsg = '定位失败，请检查网络或稍后再试';
            } else if (status === 8) {
              errorMsg = '定位超时，请稍后再试';
            }
            uni.showToast({ title: errorMsg, icon: 'none', duration: 3000 });
          }
        }
      });
      */
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
            this.startLng = longitude;
            this.startLat = latitude;
          } else if (this.selectType === 'end') {
            this.endLocation = address;
            this.endLng = longitude;
            this.endLat = latitude;
          }
        },
        fail: () => {
          const address = `经度:${longitude.toFixed(6)}, 纬度:${latitude.toFixed(6)}`;
          if (this.selectType === 'start') {
            this.startLocation = address;
            this.startLng = longitude;
            this.startLat = latitude;
          } else if (this.selectType === 'end') {
            this.endLocation = address;
            this.endLng = longitude;
            this.endLat = latitude;
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
    
    updateMapMarkers() {
      this.markers = [];
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
      } else {
        this.polyline = [];
      }
      if (this.startLng && this.startLat) {
        this.longitude = this.startLng;
        this.latitude = this.startLat;
      } else if (this.endLng && this.endLat) {
        this.longitude = this.endLng;
        this.latitude = this.endLat;
      }
    },
    
    onDateChange(e) {
      this.departureDate = e.detail.value;
    },
    onCarChange(e) {
      this.carIndex = e.detail.value;
    },
    async getCarList() {
      const userInfo = uni.getStorageSync('userInfo');
      if (!userInfo) return;
      console.log('当前登录用户id:', userInfo.id);
      const res = await getMyApprovedCars(userInfo.id);
      if (res && (res.data || Array.isArray(res))) {
        this.carList = res.data || res;
        console.log('获取到的车辆列表:', this.carList);
      }
    },
    resetForm() {
      this.startLocation = '';
      this.endLocation = '';
      this.startLng = null;
      this.startLat = null;
      this.endLng = null;
      this.endLat = null;
      this.departureDate = '';
      this.price = '';
      this.seatAvailable = '';
      this.carIndex = 0;
      this.markers = [];
      this.polyline = [];
    },
    async publishTrip() {
      if (!this.startLng || !this.endLng || !this.departureDate || !this.price || !this.seatAvailable || !this.carList[this.carIndex]) {
        uni.showToast({ title: '请填写完整信息', icon: 'none' });
        return;
      }
      const userInfo = uni.getStorageSync('userInfo');
      uni.showLoading({ title: '正在发布...' });
      const tripData = {
        driverId: userInfo.id,
        carId: this.carList[this.carIndex].id,
        startLocation: this.startLocation,
        startLng: this.startLng,
        startLat: this.startLat,
        endLocation: this.endLocation,
        endLng: this.endLng,
        endLat: this.endLat,
        departureTime: this.departureDate,
        price: this.price,
        seatAvailable: this.seatAvailable
      };
      try {
        const res = await publishTripApi(tripData);
        uni.hideLoading();
        console.log(res)
        if (res.id != null) {
          uni.showToast({ title: '发布成功', icon: 'success' });
          setTimeout(() => {
            this.resetForm();
            this.getCarList();
          }, 1300); // 2000 毫秒 = 2 秒
        } else {
          uni.showToast({ title: res && res.msg || '发布失败', icon: 'none' });
        }
      } catch (error) {
        uni.hideLoading();
        uni.showToast({ title: '发布请求失败', icon: 'none' });
      }
    },
    handleLocationPermissionDenied() {
      uni.showModal({
        title: '需要定位权限',
        content: '为了正常使用地图功能，需要您授权定位权限。是否前往设置页面开启？',
        success: (res) => {
          if (res.confirm) {
            // #ifdef APP-PLUS
            this.openAppSettings();
            // #endif
            // #ifndef APP-PLUS
            uni.showModal({
              title: '操作提示',
              content: '无法自动跳转。请在浏览器或系统设置中手动开启定位权限。',
              showCancel: false
            });
            // #endif
          }
        }
      });
    },
    openAppSettings() {
      // #ifdef APP-PLUS
      var platform = uni.getSystemInfoSync().platform;
      if (platform == 'android') {
        var main = plus.android.runtimeMainActivity();
        var Intent = plus.android.importClass('android.content.Intent');
        var Settings = plus.android.importClass('android.provider.Settings');
        var Uri = plus.android.importClass('android.net.Uri');
        var intent = new Intent();
        intent.setAction(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
        var uri = Uri.fromParts("package", main.getPackageName(), null);
        intent.setData(uri);
        main.startActivity(intent);
      } else if (platform == 'ios') {
        var UIApplication = plus.ios.importClass('UIApplication');
        var NSURL = plus.ios.importClass('NSURL');
        var setting = NSURL.URLWithString('app-settings:');
        var application = UIApplication.sharedApplication();
        application.openURL(setting);
        plus.ios.deleteObject(setting);
        plus.ios.deleteObject(application);
      }
      // #endif
    }
  },
  mounted() {
    this.getCarList();
    
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
    /*
    uni.getLocation({
      type: 'gcj02',
      success: (res) => {
        this.longitude = res.longitude;
        this.latitude = res.latitude;
      },
      fail: (err) => {
        console.error('uni.getLocation failed:', err);
        if (err.errMsg && (err.errMsg.indexOf('auth deny') > -1 || err.errMsg.indexOf('denied') > -1)) {
          this.handleLocationPermissionDenied();
        }
      }
    });
    */
    // #endif
  }
}
</script>

<style>
.publish-trip-container {
  padding: 32rpx 20rpx 20rpx 20rpx;
  background: #f6f8fa;
  min-height: 100vh;
}
.form-card {
  background: #fff;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
  padding: 32rpx 24rpx 24rpx 24rpx;
  margin-bottom: 32rpx;
}
.form-group {
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
.publish-btn {
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
.loading-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.loading-text {
  background: #fff;
  padding: 20rpx 40rpx;
  border-radius: 8rpx;
  font-size: 30rpx;
}
</style> 