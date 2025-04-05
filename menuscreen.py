import base64
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from exifInformation import get_gps_info
from infoscreen import InfoApp


class MenuApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master

        # Welcome Label
        self.label = tk.Label(self, text="WELCOME TO MIMOZA", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        # Upload Label
        self.label = tk.Label(self, text="Upload an image", font=("Arial", 14))
        self.label.pack(pady=10)

        # Upload Button
        self.upload_button = tk.Button(self, text="Choose Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # Canvas to display the image
        self.canvas = tk.Canvas(self, width=400, height=400, bg="gray")
        self.canvas.pack(pady=10)

        # Check Button
        self.check_button = tk.Button(self, text="Show Information", command=self.show_information, state=tk.DISABLED)
        self.check_button.pack(pady=10)

        self.current_image_path = None
        self.gps_info = None


    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.current_image_path = file_path
            self.gps_info = get_gps_info(file_path)

            try:
                image = Image.open(file_path)
                image.thumbnail((400, 400))
                self.img = ImageTk.PhotoImage(image)
                self.canvas.create_image(200, 200, image=self.img, anchor=CENTER)
                self.check_button.config(state=tk.NORMAL)
            except Exception as e:
                print(f"Error loading image: {e}")

    # Redirect to InfoApp
    def show_information(self):
        if not self.current_image_path:
            return

        self.pack_forget()
        InfoApp(master=self.master, image_path=self.current_image_path, gps_info=self.gps_info)


def main():
    root = tk.Tk()
    root.title("Mimoza")
    root.iconbitmap("location.ico")
    root.minsize(600, 700)
    root.maxsize(600, 700)

    MenuApp(master=root)
    root.mainloop()


if __name__ == "__main__":
    main()