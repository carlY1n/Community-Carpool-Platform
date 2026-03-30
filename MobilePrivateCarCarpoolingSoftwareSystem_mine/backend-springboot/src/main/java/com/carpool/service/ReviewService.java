package com.carpool.service;

import com.carpool.model.Review;

import java.util.List;

public interface ReviewService {
    // 添加评价
    Review addReview(Review review);
    
    // 根据订单ID查询评价
    Review findByOrderId(Long orderId);
    
    // 根据被评价人ID查询评价列表
    List<Review> findByRevieweeId(Long revieweeId);
} 