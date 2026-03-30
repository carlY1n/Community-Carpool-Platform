package com.carpool.dto;

import com.carpool.model.UserType;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserProfileResponseDTO {
    private Long id;
    private String username;
    private String phone;
    private String realName;
    private String idCard;
    private UserType userType;
} 