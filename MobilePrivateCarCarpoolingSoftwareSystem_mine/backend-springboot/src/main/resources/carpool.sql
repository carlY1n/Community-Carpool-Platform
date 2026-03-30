/*
 Navicat Premium Data Transfer

 Source Server         : changqing
 Source Server Type    : MySQL
 Source Server Version : 80039
 Source Host           : localhost:3306
 Source Schema         : carpool

 Target Server Type    : MySQL
 Target Server Version : 80039
 File Encoding         : 65001

 Date: 09/06/2025 20:29:34
*/
CREATE DATABASE IF NOT EXISTS carpool
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
USE carpool;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for car
-- ----------------------------
DROP TABLE IF EXISTS `car`;
CREATE TABLE `car`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` bigint NOT NULL COMMENT '所属用户ID',
  `plate_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '车牌号',
  `brand` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '品牌',
  `model` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '车型',
  `color` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '颜色',
  `seat_count` int NULL DEFAULT 4 COMMENT '座位数',
  `audit_status` tinyint NULL DEFAULT 0 COMMENT '审核状态（0未审核 1通过 2拒绝）',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `car_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '车辆表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for carpool_order
-- ----------------------------
DROP TABLE IF EXISTS `carpool_order`;
CREATE TABLE `carpool_order`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `trip_id` bigint NOT NULL COMMENT '行程ID',
  `passenger_id` bigint NOT NULL COMMENT '乘客用户ID',
  `seat_count` int NULL DEFAULT 1 COMMENT '预订座位数',
  `order_status` tinyint NULL DEFAULT 0 COMMENT '订单状态（0待确认 1已确认 2已完成 3已取消）',
  `order_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
  `pay_status` tinyint NULL DEFAULT 0 COMMENT '支付状态（0未支付 1已支付 2已退款）',
  `amount` decimal(10, 2) NOT NULL COMMENT '订单金额',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `trip_id`(`trip_id` ASC) USING BTREE,
  INDEX `passenger_id`(`passenger_id` ASC) USING BTREE,
  CONSTRAINT `carpool_order_ibfk_1` FOREIGN KEY (`trip_id`) REFERENCES `trip` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `carpool_order_ibfk_2` FOREIGN KEY (`passenger_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '拼车订单表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for chat_message
-- ----------------------------
DROP TABLE IF EXISTS `chat_message`;
CREATE TABLE `chat_message`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NULL DEFAULT NULL,
  `sender_id` bigint NULL DEFAULT NULL,
  `receiver_id` bigint NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `message_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT NULL,
  `status` int NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for complaint
-- ----------------------------
DROP TABLE IF EXISTS `complaint`;
CREATE TABLE `complaint`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `complainant_id` bigint NOT NULL COMMENT '投诉人ID',
  `content` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '投诉内容',
  `status` tinyint NULL DEFAULT 0 COMMENT '处理状态（0待处理 1已处理）',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '投诉时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `complainant_id`(`complainant_id` ASC) USING BTREE,
  CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `carpool_order` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `complaint_ibfk_2` FOREIGN KEY (`complainant_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '投诉表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for review
-- ----------------------------
DROP TABLE IF EXISTS `review`;
CREATE TABLE `review`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `order_id` bigint NOT NULL COMMENT '订单ID',
  `reviewer_id` bigint NOT NULL COMMENT '评价人ID',
  `reviewee_id` bigint NOT NULL COMMENT '被评价人ID',
  `rating` int NOT NULL COMMENT '评分（1-5分）',
  `content` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '评价内容',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '评价时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `reviewer_id`(`reviewer_id` ASC) USING BTREE,
  INDEX `reviewee_id`(`reviewee_id` ASC) USING BTREE,
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `carpool_order` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`reviewer_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `review_ibfk_3` FOREIGN KEY (`reviewee_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '评价表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for trip
-- ----------------------------
DROP TABLE IF EXISTS `trip`;
CREATE TABLE `trip`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `driver_id` bigint NOT NULL COMMENT '车主用户ID',
  `car_id` bigint NOT NULL COMMENT '车辆ID',
  `start_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '起点地址',
  `start_lng` double NULL DEFAULT NULL COMMENT '起点经度',
  `start_lat` double NULL DEFAULT NULL COMMENT '起点纬度',
  `end_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '终点地址',
  `end_lng` double NULL DEFAULT NULL COMMENT '终点经度',
  `end_lat` double NULL DEFAULT NULL COMMENT '终点纬度',
  `via_points` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '途径点（JSON或逗号分隔）',
  `departure_time` datetime NOT NULL COMMENT '出发时间',
  `price` decimal(10, 2) NOT NULL COMMENT '拼车价格',
  `seat_available` int NOT NULL COMMENT '可用座位数',
  `status` tinyint NULL DEFAULT 1 COMMENT '状态（1发布中 2已满员 3已结束 4已取消）',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `driver_id`(`driver_id` ASC) USING BTREE,
  INDEX `car_id`(`car_id` ASC) USING BTREE,
  CONSTRAINT `trip_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `trip_ibfk_2` FOREIGN KEY (`car_id`) REFERENCES `car` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '行程表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码（加密存储）',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '手机号',
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '真实姓名',
  `id_card` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '身份证号',
  `user_type` enum('PASSENGER','DRIVER','ADMIN') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户类型（乘客passenger/车主driver管理员admin）',
  `status` tinyint NULL DEFAULT 1 COMMENT '状态（1正常 0禁用）',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;

-- 用户
INSERT INTO user (username, password, phone, real_name, id_card, user_type, status) VALUES
('zhangsan', 'e10adc3949ba59abbe56e057f20f883e', '13800000001', '张三', '110101199001010011', 'DRIVER', 1),
('lisi', 'e10adc3949ba59abbe56e057f20f883e', '13800000002', '李四', '110101199202020022', 'PASSENGER', 1),
('admin', 'e10adc3949ba59abbe56e057f20f883e', '13800000000', '管理员', '000000000000000000', 'ADMIN', 1);
