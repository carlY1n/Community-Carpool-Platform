<template>
  <view class="car-manage-content">
    <view class="header">
      <text class="title">车辆管理</text>
      <button class="add-btn" @click="openAddCarPopup">新增车辆</button>
    </view>
    <view v-if="carList.length === 0" class="empty">暂无车辆信息</view>
    <view v-else class="car-list">
      <view class="car-item" v-for="car in carList" :key="car.id">
        <view class="car-info">
          <text>车牌号：{{car.plateNumber}}</text>
          <text>品牌：{{car.brand}}</text>
          <text>车型：{{car.model}}</text>
          <text>颜色：{{car.color}}</text>
          <text>座位数：{{car.seatCount}}</text>
        </view>
        <view class="car-actions">
          <view class="audit-status" :class="'status-' + car.auditStatus">
            <text v-if="car.auditStatus === 0">待审核</text>
            <text v-else-if="car.auditStatus === 1">审核通过</text>
            <text v-else-if="car.auditStatus === 2">审核拒绝</text>
          </view>
          <button class="delete-btn" @click="confirmDeleteCar(car.id)">删除</button>
        </view>
      </view>
    </view>
    <!-- 新增车辆弹窗 -->
    <uni-popup ref="addCarPopup" type="center">
      <view class="add-car-popup">
        <view class="popup-title">新增车辆</view>
        <view class="form-list">
          <view class="form-item" v-for="item in formItems" :key="item.key">
            <view class="input-icon">
              <image :src="item.icon" mode="aspectFit" />
            </view>
            <input
              v-model="form[item.key]"
              :type="item.type || 'text'"
              :placeholder="item.placeholder"
              :maxlength="item.maxlength || 20"
              class="input"
            />
          </view>
        </view>
        <view class="popup-actions">
          <button class="main-btn" @click="submitAddCar">提交</button>
          <button class="cancel-btn" @click="closeAddCarPopup">取消</button>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
import { addCar, getMyCars, deleteCar } from '@/common/api.js';
import uniPopup from '@dcloudio/uni-ui/lib/uni-popup/uni-popup.vue';
export default {
  components: { uniPopup },
  data() {
    return {
      carList: [],
      showAddCar: false,
      form: {
        plateNumber: '',
        brand: '',
        model: '',
        color: '',
        seatCount: 4
      },
      userInfo: null,
      formItems: [
        { key: 'plateNumber', placeholder: '请输入车牌号', icon: '/static/plate.png' },
        { key: 'brand', placeholder: '请输入品牌', icon: '/static/brand.png' },
        { key: 'model', placeholder: '请输入车型', icon: '/static/model.png' },
        { key: 'color', placeholder: '请输入颜色', icon: '/static/color.png' },
        { key: 'seatCount', placeholder: '请输入座位数', icon: '/static/seat.png', type: 'number', maxlength: 2 }
      ]
    };
  },
  onShow() {
    this.userInfo = uni.getStorageSync('userInfo');
    this.loadCarList();
  },
  methods: {
    loadCarList() {
      if (!this.userInfo) return;
      getMyCars(this.userInfo.id).then(res => {
        this.carList = res.data || res;
      });
    },
    openAddCarPopup() {
      this.showAddCar = true;
      this.$refs.addCarPopup.open();
    },
    closeAddCarPopup() {
      this.showAddCar = false;
      this.$refs.addCarPopup.close();
    },
    submitAddCar() {
      if (!this.userInfo) return;
      // 表单校验
      if (!this.form.plateNumber.trim()) {
        uni.showToast({ title: '请输入车牌号', icon: 'none' });
        return;
      }
      if (!this.form.brand.trim()) {
        uni.showToast({ title: '请输入品牌', icon: 'none' });
        return;
      }
      if (!this.form.model.trim()) {
        uni.showToast({ title: '请输入车型', icon: 'none' });
        return;
      }
      if (!this.form.color.trim()) {
        uni.showToast({ title: '请输入颜色', icon: 'none' });
        return;
      }
      if (!this.form.seatCount || this.form.seatCount < 1) {
        uni.showToast({ title: '请输入有效的座位数', icon: 'none' });
        return;
      }
      // 通过校验后再提交
      const data = {
        ...this.form,
        userId: this.userInfo.id
      };
      addCar(data).then(() => {
        uni.showToast({ title: '提交成功，等待审核', icon: 'none' });
        this.closeAddCarPopup();
        this.loadCarList();
        this.form = { plateNumber: '', brand: '', model: '', color: '', seatCount: 4 };
      });
    },
    confirmDeleteCar(id) {
      uni.showModal({
        title: '提示',
        content: '确定要删除该车辆吗？',
        success: (res) => {
          if (res.confirm) {
            this.deleteCarById(id);
          }
        }
      });
    },
    deleteCarById(id) {
      if (!this.userInfo) return;
      deleteCar(id, this.userInfo.id).then(() => {
        uni.showToast({ title: '删除成功', icon: 'none' });
        this.loadCarList();
      });
    }
  }
};
</script>

<style>
.car-manage-content {
  padding: 30rpx;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}
.title {
  font-size: 36rpx;
  font-weight: bold;
}
.add-btn {
  background: #007aff;
  color: #fff;
  border-radius: 30rpx;
  padding: 10rpx 30rpx;
  font-size: 28rpx;
}
.car-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}
.car-item {
  background: #f8f8f8;
  border-radius: 20rpx;
  padding: 20rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.car-info {
  flex: 1;
}
.car-actions {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 18rpx;
}
.car-info text {
  display: block;
  font-size: 28rpx;
  margin-bottom: 6rpx;
}
.audit-status {
  font-size: 28rpx;
  font-weight: bold;
}
.status-0 { color: #ff9500; }
.status-1 { color: #4cd964; }
.status-2 { color: #ff3b30; }
.empty {
  text-align: center;
  color: #999;
  margin-top: 100rpx;
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
@keyframes popupIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
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
}
.input-icon {
  width: 40rpx;
  height: 40rpx;
  margin-right: 16rpx;
  opacity: 0.7;
}
.input-icon image {
  width: 100%;
  height: 100%;
}
.input {
  flex: 1;
  font-size: 28rpx;
  border: none;
  outline: none;
  background: transparent;
  padding: 12rpx 0;
}
.popup-actions {
  display: flex;
  justify-content: space-between;
  gap: 24rpx;
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
.delete-btn {
  margin-left: 0;
  background: #ff3b30;
  color: #fff;
  border-radius: 24rpx;
  font-size: 26rpx;
  padding: 10rpx 24rpx;
}
</style> 