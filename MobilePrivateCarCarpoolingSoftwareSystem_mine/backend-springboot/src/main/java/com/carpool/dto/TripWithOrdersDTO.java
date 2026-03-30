package com.carpool.dto;

import com.carpool.model.Trip;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
public class TripWithOrdersDTO extends Trip {
    private List<OrderDTO> orders;

    public TripWithOrdersDTO(Trip trip, List<OrderDTO> orders) {
        // 复制Trip的所有属性
        this.setId(trip.getId());
        this.setDriverId(trip.getDriverId());
        this.setCarId(trip.getCarId());
        this.setStartLocation(trip.getStartLocation());
        this.setStartLng(trip.getStartLng());
        this.setStartLat(trip.getStartLat());
        this.setEndLocation(trip.getEndLocation());
        this.setEndLng(trip.getEndLng());
        this.setEndLat(trip.getEndLat());
        this.setDepartureTime(trip.getDepartureTime());
        this.setSeatAvailable(trip.getSeatAvailable());
        this.setPrice(trip.getPrice());
        this.setStatus(trip.getStatus());
        this.setCreateTime(trip.getCreateTime());
        // 设置订单列表
        this.orders = orders;
    }
} 