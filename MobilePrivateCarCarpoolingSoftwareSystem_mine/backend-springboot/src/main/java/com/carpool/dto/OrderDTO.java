package com.carpool.dto;

import lombok.Data;
import java.util.Date;

@Data
public class OrderDTO {
    private Long id;
    private Long passengerId;
    private String passengerName; // 乘客昵称或姓名
    private Integer seatCount;
    private Integer orderStatus;
    private Date orderTime;
} 