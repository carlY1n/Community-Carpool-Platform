package com.carpool.service;

import com.carpool.model.User;
import com.carpool.model.UserType;
import com.carpool.repository.UserRepository;
import com.carpool.dto.UpdateProfileRequestDTO;
import com.carpool.dto.UserProfileResponseDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.persistence.EntityNotFoundException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Date;
import java.util.List;

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public User register(User user) {
        if (userRepository.findByPhone(user.getPhone()) != null) {
            return null; // 手机号已注册
        }

        // 如果未设置用户类型，默认设置为乘客
        if (user.getUserType() == null) {
            user.setUserType(UserType.PASSENGER);
        }

        if (user.getRealName() == null || user.getRealName().isEmpty()) {
            user.setRealName(user.getUsername());
        }

        try {
            // 1. 对密码进行MD5加密
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] hashedBytes = md.digest(user.getPassword().getBytes());

            // 2. 转换为16进制字符串
            StringBuilder sb = new StringBuilder();
            for (byte b : hashedBytes) {
                sb.append(String.format("%02x", b));
            }
            String encryptedPassword = sb.toString();

            // 3. 存储加密后的密码
            user.setPassword(encryptedPassword);
            user.setStatus(1);
            user.setCreateTime(new Date());

            return userRepository.save(user);

        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("MD5加密失败", e);
        }
    }

    public User login(String phone, String password) {
        User user = userRepository.findByPhone(phone);
        if (user != null) {
            try {
                // 对输入的密码进行MD5加密
                MessageDigest md = MessageDigest.getInstance("MD5");
                byte[] hashedBytes = md.digest(password.getBytes());

                // 转换为16进制字符串
                StringBuilder sb = new StringBuilder();
                for (byte b : hashedBytes) {
                    sb.append(String.format("%02x", b));
                }
                String encryptedInputPassword = sb.toString();

                // 比较加密后的密码
                if (user.getPassword().equals(encryptedInputPassword)) {
                    return user;
                }
            } catch (NoSuchAlgorithmException e) {
                throw new RuntimeException("MD5加密失败", e);
            }
        }
        return null;
    }

    // 获取所有用户列表（管理员功能）
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    // 根据ID查找用户
    public User findById(Long userId) {
        return userRepository.findById(userId).orElse(null);
    }

    // 修改用户状态（启用/禁用）
    public User updateUserStatus(Long userId, Integer status) {
        User user = userRepository.findById(userId).orElse(null);
        if (user == null) {
            return null;
        }
        user.setStatus(status);
        return userRepository.save(user);
    }

    // 新增方法：获取用户个人信息
    public UserProfileResponseDTO getUserProfileById(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new EntityNotFoundException("User not found with id: " + userId));
        return new UserProfileResponseDTO(
                user.getId(),
                user.getUsername(),
                user.getPhone(),
                user.getRealName(),
                user.getIdCard(),
                user.getUserType()
        );
    }

    // 新增方法：更新用户基本信息
    public UserProfileResponseDTO updateUserProfile(Long userId, UpdateProfileRequestDTO profileDto) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new EntityNotFoundException("User not found with id: " + userId));

        if (profileDto.getUsername() != null && !profileDto.getUsername().isEmpty()) {
            user.setUsername(profileDto.getUsername());
        }
        if (profileDto.getRealName() != null && !profileDto.getRealName().isEmpty()) {
            user.setRealName(profileDto.getRealName());
        }
        if (profileDto.getIdCard() != null && !profileDto.getIdCard().isEmpty()) {
            user.setIdCard(profileDto.getIdCard());
        }
        User updatedUser = userRepository.save(user);
        return new UserProfileResponseDTO(
                updatedUser.getId(),
                updatedUser.getUsername(),
                updatedUser.getPhone(),
                updatedUser.getRealName(),
                updatedUser.getIdCard(),
                updatedUser.getUserType()
        );
    }

    // 新增方法：修改密码
    public boolean updatePassword(Long userId, String oldPassword, String newPassword) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new EntityNotFoundException("User not found with id: " + userId));

        try {
            // 1. 对输入的旧密码进行 MD5 加密
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] oldHashedBytes = md.digest(oldPassword.getBytes());

            // 转换为 16 进制字符串
            StringBuilder oldSb = new StringBuilder();
            for (byte b : oldHashedBytes) {
                oldSb.append(String.format("%02x", b));
            }
            String encryptedOldPassword = oldSb.toString();

            // 2. 校验旧密码是否匹配
            if (!user.getPassword().equals(encryptedOldPassword)) {
                return false; // 旧密码不匹配
            }

            // 3. 对新密码进行 MD5 加密
            byte[] newHashedBytes = md.digest(newPassword.getBytes());
            StringBuilder newSb = new StringBuilder();
            for (byte b : newHashedBytes) {
                newSb.append(String.format("%02x", b));
            }
            String encryptedNewPassword = newSb.toString();

            // 4. 存储加密后的新密码
            user.setPassword(encryptedNewPassword);
            userRepository.save(user);
            return true;

        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("MD5 加密失败", e);
        }
    }
} 