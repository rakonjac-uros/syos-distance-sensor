import asyncio
import json
import random
import websockets

sample_object = {
    "alarmCertainty": 1.0,
    "count": 86,
    "display_flag": False,
    "id": 811,
    "name": "BOAT",
    "pos_polar": [
        153.22033953753322,
        13.284598992254404
    ],
    "pos_unc_polar": [
        9.549194599644272,
        1.902113032590307
    ],
    "predicted": True,
    "rects": {
        "RGBnFoV": [
            -1.2153225213898593,
            0.7240401854142305,
            -0.9945541762105413,
            0.892817060670666
        ],
        "RGBwFoV": [
            0.10792629175001778,
            0.5512091951914392,
            0.158387626173218,
            0.5897867648345158
        ],
        "TnFoV": [
            -1.3730545888641357,
            0.7517790388769856,
            -1.1305638632979356,
            0.9343365673393347
        ],
        "TwFoV": [
            0.022389908875616836,
            0.5623811908163406,
            0.08386009112438317,
            0.609375
        ]
    }
}

sample_json = {
    "boatbus_timestamp": 1649245726870.0,
    "camera": {
        "pan": 27.700000762939453,
        "tilt": 3.2799999713897705
    },
    "imu": {
        "pitch": -0.035004254430532455,
        "roll": 1.9860360622406006,
        "yaw": -137.29339599609375
    },
    "messageID": 12,
    "objects": [
    {

        "alarmCertainty": 1.0,
        "count": 86,
        "display_flag": False,
        "id": 811,
        "name": "BOAT",
        "pos_polar": [
            153.22033953753322,
            13.284598992254404
        ],
        "pos_unc_polar": [
            9.549194599644272,
            1.902113032590307
        ],
        "predicted": True,
        "rects": {
            "RGBnFoV": [
                -1.2153225213898593,
                0.7240401854142305,
                -0.9945541762105413,
                0.892817060670666
            ],
            "RGBwFoV": [
                0.10792629175001778,
                0.5512091951914392,
                0.158387626173218,
                0.5897867648345158
            ],
            "TnFoV": [
                -1.3730545888641357,
                0.7517790388769856,
                -1.1305638632979356,
                0.9343365673393347
            ],
            "TwFoV": [
                0.022389908875616836,
                0.5623811908163406,
                0.08386009112438317,
                0.609375
            ]
        }
    }]
}

# Define a function to generate sample JSON messages
async def generate_sample_messages(websocket, path):
    while True:
        # Generate a random number of objects between 0 and 3
        num_objects = random.randint(0, 3)
        
        # Generate sample JSON data
        objects = []
        for _ in range(num_objects):
            current_distance = random.randint(50, 500)
            angle = random.uniform(-180, 180)
            obj = sample_object.copy()
            obj["pos_polar"] = [current_distance, angle]
            objects.append(obj)
        
        # Create JSON message
        message = sample_json
        message["objects"] = objects
        
        # Send JSON message
        await websocket.send(json.dumps(message))
        
        # Wait for a random time interval before sending the next message
        await asyncio.sleep(random.uniform(0.1, 0.125))

# Start the WebSocket server
start_server = websockets.serve(generate_sample_messages, "localhost", 9002)

# Run the WebSocket server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
