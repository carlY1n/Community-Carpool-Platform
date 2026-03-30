package com.carpool.controller;

import com.carpool.dto.TripWithOrdersDTO;
import com.carpool.model.Trip;
import com.carpool.service.TripService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.text.SimpleDateFormat;

@RestController
@RequestMapping("/api/trip")
public class TripController {
    @Autowired
    private TripService tripService;

    @GetMapping("/search")
    public List<Trip> searchTrips(
        @RequestParam Double startLng,
        @RequestParam Double startLat,
        @RequestParam Double endLng,
        @RequestParam Double endLat,
        @RequestParam(required = false) String departureTime
    ) {
        Date depTime;
        if (departureTime != null) {
            try {
                // 支持时间戳或yyyy-MM-dd
                if (departureTime.matches("\\d+")) {
                    depTime = new Date(Long.parseLong(departureTime));
                } else {
                    depTime = new SimpleDateFormat("yyyy-MM-dd").parse(departureTime);
                }
            } catch (Exception e) {
                depTime = new Date();
            }
        } else {
            depTime = new Date();
        }
        return tripService.searchTrips(startLng, startLat, endLng, endLat, depTime);
    }

    @PostMapping("/publish")
    public ResponseEntity<?> publishTrip(@RequestBody Trip trip) {
        // 校验必填项
        if (trip.getDriverId() == null || trip.getCarId() == null ||
            trip.getStartLocation() == null || trip.getStartLng() == null || trip.getStartLat() == null ||
            trip.getEndLocation() == null || trip.getEndLng() == null || trip.getEndLat() == null ||
            trip.getDepartureTime() == null || trip.getPrice() == null || trip.getSeatAvailable() == null) {
            return ResponseEntity.badRequest().body("请填写完整的行程信息（含经纬度）");
        }
        
        try {
            trip.setStatus(1); // 发布中
            trip.setCreateTime(new Date());
            Trip publishedTrip = tripService.publishTrip(trip);
            return ResponseEntity.ok(publishedTrip);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("发布行程失败，请稍后再试");
        }
    }

    // 查询单个行程（路径参数方式）
    @GetMapping("/{id}")
    public Trip getTripById(@PathVariable Long id) {
        return tripService.findTripById(id);
    }
    
    // 查询单个行程（查询参数方式）
    @GetMapping("/get")
    public Trip getTripByQueryId(@RequestParam Long id) {
        return tripService.findTripById(id);
    }
    
    // 获取司机发布的行程列表
    @GetMapping("/driver/{driverId}")
    public ResponseEntity<?> getDriverTrips(@PathVariable Long driverId) {
        try {
            // 注意：这里现在返回的是包含订单详情的DTO列表
            List<TripWithOrdersDTO> tripsWithOrders = tripService.findTripsByDriverId(driverId);
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("msg", "获取成功");
            response.put("data", tripsWithOrders);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("code", 500);
            response.put("msg", "获取行程失败：" + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    // 司机取消行程
    @PostMapping("/cancel/{tripId}")
    public ResponseEntity<?> cancelTrip(@PathVariable Long tripId, @RequestParam Long driverId) {
        try {
            Trip cancelledTrip = tripService.cancelTrip(tripId, driverId);
            Map<String, Object> response = new HashMap<>();

            if (cancelledTrip != null) {
                response.put("code", 200);
                response.put("msg", "行程已取消");
                response.put("data", cancelledTrip);
                return ResponseEntity.ok(response);
            } else {
                response.put("code", 403);
                response.put("msg", "无法取消，可能不满足取消条件（如非发布中、非本人操作）");
                return ResponseEntity.status(HttpStatus.FORBIDDEN).body(response);
            }
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("code", 500);
            response.put("msg", "操作失败：" + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    // 删除行程
    @DeleteMapping("/delete/{tripId}")
    public ResponseEntity<?> deleteTrip(@PathVariable Long tripId, @RequestParam Long driverId) {
        try {
            boolean deleted = tripService.deleteTrip(tripId, driverId);
            Map<String, Object> response = new HashMap<>();
            
            if (deleted) {
                response.put("code", 200);
                response.put("msg", "行程删除成功");
                return ResponseEntity.ok(response);
            } else {
                response.put("code", 403);
                response.put("msg", "权限不足或行程不存在");
                return ResponseEntity.status(HttpStatus.FORBIDDEN).body(response);
            }
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("code", 500);
            response.put("msg", "删除行程失败：" + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    // 管理员获取所有行程
    @GetMapping("/admin/list")
    public ResponseEntity<?> getAllTrips() {
        try {
            List<Trip> trips = tripService.findAllTrips();
            Map<String, Object> response = new HashMap<>();
            response.put("code", 200);
            response.put("msg", "获取成功");
            response.put("data", trips);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("code", 500);
            response.put("msg", "获取行程失败：" + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
    
    // 管理员删除行程
    @DeleteMapping("/admin/delete/{tripId}")
    public ResponseEntity<?> adminDeleteTrip(@PathVariable Long tripId) {
        try {
            boolean deleted = tripService.adminDeleteTrip(tripId);
            Map<String, Object> response = new HashMap<>();
            
            if (deleted) {
                response.put("code", 200);
                response.put("msg", "行程删除成功");
                return ResponseEntity.ok(response);
            } else {
                response.put("code", 404);
                response.put("msg", "行程不存在");
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
            }
        } catch (Exception e) {
            Map<String, Object> response = new HashMap<>();
            response.put("code", 500);
            response.put("msg", "删除行程失败：" + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }
} 