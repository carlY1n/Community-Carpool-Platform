package com.carpool.repository;

import com.carpool.model.Complaint;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ComplaintRepository extends JpaRepository<Complaint, Long> {
    // 根据订单ID查询投诉
    Complaint findByOrderId(Long orderId);
    
    // 根据状态查询投诉列表
    List<Complaint> findByStatus(Integer status);
    
    // 根据投诉人ID查询投诉列表
    List<Complaint> findByComplainantId(Long complainantId);
} 