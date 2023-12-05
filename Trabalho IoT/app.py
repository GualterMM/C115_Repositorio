import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt

def setup_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect

    # Connect to the Mosquitto Test Server
    client.connect("test.mosquitto.org", 1883, 60)

    # Start the MQTT client loop in a separate thread
    client.loop_start()

    return client

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def subscribe(client: mqtt.Client, topic, canvas):
    def on_message(client, userdata, msg):
        print(msg)
        # Update the sensor reading and gauge value when a new message is received
        sensor_reading = int(msg.payload.decode())
        if sensor_reading == -1:
            canvas.config(background="red")
        elif sensor_reading == 0:
            canvas.config(background="yellow")
        elif sensor_reading == 1:
            canvas.config(background="green")
        elif sensor_reading == 2:
            canvas.config(background="blue")

    client.subscribe(topic)
    client.on_message = on_message

def send_reservation(client, topic, value):
    try:
        client.publish(topic, str(value))
        print("Published value ", value)
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def main():
    root = tk.Tk()
    root.title("Estacionamento inteligente")

    client = setup_mqtt_client()

    # Vaga 1
    f1 = tk.Frame(root, width=500, height=400,)
    l1 = ttk.Label(f1, text="Vaga #1")
    canvas = tk.Canvas(f1, width=300, height=300, background='green')
    reserve_button = ttk.Button(f1, text="Reservar", command=lambda: send_reservation(client, "c115/estacionamento/reservas/vaga1", 1))
    cancel_button = ttk.Button(f1, text="Cancelar", command=lambda: send_reservation(client, "c115/estacionamento/reservas/vaga1", 0))
    f1.grid(row=0, column=0, sticky='news')
    l1.pack(side='top')
    canvas.pack(side="bottom")
    reserve_button.pack(side='left')
    cancel_button.pack(side='right')

    subscribe(client, "c115/estacionamento/vagas/vaga1", canvas)

    root.mainloop()

if __name__ == '__main__':
    main()

