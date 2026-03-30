package com.carpool.controller;

import com.carpool.model.Review;
import com.carpool.service.ReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/review")
public class ReviewController {
    @Autowired
    private ReviewService reviewService;

    // 添加评价
    @PostMapping("/add")
    public ResponseEntity<?> addReview(@RequestBody Review review) {
        // 校验必填项
        if (review.getOrderId() == null || review.getReviewerId() == null || 
            review.getRevieweeId() == null || review.getRating() == null) {
            return ResponseEntity.badRequest().body("请填写完整的评价信息");
        }
        
        try {
            Review savedReview = reviewService.addReview(review);
            return ResponseEntity.ok(savedReview);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("提交评价失败：" + e.getMessage());
        }
    }

    // 根据订单ID查询评价
    @GetMapping("/order/{orderId}")
    public ResponseEntity<?> getReviewByOrderId(@PathVariable Long orderId) {
        try {
            Review review = reviewService.findByOrderId(orderId);
            if (review == null) {
                return ResponseEntity.ok().body(null);
            }
            return ResponseEntity.ok(review);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("查询评价失败：" + e.getMessage());
        }
    }

    // 根据用户ID查询收到的评价
    @GetMapping("/user/{userId}")
    public ResponseEntity<?> getReviewsByUserId(@PathVariable Long userId) {
        try {
            return ResponseEntity.ok(reviewService.findByRevieweeId(userId));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("查询评价失败：" + e.getMessage());
        }
    }
} 