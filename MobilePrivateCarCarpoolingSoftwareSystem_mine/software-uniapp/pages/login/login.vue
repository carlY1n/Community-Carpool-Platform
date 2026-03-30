<template>
	<view class="container">
		<view class="header">
			<text class="title">欢迎登录拼车系统</text>
			<text class="subtitle">随时随地，畅享出行</text>
		</view>

		<view class="form-wrapper">
			<view class="input-item">
				<input class="input" type="number" v-model="phone" placeholder="请输入手机号" maxlength="11" />
			</view>
			<view class="input-item">
				<input class="input" type="password" v-model="password" placeholder="请输入密码" />
			</view>

			<button class="login-btn" @click="handleLogin">登 录</button>

			<view class="extra-links">
				<text class="register-link" @click="goToRegister">注册新账号</text>
				
			</view>
		</view>
	</view>
</template>

<script>
import { login } from '../../common/api.js';

export default {
	data() {
		return {
			phone: '',
			password: ''
		}
	},
	methods: {
		handleLogin() {
			// 表单验证
			if (!this.phone) {
				uni.showToast({
					title: '请输入手机号',
					icon: 'none'
				});
				return;
			}
			if (!this.password) {
				uni.showToast({
					title: '请输入密码',
					icon: 'none'
				});
				return;
			}
			
			// 显示加载中
			uni.showLoading({
				title: '登录中...'
			});
			
			// 调用登录接口
			login({
				phone: this.phone,
				password: this.password
			}).then(res => {
				uni.hideLoading();
				
				if (res.code === 200) {
					// 登录成功，保存用户信息
					uni.setStorageSync('userInfo', res.data);
					
					// 提示登录成功
					uni.showToast({
						title: '登录成功',
						icon: 'success'
					});
					
					// 跳转到首页
					setTimeout(() => {
						uni.reLaunch({
							url: '/pages/index/index'
						});
					}, 1500);
				} else {
					// 登录失败
					uni.showToast({
						title: res.msg || '登录失败',
						icon: 'none'
					});
				}
			}).catch(err => {
				uni.hideLoading();
				console.error('登录请求失败', err);
				// 显示网络错误提示
				uni.showToast({
					title: '网络请求失败，请检查网络连接',
					icon: 'none',
					duration: 2000
				});
			}).finally(() => {
				// 确保无论如何都会隐藏加载提示
				setTimeout(() => {
					uni.hideLoading();
				}, 500);
			});
		},
		goToRegister() {
			uni.navigateTo({
				url: '/pages/register/register'
			});
		}
	}
}
</script>

<style lang="scss">
.container {
	display: flex;
	flex-direction: column;
	background-color: #ffffff;
	padding: 60rpx 40rpx;
	min-height: 80vh; // 改为 min-height
	box-sizing: border-box;
	overflow-y: auto; // 添加滚动而非拖动
}


.header {
	margin-top: 80rpx;
	margin-bottom: 100rpx;
}

.title {
	font-size: 48rpx;
	font-weight: bold;
	color: $uni-text-color;
	display: block;
}

.subtitle {
	font-size: 32rpx;
	color: $uni-text-color-grey;
	margin-top: 20rpx;
	display: block;
}

.form-wrapper {
	flex: 1;
	overflow-y: auto;
}

.input-item {
	width: 100%;
	margin-bottom: 40rpx;
	border-bottom: 1rpx solid #e0e0e0;
	display: flex;
	align-items: center;
	height: 100rpx;
}

.input {
	flex: 1;
	font-size: 32rpx;
	color: $uni-text-color;
	padding: 20rpx 0;
}

.login-btn {
	width: 100%;
	height: 96rpx;
	line-height: 96rpx;
	background: $uni-color-primary;
	color: $uni-text-color-inverse;
	border: none;
	border-radius: 48rpx;
	font-size: 34rpx;
	margin-top: 60rpx;
	box-shadow: 0 10rpx 20rpx -10rpx $uni-color-primary;
	transition: all 0.3s ease;
	&:after {
		border: none;
	}
	&:active {
		transform: translateY(2rpx);
		box-shadow: 0 6rpx 15rpx -8rpx $uni-color-primary;
	}
}

.extra-links {
	display: flex;
	justify-content: space-between;
	margin-top: 40rpx;
	width: 100%;
}

.register-link,
.forgot-pwd-link {
	font-size: 28rpx;
	color: $uni-text-color-grey;
}
</style> 