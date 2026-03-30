package com.carpool.dto;

import lombok.Data;

@Data
public class UpdateProfileRequestDTO {
    private String username;
    private String realName;
    private String idCard;
} 