import socket
import struct
import time
import csv
# DataPacket class to hold the decoded telemetry data
class DataPacket:
    pass

# Decoding functions to extract specific data types
def get_single(data, index):
    return struct.unpack('f', data[index:index + 4])[0]

def get_uint16(data, index):
    return struct.unpack('H', data[index:index + 2])[0]

def get_uint32(data, index):
    return struct.unpack('I', data[index:index + 4])[0]

def get_uint8(data, index):
    return struct.unpack('B', data[index:index + 1])[0]

def get_int8(data, index):
    return struct.unpack('b', data[index:index + 1])[0]
BufferOffset = 12

# Packet parsing function
def parse_packet(packet):
    try:
        data = DataPacket()
        data.IsRaceOn = packet[0] > 0
        data.TimestampMS = get_uint32(packet, 4)
        data.EngineMaxRpm = get_single(packet, 8)
        data.EngineIdleRpm = get_single(packet, 12)
        data.CurrentEngineRpm = get_single(packet, 16)
        data.AccelerationX = get_single(packet, 20)
        data.AccelerationY = get_single(packet, 24)
        data.AccelerationZ = get_single(packet, 28)
        data.VelocityX = get_single(packet, 32)
        data.VelocityY = get_single(packet, 36)
        data.VelocityZ = get_single(packet, 40)
        data.AngularVelocityX = get_single(packet, 44)
        data.AngularVelocityY = get_single(packet, 48)
        data.AngularVelocityZ = get_single(packet, 52)
        data.Yaw = get_single(packet, 56)
        data.Pitch = get_single(packet, 60)
        data.Roll = get_single(packet, 64)
        data.NormSuspensionTravelFrontLeft = get_single(packet, 68)
        data.NormSuspensionTravelFrontRight = get_single(packet, 72)
        data.NormSuspensionTravelRearLeft = get_single(packet, 76)
        data.NormSuspensionTravelRearRight = get_single(packet, 80)
        data.TireSlipRatioFrontLeft = get_single(packet, 84)
        data.TireSlipRatioFrontRight = get_single(packet, 88)
        data.TireSlipRatioRearLeft = get_single(packet, 92)
        data.TireSlipRatioRearRight = get_single(packet, 96)
        data.WheelRotationSpeedFrontLeft = get_single(packet, 100)
        data.WheelRotationSpeedFrontRight = get_single(packet, 104)
        data.WheelRotationSpeedRearLeft = get_single(packet, 108)
        data.WheelRotationSpeedRearRight = get_single(packet, 112)
        data.WheelOnRumbleStripFrontLeft = get_single(packet, 116)
        data.WheelOnRumbleStripFrontRight = get_single(packet, 120)
        data.WheelOnRumbleStripRearLeft = get_single(packet, 124)
        data.WheelOnRumbleStripRearRight = get_single(packet, 128)
        data.WheelInPuddleFrontLeft = get_single(packet, 132)
        data.WheelInPuddleFrontRight = get_single(packet, 136)
        data.WheelInPuddleRearLeft = get_single(packet, 140)
        data.WheelInPuddleRearRight = get_single(packet, 144)
        data.SurfaceRumbleFrontLeft = get_single(packet, 148)
        data.SurfaceRumbleFrontRight = get_single(packet, 152)
        data.SurfaceRumbleRearLeft = get_single(packet, 156)
        data.SurfaceRumbleRearRight = get_single(packet, 160)
        data.TireSlipAngleFrontLeft = get_single(packet, 164)
        data.TireSlipAngleFrontRight = get_single(packet, 168)
        data.TireSlipAngleRearLeft = get_single(packet, 172)
        data.TireSlipAngleRearRight = get_single(packet, 176)
        data.TireCombinedSlipFrontLeft = get_single(packet, 180)
        data.TireCombinedSlipFrontRight = get_single(packet, 184)
        data.TireCombinedSlipRearLeft = get_single(packet, 188)
        data.TireCombinedSlipRearRight = get_single(packet, 192)
        data.SuspensionTravelMetersFrontLeft = get_single(packet, 196)
        data.SuspensionTravelMetersFrontRight = get_single(packet, 200)
        data.SuspensionTravelMetersRearLeft = get_single(packet, 204)
        data.SuspensionTravelMetersRearRight = get_single(packet, 208)
        data.PositionX = get_single(packet, 232 + BufferOffset)
        data.PositionY = get_single(packet, 236 + BufferOffset)
        data.PositionZ = get_single(packet, 240 + BufferOffset)
        data.Speed = get_single(packet, 244 + BufferOffset)
        data.Power = get_single(packet, 248 + BufferOffset)
        data.Torque = get_single(packet, 252 + BufferOffset)
        data.TireTempFrontLeft = get_single(packet, 256 + BufferOffset)
        data.TireTempFrontRight = get_single(packet, 260 + BufferOffset)
        data.TireTempRearLeft = get_single(packet, 264 + BufferOffset)
        data.TireTempRearRight = get_single(packet, 268 + BufferOffset)
        data.Boost = get_single(packet, 272 + BufferOffset)
        data.Fuel = get_single(packet, 276 + BufferOffset)
        data.Distance = get_single(packet, 280 + BufferOffset)
        data.Accelerator = get_uint8(packet, 303 + BufferOffset)
        data.Brake = get_uint8(packet, 304 + BufferOffset)
        data.Clutch = get_uint8(packet, 305 + BufferOffset)
        data.Handbrake = get_uint8(packet, 306 + BufferOffset)
        data.Gear = get_uint8(packet, 307 + BufferOffset)
        data.Steer = get_int8(packet, 308 + BufferOffset)
        data.NormalDrivingLine = get_uint8(packet, 309 + BufferOffset)
        data.NormalAiBrakeDifference = get_uint8(packet, 310 + BufferOffset)

        return data
    except IndexError as e:
        print(f"Error parsing packet: {e}")
        return None

# Configure UDP socket to receive FH4 telemetry data
UDP_IP = '127.0.0.1'  # Replace with the IP address of the machine running FH4
UDP_PORT = 5300  # Replace with the port used by FH4 to send telemetry data

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
# Create a CSV file and write the header
csv_filename = "telemetry_data.csv"
with open(csv_filename, mode='w', newline='') as csv_file:
    fieldnames = ["IsRaceOn", "TimestampMS", ...]  # Add all fieldnames here
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop to receive and process telemetry data
    print("Listening for FH4 telemetry data...")
    while True:
        try:
            packet, addr = sock.recvfrom(324)
            data_packet = parse_packet(packet)
            if data_packet:
                writer.writerow(data_packet.__dict__)
                csv_file.flush()
                # Print statements or any additional logic
                print(f"IsRaceOn: {data_packet.IsRaceOn}")
                print(f"TimestampMS: {data_packet.TimestampMS}")
                print(f"EngineMaxRpm: {data_packet.EngineMaxRpm}")
                print(f"EngineIdleRpm: {data_packet.EngineIdleRpm}")
                print(f"CurrentEngineRpm: {data_packet.CurrentEngineRpm}")
                print(f"AccelerationX: {data_packet.AccelerationX}")
                print(f"AccelerationY: {data_packet.AccelerationY}")
                print(f"AccelerationZ: {data_packet.AccelerationZ}")
                print(f"VelocityX: {data_packet.VelocityX}")
                print(f"VelocityY: {data_packet.VelocityY}")
                print(f"VelocityZ: {data_packet.VelocityZ}")
                print(f"AngularVelocityX: {data_packet.AngularVelocityX}")
                print(f"AngularVelocityY: {data_packet.AngularVelocityY}")
                print(f"AngularVelocityZ: {data_packet.AngularVelocityZ}")
                print(f"Yaw: {data_packet.Yaw}")
                print(f"Pitch: {data_packet.Pitch}")
                print(f"Roll: {data_packet.Roll}")
                print(f"NormSuspensionTravelFrontLeft: {data_packet.NormSuspensionTravelFrontLeft}")
                print(f"NormSuspensionTravelFrontRight: {data_packet.NormSuspensionTravelFrontRight}")
                print(f"NormSuspensionTravelRearLeft: {data_packet.NormSuspensionTravelRearLeft}")
                print(f"NormSuspensionTravelRearRight: {data_packet.NormSuspensionTravelRearRight}")
                print(f"TireSlipRatioFrontLeft: {data_packet.TireSlipRatioFrontLeft}")
                print(f"TireSlipRatioFrontRight: {data_packet.TireSlipRatioFrontRight}")
                print(f"TireSlipRatioRearLeft: {data_packet.TireSlipRatioRearLeft}")
                print(f"TireSlipRatioRearRight: {data_packet.TireSlipRatioRearRight}")
                print(f"WheelRotationSpeedFrontLeft: {data_packet.WheelRotationSpeedFrontLeft}")
                print(f"WheelRotationSpeedFrontRight: {data_packet.WheelRotationSpeedFrontRight}")
                print(f"WheelRotationSpeedRearLeft: {data_packet.WheelRotationSpeedRearLeft}")
                print(f"WheelRotationSpeedRearRight: {data_packet.WheelRotationSpeedRearRight}")
                print(f"WheelOnRumbleStripFrontLeft: {data_packet.WheelOnRumbleStripFrontLeft}")
                print(f"WheelOnRumbleStripFrontRight: {data_packet.WheelOnRumbleStripFrontRight}")
                print(f"WheelOnRumbleStripRearLeft: {data_packet.WheelOnRumbleStripRearLeft}")
                print(f"WheelOnRumbleStripRearRight: {data_packet.WheelOnRumbleStripRearRight}")
                print(f"WheelInPuddleFrontLeft: {data_packet.WheelInPuddleFrontLeft}")
                print(f"WheelInPuddleFrontRight: {data_packet.WheelInPuddleFrontRight}")
                print(f"WheelInPuddleRearLeft: {data_packet.WheelInPuddleRearLeft}")
                print(f"WheelInPuddleRearRight: {data_packet.WheelInPuddleRearRight}")
                print(f"SurfaceRumbleFrontLeft: {data_packet.SurfaceRumbleFrontLeft}")
                print(f"SurfaceRumbleFrontRight: {data_packet.SurfaceRumbleFrontRight}")
                print(f"SurfaceRumbleRearLeft: {data_packet.SurfaceRumbleRearLeft}")
                print(f"SurfaceRumbleRearRight: {data_packet.SurfaceRumbleRearRight}")
                print(f"TireSlipAngleFrontLeft: {data_packet.TireSlipAngleFrontLeft}")
                print(f"TireSlipAngleFrontRight: {data_packet.TireSlipAngleFrontRight}")
                print(f"TireSlipAngleRearLeft: {data_packet.TireSlipAngleRearLeft}")
                print(f"TireSlipAngleRearRight: {data_packet.TireSlipAngleRearRight}")
                print(f"TireCombinedSlipFrontLeft: {data_packet.TireCombinedSlipFrontLeft}")
                print(f"TireCombinedSlipFrontRight: {data_packet.TireCombinedSlipFrontRight}")
                print(f"TireCombinedSlipRearLeft: {data_packet.TireCombinedSlipRearLeft}")
                print(f"TireCombinedSlipRearLeft: {data_packet.TireCombinedSlipRearRight}")
                print(f"SuspensionTravelMetersFrontLeft: {data_packet.SuspensionTravelMetersFrontLeft}")
                print(f"SuspensionTravelMetersFrontRight: {data_packet.SuspensionTravelMetersFrontRight}")
                print(f"SuspensionTravelMetersRearLeft: {data_packet.SuspensionTravelMetersRearLeft}")
                print(f"SuspensionTravelMetersRearRight: {data_packet.SuspensionTravelMetersRearRight}")
                print(f"PositionX: {data_packet.PositionX}")
                print(f"PositionY: {data_packet.PositionY}")
                print(f"PositionZ: {data_packet.PositionZ}")
                print(f"Speed: {data_packet.Speed}")
                print(f"Power: {data_packet.Power}")
                print(f"Torque: {data_packet.Torque}")
                print(f"TireTempFrontLeft: {data_packet.TireTempFrontLeft}")
                print(f"TireTempFrontRight: {data_packet.TireTempFrontRight}")
                print(f"TireTempRearLeft: {data_packet.TireTempRearLeft}")
                print(f"TireTempRearRight: {data_packet.TireTempRearRight}")
                print(f"Boost: {data_packet.Boost}")
                print(f"Fuel: {data_packet.Fuel}")
                print(f"Distance: {data_packet.Distance}")
                print(f"Accelerator: {data_packet.Accelerator}")
                print(f"Brake: {data_packet.Brake}")
                print(f"Clutch: {data_packet.Clutch}")
                print(f"Handbrake: {data_packet.Handbrake}")
                print(f"Gear: {data_packet.Gear}")
                print(f"Steer: {data_packet.Steer}")
                print(f"NormalDrivingLine: {data_packet.NormalDrivingLine}")
                print(f"NormalAiBrakeDifference: {data_packet.NormalAiBrakeDifference}")
            #time.sleep(2)
        except socket.error as e:
            print(f"Socket error: {e}")

# Close the socket when done
sock.close()
          