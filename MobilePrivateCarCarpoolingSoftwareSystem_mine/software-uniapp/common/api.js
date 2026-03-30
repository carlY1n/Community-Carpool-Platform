import { BASE_URL } from './config.js';

// API 配置
// const BASE_URL = 'http://222.79.104.168:8888'; 

// 封装请求方法
const request = (options) => {
	return new Promise((resolve, reject) => {
		// 显示加载中
		if (options.showLoading !== false) {
			uni.showLoading({
				title: '加载中...',
				mask: true
			});
		}
		
		// 添加公共请求头
		const header = {
			'Content-Type': 'application/json',
			...options.header
		};
		
		uni.request({
			url: BASE_URL + options.url,
			method: options.method || 'GET',
			data: options.data || {},
			header: header,
			success: (res) => {
				// 隐藏加载
				if (options.showLoading !== false) {
					uni.hideLoading();
				}
				
				// 如果请求成功但业务状态码不是200，也当作错误处理
				if (res.statusCode >= 200 && res.statusCode < 300) {
					resolve(res.data);
				} else {
					reject(res);
					uni.showToast({
						title: '请求失败：' + (res.data?.msg || '未知错误'),
						icon: 'none'
					});
				}
			},
			fail: (err) => {
				// 隐藏加载
				if (options.showLoading !== false) {
					uni.hideLoading();
				}
				
				reject(err);
				// 如果是H5环境，尝试使用JSONP解决跨域问题
				// #ifdef H5
				if (options.method === 'GET') {
					jsonpRequest(BASE_URL + options.url, options.data)
						.then(resolve)
						.catch(() => {
							uni.showToast({
								title: '网络请求失败，请检查网络连接',
								icon: 'none'
							});
						});
				} else {
					uni.showToast({
						title: '请求被阻止，可能是跨域问题，请联系管理员',
						icon: 'none',
						duration: 2000
					});
				}
				// #endif
				
				// 非H5环境，只提示网络错误
				// #ifndef H5
				uni.showToast({
					title: '网络请求失败，请检查网络连接',
					icon: 'none'
				});
				// #endif
			},
			complete: () => {
				// 确保加载提示被关闭
				setTimeout(() => {
					uni.hideLoading();
				}, 100);
			}
		});
	});
};

// JSONP请求（仅用于GET请求）
function jsonpRequest(url, data) {
	return new Promise((resolve, reject) => {
		// #ifdef H5
		let script = document.createElement('script');
		// 回调函数名
		const callbackName = 'jsonp_' + Date.now() + Math.floor(Math.random() * 100000);
		// 全局回调函数
		window[callbackName] = function(data) {
			resolve(data);
			document.body.removeChild(script);
			delete window[callbackName];
		};
		
		// 拼接参数
		const params = [];
		if (data) {
			for (let key in data) {
				params.push(`${key}=${encodeURIComponent(data[key])}`);
			}
		}
		params.push(`callback=${callbackName}`);
		
		// 创建script标签
		script.src = `${url}${url.includes('?') ? '&' : '?'}${params.join('&')}`;
		script.onerror = reject;
		document.body.appendChild(script);
		// #endif
		
		// #ifndef H5
		reject(new Error('JSONP只支持H5环境'));
		// #endif
	});
}

// 用户登录
export const login = (data) => {
	return request({
		url: '/api/user/login',
		method: 'POST',
		data
	});
};
	
// 用户注册
export const register = (data) => {
	return request({
		url: '/api/user/register',
		method: 'POST',
		data
	});
};

// 获取用户类型
export const getUserTypes = () => {
	return request({
		url: '/api/user/types',
		method: 'GET'
	});
};

// 管理员获取所有用户列表
export const getAllUsers = () => {
	return request({
		url: '/api/user/admin/list',
		method: 'GET'
	});
};

// 修改用户状态
export const updateUserStatus = (userId, status) => {
	return request({
		url: '/api/user/admin/status',
		method: 'POST',
		data: { userId, status }
	});
};

// 新增车辆
export const addCar = (data) => request({
	url: '/api/car/add',
	method: 'POST',
	data
});

// 查询自己车辆
export const getMyApprovedCars = (userId) => request({
	url: '/api/car/myApprovedCar?userId=' + userId,
	method: 'GET'
});

// 查询自己审核通过车辆
export const getMyCars = (userId) => request({
	url: '/api/car/my?userId=' + userId,
	method: 'GET'
});

// 删除车辆
export const deleteCar = (id, userId) => request({
	url: `/api/car/delete/${id}?userId=${userId}`,
	method: 'DELETE'
});

// 新增：发布行程API函数
export const publishTripApi = (data) => request({
	url: '/api/trip/publish',
	method: 'POST',
	data
});

// 新增：搜索行程API函数
export const searchTripApi = (params) => request({
	url: '/api/trip/search',
	method: 'GET',
	data: params
});

// 管理员：获取待审核车辆列表
export const getPendingCars = () => request({
	url: '/api/car/pending',
	method: 'GET'
});

// 管理员：审核车辆
export const auditCar = (carId, auditStatus) => request({
	url: `/api/car/audit?carId=${carId}&auditStatus=${auditStatus}`,
	method: 'POST'
});

// 乘客下单，返回订单内容
export const applyOrder = (data) => request({
	url: '/api/order/apply',
	method: 'POST',
	data
});

// 订单确认
export const confirmOrder = (orderId) => request({
	url: '/api/order/confirm?orderId=' + orderId,
	method: 'POST'
});

// 订单取消
export const cancelOrder = (orderId) => request({
	url: '/api/order/cancel?orderId=' + orderId,
	method: 'POST'
});

// 查询订单
export const getOrder = (orderId) => request({
	url: '/api/order/get?orderId=' + orderId,
	method: 'GET'
});

// 查询乘客订单列表
export const getPassengerOrders = (passengerId) => request({
	url: `/api/order/passenger?passengerId=${passengerId}`,
	method: 'GET'
});

// 查询乘客已确认订单列表
export const getConfirmPassengerOrders = (passengerId) => request({
	url: `/api/order/getConfirmOrder?passengerId=${passengerId}`,
	method: 'GET'
});

// 查询单个行程
export const getTripById = (id) => request({
	url: `/api/trip/get?id=${id}`,
	method: 'GET'
});

// 提交好评
export const submitReview = (data) => request({
	url: '/api/review/add',
	method: 'POST',
	data
});

// 提交投诉
export const submitComplaint = (data) => request({
	url: '/api/complaint/add',
	method: 'POST',
	data
});

// 获取用户的投诉列表
export const getUserComplaints = (userId) => request({
	url: `/api/complaint/user/${userId}`,
	method: 'GET'
});

// 管理员获取所有投诉
export const getAllComplaints = () => request({
	url: '/api/complaint/admin/list',
	method: 'GET'
});

// 管理员处理投诉
export const processComplaint = (complaintId) => request({
	url: `/api/complaint/admin/process/${complaintId}`,
	method: 'PUT'
});

// --- 用户个人中心 API ---

// 获取用户个人信息
export const getUserProfile = (userId) => request({
	url: `/api/user/${userId}/profile`,
	method: 'GET'
});

// 更新用户基本信息
export const updateUserProfile = (userId, data) => request({
	url: `/api/user/${userId}/profile`,
	method: 'PUT',
	data
});

// 修改用户密码
export const updateUserPassword = (userId, data) => request({
	url: `/api/user/${userId}/password`,
	method: 'PUT',
	data
});

// 获取车主发布的行程列表
export const getDriverTrips = (driverId) => request({
	url: `/api/trip/driver/${driverId}`,
	method: 'GET'
});

// 司机取消行程
export const cancelTrip = (tripId, driverId) => request({
	url: `/api/trip/cancel/${tripId}?driverId=${driverId}`,
	method: 'POST'
});

// 司机删除行程
export const deleteTrip = (tripId, driverId) => request({
	url: `/api/trip/delete/${tripId}?driverId=${driverId}`,
	method: 'DELETE'
});

// 管理员获取所有行程
export const getAllTrips = () => request({
	url: '/api/trip/admin/list',
	method: 'GET'
});

// 管理员删除行程
export const adminDeleteTrip = (tripId) => request({
	url: `/api/trip/admin/delete/${tripId}`,
	method: 'DELETE'
});

// 发送聊天消息
export const sendChatMessage = (data) => request({
	url: '/api/chat/send',
	method: 'POST',
	data
});

// 获取聊天记录
export const getChatHistory = (orderId) => request({
	url: `/api/chat/history/${orderId}`,
	method: 'GET'
});