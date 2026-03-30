<template>
  <view class="trip-container">
    <view class="page-header">
      <text class="title">行程管理</text>
    </view>

    <view v-if="loading" class="loading">加载中...</view>
    
    <view v-if="trips.length === 0 && !loading" class="empty-tips">
      暂无行程记录
    </view>
    
    <!-- 行程列表 -->
    <view v-if="!loading && trips.length > 0" class="trip-list">
      <view class="trip-item" v-for="(item, index) in trips" :key="item.id">
        <view class="trip-header">
          <text class="trip-id">行程ID: {{item.id}}</text>
          <text :class="['status', getStatusClass(item.status)]">{{getStatusText(item.status)}}</text>
        </view>
        
        <view class="trip-content">
          <view class="route">
            <text class="from">{{item.startLocation}}</text>
            <text class="arrow">→</text>
            <text class="to">{{item.endLocation}}</text>
          </view>
          
          <view class="info-row">
            <view class="info-item">
              <text class="label">出发时间:</text>
              <text class="value">{{formatDate(item.departureTime)}}</text>
            </view>
            <view class="info-item">
              <text class="label">价格:</text>
              <text class="value price">¥{{item.price}}</text>
            </view>
          </view>
          
          <view class="info-row">
            <view class="info-item">
              <text class="label">车主ID:</text>
              <text class="value">{{item.driverId}}</text>
            </view>
            <view class="info-item">
              <text class="label">座位数:</text>
              <text class="value">{{item.seatAvailable}}</text>
            </view>
          </view>
        </view>
        
        <view class="trip-footer">
          <button class="btn btn-detail" @click="viewDetail(item)">查看详情</button>
          <button class="btn btn-delete" @click="handleDelete(item.id)">删除行程</button>
        </view>
      </view>
    </view>
    
    <!-- 详情弹窗 -->
    <view class="modal-overlay" v-if="showDetailModal" @click="closeDetailModal"></view>
    <view class="detail-modal" v-if="showDetailModal">
      <view class="modal-header">
        <text class="modal-title">行程详情</text>
        <text class="close-btn" @click="closeDetailModal">×</text>
      </view>
      
      <scroll-view scroll-y class="modal-body">
        <block v-if="currentTrip">
          <view class="modal-section">
            <view class="modal-section-title">基本信息</view>
            <view class="modal-item">
              <text class="modal-label">行程ID:</text>
              <text class="modal-value">{{currentTrip.id}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">状态:</text>
              <text class="modal-value status-tag" :class="getStatusClass(currentTrip.status)">
                {{getStatusText(currentTrip.status)}}
              </text>
            </view>
            <view class="modal-item">
              <text class="modal-label">发布时间:</text>
              <text class="modal-value">{{formatDate(currentTrip.createTime)}}</text>
            </view>
          </view>
          
          <view class="modal-section">
            <view class="modal-section-title">行程路线</view>
            <view class="modal-item">
              <text class="modal-label">起点:</text>
              <text class="modal-value">{{currentTrip.startLocation}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">终点:</text>
              <text class="modal-value">{{currentTrip.endLocation}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">出发时间:</text>
              <text class="modal-value">{{formatDate(currentTrip.departureTime)}}</text>
            </view>
            <view class="modal-item" v-if="currentTrip.viaPoints">
              <text class="modal-label">途经点:</text>
              <text class="modal-value">{{currentTrip.viaPoints}}</text>
            </view>
          </view>
          
          <view class="modal-section">
            <view class="modal-section-title">价格与座位</view>
            <view class="modal-item">
              <text class="modal-label">价格:</text>
              <text class="modal-value">¥{{currentTrip.price}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">可用座位:</text>
              <text class="modal-value">{{currentTrip.seatAvailable}}</text>
            </view>
          </view>
          
          <view class="modal-section">
            <view class="modal-section-title">车主与车辆信息</view>
            <view class="modal-item">
              <text class="modal-label">车主ID:</text>
              <text class="modal-value">{{currentTrip.driverId}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">车辆ID:</text>
              <text class="modal-value">{{currentTrip.carId}}</text>
            </view>
            <view v-if="currentTrip.carInfo" class="car-info">
              <view class="modal-item" v-if="currentTrip.carInfo.plateNumber">
                <text class="modal-label">车牌号:</text>
                <text class="modal-value">{{currentTrip.carInfo.plateNumber}}</text>
              </view>
              <view class="modal-item" v-if="currentTrip.carInfo.brand">
                <text class="modal-label">品牌型号:</text>
                <text class="modal-value">{{currentTrip.carInfo.brand}} {{currentTrip.carInfo.model}}</text>
              </view>
              <view class="modal-item" v-if="currentTrip.carInfo.color">
                <text class="modal-label">颜色:</text>
                <text class="modal-value">{{currentTrip.carInfo.color}}</text>
              </view>
            </view>
          </view>
          
          <view class="modal-section" v-if="currentTrip.startLat && currentTrip.startLng">
            <view class="modal-section-title">位置信息</view>
            <view class="modal-item">
              <text class="modal-label">起点坐标:</text>
              <text class="modal-value">经度: {{currentTrip.startLng}}, 纬度: {{currentTrip.startLat}}</text>
            </view>
            <view class="modal-item">
              <text class="modal-label">终点坐标:</text>
              <text class="modal-value">经度: {{currentTrip.endLng}}, 纬度: {{currentTrip.endLat}}</text>
            </view>
          </view>
        </block>
      </scroll-view>
      
      <view class="modal-footer">
        <button class="btn-delete btn-modal" @click="handleDeleteFromModal">删除行程</button>
        <button class="btn-close btn-modal" @click="closeDetailModal">关闭</button>
      </view>
    </view>
  </view>
</template>

<script>
import { getAllTrips, adminDeleteTrip, getTripById } from '@/common/api.js';

export default {
  data() {
    return {
      loading: true,
      trips: [],
      showDetailModal: false,
      currentTrip: null
    };
  },
  onLoad() {
    this.fetchTrips();
  },
  methods: {
    // 获取所有行程
    async fetchTrips() {
      this.loading = true;
      try {
        const res = await getAllTrips();
        if (res && res.code === 200) {
          this.trips = res.data || [];
        } else {
          uni.showToast({ 
            title: res.msg || '获取行程列表失败', 
            icon: 'none' 
          });
        }
      } catch (error) {
        console.error('获取行程列表出错:', error);
        uni.showToast({ 
          title: '获取行程列表失败，请检查网络', 
          icon: 'none' 
        });
      } finally {
        this.loading = false;
      }
    },
    
    // 查看行程详情
    async viewDetail(trip) {
      // 先显示简单信息
      this.currentTrip = trip;
      this.showDetailModal = true;
      
      // 获取详细信息
      try {
        const res = await getTripById(trip.id);
        if (res && res.code === 200 && res.data) {
          this.currentTrip = res.data;
        }
      } catch (error) {
        console.error('获取行程详情失败:', error);
      }
    },
    
    // 关闭详情弹窗
    closeDetailModal() {
      this.showDetailModal = false;
      this.currentTrip = null;
    },
    
    // 删除行程
    handleDelete(tripId) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除该行程吗？删除后无法恢复！',
        success: (res) => {
          if (res.confirm) {
            this.deleteTrip(tripId);
          }
        }
      });
    },
    
    // 从详情弹窗中删除行程
    handleDeleteFromModal() {
      if (!this.currentTrip) return;
      
      uni.showModal({
        title: '确认删除',
        content: '确定要删除该行程吗？删除后无法恢复！',
        success: (res) => {
          if (res.confirm) {
            this.deleteTrip(this.currentTrip.id);
            this.closeDetailModal();
          }
        }
      });
    },
    
    // 执行删除操作
    async deleteTrip(tripId) {
      try {
        uni.showLoading({ title: '删除中...' });
        const res = await adminDeleteTrip(tripId);
        
        if (res && res.code === 200) {
          uni.showToast({
            title: '删除成功',
            icon: 'success'
          });
          // 从列表中移除该行程
          this.trips = this.trips.filter(trip => trip.id !== tripId);
        } else {
          uni.showToast({
            title: res.msg || '删除失败',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('删除行程失败:', error);
        uni.showToast({
          title: '删除失败，请重试',
          icon: 'none'
        });
      } finally {
        uni.hideLoading();
      }
    },
    
    // 格式化日期
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    },
    
    // 获取状态文本
    getStatusText(status) {
      switch(status) {
        case 1: return '发布中';
        case 2: return '已满员';
        case 3: return '已结束';
        case 4: return '已取消';
        default: return '未知状态';
      }
    },
    
    // 获取状态样式类
    getStatusClass(status) {
      switch(status) {
        case 1: return 'status-active';
        case 2: return 'status-full';
        case 3: return 'status-ended';
        case 4: return 'status-canceled';
        default: return '';
      }
    }
  }
};
</script>

<style>
.trip-container {
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

.trip-list {
  margin-top: 20rpx;
}

.trip-item {
  background-color: #fff;
  border-radius: 12rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.05);
  overflow: hidden;
}

.trip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 24rpx;
  background-color: #f9f9f9;
  border-bottom: 1px solid #eee;
}

.trip-id {
  font-size: 26rpx;
  color: #666;
}

.status {
  font-size: 24rpx;
  padding: 4rpx 12rpx;
  border-radius: 6rpx;
}

.status-active {
  background-color: #e8f5e9;
  color: #4caf50;
}

.status-full {
  background-color: #e3f2fd;
  color: #2196f3;
}

.status-ended {
  background-color: #f5f5f5;
  color: #9e9e9e;
}

.status-canceled {
  background-color: #ffebee;
  color: #f44336;
}

.trip-content {
  padding: 20rpx 24rpx;
}

.route {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
  font-size: 30rpx;
}

.from, .to {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #333;
}

.arrow {
  margin: 0 20rpx;
  color: #2196f3;
  font-weight: bold;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12rpx;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  margin-right: 20rpx;
  font-size: 26rpx;
}

.label {
  color: #666;
  margin-right: 8rpx;
}

.value {
  color: #333;
}

.price {
  color: #f44336;
  font-weight: bold;
}

.trip-footer {
  display: flex;
  justify-content: flex-end;
  padding: 16rpx 24rpx;
  border-top: 1px solid #eee;
}

.btn {
  font-size: 26rpx;
  padding: 8rpx 24rpx;
  border-radius: 8rpx;
  border: none;
  margin-left: 16rpx;
}

.btn-detail {
  background-color: #e3f2fd;
  color: #2196f3;
}

.btn-delete {
  background-color: #ffebee;
  color: #f44336;
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
  max-width: 650rpx;
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

.car-info {
  background-color: #f9f9f9;
  padding: 16rpx;
  border-radius: 8rpx;
  margin-top: 10rpx;
}

.modal-footer {
  padding: 20rpx;
  border-top: 1rpx solid #eee;
  display: flex;
  justify-content: flex-end;
}

.btn-modal {
  margin-left: 16rpx;
  font-size: 28rpx;
  padding: 8rpx 24rpx;
  border-radius: 8rpx;
  border: none;
}

.btn-close {
  background-color: #f5f5f5;
  color: #333;
}

.btn-delete {
  background-color: #ffebee;
  color: #f44336;
}
</style> 