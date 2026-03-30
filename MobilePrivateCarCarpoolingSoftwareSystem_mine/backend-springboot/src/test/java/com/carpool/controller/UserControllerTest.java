package com.carpool.controller;

import com.carpool.dto.UpdatePasswordRequestDTO;
import com.carpool.dto.UpdateProfileRequestDTO;
import com.carpool.dto.UserProfileResponseDTO;
import com.carpool.model.User;
import com.carpool.model.UserType;
import com.carpool.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import javax.persistence.EntityNotFoundException;
import java.util.Arrays;
import java.util.Date;
import java.util.List;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
@DisplayName("用户控制器测试")
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    private User testUser;
    private UserProfileResponseDTO userProfileDto;

    @BeforeEach
    void setUp() {
        testUser = new User();
        testUser.setId(1L);
        testUser.setUsername("testuser");
        testUser.setPhone("13800138000");
        testUser.setPassword("123456");
        testUser.setRealName("测试用户");
        testUser.setIdCard("123456789012345678");
        testUser.setUserType(UserType.PASSENGER);
        testUser.setStatus(1);
        testUser.setCreateTime(new Date());

        userProfileDto = new UserProfileResponseDTO(
                1L, "testuser", "13800138000", "测试用户", "123456789012345678", UserType.PASSENGER
        );
    }

    @Test
    @DisplayName("用户注册成功")
    void testRegisterSuccess() throws Exception {
        // Given
        when(userService.register(any(User.class))).thenReturn(testUser);

        // When & Then
        mockMvc.perform(post("/api/user/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(testUser)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("注册成功"))
                .andExpect(jsonPath("$.data.id").value(1))
                .andExpect(jsonPath("$.data.username").value("testuser"));

        verify(userService).register(any(User.class));
    }

    @Test
    @DisplayName("用户注册失败 - 手机号已存在")
    void testRegisterFailPhoneExists() throws Exception {
        // Given
        when(userService.register(any(User.class))).thenReturn(null);

        // When & Then
        mockMvc.perform(post("/api/user/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(testUser)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(400))
                .andExpect(jsonPath("$.msg").value("手机号已注册"));

        verify(userService).register(any(User.class));
    }

    @Test
    @DisplayName("用户登录成功")
    void testLoginSuccess() throws Exception {
        // Given
        String phone = "13800138000";
        String password = "123456";
        when(userService.login(phone, password)).thenReturn(testUser);

        // 创建登录请求对象
        Object loginRequest = new Object() {
            public final String phone = "13800138000";
            public final String password = "123456";
        };

        // When & Then
        mockMvc.perform(post("/api/user/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(loginRequest)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("登录成功"))
                .andExpect(jsonPath("$.data.id").value(1))
                .andExpect(jsonPath("$.data.username").value("testuser"));

        verify(userService).login(phone, password);
    }

    @Test
    @DisplayName("用户登录失败 - 密码错误")
    void testLoginFailWrongPassword() throws Exception {
        // Given
        String phone = "13800138000";
        String wrongPassword = "wrongpassword";
        when(userService.login(phone, wrongPassword)).thenReturn(null);

        // 创建登录请求对象
        Object loginRequest = new Object() {
            public final String phone = "13800138000";
            public final String password = "wrongpassword";
        };

        // When & Then
        mockMvc.perform(post("/api/user/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(loginRequest)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(400))
                .andExpect(jsonPath("$.msg").value("手机号或密码错误"));

        verify(userService).login(phone, wrongPassword);
    }

    @Test
    @DisplayName("获取所有用户列表成功")
    void testGetAllUsersSuccess() throws Exception {
        // Given
        List<User> userList = Arrays.asList(testUser);
        when(userService.getAllUsers()).thenReturn(userList);

        // When & Then
        mockMvc.perform(get("/api/user/admin/list"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("成功"))
                .andExpect(jsonPath("$.data").isArray())
                .andExpect(jsonPath("$.data[0].id").value(1))
                .andExpect(jsonPath("$.data[0].username").value("testuser"));

        verify(userService).getAllUsers();
    }

    @Test
    @DisplayName("获取用户个人信息成功")
    void testGetUserProfileSuccess() throws Exception {
        // Given
        Long userId = 1L;
        when(userService.getUserProfileById(userId)).thenReturn(userProfileDto);

        // When & Then
        mockMvc.perform(get("/api/user/{userId}/profile", userId))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("获取用户信息成功"))
                .andExpect(jsonPath("$.data.id").value(1))
                .andExpect(jsonPath("$.data.username").value("testuser"))
                .andExpect(jsonPath("$.data.phone").value("13800138000"))
                .andExpect(jsonPath("$.data.realName").value("测试用户"));

        verify(userService).getUserProfileById(userId);
    }

    @Test
    @DisplayName("获取用户个人信息失败 - 用户不存在")
    void testGetUserProfileNotFound() throws Exception {
        // Given
        Long userId = 999L;
        when(userService.getUserProfileById(userId))
                .thenThrow(new EntityNotFoundException("User not found with id: " + userId));

        // When & Then
        mockMvc.perform(get("/api/user/{userId}/profile", userId))
                .andDo(print())
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value(404));

        verify(userService).getUserProfileById(userId);
    }

    @Test
    @DisplayName("更新用户个人信息成功")
    void testUpdateUserProfileSuccess() throws Exception {
        // Given
        Long userId = 1L;
        UpdateProfileRequestDTO profileDto = new UpdateProfileRequestDTO();
        profileDto.setUsername("updateduser");
        profileDto.setRealName("更新的用户");
        profileDto.setIdCard("987654321098765432");

        UserProfileResponseDTO updatedDto = new UserProfileResponseDTO(
                1L, "updateduser", "13800138000", "更新的用户", "987654321098765432", UserType.PASSENGER
        );

        when(userService.updateUserProfile(eq(userId), any(UpdateProfileRequestDTO.class)))
                .thenReturn(updatedDto);

        // When & Then
        mockMvc.perform(put("/api/user/{userId}/profile", userId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(profileDto)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("用户信息更新成功"))
                .andExpect(jsonPath("$.data.username").value("updateduser"))
                .andExpect(jsonPath("$.data.realName").value("更新的用户"));

        verify(userService).updateUserProfile(eq(userId), any(UpdateProfileRequestDTO.class));
    }

    @Test
    @DisplayName("更新用户状态成功")
    void testUpdateUserStatusSuccess() throws Exception {
        // Given
        Long userId = 1L;
        Integer status = 0; // 禁用
        testUser.setStatus(status);
        when(userService.updateUserStatus(userId, status)).thenReturn(testUser);

        // 创建请求参数Map
        Object statusRequest = new Object() {
            public final String userId = "1";
            public final String status = "0";
        };

        // When & Then
        mockMvc.perform(post("/api/user/admin/status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(statusRequest)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("修改成功"))
                .andExpect(jsonPath("$.data.status").value(0));

        verify(userService).updateUserStatus(userId, status);
    }

    @Test
    @DisplayName("获取用户类型列表成功")
    void testGetUserTypesSuccess() throws Exception {
        // When & Then
        mockMvc.perform(get("/api/user/types"))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("成功"))
                .andExpect(jsonPath("$.data").isArray())
                .andExpect(jsonPath("$.data[0].value").exists())
                .andExpect(jsonPath("$.data[0].label").exists());
    }

    @Test
    @DisplayName("修改密码成功")
    void testUpdatePasswordSuccess() throws Exception {
        // Given
        Long userId = 1L;
        UpdatePasswordRequestDTO passwordDto = new UpdatePasswordRequestDTO();
        passwordDto.setOldPassword("123456");
        passwordDto.setNewPassword("newpassword123");

        when(userService.updatePassword(userId, "123456", "newpassword123")).thenReturn(true);

        // When & Then
        mockMvc.perform(put("/api/user/{userId}/password", userId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(passwordDto)))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200))
                .andExpect(jsonPath("$.msg").value("密码修改成功"));

        verify(userService).updatePassword(userId, "123456", "newpassword123");
    }

    @Test
    @DisplayName("修改密码失败 - 旧密码错误")
    void testUpdatePasswordFailWrongOldPassword() throws Exception {
        // Given
        Long userId = 1L;
        UpdatePasswordRequestDTO passwordDto = new UpdatePasswordRequestDTO();
        passwordDto.setOldPassword("wrongpassword");
        passwordDto.setNewPassword("newpassword123");

        when(userService.updatePassword(userId, "wrongpassword", "newpassword123")).thenReturn(false);

        // When & Then
        mockMvc.perform(put("/api/user/{userId}/password", userId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(passwordDto)))
                .andDo(print())
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value(400))
                .andExpect(jsonPath("$.msg").value("旧密码不正确"));

        verify(userService).updatePassword(userId, "wrongpassword", "newpassword123");
    }

    @Test
    @DisplayName("修改密码失败 - 用户不存在")
    void testUpdatePasswordFailUserNotFound() throws Exception {
        // Given
        Long userId = 999L;
        UpdatePasswordRequestDTO passwordDto = new UpdatePasswordRequestDTO();
        passwordDto.setOldPassword("123456");
        passwordDto.setNewPassword("newpassword123");

        when(userService.updatePassword(userId, "123456", "newpassword123"))
                .thenThrow(new EntityNotFoundException("User not found with id: " + userId));

        // When & Then
        mockMvc.perform(put("/api/user/{userId}/password", userId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(passwordDto)))
                .andDo(print())
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value(404));

        verify(userService).updatePassword(userId, "123456", "newpassword123");
    }

    @Test
    @DisplayName("参数验证失败")
    void testValidationFail() throws Exception {
        // Given - 创建一个空的用户对象
        User invalidUser = new User();

        // When & Then
        mockMvc.perform(post("/api/user/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidUser)))
                .andDo(print())
                .andExpect(status().isOk()); // 由于控制器返回的是Result对象，HTTP状态仍是200

        // 这里可以验证service层没有被调用，或者根据实际业务逻辑调整
    }
} 