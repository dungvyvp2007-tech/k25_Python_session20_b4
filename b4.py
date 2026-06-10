import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("roster_app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

roster = [
    {
        "player_id": "P01",
        "name": "Faker",
        "role": "Mid Lane",
        "salary": 5000.0,
        "status": "Active"
    },
    {
        "player_id": "P02",
        "name": "Oner",
        "role": "Jungle",
        "salary": 3500.0,
        "status": "Active"
    },
    {
        "player_id": "P03",
        "name": "Ruler",
        "role": "ADC",
        "salary": 6000.0,
        "status": "Benched"
    }
]


def display_roster(roster_list):
    logging.info("Coach viewed the team roster.")
    
    if not roster_list:
        print("\nĐội hình hiện đang trống.")
        return

    print("\n--- ĐỘI HÌNH RIKKEI ESPORTS ---")
    print(f"{'ID':<8} | {'Tên tuyển thủ':<20} | {'Vị trí':<15} | {'Lương':<12} | Trạng thái")
    print("-" * 80)
    
    for player in roster_list:
        try:
            p_id = player["player_id"]
            name = player["name"]
            role = player["role"]
            salary = player["salary"]
            status = player.get("status", "Unknown")
            
            display_name = f"{name} [DỰ BỊ]" if status == "Benched" else name
            print(f"{p_id:<8} | {display_name:<20} | {role:<15} | {salary:,.1f} | {status}")
            
        except KeyError as e:
            logging.error(f"Missing key while displaying roster: {e}")
            print(f"[Lỗi dữ liệu] Tuyển thủ bị thiếu trường thông tin: {e}")


def _get_positive_salary():
    while True:
        try:
            salary_input = input("Nhập mức lương hàng tháng: ").strip()
            salary = float(salary_input)
            if salary <= 0:
                print("\nLương phải là số dương. Vui lòng nhập lại.")
                continue
            return salary
        except ValueError:
            print("\nLương phải là số. Vui lòng nhập lại.")
            logging.warning("Failed to sign player - Invalid salary input")


def sign_player(roster_list):
    print("\n--- CHIÊU MỘ TUYỂN THỦ MỚI ---")
    
    player_id = input("Nhập mã tuyển thủ: ").strip().upper()
    if not player_id:
        print("Mã tuyển thủ không được để trống.")
        return

    if any(p["player_id"] == player_id for p in roster_list):
        print(f"\nLỗi: Mã tuyển thủ {player_id} đã tồn tại.")
        logging.warning(f"Failed to sign player - Duplicate player ID {player_id}")
        return

    name = input("Nhập tên tuyển thủ: ").strip()
    role = input("Nhập vị trí thi đấu: ").strip()
    
    if not name or not role:
        print("Tên và vị trí thi đấu không được để trống.")
        return

    salary = _get_positive_salary()

    new_player = {
        "player_id": player_id,
        "name": name,
        "role": role,
        "salary": salary,
        "status": "Active"
    }
    roster_list.append(new_player)
    print(f"\nThành công: Đã chiêu mộ tuyển thủ {name}.")
    logging.info(f"Signed new player {name} with salary {salary}")


def update_player_status(roster_list):
    print("\n--- CẬP NHẬT LƯƠNG & TRẠNG THÁI THI ĐẤU ---")
    player_id = input("Nhập mã tuyển thủ cần cập nhật: ").strip().upper()

    target_player = None
    for p in roster_list:
        if p["player_id"] == player_id:
            target_player = p
            break

    if not target_player:
        print(f"\nKhông tìm thấy tuyển thủ mang mã {player_id}.")
        logging.warning(f"Failed to update player - Player ID {player_id} not found")
        return

    print(f"\nTuyển thủ: {target_player.get('name')}")
    print(f"Vị trí: {target_player.get('role')}")
    print(f"Lương hiện tại: {target_player.get('salary', 0):,}")
    print(f"Trạng thái hiện tại: {target_player.get('status', 'Unknown')}")

    print("\nBạn muốn cập nhật:")
    print("1. Cập nhật lương")
    print("2. Cập nhật trạng thái thi đấu")
    choice = input("Chọn chức năng cập nhật (1-2): ").strip()

    if choice == "1":
        old_salary = target_player.get("salary", 0)
        new_salary = _get_positive_salary()
        target_player["salary"] = new_salary
        print(f"\nThành công: Đã cập nhật lương cho tuyển thủ {player_id}.")
        logging.info(f"Updated player {player_id} salary from {old_salary} to {new_salary}")
        
    elif choice == "2":
        print("\nChọn trạng thái mới:")
        print("1. Active")
        print("2. Benched")
        status_choice = input("Nhập lựa chọn trạng thái (1-2): ").strip()
        
        if status_choice == "1":
            target_player["status"] = "Active"
        elif status_choice == "2":
            target_player["status"] = "Benched"
        else:
            print("Lựa chọn trạng thái không hợp lệ.")
            return
            
        print(f"\nThành công: Đã cập nhật trạng thái cho tuyển thủ {player_id}.")
        logging.info(f"Updated player {player_id} status to {target_player['status']}")
    else:
        print("Lựa chọn không hợp lệ.")


def generate_payroll_report(roster_list):
    print("\n--- BÁO CÁO QUỸ LƯƠNG HÀNG THÁNG ---")
    
    if not roster_list:
        print("Đội hình hiện đang trống. Tổng quỹ lương: 0.0")
        return

    print(f"{'ID':<8} | {'Tên tuyển thủ':<15} | {'Trạng thái':<10} | {'Lương gốc':<12} | Lương thực nhận")
    print("-" * 80)
    
    total_payroll = 0.0
    
    for player in roster_list:
        try:
            p_id = player["player_id"]
            name = player["name"]
            status = player.get("status", "Unknown")
            base_salary = player["salary"]
            
            # Giải quyết Bug logic ẩn: Dự bị (Benched) chỉ nhận 50% lương
            actual_salary = base_salary if status == "Active" else base_salary * 0.5
            total_payroll += actual_salary
            
            print(f"{p_id:<8} | {name:<15} | {status:<10} | {base_salary:<12,.1f} | {actual_salary:,.1f}")
            
        except KeyError as e:
            logging.error(f"Missing key while generating payroll report: {e}")
            print("Lỗi: Một tuyển thủ đang bị thiếu dữ liệu.")
            print("-" * 80)
            print("Tổng quỹ lương hàng tháng: 0.0")
            return

    print("-" * 80)
    print(f"Tổng quỹ lương hàng tháng: {total_payroll:,.1f}")
    logging.info(f"Generated monthly payroll report. Total: {total_payroll}")


def main():
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ ĐỘI HÌNH RIKKEI ESPORTS =====")
        print("1. Xem đội hình thi đấu hiện tại")
        print("2. Chiêu mộ tuyển thủ mới")
        print("3. Cập nhật lương & Trạng thái thi đấu")
        print("4. Báo cáo quỹ lương hàng tháng")
        print("5. Thoát hệ thống")
        print("==================================================")
        
        choice = input("Chọn chức năng (1-5): ").strip()

        if choice == "1":
            display_roster(roster)
        elif choice == "2":
            sign_player(roster)
        elif choice == "3":
            update_player_status(roster)
        elif choice == "4":
            generate_payroll_report(roster)
        elif choice == "5":
            logging.info("System shutting down.")
            print("\nHệ thống đóng. Tạm biệt huấn luyện viên!")
            break
        else:
            print("\nLựa chọn không hợp lệ! Vui lòng nhập số từ 1 đến 5.")
            logging.warning(f"Invalid menu choice selected: '{choice}'")


main()