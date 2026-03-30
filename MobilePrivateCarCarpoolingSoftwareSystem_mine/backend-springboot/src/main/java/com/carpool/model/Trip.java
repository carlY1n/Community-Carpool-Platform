package com.carpool.model;

import lombok.Data;

import javax.persistence.*;
import java.util.Date;
import java.util.Map;

@Entity
@Table(name = "trip")
@Data
public class Trip {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "driver_id")
    private Long driverId;

    @Column(name = "car_id")
    private Long carId;

    @Column(name = "start_location")
    private String startLocation;

    @Column(name = "start_lng")
    private Double startLng;

    @Column(name = "start_lat")
    private Double startLat;

    @Column(name = "end_location")
    private String endLocation;

    @Column(name = "end_lng")
    private Double endLng;

    @Column(name = "end_lat")
    private Double endLat;

    @Column(name = "via_points")
    private String viaPoints;

    @Column(name = "departure_time")
    private Date departureTime;

    @Column(name = "price")
    private Double price;

    @Column(name = "seat_available")
    private Integer seatAvailable;

    @Column(name = "status")
    private Integer status;

    @Column(name = "create_time")
    private Date createTime;
    
    // 非持久化字段，用于前端展示
    @Transient
    private Map<String, Object> carInfo;

    // getter/setter ...
} 