package com.carpool.service;

import com.carpool.model.Order;
import com.carpool.model.Trip;
import com.carpool.repository.OrderRepository;
import com.carpool.repository.TripRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private TripRepository tripRepository;

    public Order createOrder(Long tripId, Long passengerId, Integer seatCount, BigDecimal amount) {
        Order order = new Order();
        order.setTripId(tripId);
        order.setPassengerId(passengerId);
        order.setSeatCount(seatCount);
        order.setOrderStatus(0); // 0待确认
        order.setOrderTime(new Date());
        order.setPayStatus(0); // 0未支付
        order.setAmount(amount);
        return orderRepository.save(order);
    }

    public Order confirmOrder(Long orderId) {
        Order order = orderRepository.findById(orderId).orElse(null);
        if (order != null && order.getOrderStatus() == 0) { // 只能确认待确认的订单
            Trip trip = tripRepository.findById(order.getTripId()).orElse(null);
            if (trip != null && trip.getSeatAvailable() >= order.getSeatCount()) {
                
                trip.setSeatAvailable(trip.getSeatAvailable() - order.getSeatCount());
                
                if (trip.getSeatAvailable() == 0) {
                    trip.setStatus(2); // 2: 已满员
                }
                tripRepository.save(trip);
                
                order.setOrderStatus(1); // 1: 已确认
                order.setPayStatus(1);   // 1: 已支付
                return orderRepository.save(order);
            }
        }
        return null;
    }

    public Order cancelOrder(Long orderId) {
        Order order = orderRepository.findById(orderId).orElse(null);
        if (order != null) {
            order.setOrderStatus(3); // 3已取消
            return orderRepository.save(order);
        }
        return null;
    }

    public Order getOrderById(Long orderId) {
        return orderRepository.findById(orderId).orElse(null);
    }
    
    // 为了与Controller保持一致的方法名
    public Order findById(Long orderId) {
        return getOrderById(orderId);
    }

    public List<Order> getOrdersByPassengerId(Long passengerId) {
        List<Order> orders = orderRepository.findByPassengerId(passengerId);
        // 获取所有订单关联的行程ID
        List<Long> tripIds = orders.stream()
                                   .map(Order::getTripId)
                                   .distinct()
                                   .collect(Collectors.toList());
        
        if (!tripIds.isEmpty()) {
            // 一次性查询所有相关的行程
            Map<Long, Trip> tripMap = tripRepository.findAllById(tripIds).stream()
                                                    .collect(Collectors.toMap(Trip::getId, t -> t));
            // 将行程信息关联到订单上
            orders.forEach(order -> order.setTrip(tripMap.get(order.getTripId())));
        }
        return orders;
    }

    public List<Order> getConfirmOrder(Long passengerId) {
        return orderRepository.getConfirmOrder(passengerId);
    }
}