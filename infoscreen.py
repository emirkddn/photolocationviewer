from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from map import Map


class InfoApp(tk.Frame):
    def __init__(self, master=None, image_path=None, gps_info=None):
        super().__init__(master)
        self.pack()
        self.master = master

        self.image_path = image_path
        self.gps_info = gps_info

        # Location Label
        loc_text = "Location: No GPS data found"
        if gps_info and 'latitude' in gps_info and 'longitude' in gps_info:
            loc_text = f"Location: Lat {gps_info['latitude']:.4f}, Lon {gps_info['longitude']:.4f}"
        self.loc_label = tk.Label(self, text=loc_text, font=("Arial", 14))
        self.loc_label.pack(pady=20)

        # Map Canvas
        self.canvas = tk.Canvas(self, width=500, height=500, bg="white")
        self.canvas.pack(pady=10)

        # Back Button
        self.back_button = tk.Button(self, text="Back to Menu", command=self.back_to_menu)
        self.back_button.pack(pady=30)

        # Display content
        self.display_content()

    def display_content(self):
        # Display image if available
        if self.image_path:
            try:
                img = Image.open(self.image_path)
                img = img.resize((300, 300), Image.LANCZOS)
                self.img_tk = ImageTk.PhotoImage(img)
                self.canvas.create_image(150, 150, image=self.img_tk, anchor=CENTER)
            except Exception as e:
                print(f"Error loading image: {e}")

        # Display map
        lat = 0
        lon = 0
        if self.gps_info and 'latitude' in self.gps_info and 'longitude' in self.gps_info:
            lat = self.gps_info['latitude']
            lon = self.gps_info['longitude']

        # Marking location on map
        self.map = Map(self.canvas, lat, lon)
        if self.gps_info:
            self.map.add_marker(lat, lon, "Image Location", "red")
        else:
            self.map.add_marker(lat, lon, "Default Location", "blue")
        self.map.update_canvas()

    def back_to_menu(self):
        self.pack_forget()
        from menuscreen import MenuApp
        MenuApp(master=self.master)