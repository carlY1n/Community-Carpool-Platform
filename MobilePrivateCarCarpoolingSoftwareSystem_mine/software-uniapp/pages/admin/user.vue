<template>
  <view class="container">
    <view class="header">用户管理</view>
    <view v-if="loading" class="loading">加载中...</view>
    <view v-else>
      <view v-if="users.length === 0" class="empty">暂无用户</view>
      <view v-else>
        <view class="user-list">
          <view class="user-item" v-for="user in users" :key="user.id">
            <view class="user-info">
              <text class="user-name">{{ user.username }}</text>
              <text class="user-type">（{{ userTypeText(user.userType) }}）</text>
              <text class="user-phone">{{ user.phone }}</text>
            </view>
            <view class="user-actions">
              <button v-if="user.status === 1" class="disable-btn" @click="updateStatus(user, 0)">禁用</button>
              <button v-else class="enable-btn" @click="updateStatus(user, 1)">启用</button>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getAllUsers, updateUserStatus } from '../../common/api.js';

export default {
  data() {
    return {
      users: [],
      loading: false
    }
  },
  onShow() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      this.loading = true;
      getAllUsers().then(res => {
        this.loading = false;
        if (res.code === 200) {
          this.users = res.data;
        } else {
          uni.showToast({ title: res.msg || '获取用户失败', icon: 'none' });
        }
      }).catch(() => {
        this.loading = false;
        uni.showToast({ title: '网络错误', icon: 'none' });
      });
    },
    updateStatus(user, status) {
      uni.showLoading({ title: '操作中...' });
      updateUserStatus(user.id, status).then(res => {
        uni.hideLoading();
        if (res.code === 200) {
          user.status = status;
          uni.showToast({ title: '操作成功', icon: 'success' });
        } else {
          uni.showToast({ title: res.msg || '操作失败', icon: 'none' });
        }
      }).catch(() => {
        uni.hideLoading();
        uni.showToast({ title: '网络错误', icon: 'none' });
      });
    },
    userTypeText(type) {
      switch(type) {
        case 'PASSENGER': return '乘客';
        case 'DRIVER': return '车主';
        case 'ADMIN': return '管理员';
        default: return '未知';
      }
    }
  }
}
</script>

<style>
.container {
  padding: 30rpx;
}
.header {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 30rpx;
}
.loading {
  text-align: center;
  color: #888;
  margin: 40rpx 0;
}
.empty {
  text-align: center;
  color: #aaa;
  margin: 40rpx 0;
}
.user-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}
.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f8f8;
  border-radius: 16rpx;
  padding: 20rpx;
}
.user-info {
  display: flex;
  flex-direction: column;
}
.user-name {
  font-size: 30rpx;
  font-weight: bold;
}
.user-type {
  font-size: 24rpx;
  color: #007AFF;
}
.user-phone {
  font-size: 24rpx;
  color: #888;
}
.user-actions button {
  min-width: 100rpx;
  font-size: 26rpx;
  border-radius: 30rpx;
  padding: 10rpx 20rpx;
}
.disable-btn {
  background: #ff3b30;
  color: #fff;
}
.enable-btn {
  background: #4cd964;
  color: #fff;
}
</style> 