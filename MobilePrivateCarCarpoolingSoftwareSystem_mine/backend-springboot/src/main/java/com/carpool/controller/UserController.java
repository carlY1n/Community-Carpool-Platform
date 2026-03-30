package com.carpool.controller;

import com.carpool.model.User;
import com.carpool.model.UserType;
import com.carpool.service.UserService;
import com.carpool.dto.UpdatePasswordRequestDTO;
import com.carpool.dto.UpdateProfileRequestDTO;
import com.carpool.dto.UserProfileResponseDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.persistence.EntityNotFoundException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/user")

public class UserController {
    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public Object register(@RequestBody User user) {
        User res = userService.register(user);
        if (res == null) {
            return new Result(400, "手机号已注册", null);
        }
        return new Result(200, "注册成功", res);
    }

    @PostMapping("/login")
    public Object login(@RequestBody LoginRequest req) {
        User user = userService.login(req.getPhone(), req.getPassword());
        if (user == null) {
            return new Result(400, "手机号或密码错误", null);
        }
        return new Result(200, "登录成功", user);
    }
    
    // 获取用户类型枚举
    @GetMapping("/types")
    public Object getUserTypes() {
        List<Map<String, Object>> types = Arrays.stream(UserType.values())
            .map(type -> {
                Map<String, Object> map = new HashMap<>();
                map.put("value", type.name());
                map.put("label", getTypeDisplayName(type));
                return map;
            })
            .collect(Collectors.toList());
        return new Result(200, "成功", types);
    }
    
    // 管理员API: 获取所有用户
    @GetMapping("/admin/list")
    public Object getAllUsers() {
        List<User> users = userService.getAllUsers();
        return new Result(200, "成功", users);
    }
    
    // 管理员API: 修改用户状态
    @PostMapping("/admin/status")
    public Object updateUserStatus(@RequestBody Map<String, Object> params) {
        Long userId = Long.valueOf(params.get("userId").toString());
        Integer status = Integer.valueOf(params.get("status").toString());
        
        User user = userService.updateUserStatus(userId, status);
        if (user == null) {
            return new Result(400, "用户不存在", null);
        }
        return new Result(200, "修改成功", user);
    }
    
    // --- 新增个人中心相关API ---

    @GetMapping("/{userId}/profile")
    public ResponseEntity<Result> getUserProfile(@PathVariable Long userId) {
        try {
            UserProfileResponseDTO profile = userService.getUserProfileById(userId);
            return ResponseEntity.ok(new Result(200, "获取用户信息成功", profile));
        } catch (EntityNotFoundException e) {
            return ResponseEntity.status(404).body(new Result(404, e.getMessage(), null));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(new Result(500, "获取用户信息失败: " + e.getMessage(), null));
        }
    }

    @PutMapping("/{userId}/profile")
    public ResponseEntity<Result> updateUserProfile(@PathVariable Long userId, @RequestBody UpdateProfileRequestDTO profileDto) {
        // 在实际应用中，这里应该有权限校验，确保用户只能修改自己的信息，或者管理员有权限修改
        try {
            UserProfileResponseDTO updatedProfile = userService.updateUserProfile(userId, profileDto);
            return ResponseEntity.ok(new Result(200, "用户信息更新成功", updatedProfile));
        } catch (EntityNotFoundException e) {
            return ResponseEntity.status(404).body(new Result(404, e.getMessage(), null));
        } catch (Exception e) {
            // 可以针对特定异常做更细致的处理，例如用户名已存在等
            return ResponseEntity.status(500).body(new Result(500, "用户信息更新失败: " + e.getMessage(), null));
        }
    }

    @PutMapping("/{userId}/password")
    public ResponseEntity<Result> updateUserPassword(@PathVariable Long userId, @RequestBody UpdatePasswordRequestDTO passwordDto) {
        // 同样，权限校验是必要的
        try {
            boolean success = userService.updatePassword(userId, passwordDto.getOldPassword(), passwordDto.getNewPassword());
            if (success) {
                return ResponseEntity.ok(new Result(200, "密码修改成功", null));
            } else {
                return ResponseEntity.status(400).body(new Result(400, "旧密码不正确", null));
            }
        } catch (EntityNotFoundException e) {
            return ResponseEntity.status(404).body(new Result(404, e.getMessage(), null));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(new Result(500, "密码修改失败: " + e.getMessage(), null));
        }
    }

    // 获取用户类型显示名
    private String getTypeDisplayName(UserType type) {
        switch (type) {
            case PASSENGER: return "乘客";
            case DRIVER: return "车主";
            case ADMIN: return "管理员";
            default: return "未知";
        }
    }

    static class LoginRequest {
        private String phone;
        private String password;
        public String getPhone() { return phone; }
        public void setPhone(String phone) { this.phone = phone; }
        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
    }

    static class Result {
        private int code;
        private String msg;
        private Object data;
        public Result(int code, String msg, Object data) {
            this.code = code; this.msg = msg; this.data = data;
        }
        public int getCode() { return code; }
        public String getMsg() { return msg; }
        public Object getData() { return data; }
    }
} 