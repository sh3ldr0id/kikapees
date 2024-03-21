from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, imwrite, resize, imread, FONT_HERSHEY_SIMPLEX, getTextSize, LINE_AA, putText
import numpy as np
from uuid import uuid4

def generate_thumbnail(file):
    filename = None
    prefix = None
    extension = None

    if type(file) == str:
        filename = file
        prefix = file.rsplit('.', 1)[0]
        extension = file.rsplit('.', 1)[1]

    else:
        prefix = f"temp/{str(uuid4())}"
        extension = file.filename.rsplit('.', 1)[-1]
        filename = f"{prefix}.{extension}"

        file.save(f"{prefix}.{extension}")
    
    if extension in ['mp4', 'avi', 'mkv', 'mov']:
        return _video_thumbnail(filename), filename
    
    elif extension in ["png", "jpg", "jpeg", "gif"]:
        return _image_thumbnail(filename), filename
    
    elif extension in ["txt", "json", "csv"]:
        return _text_thumbnail(filename), filename
    
    else:
        return f"thumbnails/unknown.jpg", f"{filename}.{extension}"
    
def _video_thumbnail(filename):
    try:
        cap = VideoCapture(filename)

        frame_count = int(cap.get(CAP_PROP_FRAME_COUNT))
        skip_frames = round(frame_count / 2)

        cap.set(CAP_PROP_POS_FRAMES, skip_frames)
        _, frame = cap.read()
        cap.release()

        resized_frame = resize(frame, (300, 300))

        thumbnail_filename = f"temp/{uuid4()}.png"
        
        imwrite(thumbnail_filename, resized_frame)

    except:
        thumbnail_filename = "thumbnails/video.jpg"

    return thumbnail_filename

def _image_thumbnail(filename):
    try:
        frame = imread(filename)
        resized_frame = resize(frame, (300, 300))

        thumbnail_filename = f"temp/{uuid4()}.png"
        
        imwrite(thumbnail_filename, resized_frame)

    except:
        thumbnail_filename = "thumbnails/image.jpg"

    return thumbnail_filename

def _text_thumbnail(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()

        image_width = 300
        image_height = 300
        text_color = (0, 0, 0)  

        image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255
        font = FONT_HERSHEY_SIMPLEX
        text_size = getTextSize(text, font, 1, 2)[0]
        text_x = (image_width - text_size[0]) // 2
        text_y = (image_height + text_size[1]) // 2

        putText(image, text, (text_x, text_y), font, 1, text_color, 2, LINE_AA)

        thumbnail_filename = f"temp/{uuid4()}.png"

        imwrite(thumbnail_filename, image)

    except:
        thumbnail_filename = "thumbnails/text.jpg"

    return thumbnail_filename