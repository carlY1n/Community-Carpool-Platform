package com.carpool.controller;

import com.carpool.dto.ComplaintDTO;
import com.carpool.model.Complaint;
import com.carpool.model.Order;
import com.carpool.model.User;
import com.carpool.service.ComplaintService;
import com.carpool.service.UserService;
import com.carpool.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/complaint")
public class ComplaintController {
    @Autowired
    private ComplaintService complaintService;
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private OrderService orderService;

    // 添加投诉
    @PostMapping("/add")
    public ResponseEntity<?> addComplaint(@RequestBody Complaint complaint) {
        // 校验必填项
        if (complaint.getOrderId() == null || complaint.getComplainantId() == null || 
            complaint.getContent() == null || complaint.getContent().trim().isEmpty()) {
            return ResponseEntity.badRequest().body("请填写完整的投诉信息");
        }
        
        try {
            // 设置默认值
            complaint.setStatus(0); // 默认待处理
            complaint.setCreateTime(new Date());
            
            Complaint savedComplaint = complaintService.addComplaint(complaint);
            return ResponseEntity.ok(savedComplaint);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("提交投诉失败：" + e.getMessage());
        }
    }

    // 根据订单ID查询投诉
    @GetMapping("/order/{orderId}")
    public ResponseEntity<?> getComplaintByOrderId(@PathVariable Long orderId) {
        try {
            Complaint complaint = complaintService.findByOrderId(orderId);
            if (complaint == null) {
                return ResponseEntity.ok().body(null);
            }
            return ResponseEntity.ok(complaint);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("查询投诉失败：" + e.getMessage());
        }
    }

    // 查询所有待处理投诉（管理员用）
    @GetMapping("/pending")
    public ResponseEntity<?> getPendingComplaints() {
        try {
            return ResponseEntity.ok(complaintService.findPendingComplaints());
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("查询投诉失败：" + e.getMessage());
        }
    }

    // 处理投诉（管理员用）
    @PostMapping("/process/{id}")
    public ResponseEntity<?> processComplaint(@PathVariable Long id) {
        try {
            Complaint processed = complaintService.processComplaint(id);
            return ResponseEntity.ok(processed);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("处理投诉失败：" + e.getMessage());
        }
    }

    // 根据用户ID查询投诉
    @GetMapping("/user/{userId}")
    public ResponseEntity<?> getComplaintsByUserId(@PathVariable Long userId) {
        try {
            List<Complaint> complaints = complaintService.findByComplainantId(userId);
            List<ComplaintDTO> complaintDTOs = complaints.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
            return ResponseEntity.ok(complaintDTOs);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("查询投诉失败：" + e.getMessage());
        }
    }
    
    // 管理员获取所有投诉列表
    @GetMapping("/admin/list")
    public ResponseEntity<?> getAllComplaints() {
        try {
            List<Complaint> complaints = complaintService.findAllComplaints();
            List<Map<String, Object>> complaintInfoList = complaints.stream()
                .map(this::convertToAdminDTO)
                .collect(Collectors.toList());
            
            return ResponseEntity.ok(new Result(200, "获取投诉列表成功", complaintInfoList));
        } catch (Exception e) {
            return ResponseEntity.status(500)
                .body(new Result(500, "获取投诉列表失败: " + e.getMessage(), null));
        }
    }
    
    // 管理员处理投诉
    @PutMapping("/admin/process/{id}")
    public ResponseEntity<?> adminProcessComplaint(@PathVariable Long id) {
        try {
            Complaint processed = complaintService.processComplaint(id);
            return ResponseEntity.ok(new Result(200, "处理投诉成功", convertToAdminDTO(processed)));
        } catch (Exception e) {
            return ResponseEntity.status(500)
                .body(new Result(500, "处理投诉失败: " + e.getMessage(), null));
        }
    }

    // 实体转换为DTO的方法
    private ComplaintDTO convertToDTO(Complaint complaint) {
        ComplaintDTO dto = new ComplaintDTO();
        dto.setId(complaint.getId());
        dto.setOrderId(complaint.getOrderId());
        dto.setComplainantId(complaint.getComplainantId());
        dto.setContent(complaint.getContent());
        dto.setStatus(complaint.getStatus());
        dto.setCreateTime(complaint.getCreateTime());
        
        // 添加投诉人姓名（如果有）
        if (complaint.getComplainant() != null) {
            dto.setComplainantName(complaint.getComplainant().getUsername());
        }
        
        // 如果有关联订单信息，也设置进去
        if (complaint.getOrder() != null) {
            dto.setOrderTripId(complaint.getOrder().getTripId());
            
            // 如果订单关联了行程，再设置行程信息
            if (complaint.getOrder().getTrip() != null) {
                dto.setStartLocation(complaint.getOrder().getTrip().getStartLocation());
                dto.setEndLocation(complaint.getOrder().getTrip().getEndLocation());
                dto.setDepartureTime(complaint.getOrder().getTrip().getDepartureTime());
            }
        }
        
        return dto;
    }
    
    // 转换为管理员页面使用的格式
    private Map<String, Object> convertToAdminDTO(Complaint complaint) {
        Map<String, Object> dto = new HashMap<>();
        dto.put("id", complaint.getId());
        dto.put("orderId", complaint.getOrderId());
        dto.put("complainantId", complaint.getComplainantId());
        dto.put("content", complaint.getContent());
        dto.put("status", complaint.getStatus());
        dto.put("createTime", complaint.getCreateTime());
        
        // 获取投诉人信息
        try {
            User complainant = userService.findById(complaint.getComplainantId());
            if (complainant != null) {
                dto.put("complainantName", complainant.getUsername());
                dto.put("complainantPhone", complainant.getPhone());
            }
        } catch (Exception e) {
            // 即使获取用户信息失败，也不要影响整体流程
        }
        
        // 获取订单信息
        try {
            Order order = orderService.findById(complaint.getOrderId());
            if (order != null) {
                String orderInfo = "订单号: " + order.getId() + 
                                " | 乘客ID: " + order.getPassengerId() + 
                                " | 座位数: " + order.getSeatCount() +
                                " | 金额: " + order.getAmount();
                dto.put("orderInfo", orderInfo);
                dto.put("tripId", order.getTripId());
            }
        } catch (Exception e) {
            // 即使获取订单信息失败，也不要影响整体流程
        }
        
        return dto;
    }
    
    static class Result {
        private int code;
        private String msg;
        private Object data;
        
        public Result(int code, String msg, Object data) {
            this.code = code;
            this.msg = msg;
            this.data = data;
        }
        
        public int getCode() { return code; }
        public String getMsg() { return msg; }
        public Object getData() { return data; }
    }
} 