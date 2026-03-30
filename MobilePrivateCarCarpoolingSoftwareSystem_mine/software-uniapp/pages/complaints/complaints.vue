<template>
  <view class="complaints-container">
    <view class="header">
      <text class="title">投诉与建议</text>
    </view>
    
    <!-- 切换标签 -->
    <view class="tabs">
      <view 
        :class="['tab', activeTab === 'list' ? 'active' : '']" 
        @click="activeTab = 'list'"
      >我的投诉列表</view>
      <view 
        :class="['tab', activeTab === 'add' ? 'active' : '']" 
        @click="activeTab = 'add'"
      >提交新投诉</view>
    </view>

    <!-- 投诉列表 -->
    <view class="complaints-list" v-if="activeTab === 'list'">
      <view v-if="loading" class="loading">加载中...</view>
      <view v-else-if="!complaints || complaints.length === 0" class="empty">
        <text>暂无投诉记录</text>
      </view>
      <view v-else class="list">
        <view v-for="(complaint, index) in complaints" :key="index" class="complaint-card">
          <view class="complaint-header">
            <text class="complaint-id">投诉编号: {{ complaint && complaint.id || '未知' }}</text>
            <text :class="['status', complaint && complaint.status === 0 ? 'pending' : 'processed']">
              {{ complaint && complaint.status === 0 ? '待处理' : '已处理' }}
            </text>
          </view>
          <view class="order-info">
            <text class="label">相关订单:</text>
            <text class="value">{{ complaint && complaint.orderId || '未知' }}</text>
          </view>
          <view class="trip-info" v-if="complaint && complaint.startLocation || complaint && complaint.endLocation">
            <text class="label">行程:</text>
            <text class="value">{{ complaint && complaint.startLocation || '未知' }} → {{ complaint && complaint.endLocation || '未知' }}</text>
            <text v-if="complaint && complaint.departureTime" class="departure-time">
              出发时间: {{ formatDateTime(complaint.departureTime) }}
            </text>
          </view>
          <view class="complaint-content">
            <text class="content-label">投诉内容:</text>
            <text class="content-value">{{ complaint && complaint.content || '无内容' }}</text>
          </view>
          <view class="complaint-footer">
            <text class="complainant" v-if="complaint && complaint.complainantName">投诉人: {{ complaint.complainantName }}</text>
            <text class="complaint-time">提交时间: {{ formatDateTime(complaint && complaint.createTime) }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 提交新投诉 -->
    <view class="add-complaint" v-if="activeTab === 'add'">
      <view class="form-item">
        <text class="label">选择订单:</text>
        <picker class="picker" 
          :value="selectedOrderIndex" 
          :range="orderOptions" 
          range-key="text"
          @change="handleOrderSelect"
        >
          <view class="picker-value">
            {{ selectedOrderIndex > -1 ? orderOptions[selectedOrderIndex].text : '请选择订单' }}
          </view>
        </picker>
      </view>
      
      <view class="form-item content-area">
        <text class="label">投诉内容:</text>
        <textarea 
          class="content-input" 
          v-model="newComplaint.content"
          placeholder="请详细描述您的问题或建议..."
          maxlength="500"
        ></textarea>
        <text class="char-count">{{ newComplaint.content.length }}/500</text>
      </view>
      
      <button class="submit-btn" 
        :disabled="!isFormValid || submitting"
        @click="submitComplaint"
      >
        {{ submitting ? '提交中...' : '提交投诉' }}
      </button>
    </view>
  </view>
</template>

<script>
import { getUserComplaints, submitComplaint, getConfirmPassengerOrders } from '@/common/api.js';

export default {
  data() {
    return {
      activeTab: 'list', // 'list' 或 'add'
      userInfo: null,
      complaints: [],
      loading: true,
      
      // 新投诉
      newComplaint: {
        orderId: null,
        complainantId: null,
        content: ''
      },
      
      // 订单选择
      orders: [],
      selectedOrderIndex: -1,
      
      // 提交状态
      submitting: false
    }
  },
  
  computed: {
    // 订单选择选项
    orderOptions() {
      return this.orders.map(order => {
        const tripInfo = order.trip 
          ? `${order.trip.startLocation} → ${order.trip.endLocation}` 
          : '未知行程';
        return {
          id: order.id,
          text: `订单 #${order.id} (${tripInfo})`
        };
      });
    },
    
    // 表单是否有效
    isFormValid() {
      return this.newComplaint.orderId && 
        this.newComplaint.complainantId && 
        this.newComplaint.content.trim().length > 0;
    }
  },
  
  onLoad() {
    console.log('complaints页面加载');
    this.userInfo = uni.getStorageSync('userInfo');
    if (this.userInfo) {
      this.loadComplaints();
      this.loadOrders();
      this.newComplaint.complainantId = this.userInfo.id;
    } else {
      uni.showToast({ title: '请先登录', icon: 'none' });
      setTimeout(() => {
        uni.navigateTo({ url: '/pages/login/login' });
      }, 1500);
    }
  },
  
  onShow() {
    console.log('complaints页面显示');
    this.userInfo = uni.getStorageSync('userInfo');
    if (this.userInfo) {
      this.loadComplaints();
      this.loadOrders();
      this.newComplaint.complainantId = this.userInfo.id;
      
      // 确保激活的是列表标签
      console.log('设置activeTab为list');
      this.activeTab = 'list';
    } else {
      uni.showToast({ title: '请先登录', icon: 'none' });
      setTimeout(() => {
        uni.navigateTo({ url: '/pages/login/login' });
      }, 1500);
    }
  },
  
  methods: {
    // 加载投诉列表
    async loadComplaints() {
      this.loading = true;
      try {
        const response = await getUserComplaints(this.userInfo.id);
        console.log('投诉列表原始响应:', response);
        
        // 直接处理响应，不做过多判断
        if (Array.isArray(response)) {
          this.complaints = response;
        } else if (typeof response === 'object' && response !== null) {
          // 处理可能的嵌套响应结构
          if (Array.isArray(response.data)) {
            this.complaints = response.data;
          } else if (response.data) {
            this.complaints = [response.data];
          } else {
            this.complaints = [response]; // 当返回单个对象时
          }
        } else {
          this.complaints = [];
        }
        
        // 添加调试信息
        console.log('complaints数组长度:', this.complaints.length);
        console.log('处理后的投诉数据:', JSON.stringify(this.complaints));
        console.log('当前activeTab:', this.activeTab);
        
      } catch (error) {
        console.error('加载投诉失败', error);
        uni.showToast({ title: '加载投诉失败', icon: 'none' });
      } finally {
        this.loading = false;
      }
    },
    
    // 加载订单列表
    async loadOrders() {
      try {
        const response = await getConfirmPassengerOrders(this.userInfo.id);
        console.log('订单列表:', response);
        // 确保我们有一个数组
        this.orders = Array.isArray(response) ? response : (Array.isArray(response.data) ? response.data : []);
      } catch (error) {
        console.error('加载订单失败', error);
        uni.showToast({ title: '加载订单失败', icon: 'none' });
      }
    },
    
    // 处理订单选择
    handleOrderSelect(e) {
      this.selectedOrderIndex = e.detail.value;
      if (this.selectedOrderIndex >= 0 && this.selectedOrderIndex < this.orders.length) {
        this.newComplaint.orderId = this.orders[this.selectedOrderIndex].id;
      }
    },
    
    // 提交投诉
    async submitComplaint() {
      if (!this.isFormValid) {
        uni.showToast({ title: '请填写完整信息', icon: 'none' });
        return;
      }
      
      this.submitting = true;
      try {
        const response = await submitComplaint(this.newComplaint);
        console.log('投诉提交结果:', response);
        
        uni.showToast({ title: '投诉提交成功', icon: 'success' });
        
        // 重置表单并切换到列表页
        this.newComplaint.orderId = null;
        this.newComplaint.content = '';
        this.selectedOrderIndex = -1;
        this.activeTab = 'list';
        
        // 重新加载投诉列表
        this.loadComplaints();
      } catch (error) {
        console.error('提交投诉失败', error);
        uni.showToast({ title: '提交投诉失败', icon: 'none' });
      } finally {
        this.submitting = false;
      }
    },
    
    // 格式化日期时间
    formatDateTime(dateStr) {
      if (!dateStr) return '未知时间';
      
      try {
        let date;
        if (typeof dateStr === 'number') {
          date = new Date(dateStr);
        } else if (typeof dateStr === 'string') {
          date = new Date(dateStr);
        } else {
          date = dateStr; // 假设已经是Date对象
        }
        
        // 检查是否是有效日期
        if (isNaN(date.getTime())) {
          return '无效日期';
        }
        
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
      } catch (e) {
        console.error('日期格式化错误', e);
        return String(dateStr) || '未知时间';
      }
    }
  }
}
</script>

<style>
.complaints-container {
  padding: 30rpx;
}

.header {
  margin-bottom: 30rpx;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
}

.tabs {
  display: flex;
  margin-bottom: 30rpx;
  background-color: #f5f5f5;
  border-radius: 12rpx;
  overflow: hidden;
}

.tab {
  flex: 1;
  text-align: center;
  padding: 20rpx 0;
  font-size: 28rpx;
  color: #666;
  transition: all 0.3s;
}

.tab.active {
  background-color: #007AFF;
  color: #fff;
  font-weight: bold;
}

.loading, .empty {
  text-align: center;
  padding: 40rpx 0;
  color: #999;
}

.complaint-card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
}

.complaint-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16rpx;
  border-bottom: 1px solid #eee;
  padding-bottom: 16rpx;
}

.complaint-id {
  font-size: 26rpx;
  color: #333;
  font-weight: bold;
}

.status {
  font-size: 24rpx;
  border-radius: 30rpx;
  padding: 4rpx 16rpx;
}

.status.pending {
  background-color: #FFF3E0;
  color: #FF9800;
}

.status.processed {
  background-color: #E8F5E9;
  color: #4CAF50;
}

.order-info {
  margin-bottom: 16rpx;
}

.label {
  font-size: 26rpx;
  color: #666;
  margin-right: 10rpx;
}

.value {
  font-size: 26rpx;
  color: #333;
}

.trip-info {
  margin-bottom: 16rpx;
  background-color: #f5f8fa;
  padding: 12rpx;
  border-radius: 8rpx;
}

.departure-time {
  display: block;
  font-size: 24rpx;
  color: #666;
  margin-top: 8rpx;
}

.complaint-content {
  background-color: #f9f9f9;
  padding: 16rpx;
  border-radius: 8rpx;
  margin-bottom: 16rpx;
}

.content-label {
  font-size: 26rpx;
  color: #666;
  display: block;
  margin-bottom: 8rpx;
}

.content-value {
  font-size: 28rpx;
  color: #333;
  word-break: break-all;
}

.complaint-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16rpx;
}

.complainant {
  font-size: 24rpx;
  color: #666;
}

.complaint-time {
  font-size: 24rpx;
  color: #999;
  text-align: right;
}

/* 添加投诉表单样式 */
.form-item {
  margin-bottom: 30rpx;
}

.picker {
  border: 1px solid #ddd;
  border-radius: 8rpx;
  padding: 20rpx;
  margin-top: 10rpx;
  background-color: #fff;
}

.picker-value {
  font-size: 28rpx;
  color: #333;
}

.content-area {
  position: relative;
}

.content-input {
  margin-top: 10rpx;
  border: 1px solid #ddd;
  border-radius: 8rpx;
  padding: 20rpx;
  width: 100%;
  box-sizing: border-box;
  height: 300rpx;
  font-size: 28rpx;
}

.char-count {
  position: absolute;
  right: 10rpx;
  bottom: 10rpx;
  font-size: 24rpx;
  color: #999;
}

.submit-btn {
  background-color: #007AFF;
  color: #fff;
  margin-top: 40rpx;
}

.submit-btn[disabled] {
  background-color: #ccc;
  color: #fff;
}
</style> 