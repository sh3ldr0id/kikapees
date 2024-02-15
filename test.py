import cv2

def generate_thumbnail(video_path, thumbnail_path):
    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()
    cap.release()
    
    if ret:
        cv2.imwrite(thumbnail_path, frame)

generate_thumbnail("temp/vid.mp4", "temp/thumbnail.png")