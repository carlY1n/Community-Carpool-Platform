package com.carpool.repository;

import com.carpool.model.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByPassengerId(Long passengerId);

    @Query("SELECT o FROM Order o WHERE o.passengerId = :passengerId AND o.orderStatus = 1 ")
    List<Order> getConfirmOrder(Long passengerId);

    List<Order> findByTripIdIn(List<Long> tripIds);
}