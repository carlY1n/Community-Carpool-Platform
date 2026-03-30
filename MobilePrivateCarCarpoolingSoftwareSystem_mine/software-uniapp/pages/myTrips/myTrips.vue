<template>
  <view class="trips-container">
    <view class="page-header">
      <text class="page-title">我的行程</text>
    </view>
    
    <view class="loading" v-if="loading">
      <text>加载中...</text>
    </view>
    
    <view v-else-if="trips.length === 0" class="empty-list">
      <image class="empty-icon" src="/static/empty.png" mode="aspectFit"></image>
      <text class="empty-text">暂无行程记录</text>
      <button class="create-btn" @click="goToCreateTrip">发布新行程</button>
    </view>
    
    <view v-else class="trips-list">
      <view class="list-header">
        <text>共 {{trips.length}} 条行程</text>
      </view>
      
      <view v-for="(trip, index) in trips" :key="trip.id" class="trip-card">
        <view class="trip-header">
          <text class="trip-id">行程ID: {{trip.id}}</text>
          <text class="trip-status">状态: {{getTripStatusText(trip.status)}}</text>
        </view>
        
        <view class="trip-info">
          <view class="route-info">
            <view class="start-point">
              <text class="label">出发地:</text>
              <text class="value">{{trip.startLocation}}</text>
            </view>
            <view class="end-point">
              <text class="label">目的地:</text>
              <text class="value">{{trip.endLocation}}</text>
            </view>
          </view>
          
          <view class="trip-details">
            <view class="detail-item">
              <text class="label">发车时间:</text>
              <text class="value">{{formatDate(trip.departureTime)}}</text>
            </view>
            <view class="detail-item">
              <text class="label">座位数:</text>
              <text class="value">{{trip.seatAvailable}}</text>
            </view>
            <view class="detail-item">
              <text class="label">价格:</text>
              <text class="value">¥{{trip.price}}</text>
            </view>
          </view>
          
          <view class="car-info">
            <text class="label">车辆信息:</text>
            <text class="value">{{trip.carInfo ? `${trip.carInfo.carBrand} ${trip.carInfo.carModel} (${trip.carInfo.carColor})` : '无车辆信息'}}</text>
          </view>
        </view>
        
        <!-- 乘客列表 -->
        <view class="passengers-section" v-if="trip.orders && trip.orders.length > 0">
          <text class="section-title">已预订乘客</text>
          <view v-for="order in trip.orders" :key="order.id" class="passenger-item">
            <text class="passenger-name">{{ order.passengerName || `乘客ID: ${order.passengerId}` }} ({{ order.seatCount }}座)</text>
            <!-- 仅在订单状态为"已确认/待出行"时显示聊天按钮 -->
            <button  class="chat-btn" @click="goToChat(order)">联系乘客</button>
          </view>
        </view>

        <view class="trip-actions">
          <!-- 仅在发布中时显示取消按钮 -->
          <button v-if="trip.status === 1" class="cancel-btn" @click="confirmCancel(trip)">取消行程</button>
          <!-- <button class="delete-btn" @click="confirmDelete(trip)">删除行程</button> -->
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getDriverTrips, deleteTrip, cancelTrip as cancelTripApi } from '@/common/api.js';

export default {
  data() {
    return {
      loading: true,
      userId: null,
      trips: [],
      // 添加模拟数据标志
      useMockData: false
    };
  },
  onLoad() {
    // 从本地存储获取用户信息
    const userInfo = uni.getStorageSync('userInfo');
    if (userInfo && userInfo.id) {
      this.userId = userInfo.id;
      this.fetchTrips();
    } else {
      uni.showToast({
        title: '请先登录',
        icon: 'none'
      });
      setTimeout(() => {
        uni.navigateTo({ url: '/pages/login/login' });
      }, 2000);
    }
  },
  methods: {
    goToChat(order) {
      console.log('准备进入聊天，传递的订单参数为:', order);
      const chatParams = {
        orderId: order.id,
        receiverId: order.passengerId
      };
      uni.navigateTo({
        url: `/pages/chat/chat?params=${encodeURIComponent(JSON.stringify(chatParams))}`
      });
    },
    // 获取车主发布的行程
    async fetchTrips() {
      this.loading = true;
      try {
        const res = await getDriverTrips(this.userId);
        if (res && res.code === 200) {
          this.trips = res.data || [];
          this.useMockData = false;
        } else {
          // 如果API调用失败，使用模拟数据
          this.loadMockTrips();
          this.useMockData = true;
        }
      } catch (error) {
        console.error('获取行程失败:', error);
        // 如果API调用失败，使用模拟数据
        this.loadMockTrips();
        this.useMockData = true;
      } finally {
        this.loading = false;
      }
    },
    
    // 加载模拟数据
    loadMockTrips() {
      this.trips = [
        {
          id: 1001,
          startLocation: '北京市海淀区',
          endLocation: '北京市朝阳区',
          departureTime: '2023-12-10T08:30:00',
          availableSeats: 3,
          price: 15,
          status: 'CREATED',
          carInfo: {
            carBrand: '大众',
            carModel: '宝来',
            carColor: '黑色'
          }
        },
        {
          id: 1002,
          startLocation: '上海市徐汇区',
          endLocation: '上海市浦东新区',
          departureTime: '2023-12-12T17:15:00',
          availableSeats: 2,
          price: 20,
          status: 'ONGOING',
          carInfo: {
            carBrand: '本田',
            carModel: '雅阁',
            carColor: '白色'
          }
        },
        {
          id: 1003,
          startLocation: '广州市天河区',
          endLocation: '深圳市南山区',
          departureTime: '2023-12-15T09:00:00',
          availableSeats: 4,
          price: 150,
          status: 'CREATED',
          carInfo: null
        }
      ];
      
      // 显示提示，告知用户正在使用模拟数据
      uni.showToast({
        title: '使用模拟数据（后端API未实现）',
        icon: 'none',
        duration: 2500
      });
    },
    
    // 格式化日期显示
    formatDate(dateStr) {
      if (!dateStr) return '未设置';
      const date = new Date(dateStr);
      return date.getFullYear() + '-' + 
             this.padZero(date.getMonth() + 1) + '-' + 
             this.padZero(date.getDate()) + ' ' + 
             this.padZero(date.getHours()) + ':' + 
             this.padZero(date.getMinutes());
    },
    
    // 数字补零
    padZero(num) {
      return num < 10 ? '0' + num : num;
    },
    
    // 获取行程状态文本
    getTripStatusText(status) {
      const statusMap = {
        1: '发布中',
        2: '已满员',
        3: '已结束',
        4: '已取消'
      };
      return statusMap[status] || '未知状态';
    },
    
    // 确认取消行程
    confirmCancel(trip) {
      uni.showModal({
        title: '确认取消',
        content: `确定要取消从 ${trip.startLocation} 到 ${trip.endLocation} 的行程吗？`,
        success: async (res) => {
          if (res.confirm) {
            await this.handleCancel(trip.id);
          }
        }
      });
    },

    // 取消行程
    async handleCancel(tripId) {
      uni.showLoading({ title: '取消中...' });
      try {
        const res = await cancelTripApi(tripId, this.userId);
        if (res && res.code === 200) {
          uni.showToast({ title: '行程已取消', icon: 'success' });
          // 更新本地数据
          const trip = this.trips.find(t => t.id === tripId);
          if (trip) {
            trip.status = 4; // 4: 已取消
          }
        } else {
          uni.showToast({ title: res.msg || '取消失败', icon: 'none' });
        }
      } catch (error) {
        console.error('取消行程失败:', error);
        uni.showToast({ title: '操作失败，请稍后重试', icon: 'none' });
      } finally {
        uni.hideLoading();
      }
    },
    
    // 确认删除行程
    confirmDelete(trip) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除从 ${trip.startLocation} 到 ${trip.endLocation} 的行程吗？`,
        success: async (res) => {
          if (res.confirm) {
            await this.handleDelete(trip.id);
          }
        }
      });
    },
    
    // 删除行程
    async handleDelete(tripId) {
      uni.showLoading({ title: '删除中...' });
      try {
        // 如果使用的是模拟数据，直接模拟删除操作
        if (this.useMockData) {
          // 模拟网络延迟
          await new Promise(resolve => setTimeout(resolve, 500));
          
          // 从本地数组中删除
          this.trips = this.trips.filter(trip => trip.id !== tripId);
          
          uni.showToast({
            title: '删除成功（模拟）',
            icon: 'success'
          });
          return;
        }
        
        // 正常API调用
        const res = await deleteTrip(tripId, this.userId);
        if (res && res.code === 200) {
          uni.showToast({
            title: '删除成功',
            icon: 'success'
          });
          // 重新加载行程列表
          this.fetchTrips();
        } else {
          uni.showToast({
            title: res.msg || '删除失败',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('删除行程失败:', error);
        
        // 如果使用的是模拟数据，则伪造成功删除
        if (this.useMockData) {
          this.trips = this.trips.filter(trip => trip.id !== tripId);
          uni.showToast({
            title: '删除成功（模拟）',
            icon: 'success'
          });
        } else {
          uni.showToast({
            title: '删除行程失败',
            icon: 'none'
          });
        }
      } finally {
        uni.hideLoading();
      }
    },
    
    // 前往发布行程页面
    goToCreateTrip() {
      uni.navigateTo({
        url: '/pages/publishTrip/publishTrip'
      });
    }
  }
};
</script>

<style>
.trips-container {
  padding: 30rpx;
  background-color: #f8f8f8;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30rpx;
}

.page-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.loading, .empty-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
}

.empty-icon {
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 40rpx;
}

.create-btn {
  background-color: #007AFF;
  color: #fff;
  font-size: 28rpx;
  width: 240rpx;
  height: 80rpx;
  line-height: 80rpx;
  border-radius: 40rpx;
}

.list-header {
  font-size: 24rpx;
  color: #666;
  padding: 20rpx 0;
}

.trip-card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.trip-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
  border-bottom: 1rpx solid #eee;
  padding-bottom: 20rpx;
}

.trip-id {
  font-size: 24rpx;
  color: #999;
}

.trip-status {
  font-size: 24rpx;
  color: #007AFF;
  font-weight: bold;
}

.route-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.start-point, .end-point {
  width: 48%;
}

.trip-details {
  display: flex;
  flex-wrap: wrap;
  margin: 20rpx 0;
}

.detail-item {
  width: 50%;
  margin-bottom: 10rpx;
}

.car-info {
  margin-top: 10rpx;
}

.label {
  color: #666;
  font-size: 24rpx;
  margin-right: 10rpx;
}

.value {
  color: #333;
  font-size: 28rpx;
  font-weight: 500;
}

.trip-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20rpx;
  border-top: 1rpx solid #eee;
  padding-top: 20rpx;
}

.delete-btn {
  background-color: #ff3b30;
  color: #fff;
  font-size: 24rpx;
  width: 180rpx;
  height: 70rpx;
  line-height: 70rpx;
  border-radius: 35rpx;
}

.passengers-section {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}
.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  display: block;
}
.passenger-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}
.passenger-name {
  font-size: 14px;
  color: #555;
}
.chat-btn {
  background-color: #007aff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 12px;
  margin-left: 10px;
}
</style> 