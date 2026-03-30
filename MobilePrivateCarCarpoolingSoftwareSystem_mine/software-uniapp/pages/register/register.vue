<template>
	<view class="container">
		<view class="header">
			<text class="title">加入我们，开启新旅程</text>
			<text class="subtitle">仅需几步，即可完成注册</text>
		</view>

		<view class="form-wrapper">
			<view class="input-item">
				<input class="input" type="number" v-model="user.phone" placeholder="请输入手机号" maxlength="11" />
			</view>
			<view class="input-item">
				<input class="input" type="text" v-model="user.username" placeholder="请输入姓名" />
			</view>
			<view class="input-item">
				<input class="input" type="password" v-model="user.password" placeholder="请设置密码（不少于6位）" />
			</view>
			<view class="input-item">
				<input class="input" type="password" v-model="confirmPassword" placeholder="请再次输入密码" />
			</view>

			<view class="user-type-selector">
				<text class="selector-label">选择您的身份</text>
				<view class="type-options">
					<view 
						class="option" 
						:class="{'active': user.userType === 'PASSENGER'}" 
						@click="user.userType = 'PASSENGER'">
						<image class="option-icon" src="/static/icon/passenger.png"></image>
						<text class="option-text">我是乘客</text>
					</view>
					<view 
						class="option" 
						:class="{'active': user.userType === 'DRIVER'}" 
						@click="user.userType = 'DRIVER'">
						<image class="option-icon" src="/static/icon/driver.png"></image>
						<text class="option-text">我是车主</text>
					</view>
				</view>
			</view>

			<button class="register-btn" @click="handleRegister">注 册</button>

			<view class="extra-links">
				<text class="login-link" @click="goToLogin">已有账号？直接登录</text>
			</view>
		</view>
	</view>
</template>

<script>
import { register, getUserTypes } from '../../common/api.js';

export default {
	data() {
		return {
			user: {
				phone: '',
				username: '',
				password: '',
				userType: 'PASSENGER'
			},
			confirmPassword: '',
			userTypes: [] // 用户类型列表
		}
	},
	onLoad() {
		// 获取用户类型列表
		this.fetchUserTypes();
	},
	methods: {
		// 获取用户类型
		fetchUserTypes() {
			getUserTypes().then(res => {
				if (res.code === 200) {
					this.userTypes = res.data;
				}
			}).catch(err => {
				console.error('获取用户类型失败', err);
			});
		},
		handleRegister() {
			// 表单验证
			if (!this.user.phone) {
				uni.showToast({
					title: '请输入手机号',
					icon: 'none'
				});
				return;
			}
			if (!/^1\d{10}$/.test(this.user.phone)) {
				uni.showToast({
					title: '请输入有效的手机号',
					icon: 'none'
				});
				return;
			}
			if (!this.user.username) {
				uni.showToast({
					title: '请输入姓名',
					icon: 'none'
				});
				return;
			}
			if (!this.user.password) {
				uni.showToast({
					title: '请输入密码',
					icon: 'none'
				});
				return;
			}
			if (this.user.password.length < 6) {
				uni.showToast({
					title: '密码长度不能少于6位',
					icon: 'none'
				});
				return;
			}
			if (this.user.password !== this.confirmPassword) {
				uni.showToast({
					title: '两次输入的密码不一致',
					icon: 'none'
				});
				return;
			}
			
			// 显示加载中
			uni.showLoading({
				title: '注册中...'
			});
			
			// 调用注册接口
			register(this.user).then(res => {
				uni.hideLoading();
				
				if (res.code === 200) {
					// 注册成功
					uni.showToast({
						title: '注册成功',
						icon: 'success'
					});
					
					// 跳转到登录页
					setTimeout(() => {
						uni.navigateTo({
							url: '/pages/login/login'
						});
					}, 1500);
				} else {
					// 注册失败
					uni.showToast({
						title: res.msg || '注册失败',
						icon: 'none'
					});
				}
			}).catch(err => {
				// 确保在出错时也隐藏加载提示
				uni.hideLoading();
				console.error('注册请求失败', err);
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
		goToLogin() {
			uni.navigateTo({
				url: '/pages/login/login'
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
	margin-top: 20rpx;
	margin-bottom: 80rpx;
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
	width: 100%;
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

.user-type-selector {
	margin-top: 20rpx;
	margin-bottom: 60rpx;
	.selector-label {
		font-size: 28rpx;
		color: $uni-text-color-grey;
		margin-bottom: 30rpx;
		display: block;
	}
	.type-options {
		display: flex;
		justify-content: space-between;
		gap: 30rpx;
	}
	.option {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 30rpx;
		border-radius: 20rpx;
		border: 2rpx solid #eee;
		transition: all 0.3s ease;
		.option-icon {
			width: 80rpx;
			height: 80rpx;
			margin-bottom: 20rpx;
		}
		.option-text {
			font-size: 28rpx;
			color: $uni-text-color;
		}
		&.active {
			border-color: $uni-color-primary;
			background-color: lighten($uni-color-primary, 35%);
		}
	}
}

.register-btn {
	width: 100%;
	height: 96rpx;
	line-height: 96rpx;
	background: $uni-color-primary;
	color: $uni-text-color-inverse;
	border: none;
	border-radius: 48rpx;
	font-size: 34rpx;
	margin-top: 20rpx;
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
	justify-content: center;
	margin-top: 40rpx;
	width: 100%;
}

.login-link {
	font-size: 28rpx;
	color: $uni-text-color-grey;
}
</style> 