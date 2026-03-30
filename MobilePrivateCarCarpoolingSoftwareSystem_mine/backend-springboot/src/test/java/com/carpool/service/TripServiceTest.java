package com.carpool.service;

import com.carpool.dto.OrderDTO;
import com.carpool.dto.TripWithOrdersDTO;
import com.carpool.model.Car;
import com.carpool.model.Order;
import com.carpool.model.Trip;
import com.carpool.model.User;
import com.carpool.repository.CarRepository;
import com.carpool.repository.OrderRepository;
import com.carpool.repository.TripRepository;
import com.carpool.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("行程服务测试")
class TripServiceTest {

    @Mock
    private TripRepository tripRepository;
    
    @Mock
    private CarRepository carRepository;
    
    @Mock
    private OrderRepository orderRepository;
    
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private TripService tripService;

    private Trip testTrip;
    private Car testCar;
    private User testDriver;
    private User testPassenger;
    private Order testOrder;

    @BeforeEach
    void setUp() {
        // 准备测试数据
        testDriver = new User();
        testDriver.setId(1L);
        testDriver.setUsername("司机小李");

        testPassenger = new User();
        testPassenger.setId(2L);
        testPassenger.setUsername("乘客小王");

        testCar = new Car();
        testCar.setId(1L);
        testCar.setBrand("丰田");
        testCar.setModel("凯美瑞");
        testCar.setColor("白色");
        testCar.setPlateNumber("粤B12345");
        testCar.setSeatCount(5);

        testTrip = new Trip();
        testTrip.setId(1L);
        testTrip.setDriverId(1L);
        testTrip.setCarId(1L);
        testTrip.setStartLocation("深圳南山");
        testTrip.setEndLocation("深圳宝安");
        testTrip.setStartLng(113.9308);
        testTrip.setStartLat(22.5329);
        testTrip.setEndLng(113.8889);
        testTrip.setEndLat(22.5551);
        testTrip.setDepartureTime(new Date());
        testTrip.setPrice(25.0);
        testTrip.setSeatAvailable(3);
        testTrip.setStatus(1); // 发布中

        testOrder = new Order();
        testOrder.setId(1L);
        testOrder.setTripId(1L);
        testOrder.setPassengerId(2L);
        testOrder.setOrderStatus(1);
    }

    @Test
    @DisplayName("搜索附近行程成功")
    void testSearchTripsSuccess() {
        // Given
        Double startLng = 113.9308;
        Double startLat = 22.5329;
        Double endLng = 113.8889;
        Double endLat = 22.5551;
        Date departureTime = new Date();
        
        List<Trip> mockTrips = Arrays.asList(testTrip);
        when(tripRepository.findNearbyTrips(eq(startLng), eq(startLat), eq(endLng), eq(endLat), 
                eq(departureTime), eq(5000.0), eq(2000.0))).thenReturn(mockTrips);
        when(carRepository.findById(1L)).thenReturn(Optional.of(testCar));

        // When
        List<Trip> result = tripService.searchTrips(startLng, startLat, endLng, endLat, departureTime);

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        Trip resultTrip = result.get(0);
        assertEquals(testTrip.getId(), resultTrip.getId());
        assertNotNull(resultTrip.getCarInfo()); // 验证车辆信息已加载
        verify(tripRepository).findNearbyTrips(startLng, startLat, endLng, endLat, departureTime, 5000.0, 2000.0);
    }

    @Test
    @DisplayName("发布行程成功")
    void testPublishTripSuccess() {
        // Given
        when(tripRepository.save(testTrip)).thenReturn(testTrip);

        // When
        Trip result = tripService.publishTrip(testTrip);

        // Then
        assertNotNull(result);
        assertEquals(testTrip.getId(), result.getId());
        assertEquals(testTrip.getStartLocation(), result.getStartLocation());
        verify(tripRepository).save(testTrip);
    }

    @Test
    @DisplayName("根据ID查找行程成功")
    void testFindTripByIdSuccess() {
        // Given
        Long tripId = 1L;
        when(tripRepository.findById(tripId)).thenReturn(Optional.of(testTrip));

        // When
        Trip result = tripService.findTripById(tripId);

        // Then
        assertNotNull(result);
        assertEquals(testTrip.getId(), result.getId());
        verify(tripRepository).findById(tripId);
    }

    @Test
    @DisplayName("根据ID查找行程失败 - 行程不存在")
    void testFindTripByIdNotFound() {
        // Given
        Long tripId = 999L;
        when(tripRepository.findById(tripId)).thenReturn(Optional.empty());

        // When
        Trip result = tripService.findTripById(tripId);

        // Then
        assertNull(result);
        verify(tripRepository).findById(tripId);
    }

    @Test
    @DisplayName("根据司机ID查找行程和订单信息成功")
    void testFindTripsByDriverIdSuccess() {
        // Given
        Long driverId = 1L;
        List<Trip> trips = Arrays.asList(testTrip);
        List<Order> orders = Arrays.asList(testOrder);
        List<User> passengers = Arrays.asList(testPassenger);

        when(tripRepository.findByDriverIdOrderByDepartureTimeDesc(driverId)).thenReturn(trips);
        when(orderRepository.findByTripIdIn(Arrays.asList(1L))).thenReturn(orders);
        when(userRepository.findAllById(Arrays.asList(2L))).thenReturn(passengers);
        when(carRepository.findById(1L)).thenReturn(Optional.of(testCar));

        // When
        List<TripWithOrdersDTO> result = tripService.findTripsByDriverId(driverId);

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        TripWithOrdersDTO tripWithOrders = result.get(0);
        assertEquals(1, tripWithOrders.getOrders().size());
        assertEquals("乘客小王", tripWithOrders.getOrders().get(0).getPassengerName());
        verify(tripRepository).findByDriverIdOrderByDepartureTimeDesc(driverId);
    }

    @Test
    @DisplayName("根据司机ID查找行程 - 无行程")
    void testFindTripsByDriverIdEmpty() {
        // Given
        Long driverId = 1L;
        when(tripRepository.findByDriverIdOrderByDepartureTimeDesc(driverId)).thenReturn(Collections.emptyList());

        // When
        List<TripWithOrdersDTO> result = tripService.findTripsByDriverId(driverId);

        // Then
        assertNotNull(result);
        assertTrue(result.isEmpty());
        verify(tripRepository).findByDriverIdOrderByDepartureTimeDesc(driverId);
    }

    @Test
    @DisplayName("删除行程成功")
    void testDeleteTripSuccess() {
        // Given
        Long tripId = 1L;
        Long driverId = 1L;
        when(tripRepository.findById(tripId)).thenReturn(Optional.of(testTrip));

        // When
        boolean result = tripService.deleteTrip(tripId, driverId);

        // Then
        assertTrue(result);
        verify(tripRepository).findById(tripId);
        verify(tripRepository).deleteById(tripId);
    }

    @Test
    @DisplayName("删除行程失败 - 不是行程发布者")
    void testDeleteTripFailNotOwner() {
        // Given
        Long tripId = 1L;
        Long wrongDriverId = 999L;
        when(tripRepository.findById(tripId)).thenReturn(Optional.of(testTrip));

        // When
        boolean result = tripService.deleteTrip(tripId, wrongDriverId);

        // Then
        assertFalse(result);
        verify(tripRepository).findById(tripId);
        verify(tripRepository, never()).deleteById(any());
    }

    @Test
    @DisplayName("删除行程失败 - 行程不存在")
    void testDeleteTripFailNotFound() {
        // Given
        Long tripId = 999L;
        Long driverId = 1L;
        when(tripRepository.findById(tripId)).thenReturn(Optional.empty());

        // When
        boolean result = tripService.deleteTrip(tripId, driverId);

        // Then
        assertFalse(result);
        verify(tripRepository).findById(tripId);
        verify(tripRepository, never()).deleteById(any());
    }

    @Test
    @DisplayName("取消行程成功")
    void testCancelTripSuccess() {
        // Given
        Long tripId = 1L;
        Long driverId = 1L;
        testTrip.setStatus(1); // 发布中状态
        
        when(tripRepository.findById(tripId)).thenReturn(Optional.of(testTrip));
        when(tripRepository.save(any(Trip.class))).thenReturn(testTrip);

        // When
        Trip result = tripService.cancelTrip(tripId, driverId);

        // Then
        assertNotNull(result);
        assertEquals(4, testTrip.getStatus()); // 已取消状态
        verify(tripRepository).findById(tripId);
        verify(tripRepository).save(testTrip);
    }

    @Test
    @DisplayName("取消行程失败 - 行程状态不允许取消")
    void testCancelTripFailWrongStatus() {
        // Given
        Long tripId = 1L;
        Long driverId = 1L;
        testTrip.setStatus(2); // 进行中状态，不能取消
        
        when(tripRepository.findById(tripId)).thenReturn(Optional.of(testTrip));

        // When
        Trip result = tripService.cancelTrip(tripId, driverId);

        // Then
        assertNull(result);
        verify(tripRepository).findById(tripId);
        verify(tripRepository, never()).save(any());
    }

    @Test
    @DisplayName("取消行程失败 - 不是行程发布者")
    void testCancelTripFailNotOwner() {
        // Given
        Long tripId = 1L;
        Long wrongDriverId = 999L;
        testTrip.setStatus(1);
        
        when(tripRepository.findById(tripId)).thenReturn(Optional.of(testTrip));

        // When
        Trip result = tripService.cancelTrip(tripId, wrongDriverId);

        // Then
        assertNull(result);
        verify(tripRepository).findById(tripId);
        verify(tripRepository, never()).save(any());
    }

    @Test
    @DisplayName("管理员查询所有行程")
    void testFindAllTrips() {
        // Given
        List<Trip> allTrips = Arrays.asList(testTrip);
        when(tripRepository.findAll()).thenReturn(allTrips);

        // When
        List<Trip> result = tripService.findAllTrips();

        // Then
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals(testTrip.getId(), result.get(0).getId());
        verify(tripRepository).findAll();
    }

    @Test
    @DisplayName("管理员删除行程成功")
    void testAdminDeleteTripSuccess() {
        // Given
        Long tripId = 1L;
        when(tripRepository.findById(tripId)).thenReturn(Optional.of(testTrip));
        when(tripRepository.save(any(Trip.class))).thenReturn(testTrip);

        // When
        boolean result = tripService.adminDeleteTrip(tripId);

        // Then
        assertTrue(result);
        assertEquals(4, testTrip.getStatus()); // 已取消状态
        verify(tripRepository).findById(tripId);
        verify(tripRepository).save(testTrip);
    }

    @Test
    @DisplayName("管理员删除行程失败 - 行程不存在")
    void testAdminDeleteTripFailNotFound() {
        // Given
        Long tripId = 999L;
        when(tripRepository.findById(tripId)).thenReturn(Optional.empty());

        // When
        boolean result = tripService.adminDeleteTrip(tripId);

        // Then
        assertFalse(result);
        verify(tripRepository).findById(tripId);
        verify(tripRepository, never()).save(any());
    }

    @Test
    @DisplayName("加载车辆信息成功")
    void testLoadCarInfoSuccess() {
        // Given
        testTrip.setCarId(1L);
        when(carRepository.findById(1L)).thenReturn(Optional.of(testCar));

        // When
        List<Trip> trips = Arrays.asList(testTrip);
        when(tripRepository.findNearbyTrips(any(), any(), any(), any(), any(), any(), any())).thenReturn(trips);
        List<Trip> result = tripService.searchTrips(113.0, 22.0, 114.0, 23.0, new Date());

        // Then
        assertNotNull(result);
        Trip resultTrip = result.get(0);
        assertNotNull(resultTrip.getCarInfo());
        @SuppressWarnings("unchecked")
        Map<String, Object> carInfo = (Map<String, Object>) resultTrip.getCarInfo();
        assertEquals("丰田", carInfo.get("brand"));
        assertEquals("凯美瑞", carInfo.get("model"));
        assertEquals("白色", carInfo.get("color"));
        assertEquals("粤B12345", carInfo.get("plateNumber"));
        assertEquals(5, carInfo.get("seatCount"));
    }

    @Test
    @DisplayName("加载车辆信息 - 车辆不存在")
    void testLoadCarInfoNotFound() {
        // Given
        testTrip.setCarId(999L);
        when(carRepository.findById(999L)).thenReturn(Optional.empty());

        // When
        List<Trip> trips = Arrays.asList(testTrip);
        when(tripRepository.findNearbyTrips(any(), any(), any(), any(), any(), any(), any())).thenReturn(trips);
        List<Trip> result = tripService.searchTrips(113.0, 22.0, 114.0, 23.0, new Date());

        // Then
        assertNotNull(result);
        Trip resultTrip = result.get(0);
        assertNull(resultTrip.getCarInfo()); // 车辆信息为空
    }
} 