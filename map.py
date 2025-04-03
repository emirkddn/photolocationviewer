import folium
import tempfile
import os
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import atexit
import io


class Map:
    def __init__(self, canvas, lat=30, lon=40, zoom=12):
        self.canvas = canvas
        self.lat = lat
        self.lon = lon
        self.zoom = zoom
        self.map = folium.Map(location=[lat, lon], zoom_start=zoom)
        self.driver = None
        self.setup_selenium()

    def setup_selenium(self):
        """Initialize headless Chrome browser for screenshot"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=600,600")
        self.driver = webdriver.Chrome(options=chrome_options)
        atexit.register(self.cleanup)

    def add_marker(self, lat, lon, tooltip="", color="green"):
        folium.Marker(
            location=[lat, lon],
            tooltip=tooltip,
            icon=folium.Icon(color=color),
        ).add_to(self.map)

    def update_canvas(self):
        """Save map to HTML and take screenshot"""
        temp_html = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
        self.map.save(temp_html.name)

        # Open in browser and take screenshot
        self.driver.get(f"file://{temp_html.name}")
        time.sleep(1)  # Wait for map to load

        # Get screenshot as PNG
        png = self.driver.get_screenshot_as_png()
        img = Image.open(io.BytesIO(png))
        img = img.resize((600, 600), Image.LANCZOS)

        # Display on canvas
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor='nw', image=img_tk)
        self.canvas.image = img_tk

        # Cleanup
        temp_html.close()
        os.unlink(temp_html.name)

    def cleanup(self):
        if self.driver:
            self.driver.quit()