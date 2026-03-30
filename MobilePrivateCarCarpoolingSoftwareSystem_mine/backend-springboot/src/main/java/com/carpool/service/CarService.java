package com.carpool.service;

import com.carpool.model.Car;
import com.carpool.repository.CarRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

@Service
public class CarService {
    @Autowired
    private CarRepository carRepository;

    public Car addCar(Car car) {
        car.setAuditStatus(0); // 默认未审核
        car.setCreateTime(new Date());
        return carRepository.save(car);
    }

    public List<Car> getCarsByUserId(Long userId) {
        return carRepository.findByUserId(userId);
    }

    public void deleteCarByIdAndUserId(Long id, Long userId) {
        Car car = carRepository.findById(id).orElse(null);
        if (car != null && car.getUserId().equals(userId)) {
            carRepository.deleteById(id);
        }
    }

    public List<Car> getCarsByAuditStatus(Integer auditStatus) {
        return carRepository.findByAuditStatus(auditStatus);
    }

    public Car auditCar(Integer carId, Integer auditStatus) {
        Car car = carRepository.findById(carId.longValue()).orElse(null);
        if (car != null) {
            car.setAuditStatus(auditStatus);
            return carRepository.save(car);
        }
        return null;
    }

    public List<Car> getApprovedCarsByUserId(Long userId) {
        List<Car> ApprovedCars =  carRepository.getApprovedCarsByUserId(userId);
        System.out.println("ApprovedCars:"+ApprovedCars);
        return ApprovedCars;
    }
}