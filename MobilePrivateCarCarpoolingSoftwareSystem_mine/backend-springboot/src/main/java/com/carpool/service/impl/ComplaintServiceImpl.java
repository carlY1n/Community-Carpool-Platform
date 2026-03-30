package com.carpool.service.impl;

import com.carpool.model.Complaint;
import com.carpool.repository.ComplaintRepository;
import com.carpool.service.ComplaintService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

@Service
public class ComplaintServiceImpl implements ComplaintService {
    @Autowired
    private ComplaintRepository complaintRepository;

    @Override
    public Complaint addComplaint(Complaint complaint) {
        // 设置创建时间
        if (complaint.getCreateTime() == null) {
            complaint.setCreateTime(new Date());
        }
        // 设置默认状态为待处理
        if (complaint.getStatus() == null) {
            complaint.setStatus(0);
        }
        return complaintRepository.save(complaint);
    }

    @Override
    public Complaint findByOrderId(Long orderId) {
        return complaintRepository.findByOrderId(orderId);
    }

    @Override
    public List<Complaint> findPendingComplaints() {
        return complaintRepository.findByStatus(0);
    }

    @Override
    public Complaint processComplaint(Long id) {
        Complaint complaint = complaintRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("投诉不存在"));
        complaint.setStatus(1); // 设置为已处理
        return complaintRepository.save(complaint);
    }

    @Override
    public List<Complaint> findByComplainantId(Long complainantId) {
        return complaintRepository.findByComplainantId(complainantId);
    }

    @Override
    public List<Complaint> findAllComplaints() {
        return complaintRepository.findAll();
    }
} 