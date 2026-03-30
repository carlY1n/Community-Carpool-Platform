package com.carpool.model;

import lombok.Data;
import javax.persistence.*;
import java.util.Date;

@Entity
@Data
@Table(name = "chat_message")
public class ChatMessage {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 关联的订单ID
    private Long orderId;

    // 发送者ID
    private Long senderId;

    // 接收者ID
    private Long receiverId;

    // 消息内容
    @Column(columnDefinition = "TEXT")
    private String content;
    
    // 消息类型，例如 "TEXT", "IMAGE"
    private String messageType;

    // 消息发送时间
    @Temporal(TemporalType.TIMESTAMP)
    private Date createTime;

    // 消息状态，例如 0-未读 1-已读
    private Integer status = 0;
} 