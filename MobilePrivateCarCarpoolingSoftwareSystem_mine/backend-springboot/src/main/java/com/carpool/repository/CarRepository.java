package com.carpool.repository;

import com.carpool.model.Car;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface CarRepository extends JpaRepository<Car, Long> {
    List<Car> findByUserId(Long userId);
    List<Car> findByAuditStatus(Integer auditStatus);

    @Query("SELECT c FROM Car c WHERE c.userId = :userId AND c.auditStatus = 1")
    List<Car> getApprovedCarsByUserId(Long userId);
}