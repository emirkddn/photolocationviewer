from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Photo GPS Information
def get_gps_info(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()  #Extracts exif information of the photo.

        if not exif_data:
            return None

        # Extracts GPS from EXIF information.
        gps_info = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "GPSInfo":
                for gps_tag in value:
                    gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                    gps_info[gps_tag_name] = value[gps_tag]

        if not gps_info:
            return None

        # Convert GPS coordinates to decimal degrees.
        def convert_to_degrees(value):
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)

        # Latitude
        lat = convert_to_degrees(gps_info[2])
        if gps_info[1] == 'S':
            lat = -lat

        # Longitude
        lon = convert_to_degrees(gps_info[4])
        if gps_info[3] == 'W':
            lon = -lon

        return {'latitude': lat, 'longitude': lon}

    except Exception as e:
        print(f"Error reading EXIF data: {e}")
        return None