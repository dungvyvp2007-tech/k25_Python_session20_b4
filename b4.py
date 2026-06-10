import logging

logging.basicConfig(
    filename="roster_app.log",
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


def calculate_actual_pay(player: dict[str, object]) -> float:
    """
    Tính toán mức lương thực nhận dựa trên trạng thái thi đấu của tuyển thủ.
    Active: 100% lương, Benched: 50% lương.
    
    Sử dụng dict[str, object] thay cho Dict[str, Any].
    """
    try:
        status = player["status"]
        salary = player["salary"]
        
        base_salary = float(salary) 
        
        if status == "Active":
            return base_salary
        elif status == "Benched":
            return base_salary * 0.5
        else:
            return base_salary
    except KeyError as e:
        raise KeyError(str(e))


def display_roster(roster_list: list[dict[str, object]]) -> None:
    """Chức năng 1: Hiển thị đội hình hiện tại dạng bảng phẳng chuẩn đẹp."""
    if not roster_list:
        print("\nĐội hình hiện đang trống.")
        logging.info("Coach viewed the team roster. (Roster was empty)")
        return

    print("\n--- ĐỘI HÌNH RIKKEI ESPORTS ---")
    print(f"{'ID':<8} | {'Tên tuyển thủ':<20} | {'Vị trí':<15} | {'Lương':<12} | Trạng thái")
    print("-" * 75)

    for player in roster_list:
        try:
            pid = player.get("player_id", "N/A")
            name = player.get("name", "Unknown")
            role = player.get("role", "Unknown")
            salary = player.get("salary", 0.0)
            status = player.get("status", "Unknown")

            display_name = f"{name} [DỰ BỊ]" if status == "Benched" else name

            formatted_salary = float(salary)
            print(f"{pid:<8} | {display_name:<20} | {role:<15} | {formatted_salary:,.1f}      | {status}")
        except Exception as e:
            print(f"Lỗi hiển thị dòng dữ liệu tuyển thủ: {e}")

    logging.info("Coach viewed the team roster.")


def sign_player(roster_list: list[dict[str, object]]) -> None:
    """Chức năng 2: Chiêu mộ thành viên mới với validation dữ liệu chặt chẽ."""
    print("\n--- CHIÊU MỘ TUYỂN THỦ MỚI ---")
    
    player_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    if any(p.get("player_id") == player_id for p in roster_list):
        print(f"\nLỗi: Mã tuyển thủ {player_id} đã tồn tại.")
        logging.warning(f"Failed to sign player - Duplicate player ID {player_id}")
        return

    name = input("Nhập tên tuyển thủ: ").strip()
    role = input("Nhập vị trí thi đấu: ").strip()

    while True:
        try:
            salary_input = input("Nhập mức lương hàng tháng: ").strip()
            salary = float(salary_input)
            if salary <= 0:
                print("Lương phải là số dương. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Lương phải là số. Vui lòng nhập lại.")
            logging.warning("Failed to sign player - Invalid salary input")

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


def update_player_status(roster_list: list[dict[str, object]]) -> None:
    """Chức năng 3: Cập nhật lương hoặc trạng thái thi đấu."""
    print("\n--- CẬP NHẬT LƯƠNG & TRẠNG THÁI THI ĐẤU ---")
    player_id = input("Nhập mã tuyển thủ cần cập nhật: ").strip().upper()

    player = next((p for p in roster_list if p.get("player_id") == player_id), None)
    if not player:
        print(f"\nKhông tìm thấy tuyển thủ mang mã {player_id}.")
        logging.warning(f"Failed to update player - Player ID {player_id} not found")
        return

    print(f"\nTuyển thủ: {player.get('name')}")
    print(f"Vị trí: {player.get('role')}")
    
    current_salary = float(player.get("salary", 0.0))
    print(f"Lương hiện tại: {current_salary:,}")
    print(f"Trạng thái hiện tại: {player.get('status')}")

    print("\nBạn muốn cập nhật:")
    print("1. Cập nhật lương")
    print("2. Cập nhật trạng thái thi đấu")
    
    while True:
        choice = input("Chọn chức năng cập nhật (1-2): ").strip()
        if choice in ["1", "2"]:
            break
        print("Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.")

    if choice == "1":
        while True:
            try:
                new_salary = float(input("Nhập mức lương mới: ").strip())
                if new_salary <= 0:
                    print("Lương phải là số dương. Vui lòng nhập lại.")
                    continue
                old_salary = player["salary"]
                player["salary"] = new_salary
                print(f"\nThành công: Đã cập nhật lương cho tuyển thủ {player_id}.")
                logging.info(f"Updated player {player_id} salary from {old_salary} to {new_salary}")
                break
            except ValueError:
                print("Lương phải là số. Vui lòng nhập lại.")
    
    elif choice == "2":
        print("\nChọn trạng thái mới:")
        print("1. Active")
        print("2. Benched")
        while True:
            status_choice = input("Nhập lựa chọn trạng thái (1-2): ").strip()
            if status_choice == "1":
                player["status"] = "Active"
                break
            elif status_choice == "2":
                player["status"] = "Benched"
                break
            print("Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.")
        
        print(f"\nThành công: Đã cập nhật trạng thái cho tuyển thủ {player_id}.")
        logging.info(f"Updated player {player_id} status to {player['status']}")


def generate_payroll_report(roster_list: list[dict[str, object]]) -> None:
    """Chức năng 4: Kết xuất báo cáo quỹ lương và bẫy lỗi cấu trúc dữ liệu khuyết thiếu."""
    print("\n--- BÁO CÁO QUỸ LƯƠNG HÀNG THÁNG ---")
    
    if not roster_list:
        print("Đội hình hiện đang trống. Tổng quỹ lương: 0.0")
        logging.info("Generated monthly payroll report. Total: 0.0")
        return

    print(f"{'ID':<8} | {'Tên tuyển thủ':<15} | {'Trạng thái':<10} | {'Lương gốc':<12} | Lương thực nhận")
    print("-" * 75)

    total_payroll = 0.0
    has_error = False

    for player in roster_list:
        try:
            actual_pay = calculate_actual_pay(player)
            base_salary = float(player['salary'])
            print(f"{player['player_id']:<8} | {player['name']:<15} | {player['status']:<10} | {base_salary:<12,.1f} | {actual_pay:,.1f}")
            total_payroll += actual_pay
        except KeyError as e:
            print("Lỗi: Một tuyển thủ đang bị thiếu dữ liệu.")
            logging.error(f"Missing key while generating payroll report: {str(e)}")
            has_error = True
            break 

    print("-" * 75)
    if has_error:
        total_payroll = 0.0

    print(f"Tổng quỹ lương hàng tháng: {total_payroll:,}")
    if not has_error:
        logging.info(f"Generated monthly payroll report. Total: {total_payroll}")


def main():
    roster = [
        {"player_id": "P01", "name": "Faker", "role": "Mid Lane", "salary": 5000.0, "status": "Active"},
        {"player_id": "P02", "name": "Oner", "role": "Jungle", "salary": 3500.0, "status": "Active"},
        {"player_id": "P03", "name": "Ruler", "role": "ADC", "salary": 6000.0, "status": "Benched"}
    ]

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
            print("\nĐang đóng hệ thống... Tạm biệt Coach!")
            logging.info("System shutdown gracefully.")
            break
        else:
            print("\nLựa chọn không hợp lệ! Vui lòng nhập từ 1 đến 5.")


if __name__ == "__main__":
    main()
