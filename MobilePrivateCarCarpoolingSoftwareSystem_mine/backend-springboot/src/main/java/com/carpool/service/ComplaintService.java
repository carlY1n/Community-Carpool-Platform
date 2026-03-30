package com.carpool.service;

import com.carpool.model.Complaint;

import java.util.List;

public interface ComplaintService {
    // 添加投诉
    Complaint addComplaint(Complaint complaint);
    
    // 根据订单ID查询投诉
    Complaint findByOrderId(Long orderId);
    
    // 查询所有待处理投诉
    List<Complaint> findPendingComplaints();
    
    // 处理投诉
    Complaint processComplaint(Long id);
    
    // 根据投诉人ID查询投诉
    List<Complaint> findByComplainantId(Long complainantId);
    
    // 查询所有投诉（管理员用）
    List<Complaint> findAllComplaints();
} 