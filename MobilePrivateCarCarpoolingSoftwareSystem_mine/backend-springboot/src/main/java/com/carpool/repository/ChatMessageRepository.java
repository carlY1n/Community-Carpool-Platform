package com.carpool.repository;

import com.carpool.model.ChatMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ChatMessageRepository extends JpaRepository<ChatMessage, Long> {
    
    /**
     * 根据订单ID查询聊天记录，并按时间升序排序
     * @param orderId 订单ID
     * @return 聊天消息列表
     */
    List<ChatMessage> findByOrderIdOrderByCreateTimeAsc(Long orderId);
} 