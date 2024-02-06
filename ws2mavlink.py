from pymavlink import mavutil
import json
import websockets
import time
import asyncio
import argparse

mavlink_device = '/dev/ttyUSB0'
baudrate = 57600
camera_ip_address = "192.168.1.114"
start_time = None

def angle_to_sector(angle):
    if angle < -180 or angle > 180:
        raise ValueError("Angle not in the range -180 to 180 degrees")

    angle += 22.5
    if angle < 0:
        angle += 360

    sector = int(angle / 45) % 8

    return sector

def send_distance_sensor(current_distance, angle):
    # print("current_distance: ", current_distance)
    # print("angle: ", angle)
    sensor_id = 0  # Sensor ID (choose a unique value)
    orientation = angle_to_sector(angle)  # Orientation of the sensor (0-7, [-22.5, 22.5],[22.5, 67.5],...)
    # print("orientation: ", orientation)
    min_distance = 10*100  # Minimum measurable distance in centimeters TODO
    max_distance = 10000*100  # Maximum measurable distance in centimeters TODO
    covariance = 0

    master.mav.distance_sensor_send(
        int(time.time() * 1e3),
        min_distance,
        max_distance,
        current_distance*100,
        sensor_id,
        orientation,
        covariance
    )


async def receive_messages():
    global start_time
    async with websockets.connect(websocket_url) as websocket:
        while True:
            message = await websocket.recv()
            try:
                data = json.loads(message)
                if start_time is None:
                    start_time = time.time()
                objects = data.get('objects', [])
                for obj in objects:
                    pos_polar = obj.get('pos_polar', [])
                    if len(pos_polar) == 2:
                        current_distance, angle = pos_polar
                        send_distance_sensor(current_distance, angle)
            except Exception as e:
                print("Error:", e)



# FOR WEBSOCKET-CLIENT LIBRARY (websocket without s)
# Define a function to handle WebSocket messages
# def on_message(ws, message):
#     try:
#         data = json.loads(message)
#         objects = data.get('objects', [])
#         for obj in objects:
#             pos_polar = obj.get('pos_polar', [])
#             if len(pos_polar) == 2:
#                 current_distance, angle = pos_polar
#                 send_distance_sensor(current_distance, angle)
#     except Exception as e:
#         print("Error:", e)

# # Connect to the WebSocket server
# ws = websockets.WebSocketApp(websocket_url, on_message=on_message)
# ws.run_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert sentry detections to distance_sensor mavlink messages.")
    parser.add_argument("--camera_ip", type=str, help="Camera IP address")
    args = parser.parse_args()
    camera_ip_address = args.camera_ip
    master = mavutil.mavlink_connection(mavlink_device, baud=baudrate)
    # master = None
    websocket_url = f"ws://{camera_ip_address}:9002/v1/sentrydatasource" # :9002/v1/sentrydatasource

    asyncio.get_event_loop().run_until_complete(receive_messages())
