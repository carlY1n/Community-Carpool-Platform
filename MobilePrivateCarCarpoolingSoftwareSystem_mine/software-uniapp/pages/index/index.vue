<template>
	<view class="content">
		<view class="header">
			<text class="welcome">欢迎, {{userInfo.username}}</text>
			<text class="user-info">开始您的{{userTypeText}}之旅</text>
		</view>

		<!-- 功能菜单 -->
		<view class="menu-grid" v-if="userInfo">
			<!-- 乘客功能菜单 -->
			<template v-if="userInfo.userType === 'PASSENGER'">
				<view class="menu-item style-1" @click="navigateTo('/pages/searchTrip/searchTrip')">
					<text class="menu-text">查找行程</text>
					<text class="menu-desc">开启新旅程</text>
				</view>
				<view class="menu-item style-2" @click="navigateTo('/pages/myOrders/myOrders')">
					<text class="menu-text">我的订单</text>
					<text class="menu-desc">查看历史订单</text>
				</view>
				<view class="menu-item style-3" @click="navigateTo('/pages/profile/profile')">
					<text class="menu-text">个人中心</text>
					<text class="menu-desc">管理您的账户</text>
				</view>
				<view class="menu-item style-4" @click="navigateTo('/pages/complaints/complaints')">
					<text class="menu-text">投诉建议</text>
					<text class="menu-desc">帮助我们改进</text>
				</view>
			</template>

			<!-- 车主功能菜单 -->
			<template v-if="userInfo.userType === 'DRIVER'">
				<view class="menu-item style-5" @click="navigateTo('/pages/publishTrip/publishTrip')">
					<text class="menu-text">发布行程</text>
					<text class="menu-desc">分享您的空座</text>
				</view>
				<view class="menu-item style-6" @click="navigateTo('/pages/myTrips/myTrips')">
					<text class="menu-text">我的行程</text>
					<text class="menu-desc">管理已发布行程</text>
				</view>
				<view class="menu-item style-7" @click="navigateTo('/pages/carManage/carManage')">
					<text class="menu-text">车辆管理</text>
					<text class="menu-desc">添加或修改车辆</text>
				</view>
				<view class="menu-item style-3" @click="navigateTo('/pages/profile/profile')">
					<text class="menu-text">个人中心</text>
					<text class="menu-desc">管理您的账户</text>
				</view>
			</template>

			<!-- 管理员功能菜单 -->
			<template v-if="userInfo.userType === 'ADMIN'">
				<view class="menu-item style-1" @click="navigateTo('/pages/admin/user')">
					<text class="menu-text">用户管理</text>
					<text class="menu-desc">查看所有用户</text>
				</view>
				<view class="menu-item style-2" @click="navigateTo('/pages/admin/carAudit')">
					<text class="menu-text">车辆审核</text>
					<text class="menu-desc">处理待审车辆</text>
				</view>
				<view class="menu-item style-3" @click="navigateTo('/pages/admin/trip')">
					<text class="menu-text">行程管理</text>
					<text class="menu-desc">监控所有行程</text>
				</view>
				<view class="menu-item style-4" @click="navigateTo('/pages/admin/complaint')">
					<text class="menu-text">投诉处理</text>
					<text class="menu-desc">跟进用户反馈</text>
				</view>
			</template>
		</view>
		
		<view class="logout-box">
			<button class="logout-btn" @click="handleLogout">退出登录</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				userInfo: null
			}
		},
		computed: {
			// 用户类型显示文本
			userTypeText() {
				if (!this.userInfo) return '';
				
				switch(this.userInfo.userType) {
					case 'PASSENGER': return '乘客';
					case 'DRIVER': return '车主';
					case 'ADMIN': return '管理员';
					default: return '未知';
				}
			}
		},
		onShow() {
			// 每次显示页面时，检查登录状态
			this.checkLogin();
		},
		onLoad() {
			// 页面加载时，检查登录状态
			this.checkLogin();
		},
		methods: {
			checkLogin() {
				// 获取存储的用户信息
				const userInfo = uni.getStorageSync('userInfo');
				if (userInfo) {
					this.userInfo = userInfo;
				} else {
					// 未登录，跳转到登录页
					uni.redirectTo({
						url: '/pages/login/login'
					});
				}
			},
			handleLogout() {
				// 显示确认对话框
				uni.showModal({
					title: '提示',
					content: '确定要退出登录吗？',
					success: (res) => {
						if (res.confirm) {
							// 清除用户信息
							uni.removeStorageSync('userInfo');
							this.userInfo = null;
							
							// 跳转到登录页
							uni.redirectTo({
								url: '/pages/login/login'
							});
						}
					}
				});
			},
			navigateTo(url) {
				uni.navigateTo({ url });
			}
		}
	}
</script>

<style lang="scss">
.content {
  display: flex;
  flex-direction: column;
  justify-content: space-between; // 核心变化
  padding: 40rpx;
  box-sizing: border-box;
  background-color: #f7f8fa;
  overflow: hidden; // ❌禁止滚动拖动
  min-height: 100vh; // 改为 min-height
}

.header {
	margin-bottom: 60rpx;
	padding: 20rpx 0;
}

.welcome {
	font-size: 52rpx;
	font-weight: bold;
	color: $uni-text-color;
	display: block;
}

.user-info {
	font-size: 32rpx;
	color: $uni-text-color-grey;
	margin-top: 10rpx;
}

.menu-grid {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 30rpx;
}

.menu-item {
	border-radius: 24rpx;
	padding: 35rpx;
	color: #fff;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	height: 200rpx;
	box-shadow: 0 10rpx 25rpx rgba(0, 0, 0, 0.1);
	transition: transform 0.2s ease-in-out;
	&:active {
		transform: scale(0.97);
	}

	&.style-1 { background: linear-gradient(135deg, #4fadff 0%, #2575fc 100%); }
	&.style-2 { background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); }
	&.style-3 { background: linear-gradient(135deg, $uni-color-primary 0%, #f39c12 100%); }
	&.style-4 { background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); }
	&.style-5 { background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); }
	&.style-6 { background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%); }
	&.style-7 { background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); }
}

.menu-text {
	font-size: 34rpx;
	font-weight: bold;
}

.menu-desc {
	font-size: 24rpx;
	opacity: 0.9;
}

.logout-box {
  margin-top: auto;
  padding-bottom: 100rpx; // 比默认多一点，让它离底部远一点
}


.logout-btn {
	background-color: #fff;
	color: $uni-color-error;
	font-size: 32rpx;
	border-radius: 20rpx;
	border: 1rpx solid #fdecec;
	&:after {
		border: none;
	}
}
</style>
