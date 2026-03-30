<template>
  <view class="profile-container">
    <view class="profile-header">
      <text class="title">个人中心</text>
    </view>

    <view v-if="loading" class="loading-text">加载中...</view>

    <view v-if="!loading && userInfo" class="profile-content">
      <!-- 显示用户信息 -->
      <view class="info-section card">
        <text class="section-title">基本信息</text>
        <view class="info-item">
          <text class="label">用户名:</text>
          <text class="value">{{ userInfo.username }}</text>
        </view>
        <view class="info-item">
          <text class="label">手机号:</text>
          <text class="value">{{ userInfo.phone }}</text>
        </view>
        <view class="info-item">
          <text class="label">真实姓名:</text>
          <text class="value">{{ userInfo.realName || '未设置' }}</text>
        </view>
        <view class="info-item">
          <text class="label">身份证号:</text>
          <text class="value">{{ userInfo.idCard || '未设置' }}</text>
        </view>
      </view>

      <!-- 修改基本信息 -->
      <view class="form-section card">
        <text class="section-title">修改基本信息</text>
        <input class="input-field" v-model="profileForm.username" placeholder="新用户名 (可选)" />
        <input class="input-field" v-model="profileForm.realName" placeholder="真实姓名 (可选)" />
        <input class="input-field" v-model="profileForm.idCard" placeholder="身份证号 (可选)" />
        <button class="submit-btn" @click="handleUpdateProfile">保存基本信息</button>
      </view>

      <!-- 修改密码 -->
      <view class="form-section card">
        <text class="section-title">修改密码</text>
        <input class="input-field" type="password" v-model="passwordForm.oldPassword" placeholder="当前密码" />
        <input class="input-field" type="password" v-model="passwordForm.newPassword" placeholder="新密码" />
        <input class="input-field" type="password" v-model="passwordForm.confirmNewPassword" placeholder="确认新密码" />
        <button class="submit-btn" @click="handleUpdatePassword">修改密码</button>
      </view>
    </view>

    <view v-if="!loading && !userInfo" class="empty-text">
      无法加载用户信息，请重新登录。
    </view>
  </view>
</template>

<script>
import { getUserProfile, updateUserProfile, updateUserPassword } from '@/common/api.js';

export default {
  data() {
    return {
      loading: true,
      userInfo: null, // 从本地存储获取的原始用户信息
      profileData: null, // 从API获取的详细用户信息，用于显示
      userId: null,
      profileForm: {
        username: '',
        realName: '',
        idCard: ''
      },
      passwordForm: {
        oldPassword: '',
        newPassword: '',
        confirmNewPassword: ''
      }
    };
  },
  onLoad() {
    const storedUserInfo = uni.getStorageSync('userInfo');
    if (storedUserInfo && storedUserInfo.id) {
      this.userId = storedUserInfo.id;
      this.fetchUserProfile();
    } else {
      this.loading = false;
      uni.showToast({
        title: '请先登录',
        icon: 'none',
        duration: 2000
      });
      setTimeout(() => {
        uni.navigateTo({ url: '/pages/login/login' });
      }, 2000);
    }
  },
  methods: {
    async fetchUserProfile() {
      this.loading = true;
      try {
        const res = await getUserProfile(this.userId);
        if (res && res.code === 200 && res.data) {
          this.userInfo = res.data; // 更新userInfo用于显示
          // 初始化表单预填项 (可选，如果希望预填)
          this.profileForm.username = res.data.username || '';
          this.profileForm.realName = res.data.realName || '';
          this.profileForm.idCard = res.data.idCard || '';
        } else {
          uni.showToast({ title: res.msg || '获取用户信息失败', icon: 'none' });
        }
      } catch (error) {
        console.error("获取用户信息失败:", error);
        // uni.showToast 在 api.js 中已处理
      } finally {
        this.loading = false;
      }
    },
    async handleUpdateProfile() {
      if (!this.profileForm.username && !this.profileForm.realName && !this.profileForm.idCard) {
        uni.showToast({ title: '请输入至少一项要修改的信息', icon: 'none' });
        return;
      }
      const dataToUpdate = {};
      if (this.profileForm.username) dataToUpdate.username = this.profileForm.username;
      if (this.profileForm.realName) dataToUpdate.realName = this.profileForm.realName;
      if (this.profileForm.idCard) dataToUpdate.idCard = this.profileForm.idCard;

      uni.showLoading({ title: '正在保存...' });
      try {
        const res = await updateUserProfile(this.userId, dataToUpdate);
        if (res && res.code === 200) {
          uni.showToast({ title: '基本信息更新成功', icon: 'success' });
          this.fetchUserProfile(); // 重新加载以显示最新信息
          // 清空部分表单，保留用户名预填（如果需要）
          this.profileForm.realName = res.data.realName || '';
          this.profileForm.idCard = res.data.idCard || ''; 
          // 更新本地存储的userInfo中的username (如果修改成功且返回了新的username)
          if (res.data && res.data.username) {
            const storedUserInfo = uni.getStorageSync('userInfo');
            if (storedUserInfo) {
              storedUserInfo.username = res.data.username;
              uni.setStorageSync('userInfo', storedUserInfo);
            }
          }
        } else {
          uni.showToast({ title: res.msg || '更新失败', icon: 'none' });
        }
      } catch (error) {
        console.error("更新基本信息失败:", error);
      } finally {
        uni.hideLoading();
      }
    },
    async handleUpdatePassword() {
      if (!this.passwordForm.oldPassword || !this.passwordForm.newPassword || !this.passwordForm.confirmNewPassword) {
        uni.showToast({ title: '请填写所有密码字段', icon: 'none' });
        return;
      }
      if (this.passwordForm.newPassword !== this.passwordForm.confirmNewPassword) {
        uni.showToast({ title: '新密码与确认密码不一致', icon: 'none' });
        return;
      }
      if (this.passwordForm.newPassword.length < 6) { // 简单示例，实际应有更复杂规则
          uni.showToast({ title: '新密码长度至少为6位', icon: 'none' });
          return;
      }

      uni.showLoading({ title: '正在修改密码...' });
      try {
        const res = await updateUserPassword(this.userId, {
          oldPassword: this.passwordForm.oldPassword,
          newPassword: this.passwordForm.newPassword
        });
        if (res && res.code === 200) {
          uni.showToast({ title: '密码修改成功，请重新登录', icon: 'success', duration: 2000 });
          uni.removeStorageSync('userInfo'); // 清除旧的登录信息
          this.passwordForm = { oldPassword: '', newPassword: '', confirmNewPassword: '' };
          setTimeout(() => {
            uni.reLaunch({ url: '/pages/login/login' });
          }, 2000);
        } else {
          uni.showToast({ title: res.msg || '密码修改失败', icon: 'none' });
        }
      } catch (error) {
        console.error("修改密码失败:", error);
      } finally {
        uni.hideLoading();
      }
    }
  }
};
</script>

<style>
.profile-container {
  padding: 30rpx;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.profile-header {
  margin-bottom: 30rpx;
}

.title {
  font-size: 40rpx;
  font-weight: bold;
  color: #333;
}

.loading-text, .empty-text {
  text-align: center;
  color: #999;
  margin-top: 100rpx;
  font-size: 28rpx;
}

.profile-content { }

.card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
  padding-bottom: 15rpx;
  border-bottom: 1rpx solid #eee;
  display: block;
}

.info-section .info-item {
  display: flex;
  justify-content: space-between;
  padding: 15rpx 0;
  font-size: 28rpx;
}

.info-item .label {
  color: #666;
}

.info-item .value {
  color: #333;
  text-align: right;
}

.form-section .input-field {
  width: 100%;
  height: 80rpx;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  padding: 0 20rpx;
  margin-bottom: 20rpx;
  font-size: 28rpx;
  box-sizing: border-box;
}

.form-section .submit-btn {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  background-color: #007aff;
  color: #fff;
  border-radius: 8rpx;
  font-size: 30rpx;
  text-align: center;
  margin-top: 10rpx;
}
.form-section .submit-btn:active {
    background-color: #0056b3;
}
</style> 