package com.carpool.service;

import com.carpool.dto.OrderDTO;
import com.carpool.dto.TripWithOrdersDTO;
import com.carpool.model.Car;
import com.carpool.model.Order;
import com.carpool.model.Trip;
import com.carpool.model.User;
import com.carpool.repository.CarRepository;
import com.carpool.repository.OrderRepository;
import com.carpool.repository.TripRepository;
import com.carpool.repository.UserRepository;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class TripService {
    @Autowired
    private TripRepository tripRepository;
    
    @Autowired
    private CarRepository carRepository;

    @Autowired
    private OrderRepository orderRepository;

    @Autowired
    private UserRepository userRepository;

    public List<Trip> searchTrips(Double startLng, Double startLat, Double endLng, Double endLat, Date departureTime) {
        double startRadius = 5000.0; // 5公里
        double endRadius = 2000.0;   // 2公里
        List<Trip> trips = tripRepository.findNearbyTrips(startLng, startLat, endLng, endLat, departureTime, startRadius, endRadius);
        // 为每个行程加载车辆信息
        return trips.stream().peek(this::loadCarInfo).collect(Collectors.toList());
    }

    public Trip publishTrip(Trip trip) {
        return tripRepository.save(trip);
    }

    public Trip findTripById(Long id) {
        return tripRepository.findById(id).orElse(null);
    }
    
    // 根据司机ID查询其发布的所有行程，并附带订单信息
    public List<TripWithOrdersDTO> findTripsByDriverId(Long driverId) {
        List<Trip> trips = tripRepository.findByDriverIdOrderByDepartureTimeDesc(driverId);
        if (trips.isEmpty()) {
            return Collections.emptyList();
        }

        // 获取所有行程的ID
        List<Long> tripIds = trips.stream().map(Trip::getId).collect(Collectors.toList());
        
        // 一次性查询所有相关的订单
        List<Order> orders = orderRepository.findByTripIdIn(tripIds);
        
        // 获取这些订单中所有乘客的ID
        List<Long> passengerIds = orders.stream().map(Order::getPassengerId).distinct().collect(Collectors.toList());
        
        // 一次性查询所有相关的乘客信息
        Map<Long, User> passengerMap = userRepository.findAllById(passengerIds).stream()
                .collect(Collectors.toMap(User::getId, user -> user));

        // 将订单按行程ID分组
        Map<Long, List<Order>> ordersByTripId = orders.stream().collect(Collectors.groupingBy(Order::getTripId));

        // 组装最终的DTO列表
        return trips.stream().map(trip -> {
            List<Order> relatedOrders = ordersByTripId.getOrDefault(trip.getId(), Collections.emptyList());
            List<OrderDTO> orderDTOs = relatedOrders.stream().map(order -> {
                OrderDTO dto = new OrderDTO();
                BeanUtils.copyProperties(order, dto);
                User passenger = passengerMap.get(order.getPassengerId());
                if (passenger != null) {
                    dto.setPassengerName(passenger.getUsername()); // 假设User有getUsername方法
                }
                return dto;
            }).collect(Collectors.toList());
            
            loadCarInfo(trip); // 附加车辆信息
            return new TripWithOrdersDTO(trip, orderDTOs);
        }).collect(Collectors.toList());
    }
    
    // 删除行程（仅司机本人可删除）
    public boolean deleteTrip(Long tripId, Long driverId) {
        Trip trip = tripRepository.findById(tripId).orElse(null);
        if (trip != null && trip.getDriverId().equals(driverId)) {
            tripRepository.deleteById(tripId);
            return true;
        }
        return false;
    }
    
    public Trip cancelTrip(Long tripId, Long driverId) {
        Trip trip = tripRepository.findById(tripId).orElse(null);
        // 只能取消"发布中"的行程，且必须是司机本人
        if (trip != null && trip.getDriverId().equals(driverId) && trip.getStatus() == 1) {
            trip.setStatus(4); // 4: 已取消
            return tripRepository.save(trip);
        }
        return null;
    }
    
    // 管理员查询所有行程
    public List<Trip> findAllTrips() {
        return tripRepository.findAll();
    }
    
    // 管理员删除行程
    public boolean adminDeleteTrip(Long tripId) {
        Optional<Trip> tripOptional = tripRepository.findById(tripId);
        if (tripOptional.isPresent()) {
            Trip trip = tripOptional.get();
            // 管理员可直接删除/取消任何行程
            trip.setStatus(4); // 4表示已取消
            tripRepository.save(trip);
            return true;
        }
        return false;
    }
    
    // 加载车辆信息的辅助方法
    private void loadCarInfo(Trip trip) {
        if (trip.getCarId() != null) {
            Optional<Car> carOpt = carRepository.findById(trip.getCarId());
            if (carOpt.isPresent()) {
                Car car = carOpt.get();
                // 创建车辆信息映射
                Map<String, Object> carInfo = new HashMap<>();
                carInfo.put("id", car.getId());
                carInfo.put("brand", car.getBrand());
                carInfo.put("model", car.getModel());
                carInfo.put("color", car.getColor());
                carInfo.put("plateNumber", car.getPlateNumber());
                carInfo.put("seatCount", car.getSeatCount());
                
                // 设置到Trip的临时字段
                trip.setCarInfo(carInfo);
            }
        }
    }
} 