import requests

response = requests.head(
    "http://127.0.0.1:8000/media/static/videos/The_Drive_-_1_Hour_Version_-_4K_60fps_lrf-GAYUOkQ.mp4",
    headers={"Range": "bytes=0-1"}
)

print(response.status_code)
