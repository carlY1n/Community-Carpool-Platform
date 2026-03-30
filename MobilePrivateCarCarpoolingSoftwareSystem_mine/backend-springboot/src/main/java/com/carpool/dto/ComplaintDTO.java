package com.carpool.dto;

import java.util.Date;

/**
 * 投诉数据传输对象
 */
public class ComplaintDTO {
    private Long id;
    private Long orderId;
    private Long complainantId;
    private String content;
    private Integer status;
    private Date createTime;
    
    // 简化的订单和行程信息
    private Long orderTripId;
    private String startLocation;
    private String endLocation;
    private Date departureTime;
    private String complainantName; // 投诉人姓名
    
    // 构造函数
    public ComplaintDTO() {}
    
    // 从Complaint实体转换为DTO - 为避免依赖问题，将在Controller中实现
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public Long getOrderId() {
        return orderId;
    }
    
    public void setOrderId(Long orderId) {
        this.orderId = orderId;
    }
    
    public Long getComplainantId() {
        return complainantId;
    }
    
    public void setComplainantId(Long complainantId) {
        this.complainantId = complainantId;
    }
    
    public String getContent() {
        return content;
    }
    
    public void setContent(String content) {
        this.content = content;
    }
    
    public Integer getStatus() {
        return status;
    }
    
    public void setStatus(Integer status) {
        this.status = status;
    }
    
    public Date getCreateTime() {
        return createTime;
    }
    
    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }
    
    public Long getOrderTripId() {
        return orderTripId;
    }
    
    public void setOrderTripId(Long orderTripId) {
        this.orderTripId = orderTripId;
    }
    
    public String getStartLocation() {
        return startLocation;
    }
    
    public void setStartLocation(String startLocation) {
        this.startLocation = startLocation;
    }
    
    public String getEndLocation() {
        return endLocation;
    }
    
    public void setEndLocation(String endLocation) {
        this.endLocation = endLocation;
    }
    
    public Date getDepartureTime() {
        return departureTime;
    }
    
    public void setDepartureTime(Date departureTime) {
        this.departureTime = departureTime;
    }
    
    public String getComplainantName() {
        return complainantName;
    }
    
    public void setComplainantName(String complainantName) {
        this.complainantName = complainantName;
    }
} 