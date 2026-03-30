package com.carpool.controller;

import com.carpool.model.ChatMessage;
import com.carpool.repository.ChatMessageRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RequestMapping;


import java.util.Date;
import java.util.List;

@Controller
@RequestMapping("/api/chat")
public class ChatController {

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    @Autowired
    private ChatMessageRepository chatMessageRepository;

    /**
     * WebSocket端点，用于处理和转发聊天消息
     * 客户端发送消息到 /app/chat.sendMessage
     */
    @MessageMapping("/chat.sendMessage")
    public void sendMessage(@Payload ChatMessage chatMessage) {
        chatMessage.setCreateTime(new Date());
        System.out.println("chatMessage:"+chatMessage);
        // 1. 将消息保存到数据库
        ChatMessage savedMessage = chatMessageRepository.save(chatMessage);

        // 2. 构建订阅地址
        String destination = "/topic/orders/" + savedMessage.getOrderId();

        // 3. 将消息发送给订阅了该订单频道的客户端
        messagingTemplate.convertAndSend(destination, savedMessage);
    }

    /**
     * REST API端点，用于获取历史聊天记录
     */
    @GetMapping("/history/{orderId}")
    @ResponseBody
    public List<ChatMessage> getChatHistory(@PathVariable Long orderId) {
        return chatMessageRepository.findByOrderIdOrderByCreateTimeAsc(orderId);
    }
} 