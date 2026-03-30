package com.carpool.repository;

import com.carpool.model.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {
    // 根据订单ID查询评价
    Review findByOrderId(Long orderId);
    
    // 根据被评价人ID查询评价列表
    List<Review> findByRevieweeId(Long revieweeId);
} 