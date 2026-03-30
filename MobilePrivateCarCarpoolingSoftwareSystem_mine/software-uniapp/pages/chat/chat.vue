<template>
	<view class="chat-container">
		<!-- 状态提示栏 -->
		<view v-if="connectionStatus" class="connection-status" :class="{
			connected: isConnected,
			error: connectionStatus.includes('失败') || connectionStatus.includes('断开')
		}">
			{{ connectionStatus }}
		</view>

		<!-- 聊天消息列表 -->
		<scroll-view scroll-y class="message-list" :scroll-top="scrollTop">
			<view v-for="msg in messages" :key="msg.id || msg.createTime"
				:class="['message-item', msg.senderId === myUserId ? 'my-message' : 'other-message']">
				<view class="message-bubble">{{ msg.content }}</view>
			</view>
		</scroll-view>

		<!-- 输入栏 -->
		<view class="input-container">
			<input v-model="newMessage" type="text" class="input-field" placeholder="输入消息..." :disabled="!isConnected" />
			<button @click="sendMessage" class="send-button" :disabled="!isConnected">发送</button>
		</view>
	</view>
</template>

<script>
	import {
		Client
	} from '@stomp/stompjs';
	import SockJS from 'sockjs-client';
    // 注意：你需要一个配置文件来管理API基地址
	const API_BASE_URL = 'http://localhost:8888'; 

	export default {
		data() {
			return {
				messages: [],
				newMessage: '',
				stompClient: null,
				orderId: null,
				myUserId: null, // 当前登录用户的ID
				receiverId: null, // 对方的ID
				scrollTop: 0,
				isConnected: false,
				connectionStatus: ''
			};
		},
		onLoad(options) {
			if (options.params) {
				const params = JSON.parse(decodeURIComponent(options.params));
				this.orderId = parseInt(params.orderId, 10);
				this.receiverId = parseInt(params.receiverId, 10);
			}
			
			// 从userInfo对象中获取当前登录用户的ID
			const userInfo = uni.getStorageSync('userInfo');
			this.myUserId = userInfo ? parseInt(userInfo.id, 10) : null;

			// 验证ID是否存在
			if (!this.orderId || !this.receiverId || !this.myUserId) {
				console.error("聊天参数不完整!", {
					orderId: this.orderId,
					receiverId: this.receiverId,
					myUserId: this.myUserId
				});
				uni.showToast({
					title: '进入聊天室失败，参数错误',
					icon: 'none'
				});
				this.connectionStatus = '参数错误，无法连接';
				this.isConnected = false;
				return; // 阻止后续连接
			}

			this.fetchHistory();
			this.connect();
		},
		onUnload() {
			this.disconnect();
		},
		methods: {
			async fetchHistory() {
				try {
					const response = await uni.request({
						url: `${API_BASE_URL}/api/chat/history/${this.orderId}`,
						method: 'GET'
					});
					if (response.statusCode === 200) {
						this.messages = response.data;
						this.scrollToBottom();
					}
				} catch (error) {
					console.error('获取历史消息失败:', error);
				}
			},
			connect() {
				this.connectionStatus = '正在连接...';
				const socketFactory = () => new SockJS(`${API_BASE_URL}/ws-chat`);
				this.stompClient = new Client({
					webSocketFactory: socketFactory,
					reconnectDelay: 5000,
					onConnect: () => {
						console.log('WebSocket已连接');
						this.isConnected = true;
						this.connectionStatus = ''; // 连接成功后可以隐藏提示
						this.stompClient.subscribe(`/topic/orders/${this.orderId}`, (message) => {
							const receivedMsg = JSON.parse(message.body);

							// 如果消息来自当前用户, 则说明是服务器对自己发送消息的确认
							// 我们需要用服务器返回的真实消息替换掉我们之前乐观添加的临时消息
							if (receivedMsg.senderId === this.myUserId) {
								const optimisticMsgIndex = this.messages.findIndex(
									// 通过没有ID和内容相同来找到临时消息
									msg => !msg.id && msg.content === receivedMsg.content
								);
								
								if (optimisticMsgIndex > -1) {
									// 使用服务器返回的权威消息替换临时消息
									this.messages.splice(optimisticMsgIndex, 1, receivedMsg);
									return; // 处理完毕，退出
								}
							}
							
							// 如果是对方发来的消息，或者找不到对应的临时消息，则直接添加到列表
							this.messages.push(receivedMsg);
							this.scrollToBottom();
						});
					},
					onStompError: (frame) => {
						console.error('STOMP错误:', frame.headers['message']);
						console.error('详细信息:', frame.body);
						this.isConnected = false;
						this.connectionStatus = '连接失败，请稍后重试';
					},
					onWebSocketClose: () => {
						console.log('WebSocket 连接已关闭');
						this.isConnected = false;
						this.connectionStatus = '连接已断开';
					}
				});
				this.stompClient.activate();
			},
			disconnect() {
				if (this.stompClient) {
					this.stompClient.deactivate();
					this.isConnected = false;
					console.log('WebSocket已断开');
				}
			},
			sendMessage() {
				if (!this.newMessage.trim()) return;
				
				if (this.isConnected && this.stompClient) {
					const chatMessage = {
						// 注意：这个对象没有数据库ID，是临时的
						orderId: this.orderId,
						senderId: this.myUserId,
						receiverId: this.receiverId,
						content: this.newMessage.trim(),
						messageType: 'TEXT',
						createTime: new Date().toISOString() // 使用ISO格式时间戳
					};

					// 1. 乐观更新UI：立即将消息添加到聊天列表
					this.messages.push(chatMessage);
					this.scrollToBottom();

					// 2. 将消息发送到服务器
					this.stompClient.publish({
						destination: '/app/chat.sendMessage',
						body: JSON.stringify(chatMessage),
					});
					
					// 3. 清空输入框
					this.newMessage = '';
				} else {
					uni.showToast({
						title: '连接尚未建立，请稍候',
						icon: 'none'
					});
				}
			},
			scrollToBottom() {
				this.$nextTick(() => {
					this.scrollTop = this.messages.length * 1000; // 一个足够大的值
				});
			}
		}
	};
</script>

<style>
.chat-container {
	display: flex;
	flex-direction: column;
	height: 100vh;
	width: 100vw;
	max-width: 100vw;
	overflow: hidden;
	box-sizing: border-box;
	background-color: #f0f2f5;
}
.connection-status {
	text-align: center;
	padding: 6px 12px;
	font-size: 13px;
	color: #555;
}

.connection-status.connected {
	background-color: #e6ffed;
	color: #2e7d32;
}

.connection-status.error {
	background-color: #fff1f0;
	color: #cf1322;
}

.message-list {
	flex: 1;
	width: 100%;
	box-sizing: border-box;
	overflow-y: auto;
}

.message-item {
	display: flex;
	margin-bottom: 12px;
}

.my-message {
	justify-content: flex-end;
}

.other-message {
	justify-content: flex-start;
}

.message-bubble {
	max-width: 75%; /* 改为百分比，适应不同屏幕 */
	padding: 10px 14px;
	border-radius: 20px;
	line-height: 1.4;
	font-size: 14px;
	word-break: break-word;
	background-color: #ffffff;
	box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.my-message .message-bubble {
	background-color: #4cd964;
	color: white;
}

.input-container {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	align-items: center;
	padding: 8px 12px env(safe-area-inset-bottom, 12px);
	background-color: #ffffff;
	border-top: 1px solid #e0e0e0;
	box-sizing: border-box;
	z-index: 999;
}

.input-field {
	flex: 1;
	min-width: 0; /* 必加！否则 input 不会收缩 */
	height: 38px;
	padding: 0 15px;
	border-radius: 20px;
	border: 1px solid #ccc;
	font-size: 14px;
	box-sizing: border-box;
}

.input-field:disabled {
	background-color: #f0f0f0;
}

.send-button {
	margin-left: 10px;
	height: 38px;
	padding: 0 16px;
	border-radius: 20px;
	background-color: #4cd964;
	color: white;
	font-size: 14px;
	white-space: nowrap;
	box-sizing: border-box;
}

.send-button:disabled {
	background-color: #cfcfcf;
	color: #888888;
}
</style> 