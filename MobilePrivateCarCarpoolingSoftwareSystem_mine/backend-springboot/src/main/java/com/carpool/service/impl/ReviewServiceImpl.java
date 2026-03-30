package com.carpool.service.impl;

import com.carpool.model.Review;
import com.carpool.repository.ReviewRepository;
import com.carpool.service.ReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

@Service
public class ReviewServiceImpl implements ReviewService {
    @Autowired
    private ReviewRepository reviewRepository;

    @Override
    public Review addReview(Review review) {
        // 设置创建时间
        if (review.getCreateTime() == null) {
            review.setCreateTime(new Date());
        }
        return reviewRepository.save(review);
    }

    @Override
    public Review findByOrderId(Long orderId) {
        return reviewRepository.findByOrderId(orderId);
    }

    @Override
    public List<Review> findByRevieweeId(Long revieweeId) {
        return reviewRepository.findByRevieweeId(revieweeId);
    }
} 