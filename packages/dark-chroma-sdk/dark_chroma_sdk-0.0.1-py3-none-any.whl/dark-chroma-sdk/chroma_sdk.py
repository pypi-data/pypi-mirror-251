import threading
from time import sleep
import requests
import keyboard
import json
from color_parsing import parse_rgb
from pynput.mouse import Listener

global middle_mouse_pressed


# Callback function for mouse events
def on_click(_, __, button, pressed):
    global middle_mouse_pressed
    if button == button.middle:
        middle_mouse_pressed = pressed


def heartbeat_thread(chromasdk):
    try:
        while True:
            if chromasdk.enabled:
                requests.put(chromasdk.uri + '/heartbeat')
                sleep(1)
            else:
                break
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting...")
        chromasdk.quit()
        exit(0)


class ChromaSDK:
    def __init__(self, config):
        self.config = config
        self.map = config['map']

        self.id, self.uri = self.initialize()

        self.enabled = True
        self.heartbeat_thread = threading.Thread(target=heartbeat_thread, args=(self,))
        self.heartbeat_thread.start()

        sleep(3)

    def initialize(self):
        # send config to server, and get session id
        response = requests.post('http://localhost:54235/razer/chromasdk', json=self.config['chroma'])
        print(f"response from init: {response.json()}")
        try:
            return response.json()['sessionid'], response.json()['uri']
        except KeyError:
            print("Error initializing Chroma SDK")
            print(f"response: {response.json()}")
            exit(1)

    def save_config(self):
        json.dump(self.config, open('config.json', 'w'), indent=4)

        print("saved config to config.json")
        print(f"config: {self.config}")

    def quit(self):
        requests.delete(self.uri)
        self.enabled = False
        self.heartbeat_thread.join()

    def send_grid(self, grid):
        data = {
            'effect': 'CHROMA_CUSTOM',
            'param': grid
        }
        try:
            requests.put(self.uri + '/keyboard', json=data)
        except requests.exceptions.ConnectionError:
            print("ConnectionError while sending grid...")
            sleep(2)

    def light_index(self, pos, color):
        parsed_color = parse_rgb(color)

        # generate array with 6 rows and 22 columns of 0
        grid = [[0 for _ in range(22)] for _ in range(6)]

        # set the color of the key
        grid[pos[1]][pos[0]] = parsed_color

        # send the array to the server
        self.send_grid(grid)

    def light_static(self, color):
        color = parse_rgb(color)
        data = {
            "effect": "CHROMA_STATIC",
            "param": {
                "color": color
            }
        }
        requests.put(self.uri + '/keyboard', json=data)

    def light_keys(self, keys, color=(0, 0, 0), background=(0, 0, 0)):
        multi_color = isinstance(keys, dict)
        if multi_color:
            corrected_keys = []
            corrected_colors = []

            for key in keys:
                corrected_keys.append(key)
                corrected_colors.append(keys[key])

            keys = corrected_keys

        positions = [self.map[key] for key in keys if key in self.map]

        # generate array with 6 rows and 22 columns of 0
        grid = [[parse_rgb(background) for _ in range(22)] for _ in range(6)]

        # set the color of the keys
        for pos in positions:
            if multi_color:
                grid[pos[0]][pos[1]] = parse_rgb(corrected_colors[positions.index(pos)])
            else:
                grid[pos[0]][pos[1]] = parse_rgb(color)

        self.send_grid(grid)

    def generate_map(self):
        self.light_static((0, 0, 0))

        saved_keys = []
        for row in range(6):
            for key_index in range(22):
                self.light_index((key_index, row), (0, 0, 255))

                print("press lit up key or alt n to skip")
                while True:
                    event = keyboard.read_event()

                    if event.is_keypad:
                        event.name = "keypad " + event.name
                    event.name = event.name.replace(" ", "_")

                    if event.name not in saved_keys:
                        break
                    else:
                        print("key already saved")

                    if middle_mouse_pressed:
                        print("skipped")
                        sleep(.5)
                        break

                if middle_mouse_pressed:
                    print("skipped")
                    sleep(.5)
                    continue

                self.map[event.name.lower()] = [row, key_index]

                print(f"key {event.name.lower()} saved")
                saved_keys.append(event.name.lower())

                sleep(.2)

        self.save_config()


listener = Listener(on_click=on_click)
listener.start()
