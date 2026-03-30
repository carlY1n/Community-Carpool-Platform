<template>
  <view class="my-orders-container">
    <view class="header">
      <text class="title">我的订单</text>
    </view>
    <view v-if="loading" class="loading">加载订单中...</view>
    <view v-else-if="orders.length === 0" class="empty">暂无订单记录</view>
    <view v-else class="order-list">
      <view v-for="(order, index) in orders" :key="order.id" class="order-card">
        <view class="order-header">
          <text class="order-id">订单号: {{ order.id }}</text>
          <text :class="['order-status', getOrderStatusClass(order.orderStatus)]">{{ orderStatusText(order.orderStatus) }}</text>
        </view>
        <view class="trip-info">
          <view class="trip-route" v-if="order.trip">
            <text class="trip-point">{{ order.trip.startLocation || `经度:${order.trip.startLng}, 纬度:${order.trip.startLat}` }}</text>
            <text class="trip-arrow">→</text>
            <text class="trip-point">{{ order.trip.endLocation || `经度:${order.trip.endLng}, 纬度:${order.trip.endLat}` }}</text>
          </view>
          <view v-else class="no-trip-info">
            <text>行程ID: {{ order.tripId }}</text>
          </view>
          <view class="departure-time">
            <text class="label">出发时间:</text>
            <text class="value">{{ order.trip && order.trip.departureTime ? formatDateTime(order.trip.departureTime) : '未知' }}</text>
          </view>
          <text v-if="order.trip">价格: ¥{{ order.trip.price || '未知' }}</text>
        </view>
        <view class="passenger-info" v-if="userInfo && userInfo.username">
          <text>乘客: {{ userInfo.username }}</text>
        </view>
        <view class="order-details">
          <text>座位数: {{ order.seatCount }}</text>
          <text>金额: ¥{{ order.amount }}</text>
          <text>下单时间: {{ formatDateTime(order.orderTime) }}</text>
          <text>支付状态: {{ payStatusText(order.payStatus) }}</text>
        </view>
        <view class="order-actions">
          <button v-if="order.orderStatus === 0" class="confirm-btn" @click="confirmOrder(order.id)">确认订单</button>
          <button v-if="order.orderStatus === 0" class="cancel-btn" @click="cancelOrder(order.id)">取消订单</button>
          <button v-if="order.orderStatus === 1" class="chat-btn" @click="goToChat(order)">联系司机</button>
        </view>
        <view class="order-actions" v-if="shouldShowReviewButton(order)">
          <button class="review-btn" @click="openReviewDialog(order)">评价订单</button>
        </view>
      </view>
    </view>

    <!-- 评价弹窗 -->
    <uni-popup ref="reviewPopup" type="center">
      <view class="review-popup">
        <view class="review-header">
          <text class="review-title">订单评价</text>
          <text class="review-close" @click="closeReviewDialog">×</text>
        </view>
        
        <view class="review-tabs">
          <view 
            :class="['review-tab', reviewType === 'good' ? 'active' : '']" 
            @click="reviewType = 'good'"
          >好评</view>
          <view 
            :class="['review-tab', reviewType === 'bad' ? 'active' : '']" 
            @click="reviewType = 'bad'"
          >差评</view>
        </view>
        
        <view class="review-content">
          <view v-if="reviewType === 'good'" class="good-review">
            <view class="rating-section">
              <text class="rating-label">评分:</text>
              <view class="rating-stars">
                <text 
                  v-for="star in 5" 
                  :key="star" 
                  :class="['star', star <= rating ? 'active' : '']"
                  @click="rating = star"
                >★</text>
              </view>
            </view>
            <textarea 
              class="review-textarea" 
              v-model="reviewContent" 
              placeholder="请输入您的评价内容..." 
              maxlength="200"
            ></textarea>
          </view>
          
          <view v-else class="bad-review">
            <textarea 
              class="review-textarea" 
              v-model="complaintContent" 
              placeholder="请输入您的投诉内容..." 
              maxlength="200"
            ></textarea>
          </view>
        </view>
        
        <view class="review-footer">
          <button class="cancel-btn" @click="closeReviewDialog">取消</button>
          <button class="submit-btn" @click="submitReviewOrComplaint">提交</button>
        </view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
import { getPassengerOrders, confirmOrder, cancelOrder, submitReview, submitComplaint } from '@/common/api.js';

export default {
  components: {
    uniPopup: () => import('@dcloudio/uni-ui/lib/uni-popup/uni-popup')
  },
  data() {
    return {
      orders: [],
      loading: true,
      userInfo: null,
      // 评价相关数据
      currentOrder: null,
      reviewType: 'good', // 'good' 或 'bad'
      rating: 5, // 默认5星
      reviewContent: '',
      complaintContent: ''
    }
  },
  onShow() {
    this.userInfo = uni.getStorageSync('userInfo');
    if (this.userInfo) {
      this.loadOrders();
    } else {
      uni.showToast({ title: '请先登录', icon: 'none' });
      setTimeout(() => {
        uni.navigateTo({ url: '/pages/login/login' });
      }, 1500);
    }
  },
  methods: {
    async loadOrders() {
      this.loading = true;
      try {
        const res = await getPassengerOrders(this.userInfo.id);
        console.log('订单列表:', res); // 调试输出
        
        const rawOrders = Array.isArray(res) ? res : (res.data || []);
        if (Array.isArray(rawOrders)) {
          this.orders = rawOrders.map(order => ({
            ...order,
            // Ensure orderStatus is an integer
            orderStatus: (order.orderStatus !== undefined && order.orderStatus !== null && order.orderStatus !== '')
                          ? parseInt(order.orderStatus, 10)
                          : order.orderStatus
          }));
        } else {
          this.orders = []; // Handle cases where rawOrders is not an array or is null
        }
        
        console.log('Processed orders data for debugging:', JSON.stringify(this.orders));
      } catch (e) {
        console.error('加载订单失败', e);
        uni.showToast({ title: '加载订单失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    },
    shouldShowReviewButton(order) {
      if (!order) return false;
      const status = order.orderStatus;
      console.log(`检查订单ID ${order.id} 的评价按钮: status = ${status}, typeof status = ${typeof status}`);
      const result = status === 1 || status === 2;
      console.log(`订单ID ${order.id} 的评价按钮显示结果: ${result}`);
      return result;
    },
    async confirmOrder(orderId) {
      try {
        await confirmOrder(orderId);
        uni.showToast({ title: '确认成功', icon: 'success' });
        this.loadOrders(); // 重新加载订单列表
      } catch (e) {
        uni.showToast({ title: '确认失败', icon: 'none' });
      }
    },
    async cancelOrder(orderId) {
      uni.showModal({
        title: '提示',
        content: '确定要取消该订单吗？',
        success: async (res) => {
          if (res.confirm) {
            try {
              await cancelOrder(orderId);
              uni.showToast({ title: '取消成功', icon: 'success' });
              this.loadOrders(); // 重新加载订单列表
            } catch (e) {
              uni.showToast({ title: '取消失败', icon: 'none' });
            }
          }
        }
      });
    },
    // 打开评价弹窗
    openReviewDialog(order) {
      this.currentOrder = order;
      this.reviewType = 'good';
      this.rating = 5;
      this.reviewContent = '';
      this.complaintContent = '';
      this.$refs.reviewPopup.open();
    },
    // 关闭评价弹窗
    closeReviewDialog() {
      this.$refs.reviewPopup.close();
    },
    // 提交评价或投诉
    async submitReviewOrComplaint() {
      if (!this.currentOrder) return;
      
      try {
        if (this.reviewType === 'good') {
          // 提交好评
          if (!this.reviewContent.trim()) {
            uni.showToast({ title: '请输入评价内容', icon: 'none' });
            return;
          }
          
          const reviewData = {
            orderId: this.currentOrder.id,
            reviewerId: this.userInfo.id,
            revieweeId: this.currentOrder.trip ? this.currentOrder.trip.driverId : null,
            rating: this.rating,
            content: this.reviewContent
          };
          
          await submitReview(reviewData);
          uni.showToast({ title: '评价成功', icon: 'success' });
        } else {
          // 提交投诉
          if (!this.complaintContent.trim()) {
            uni.showToast({ title: '请输入投诉内容', icon: 'none' });
            return;
          }
          
          const complaintData = {
            orderId: this.currentOrder.id,
            complainantId: this.userInfo.id,
            content: this.complaintContent
          };
          
          await submitComplaint(complaintData);
          uni.showToast({ title: '投诉已提交', icon: 'success' });
        }
        
        this.closeReviewDialog();
        this.loadOrders(); // 刷新订单列表
      } catch (e) {
        console.error('提交失败', e);
        uni.showToast({ title: '提交失败，请稍后再试', icon: 'none' });
      }
    },
    orderStatusText(status) {
      switch(status) {
        case 0: return '待确认';
        case 1: return '已确认';
        case 2: return '已完成';
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
    getOrderStatusClass(status) {
      switch(status) {
        case 0: return 'status-pending';
        case 1: return 'status-confirmed';
        case 2: return 'status-completed';
        case 3: return 'status-canceled';
        default: return '';
      }
    },
    formatDateTime(dateStr) {
      if (!dateStr) return '未知';
      try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return '时间格式错误';
        return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
      } catch (e) {
        console.error('日期格式化错误', e);
        return '时间格式错误';
      }
    },
    goToChat(order) {
      const driverId = order.trip ? order.trip.driverId : null;
      if (!driverId) {
        uni.showToast({ title: '无法获取司机信息', icon: 'none' });
        return;
      }
      const chatParams = {
        orderId: order.id,
        receiverId: driverId
      };
      uni.navigateTo({
        url: `/pages/chat/chat?params=${encodeURIComponent(JSON.stringify(chatParams))}`
      });
    }
  }
}
</script>

<style>
.my-orders-container {
  padding: 30rpx;
  background: #f8f9fa;
  min-height: 100vh;
}

.header {
  margin-bottom: 30rpx;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
}

.loading {
  text-align: center;
  margin-top: 100rpx;
  color: #999;
}

.empty {
  text-align: center;
  margin-top: 100rpx;
  color: #999;
  font-size: 28rpx;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.order-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
  padding-bottom: 16rpx;
  border-bottom: 1px solid #eee;
}

.order-id {
  font-size: 26rpx;
  color: #666;
}

.order-status {
  font-size: 26rpx;
  font-weight: bold;
}

.status-pending {
  color: #ff9800;
}

.status-confirmed {
  color: #4caf50;
}

.status-completed {
  color: #2196f3;
}

.status-canceled {
  color: #f44336;
}

.trip-info {
  background: #f9f9f9;
  padding: 16rpx;
  margin: 16rpx 0;
  border-radius: 8rpx;
}

.trip-route {
  display: flex;
  align-items: center;
  margin-bottom: 10rpx;
}

.no-trip-info {
  color: #999;
  font-style: italic;
  font-size: 24rpx;
}

.trip-point {
  font-weight: bold;
  color: #007aff;
}

.trip-arrow {
  margin: 0 10rpx;
  color: #aaa;
}

.departure-time {
  display: flex;
  margin: 10rpx 0;
}

.departure-time .label {
  color: #666;
  margin-right: 10rpx;
}

.departure-time .value {
  color: #333;
  font-weight: bold;
}

.passenger-info {
  background: #f0f7ff;
  padding: 12rpx 16rpx;
  margin: 16rpx 0;
  border-radius: 8rpx;
  font-size: 26rpx;
  color: #333;
}

.order-details {
  display: flex;
  flex-direction: column;
  font-size: 26rpx;
  color: #666;
  gap: 8rpx;
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px; /* 按钮间距 */
  margin-top: 10px;
}

.confirm-btn {
  background: linear-gradient(90deg, #007aff 0%, #00c6ff 100%);
  color: #fff;
  border-radius: 30rpx;
  font-size: 26rpx;
  padding: 8rpx 24rpx;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
  border-radius: 30rpx;
  font-size: 26rpx;
  padding: 8rpx 24rpx;
}

.chat-btn {
  background-color: #007aff;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.review-btn {
  background: linear-gradient(90deg, #ff9500 0%, #ff5e3a 100%);
  color: #fff;
  border-radius: 30rpx;
  font-size: 26rpx;
  padding: 8rpx 24rpx;
}

/* 评价弹窗样式 */
.review-popup {
  width: 600rpx;
  background: #fff;
  border-radius: 20rpx;
  overflow: hidden;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx;
  border-bottom: 1px solid #eee;
}

.review-title {
  font-size: 32rpx;
  font-weight: bold;
}

.review-close {
  font-size: 40rpx;
  color: #999;
}

.review-tabs {
  display: flex;
  border-bottom: 1px solid #eee;
}

.review-tab {
  flex: 1;
  text-align: center;
  padding: 20rpx 0;
  font-size: 28rpx;
  color: #666;
}

.review-tab.active {
  color: #007aff;
  font-weight: bold;
  position: relative;
}

.review-tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 25%;
  width: 50%;
  height: 4rpx;
  background: #007aff;
}

.review-content {
  padding: 30rpx;
}

.rating-section {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.rating-label {
  font-size: 28rpx;
  color: #333;
  margin-right: 20rpx;
}

.rating-stars {
  display: flex;
}

.star {
  font-size: 40rpx;
  color: #ddd;
  margin-right: 10rpx;
}

.star.active {
  color: #ff9800;
}

.review-textarea {
  width: 100%;
  height: 200rpx;
  border: 1px solid #eee;
  border-radius: 10rpx;
  padding: 16rpx;
  font-size: 28rpx;
  color: #333;
  box-sizing: border-box;
}

.review-footer {
  display: flex;
  justify-content: flex-end;
  padding: 24rpx;
  border-top: 1px solid #eee;
  gap: 20rpx;
}

.submit-btn {
  background: #007aff;
  color: #fff;
  border-radius: 30rpx;
  font-size: 28rpx;
  padding: 10rpx 40rpx;
}
</style> 