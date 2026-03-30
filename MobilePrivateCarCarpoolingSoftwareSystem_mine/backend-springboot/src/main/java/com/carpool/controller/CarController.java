package com.carpool.controller;

import com.carpool.model.Car;
import com.carpool.service.CarService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/car")
public class CarController {
    @Autowired
    private CarService carService;

    // 新增车辆
    @PostMapping("/add")
    public Car addCar(@RequestBody Car car) {
        return carService.addCar(car);
    }

    // 查询自己车辆
    @GetMapping("/my")
    public List<Car> getMyCars(@RequestParam Long userId) {
        return carService.getCarsByUserId(userId);
    }
    // 查询自己审核通过车辆
    @GetMapping("/myApprovedCar")
    public List<Car> getMyApprovedCars(@RequestParam Long userId) {
        return carService.getApprovedCarsByUserId(userId);
    }

    // 管理员：获取待审核车辆列表
    @GetMapping("/pending")
    public List<Car> getPendingCars() {
        return carService.getCarsByAuditStatus(0); // 0为待审核
    }

    // 管理员：审核车辆
    @PostMapping("/audit")
    public Car auditCar(@RequestParam Integer carId, @RequestParam Integer auditStatus) {
        return carService.auditCar(carId, auditStatus);
    }

    // 删除车辆
    @DeleteMapping("/delete/{id}")
    public void deleteCar(@PathVariable Long id, @RequestParam Long userId) {
        carService.deleteCarByIdAndUserId(id, userId);
    }
} 