package com.carpool.controller;

import com.carpool.model.Order;
import com.carpool.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/order")
public class OrderController {
    @Autowired
    private OrderService orderService;

    // 下单，返回订单内容，前端确认
    @PostMapping("/apply")
    public Order applyOrder(@RequestBody Map<String, Object> params) {
        Long tripId = Long.valueOf(params.get("tripId").toString());
        Long passengerId = Long.valueOf(params.get("passengerId").toString());
        Integer seatCount = params.get("seatCount") == null ? 1 : Integer.valueOf(params.get("seatCount").toString());
        BigDecimal amount = new BigDecimal(params.get("amount").toString());
        return orderService.createOrder(tripId, passengerId, seatCount, amount);
    }

    // 确认订单
    @PostMapping("/confirm")
    public ResponseEntity<Map<String, Object>> confirmOrder(@RequestParam Long orderId) {
        Order confirmedOrder = orderService.confirmOrder(orderId);
        Map<String, Object> response = new HashMap<>();
        if (confirmedOrder != null) {
            response.put("code", 200);
            response.put("msg", "订单确认成功");
            response.put("data", confirmedOrder);
        } else {
            response.put("code", 500);
            response.put("msg", "订单确认失败");
        }
        return ResponseEntity.ok(response);
    }

    // 取消订单
    @PostMapping("/cancel")
    public Order cancelOrder(@RequestParam Long orderId) {
        return orderService.cancelOrder(orderId);
    }

    // 查询订单
    @GetMapping("/get")
    public Order getOrder(@RequestParam Long orderId) {
        return orderService.getOrderById(orderId);
    }
    // 查询确认后的订单
    @GetMapping("/getConfirmOrder")
    public List<Order> getConfirmOrder(@RequestParam Long passengerId) {
        return orderService.getConfirmOrder(passengerId);
    }

    // 查询乘客订单列表
    @GetMapping("/passenger")
    public List<Order> getPassengerOrders(@RequestParam Long passengerId) {
        return orderService.getOrdersByPassengerId(passengerId);
    }
} 