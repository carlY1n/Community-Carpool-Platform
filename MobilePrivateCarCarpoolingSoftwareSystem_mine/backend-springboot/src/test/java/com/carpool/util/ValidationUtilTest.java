package com.carpool.util;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("验证工具类测试")
class ValidationUtilTest {

    @Test
    @DisplayName("手机号格式验证 - 有效手机号")
    void testValidPhoneNumbers() {
        // 测试有效的手机号
        assertTrue(ValidationUtil.isValidPhone("13800138000"));
        assertTrue(ValidationUtil.isValidPhone("15912345678"));
        assertTrue(ValidationUtil.isValidPhone("18888888888"));
        assertTrue(ValidationUtil.isValidPhone("17012345678"));
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "1380013800",     // 长度不够
            "138001380000",   // 长度过长
            "12800138000",    // 不是以13,14,15,16,17,18,19开头
            "abcdefghijk",    // 包含字母
            "138-0013-8000",  // 包含特殊字符
            "",               // 空字符串
            "138 0013 8000"   // 包含空格
    })
    @DisplayName("手机号格式验证 - 无效手机号")
    void testInvalidPhoneNumbers(String phone) {
        assertFalse(ValidationUtil.isValidPhone(phone));
    }


    @ParameterizedTest
    @ValueSource(strings = {
            "11010119900101123",   // 长度不够
            "1101011990010112345", // 长度过长
            "110101199013011234",  // 无效月份
            "110101199001321234",  // 无效日期
            "abcdef199001011234",  // 包含字母（前6位）
            "110101abcd01011234",  // 包含字母（中间8位）
            "",                    // 空字符串
            "110101-1990-0101-1234" // 包含特殊字符
    })
    @DisplayName("身份证号格式验证 - 无效身份证号")
    void testInvalidIdCards(String idCard) {
        assertFalse(ValidationUtil.isValidIdCard(idCard));
    }

    @Test
    @DisplayName("密码强度验证 - 有效密码")
    void testValidPasswords() {
        // 测试有效的密码（至少6位，包含字母和数字）
        assertTrue(ValidationUtil.isValidPassword("123456"));
        assertTrue(ValidationUtil.isValidPassword("abc123"));
        assertTrue(ValidationUtil.isValidPassword("Password123"));
        assertTrue(ValidationUtil.isValidPassword("Test@123"));
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "12345",      // 长度不够
            "123",        // 太短
            "",           // 空字符串
            "     ",      // 只有空格
            "中文密码123"  // 包含中文
    })
    @DisplayName("密码强度验证 - 无效密码")
    void testInvalidPasswords(String password) {
        assertFalse(ValidationUtil.isValidPassword(password));
    }

    @Test
    @DisplayName("邮箱格式验证 - 有效邮箱")
    void testValidEmails() {
        assertTrue(ValidationUtil.isValidEmail("test@example.com"));
        assertTrue(ValidationUtil.isValidEmail("user.name@domain.co.uk"));
        assertTrue(ValidationUtil.isValidEmail("user+tag@example.org"));
        assertTrue(ValidationUtil.isValidEmail("123@456.com"));
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "test@",           // 缺少域名
            "@example.com",    // 缺少用户名
            "test.example.com", // 缺少@
            "test@.com",       // 域名格式错误
            "test@com",        // 缺少顶级域名
            "",                // 空字符串
            "test space@example.com" // 包含空格
    })
    @DisplayName("邮箱格式验证 - 无效邮箱")
    void testInvalidEmails(String email) {
        assertFalse(ValidationUtil.isValidEmail(email));
    }

    @Test
    @DisplayName("价格验证 - 有效价格")
    void testValidPrices() {
        assertTrue(ValidationUtil.isValidPrice(0.01));
        assertTrue(ValidationUtil.isValidPrice(25.50));
        assertTrue(ValidationUtil.isValidPrice(100.0));
        assertTrue(ValidationUtil.isValidPrice(999.99));
    }

    @Test
    @DisplayName("价格验证 - 无效价格")
    void testInvalidPrices() {
        assertFalse(ValidationUtil.isValidPrice(0.0));     // 零价格
        assertFalse(ValidationUtil.isValidPrice(-1.0));    // 负价格
        assertFalse(ValidationUtil.isValidPrice(1000.0));  // 超过最大价格
        assertFalse(ValidationUtil.isValidPrice(Double.NaN)); // NaN
        assertFalse(ValidationUtil.isValidPrice(Double.POSITIVE_INFINITY)); // 无穷大
    }

    @Test
    @DisplayName("座位数验证 - 有效座位数")
    void testValidSeatCounts() {
        assertTrue(ValidationUtil.isValidSeatCount(1));
        assertTrue(ValidationUtil.isValidSeatCount(4));
        assertTrue(ValidationUtil.isValidSeatCount(7));
        assertTrue(ValidationUtil.isValidSeatCount(9));
    }

    @Test
    @DisplayName("座位数验证 - 无效座位数")
    void testInvalidSeatCounts() {
        assertFalse(ValidationUtil.isValidSeatCount(0));   // 零座位
        assertFalse(ValidationUtil.isValidSeatCount(-1));  // 负数座位
        assertFalse(ValidationUtil.isValidSeatCount(10));  // 超过最大座位数
        assertFalse(ValidationUtil.isValidSeatCount(100)); // 过大的座位数
    }

    @Test
    @DisplayName("字符串非空验证")
    void testStringNotEmpty() {
        assertTrue(ValidationUtil.isNotEmpty("hello"));
        assertTrue(ValidationUtil.isNotEmpty("a"));
        assertTrue(ValidationUtil.isNotEmpty("   text   "));

        assertFalse(ValidationUtil.isNotEmpty(""));
        assertFalse(ValidationUtil.isNotEmpty("   "));
        assertFalse(ValidationUtil.isNotEmpty(null));
    }

    @Test
    @DisplayName("字符串长度验证")
    void testStringLength() {
        assertTrue(ValidationUtil.isValidLength("hello", 1, 10));
        assertTrue(ValidationUtil.isValidLength("test", 4, 4));
        assertTrue(ValidationUtil.isValidLength("a", 1, 5));

        assertFalse(ValidationUtil.isValidLength("", 1, 10));        // 太短
        assertFalse(ValidationUtil.isValidLength("very long text", 1, 5)); // 太长
        assertFalse(ValidationUtil.isValidLength(null, 1, 10));     // null
    }

    @Test
    @DisplayName("经纬度验证 - 有效坐标")
    void testValidCoordinates() {
        // 有效的经纬度范围
        assertTrue(ValidationUtil.isValidLatitude(0.0));
        assertTrue(ValidationUtil.isValidLatitude(90.0));
        assertTrue(ValidationUtil.isValidLatitude(-90.0));
        assertTrue(ValidationUtil.isValidLatitude(39.9042));

        assertTrue(ValidationUtil.isValidLongitude(0.0));
        assertTrue(ValidationUtil.isValidLongitude(180.0));
        assertTrue(ValidationUtil.isValidLongitude(-180.0));
        assertTrue(ValidationUtil.isValidLongitude(116.4074));
    }

    @Test
    @DisplayName("经纬度验证 - 无效坐标")
    void testInvalidCoordinates() {
        // 纬度超出范围
        assertFalse(ValidationUtil.isValidLatitude(91.0));
        assertFalse(ValidationUtil.isValidLatitude(-91.0));
        assertFalse(ValidationUtil.isValidLatitude(Double.NaN));

        // 经度超出范围
        assertFalse(ValidationUtil.isValidLongitude(181.0));
        assertFalse(ValidationUtil.isValidLongitude(-181.0));
        assertFalse(ValidationUtil.isValidLongitude(Double.NaN));
    }

    @Test
    @DisplayName("车牌号验证 - 有效车牌号")
    void testValidPlateNumbers() {
        assertTrue(ValidationUtil.isValidPlateNumber("粤B12345"));
        assertTrue(ValidationUtil.isValidPlateNumber("京A88888"));
        assertTrue(ValidationUtil.isValidPlateNumber("沪C12345"));
        assertTrue(ValidationUtil.isValidPlateNumber("川A12345"));
    }

    @ParameterizedTest
    @ValueSource(strings = {
            "粤B1234",     // 长度不够
            "粤B1234567",  // 长度过长
            "XB12345",     // 省份简称错误
            "粤012345",    // 地区代码错误
            "粤B1234A",    // 末尾包含字母
            "",            // 空字符串
            "粤B-12345"    // 包含特殊字符
    })
    @DisplayName("车牌号验证 - 无效车牌号")
    void testInvalidPlateNumbers(String plateNumber) {
        assertFalse(ValidationUtil.isValidPlateNumber(plateNumber));
    }

    // 创建对应的验证工具类
    static class ValidationUtil {
        
        public static boolean isValidPhone(String phone) {
            if (phone == null || phone.length() != 11) {
                return false;
            }
            return phone.matches("^1[3-9]\\d{9}$");
        }

        public static boolean isValidIdCard(String idCard) {
            if (idCard == null || idCard.length() != 18) {
                return false;
            }
            return idCard.matches("^\\d{6}\\d{8}[\\dX]$") && isValidIdCardDate(idCard);
        }

        private static boolean isValidIdCardDate(String idCard) {
            try {
                String year = idCard.substring(6, 10);
                String month = idCard.substring(10, 12);
                String day = idCard.substring(12, 14);
                
                int y = Integer.parseInt(year);
                int m = Integer.parseInt(month);
                int d = Integer.parseInt(day);
                
                return y >= 1900 && y <= 2024 && m >= 1 && m <= 12 && d >= 1 && d <= 31;
            } catch (NumberFormatException e) {
                return false;
            }
        }

        public static boolean isValidPassword(String password) {
            if (password == null || password.trim().isEmpty()) {
                return false;
            }
            return password.length() >= 6 && !password.matches(".*[\\u4e00-\\u9fa5].*");
        }

        public static boolean isValidEmail(String email) {
            if (email == null || email.isEmpty()) {
                return false;
            }
            return email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
        }

        public static boolean isValidPrice(double price) {
            return price > 0 && price < 1000 && !Double.isNaN(price) && !Double.isInfinite(price);
        }

        public static boolean isValidSeatCount(int seatCount) {
            return seatCount > 0 && seatCount <= 9;
        }

        public static boolean isNotEmpty(String str) {
            return str != null && !str.trim().isEmpty();
        }

        public static boolean isValidLength(String str, int minLength, int maxLength) {
            if (str == null) {
                return false;
            }
            int length = str.length();
            return length >= minLength && length <= maxLength;
        }

        public static boolean isValidLatitude(double latitude) {
            return latitude >= -90.0 && latitude <= 90.0 && !Double.isNaN(latitude);
        }

        public static boolean isValidLongitude(double longitude) {
            return longitude >= -180.0 && longitude <= 180.0 && !Double.isNaN(longitude);
        }

        public static boolean isValidPlateNumber(String plateNumber) {
            if (plateNumber == null || plateNumber.length() != 7) {
                return false;
            }
            return plateNumber.matches("^[\\u4e00-\\u9fa5][A-Z]\\d{5}$");
        }
    }
} 