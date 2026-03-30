package com.carpool.service;

import com.carpool.dto.UpdateProfileRequestDTO;
import com.carpool.dto.UserProfileResponseDTO;
import com.carpool.model.User;
import com.carpool.model.UserType;
import com.carpool.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import javax.persistence.EntityNotFoundException;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("用户服务测试")
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    private User testUser;
    private User existingUser;

    @BeforeEach
    void setUp() {
        // 准备测试用户数据
        testUser = new User();
        testUser.setId(1L);
        testUser.setUsername("testuser");
        testUser.setPhone("13800138000");
        testUser.setPassword("123456");
        testUser.setRealName("测试用户");
        testUser.setUserType(UserType.PASSENGER);
        testUser.setStatus(1);
        testUser.setCreateTime(new Date());

        existingUser = new User();
        existingUser.setId(2L);
        existingUser.setUsername("existing");
        existingUser.setPhone("13800138001");
        existingUser.setPassword("existing123");
        existingUser.setUserType(UserType.DRIVER);
        existingUser.setStatus(1);
    }

    @Test
    @DisplayName("用户注册成功")
    void testRegisterSuccess() {
        // Given
        User newUser = new User();
        newUser.setUsername("newuser");
        newUser.setPhone("13900139000");
        newUser.setPassword("password123");

        when(userRepository.findByPhone(newUser.getPhone())).thenReturn(null);
        when(userRepository.save(any(User.class))).thenReturn(testUser);

        // When
        User result = userService.register(newUser);

        // Then
        assertNotNull(result);
        assertEquals(UserType.PASSENGER, newUser.getUserType()); // 默认设置为乘客
        assertEquals(1, newUser.getStatus()); // 状态设置为启用
        assertNotNull(newUser.getCreateTime()); // 创建时间不为空
        verify(userRepository).findByPhone(newUser.getPhone());
        verify(userRepository).save(newUser);
    }

    @Test
    @DisplayName("用户注册失败 - 手机号已存在")
    void testRegisterFailPhoneExists() {
        // Given
        User newUser = new User();
        newUser.setPhone("13800138000");

        when(userRepository.findByPhone(newUser.getPhone())).thenReturn(existingUser);

        // When
        User result = userService.register(newUser);

        // Then
        assertNull(result);
        verify(userRepository).findByPhone(newUser.getPhone());
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("用户登录成功")
    void testLoginSuccess() {
        // Given
        String phone = "13800138000";
        String password = "123456";

        when(userRepository.findByPhone(phone)).thenReturn(testUser);

        // When
        User result = userService.login(phone, password);

        // Then
        assertNotNull(result);
        assertEquals(testUser.getId(), result.getId());
        assertEquals(testUser.getUsername(), result.getUsername());
        verify(userRepository).findByPhone(phone);
    }

    @Test
    @DisplayName("用户登录失败 - 密码错误")
    void testLoginFailWrongPassword() {
        // Given
        String phone = "13800138000";
        String wrongPassword = "wrongpassword";

        when(userRepository.findByPhone(phone)).thenReturn(testUser);

        // When
        User result = userService.login(phone, wrongPassword);

        // Then
        assertNull(result);
        verify(userRepository).findByPhone(phone);
    }

    @Test
    @DisplayName("用户登录失败 - 用户不存在")
    void testLoginFailUserNotFound() {
        // Given
        String phone = "19900199000";
        String password = "123456";

        when(userRepository.findByPhone(phone)).thenReturn(null);

        // When
        User result = userService.login(phone, password);

        // Then
        assertNull(result);
        verify(userRepository).findByPhone(phone);
    }

    @Test
    @DisplayName("获取所有用户列表")
    void testGetAllUsers() {
        // Given
        List<User> userList = Arrays.asList(testUser, existingUser);
        when(userRepository.findAll()).thenReturn(userList);

        // When
        List<User> result = userService.getAllUsers();

        // Then
        assertNotNull(result);
        assertEquals(2, result.size());
        assertTrue(result.contains(testUser));
        assertTrue(result.contains(existingUser));
        verify(userRepository).findAll();
    }

    @Test
    @DisplayName("根据ID查找用户成功")
    void testFindByIdSuccess() {
        // Given
        Long userId = 1L;
        when(userRepository.findById(userId)).thenReturn(Optional.of(testUser));

        // When
        User result = userService.findById(userId);

        // Then
        assertNotNull(result);
        assertEquals(testUser.getId(), result.getId());
        verify(userRepository).findById(userId);
    }

    @Test
    @DisplayName("根据ID查找用户失败 - 用户不存在")
    void testFindByIdNotFound() {
        // Given
        Long userId = 999L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // When
        User result = userService.findById(userId);

        // Then
        assertNull(result);
        verify(userRepository).findById(userId);
    }

    @Test
    @DisplayName("更新用户状态成功")
    void testUpdateUserStatusSuccess() {
        // Given
        Long userId = 1L;
        Integer newStatus = 0; // 禁用
        when(userRepository.findById(userId)).thenReturn(Optional.of(testUser));
        when(userRepository.save(any(User.class))).thenReturn(testUser);

        // When
        User result = userService.updateUserStatus(userId, newStatus);

        // Then
        assertNotNull(result);
        assertEquals(newStatus, testUser.getStatus());
        verify(userRepository).findById(userId);
        verify(userRepository).save(testUser);
    }

    @Test
    @DisplayName("获取用户个人信息成功")
    void testGetUserProfileByIdSuccess() {
        // Given
        Long userId = 1L;
        when(userRepository.findById(userId)).thenReturn(Optional.of(testUser));

        // When
        UserProfileResponseDTO result = userService.getUserProfileById(userId);

        // Then
        assertNotNull(result);
        assertEquals(testUser.getId(), result.getId());
        assertEquals(testUser.getUsername(), result.getUsername());
        assertEquals(testUser.getPhone(), result.getPhone());
        assertEquals(testUser.getRealName(), result.getRealName());
        assertEquals(testUser.getUserType(), result.getUserType());
        verify(userRepository).findById(userId);
    }

    @Test
    @DisplayName("获取用户个人信息失败 - 用户不存在")
    void testGetUserProfileByIdNotFound() {
        // Given
        Long userId = 999L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(EntityNotFoundException.class, () -> {
            userService.getUserProfileById(userId);
        });
        verify(userRepository).findById(userId);
    }

    @Test
    @DisplayName("更新用户基本信息成功")
    void testUpdateUserProfileSuccess() {
        // Given
        Long userId = 1L;
        UpdateProfileRequestDTO profileDto = new UpdateProfileRequestDTO();
        profileDto.setUsername("updateduser");
        profileDto.setRealName("更新的用户");
        profileDto.setIdCard("123456789012345678");

        when(userRepository.findById(userId)).thenReturn(Optional.of(testUser));
        when(userRepository.save(any(User.class))).thenReturn(testUser);

        // When
        UserProfileResponseDTO result = userService.updateUserProfile(userId, profileDto);

        // Then
        assertNotNull(result);
        assertEquals(profileDto.getUsername(), testUser.getUsername());
        assertEquals(profileDto.getRealName(), testUser.getRealName());
        assertEquals(profileDto.getIdCard(), testUser.getIdCard());
        verify(userRepository).findById(userId);
        verify(userRepository).save(testUser);
    }

    @Test
    @DisplayName("修改密码成功")
    void testUpdatePasswordSuccess() {
        // Given
        Long userId = 1L;
        String oldPassword = "123456";
        String newPassword = "newpassword123";

        when(userRepository.findById(userId)).thenReturn(Optional.of(testUser));
        when(userRepository.save(any(User.class))).thenReturn(testUser);

        // When
        boolean result = userService.updatePassword(userId, oldPassword, newPassword);

        // Then
        assertTrue(result);
        assertEquals(newPassword, testUser.getPassword());
        verify(userRepository).findById(userId);
        verify(userRepository).save(testUser);
    }

    @Test
    @DisplayName("修改密码失败 - 旧密码错误")
    void testUpdatePasswordFailWrongOldPassword() {
        // Given
        Long userId = 1L;
        String wrongOldPassword = "wrongpassword";
        String newPassword = "newpassword123";

        when(userRepository.findById(userId)).thenReturn(Optional.of(testUser));

        // When
        boolean result = userService.updatePassword(userId, wrongOldPassword, newPassword);

        // Then
        assertFalse(result);
        assertEquals("123456", testUser.getPassword()); // 密码未改变
        verify(userRepository).findById(userId);
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("修改密码失败 - 用户不存在")
    void testUpdatePasswordFailUserNotFound() {
        // Given
        Long userId = 999L;
        String oldPassword = "123456";
        String newPassword = "newpassword123";

        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // When & Then
        assertThrows(EntityNotFoundException.class, () -> {
            userService.updatePassword(userId, oldPassword, newPassword);
        });
        verify(userRepository).findById(userId);
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("注册时设置默认真实姓名")
    void testRegisterWithDefaultRealName() {
        // Given
        User newUser = new User();
        newUser.setUsername("testuser");
        newUser.setPhone("13900139000");
        newUser.setPassword("password123");
        // 不设置 realName

        when(userRepository.findByPhone(newUser.getPhone())).thenReturn(null);
        when(userRepository.save(any(User.class))).thenReturn(newUser);

        // When
        User result = userService.register(newUser);

        // Then
        assertNotNull(result);
        assertEquals(newUser.getUsername(), newUser.getRealName()); // 真实姓名默认为用户名
        verify(userRepository).save(newUser);
    }
} 