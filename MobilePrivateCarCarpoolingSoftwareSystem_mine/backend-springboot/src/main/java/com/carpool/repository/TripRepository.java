package com.carpool.repository;

import com.carpool.model.Trip;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.Date;
import java.util.List;

@Repository
public interface TripRepository extends JpaRepository<Trip, Long> {
    // 可扩展自定义查询方法

    @Query(value = "SELECT * FROM trip t " +
            "WHERE (6371000 * 2 * ASIN(SQRT(POWER(SIN((:startLat - t.start_lat) * PI() / 180 / 2), 2) + COS(:startLat * PI() / 180) * COS(t.start_lat * PI() / 180) * POWER(SIN((:startLng - t.start_lng) * PI() / 180 / 2), 2)))) < :startRadius " +
            "AND (6371000 * 2 * ASIN(SQRT(POWER(SIN((:endLat - t.end_lat) * PI() / 180 / 2), 2) + COS(:endLat * PI() / 180) * COS(t.end_lat * PI() / 180) * POWER(SIN((:endLng - t.end_lng) * PI() / 180 / 2), 2)))) < :endRadius " +
            "AND t.departure_time >= :departureTime " +
            "AND t.status = 1 " +
            "AND t.seat_available > (SELECT COUNT(*) FROM carpool_order co WHERE co.trip_id = t.id AND co.order_status NOT IN (3, 4)) " +
            "ORDER BY t.departure_time ASC",
            nativeQuery = true)
    List<Trip> findNearbyTrips(
        @Param("startLng") Double startLng,
        @Param("startLat") Double startLat,
        @Param("endLng") Double endLng,
        @Param("endLat") Double endLat,
        @Param("departureTime") Date departureTime,
        @Param("startRadius") Double startRadius,
        @Param("endRadius") Double endRadius
    );
    
    // 查询司机发布的所有行程
    List<Trip> findByDriverIdOrderByDepartureTimeDesc(Long driverId);
    
    // 查询所有行程，按创建时间倒序
    List<Trip> findAllByOrderByCreateTimeDesc();
} 