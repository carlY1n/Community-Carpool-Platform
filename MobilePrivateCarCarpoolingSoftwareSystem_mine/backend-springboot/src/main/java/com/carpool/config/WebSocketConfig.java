package com.carpool.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        // 客户端订阅消息的前缀
        config.enableSimpleBroker("/topic");
        // 服务端接收消息的前缀
        config.setApplicationDestinationPrefixes("/app");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        // 注册一个STOMP端点，客户端将使用它进行连接
        // SockJS端点需要在这里专门配置CORS策略
        // withSockJS()是用来为不支持WebSocket的浏览器启用后备选项
        registry.addEndpoint("/ws-chat")
                .setAllowedOrigins("http://localhost:8080") // 明确允许的前端域
                .withSockJS();
    }
} 