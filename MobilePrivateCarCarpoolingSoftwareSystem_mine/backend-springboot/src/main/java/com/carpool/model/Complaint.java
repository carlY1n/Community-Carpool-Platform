package com.carpool.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import javax.persistence.*;
import java.util.Date;

@Entity
@Table(name = "complaint")
@Data
public class Complaint {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "order_id")
    private Long orderId;

    @Column(name = "complainant_id")
    private Long complainantId;

    @Column(name = "content", length = 500, nullable = false)
    private String content;

    @Column(name = "status")
    private Integer status;

    @Column(name = "create_time")
    private Date createTime;

    // 订单关联（可选）
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", insertable = false, updatable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private Order order;

    // 投诉人关联（可选）
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "complainant_id", insertable = false, updatable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private User complainant;
} 