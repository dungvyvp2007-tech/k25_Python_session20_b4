import unittest
# Import hàm cần test từ file main
from b4 import calculate_actual_pay


class TestRosterPayroll(unittest.TestCase):

    def test_calculate_actual_pay_active(self):
        """Test Case 1: Tuyển thủ đang Active phải nhận chuẩn 100% lương."""
        active_player = {
            "player_id": "P01",
            "name": "Faker",
            "role": "Mid Lane",
            "salary": 5000.0,
            "status": "Active"
        }
        expected_salary = 5000.0
        self.assertEqual(calculate_actual_pay(active_player), expected_salary)

    def test_calculate_actual_pay_benched(self):
        """Test Case 2: Tuyển thủ đang Benched chỉ được nhận đúng 50% lương."""
        benched_player = {
            "player_id": "P03",
            "name": "Ruler",
            "role": "ADC",
            "salary": 6000.0,
            "status": "Benched"
        }
        expected_salary = 3000.0  # 6000.0 * 50%
        self.assertEqual(calculate_actual_pay(benched_player), expected_salary)

    def test_calculate_actual_pay_missing_key(self):
        """Test Case mở rộng: Kiểm tra bẫy lỗi dữ liệu khuyết thiếu cấu trúc."""
        bad_player = {
            "player_id": "P04",
            "name": "Zeus",
            "role": "Top Lane",
            "status": "Active"
            # Thiếu hụt key 'salary'
        }
        with self.assertRaises(KeyError):
            calculate_actual_pay(bad_player)


if __name__ == "__main__":
    unittest.main()