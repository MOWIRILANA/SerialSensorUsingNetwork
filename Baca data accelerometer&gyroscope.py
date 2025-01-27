import socket
import struct
import errno

#konfigurasi UDP
UDP_IP = "192.168.43.157"  #IP jaringan yang terhubung
UDP_PORT = 8888
MESSAGE_LENGTH = 13  #Panjang data bytes

print("This PC's IP: ", UDP_IP)
print("Listening on Port: ", UDP_PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind((UDP_IP, UDP_PORT))

accel_data = []
gyro_data = []

while True:

    keepReceiving = True
    newestData = None
    while keepReceiving:
        try:
            data, fromAddr = sock.recvfrom(MESSAGE_LENGTH)
            if data:
                newestData = data
        except socket.error as why:
            if why.args[0] == errno.EWOULDBLOCK:
                keepReceiving = False
            else:
                raise why

    if newestData is not None:
        if len(newestData) != MESSAGE_LENGTH:
            print(f"Warning: Unexpected data length {len(newestData)} bytes")
            continue

        sensor_type = struct.unpack_from('<B', newestData, 0)[0]  # Byte ke-0

        #Menampilkan data real
        value1 = struct.unpack_from('<f', newestData, 1)[0]  # Byte ke-1 hingga 4
        value2 = struct.unpack_from('<f', newestData, 5)[0]  # Byte ke-5 hingga 8
        value3 = struct.unpack_from('<f', newestData, 9)[0]  # Byte ke-9 hingga 12

        #Konversi data menjadi 2 bagian
        if sensor_type == 1:
            accel_data.append((value1, value2, value3))
            print(f"Accelerometer: X={value1:.6f}, Y={value2:.6f}, Z={value3:.6f}")
        else:
            gyro_data.append((sensor_type, value1, value2, value3))
            print(f"Gyroscope: X={value1:.6f}, Y={value2:.6f}, Z={value3:.6f}")
