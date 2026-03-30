<template>
  <view class="complaint-container">
    <view class="page-header">
      <text class="title">投诉处理</text>
    </view>

    <view v-if="loading" class="loading">加载中...</view>
    
    <view v-if="complaints.length === 0 && !loading" class="empty-tips">
      暂无投诉记录
    </view>

    <view v-if="!loading" class="complaint-list">
      <view v-for="(item, index) in complaints" :key="item.id" class="complaint-item">
        <view class="complaint-header">
          <text class="order-id">订单ID: {{item.orderId}}</text>
          <text :class="['status', item.status === 0 ? 'pending' : 'processed']">
            {{item.status === 0 ? '待处理' : '已处理'}}
          </text>
        </view>
        
        <view class="complaint-body">
          <view class="content-row">
            <text class="label">投诉内容:</text>
            <text class="content">{{item.content}}</text>
          </view>
          <view class="info-row">
            <text class="label">投诉人ID:</text>
            <text class="value">{{item.complainantId}}</text>
            <text class="label ml-20">投诉时间:</text>
            <text class="value">{{formatDate(item.createTime)}}</text>
          </view>
          
          <view class="user-info" v-if="item.complainantName">
            <text class="label">投诉人:</text>
            <text class="value">{{item.complainantName}} ({{item.complainantPhone}})</text>
          </view>
          
          <view class="order-detail" v-if="item.orderInfo">
            <text class="detail-label">订单信息:</text>
            <text class="detail-value">{{item.orderInfo}}</text>
          </view>
        </view>
        
        <view class="complaint-footer">
          <button 
            v-if="item.status === 0" 
            class="process-btn" 
            @click="handleProcess(item.id)"
          >标记为已处理</button>
          <button 
            v-else 
            class="view-btn" 
            @click="viewDetail(item)"
          >查看详情</button>
        </view>
      </view>
    </view>
    
    <!-- 详情弹窗 -->
    <view class="modal-overlay" v-if="showDetailModal" @click="closeDetailModal"></view>
    <view class="detail-modal" v-if="showDetailModal">
      <view class="modal-header">
        <text class="modal-title">投诉详情</text>
        <text class="close-btn" @click="closeDetailModal">×</text>
      </view>
      
      <scroll-view scroll-y class="modal-body">
        <block v-if="currentComplaint">
          <view class="modal-section">
            <view class="modal-section-title">基本信息</view>
            <view class="modal-item">
              <text class="modal-label">投诉ID:</text>
              <text class="modal-value">{{currentComplaint.id}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">订单ID:</text>
              <text class="modal-value">{{currentComplaint.orderId}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">状态:</text>
              <text class="modal-value status-tag" 
                    :class="currentComplaint.status === 0 ? 'pending' : 'processed'">
                {{currentComplaint.status === 0 ? '待处理' : '已处理'}}
              </text>
            </view>
            <view class="modal-item">
              <text class="modal-label">投诉时间:</text>
              <text class="modal-value">{{formatDate(currentComplaint.createTime)}}</text>
            </view>
          </view>
          
          <view class="modal-section">
            <view class="modal-section-title">投诉内容</view>
            <view class="modal-content-box">
              {{currentComplaint.content}}
            </view>
          </view>
          
          <view class="modal-section" v-if="currentComplaint.complainantName">
            <view class="modal-section-title">投诉人信息</view>
            <view class="modal-item">
              <text class="modal-label">用户ID:</text>
              <text class="modal-value">{{currentComplaint.complainantId}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">用户名:</text>
              <text class="modal-value">{{currentComplaint.complainantName}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">联系电话:</text>
              <text class="modal-value">{{currentComplaint.complainantPhone}}</text>
            </view>
          </view>
          
          <view class="modal-section" v-if="currentComplaint.orderInfo">
            <view class="modal-section-title">订单信息</view>
            <view class="modal-content-box">
              {{currentComplaint.orderInfo}}
            </view>
          </view>
        </block>
      </scroll-view>
      
      <view class="modal-footer">
        <button class="modal-close-btn" @click="closeDetailModal">关闭</button>
      </view>
    </view>
  </view>
</template>

<script>
import { getAllComplaints, processComplaint } from '@/common/api.js';

export default {
  data() {
    return {
      loading: true,
      complaints: [],
      showDetailModal: false,
      currentComplaint: null
    };
  },
  onLoad() {
    this.fetchComplaints();
  },
  methods: {
    // 获取所有投诉
    async fetchComplaints() {
      this.loading = true;
      try {
        const res = await getAllComplaints();
        if (res && res.code === 200) {
          this.complaints = res.data || [];
        } else {
          uni.showToast({ 
            title: res.msg || '获取投诉列表失败', 
            icon: 'none' 
          });
        }
      } catch (error) {
        console.error('获取投诉列表出错:', error);
        uni.showToast({ 
          title: '获取投诉列表失败，请检查网络', 
          icon: 'none' 
        });
      } finally {
        this.loading = false;
      }
    },
    
    // 处理投诉
    async handleProcess(complaintId) {
      uni.showModal({
        title: '确认',
        content: '确定将此投诉标记为已处理？',
        success: async (res) => {
          if (res.confirm) {
            try {
              uni.showLoading({ title: '处理中...' });
              const res = await processComplaint(complaintId);
              
              if (res && res.code === 200) {
                uni.showToast({ 
                  title: '处理成功', 
                  icon: 'success' 
                });
                // 更新本地数据状态
                const index = this.complaints.findIndex(item => item.id === complaintId);
                if (index !== -1) {
                  this.complaints[index].status = 1;
                  // 强制视图更新
                  this.complaints = [...this.complaints];
                }
              } else {
                uni.showToast({ 
                  title: res.msg || '处理失败', 
                  icon: 'none' 
                });
              }
            } catch (error) {
              console.error('处理投诉出错:', error);
              uni.showToast({ 
                title: '处理投诉失败，请重试', 
                icon: 'none' 
              });
            } finally {
              uni.hideLoading();
            }
          }
        }
      });
    },
    
    // 查看详情 - 显示弹窗
    viewDetail(complaint) {
      this.currentComplaint = complaint;
      this.showDetailModal = true;
    },
    
    // 关闭详情弹窗
    closeDetailModal() {
      this.showDetailModal = false;
      this.currentComplaint = null;
    },
    
    // 格式化日期
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    }
  }
};
</script>

<style>
.complaint-container {
  padding: 30rpx;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 30rpx;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
}

.loading, .empty-tips {
  text-align: center;
  color: #999;
  margin-top: 100rpx;
}

.complaint-list {
  margin-top: 20rpx;
}

.complaint-item {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 24rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.05);
}

.complaint-header {
  display: flex;
  justify-content: space-between;
  padding-bottom: 16rpx;
  border-bottom: 1px solid #eee;
  margin-bottom: 16rpx;
}

.order-id {
  font-size: 28rpx;
  color: #333;
}

.status {
  font-size: 24rpx;
  padding: 4rpx 12rpx;
  border-radius: 6rpx;
}

.pending {
  background-color: #ffebee;
  color: #f44336;
}

.processed {
  background-color: #e8f5e9;
  color: #4caf50;
}

.complaint-body {
  padding: 10rpx 0;
}

.content-row {
  margin-bottom: 16rpx;
}

.info-row, .user-info {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  font-size: 26rpx;
  margin-bottom: 12rpx;
}

.ml-20 {
  margin-left: 20rpx;
}

.label {
  color: #666;
  margin-right: 8rpx;
}

.content {
  color: #333;
  word-break: break-all;
}

.value {
  color: #333;
  margin-right: 16rpx;
}

.order-detail {
  margin-top: 16rpx;
  font-size: 26rpx;
  color: #666;
}

.complaint-footer {
  margin-top: 20rpx;
  display: flex;
  justify-content: flex-end;
}

.process-btn, .view-btn {
  font-size: 26rpx;
  padding: 8rpx 24rpx;
  border-radius: 8rpx;
  border: none;
}

.process-btn {
  background-color: #2196f3;
  color: #fff;
}

.view-btn {
  background-color: #f5f5f5;
  color: #666;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.detail-modal {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 600rpx;
  background-color: #fff;
  border-radius: 12rpx;
  overflow: hidden;
  z-index: 1000;
  box-shadow: 0 4rpx 24rpx rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 24rpx;
  border-bottom: 1rpx solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.close-btn {
  font-size: 40rpx;
  color: #999;
  line-height: 1;
  padding: 0 10rpx;
}

.modal-body {
  padding: 24rpx;
  max-height: 60vh;
}

.modal-section {
  margin-bottom: 24rpx;
}

.modal-section-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 12rpx;
  padding-bottom: 8rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.modal-item {
  display: flex;
  margin-bottom: 8rpx;
  font-size: 26rpx;
}

.modal-label {
  color: #666;
  width: 160rpx;
  flex-shrink: 0;
}

.modal-value {
  color: #333;
  flex: 1;
}

.status-tag {
  display: inline-block;
  padding: 4rpx 12rpx;
  border-radius: 4rpx;
  font-size: 24rpx;
}

.modal-content-box {
  background-color: #f9f9f9;
  padding: 16rpx;
  border-radius: 8rpx;
  font-size: 26rpx;
  color: #333;
  word-break: break-all;
}

.modal-footer {
  padding: 20rpx;
  border-top: 1rpx solid #eee;
  display: flex;
  justify-content: center;
}

.modal-close-btn {
  background-color: #f5f5f5;
  color: #333;
  font-size: 28rpx;
  padding: 10rpx 30rpx;
  border-radius: 8rpx;
  border: none;
}
</style> 