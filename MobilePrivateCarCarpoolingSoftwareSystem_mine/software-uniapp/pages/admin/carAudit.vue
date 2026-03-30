<template>
  <view class="car-audit-container">
    <view class="title">待审核车辆列表</view>
    <view v-if="loading" class="loading">加载中...</view>
    <view v-else>
      <view v-if="cars.length === 0" class="empty">暂无待审核车辆</view>
      <view v-for="car in cars" :key="car.id" class="car-card">
        <view class="car-info">
          <text>车牌号：{{ car.plateNumber }}</text>
          <text>品牌：{{ car.brand }}</text>
          <text>型号：{{ car.model }}</text>
          <text>颜色：{{ car.color }}</text>
          <text>座位数：{{ car.seatCount }}</text>
          <text>注册时间：{{ formatDate(car.createTime) }}</text>
        </view>
        <view class="btn-group">
          <button class="pass-btn" @click="auditCar(car.id, 1)">通过</button>
          <button class="reject-btn" @click="auditCar(car.id, 2)">拒绝</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getPendingCars, auditCar } from '@/common/api.js';
export default {
  data() {
    return {
      cars: [],
      loading: false
    }
  },
  methods: {
    async fetchPendingCars() {
      this.loading = true;
      try {
        const res = await getPendingCars();
        this.cars = res;
      } catch (e) {
        uni.showToast({ title: '获取车辆失败', icon: 'none' });
      }
      this.loading = false;
    },
    async auditCar(carId, auditStatus) {
      uni.showLoading({ title: '提交中...' });
      try {
        await auditCar(carId, auditStatus);
        uni.hideLoading();
        uni.showToast({ title: auditStatus === 1 ? '审核通过' : '已拒绝', icon: 'success' });
        this.fetchPendingCars();
      } catch (e) {
        uni.hideLoading();
        uni.showToast({ title: '操作失败', icon: 'none' });
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`;
    }
  },
  onShow() {
    this.fetchPendingCars();
  }
}
</script>

<style>
.car-audit-container {
  padding: 32rpx;
}
.title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 24rpx;
}
.loading {
  color: #888;
  font-size: 28rpx;
  margin: 40rpx 0;
}
.empty {
  color: #aaa;
  font-size: 28rpx;
  margin: 40rpx 0;
  text-align: center;
}
.car-card {
  background: #fff;
  border-radius: 18rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
  margin-bottom: 24rpx;
  padding: 24rpx;
}
.car-info text {
  display: block;
  font-size: 28rpx;
  margin-bottom: 8rpx;
}
.btn-group {
  display: flex;
  gap: 24rpx;
  margin-top: 16rpx;
}
.pass-btn {
  background: #4caf50;
  color: #fff;
  border-radius: 10rpx;
  padding: 12rpx 32rpx;
}
.reject-btn {
  background: #f44336;
  color: #fff;
  border-radius: 10rpx;
  padding: 12rpx 32rpx;
}
</style> 