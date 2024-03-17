from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, imwrite
from uuid import uuid4

def generate_thumbnail(file):
    filename = None
    extension = None

    if type(file) == str:
        filename = file.rsplit('.', 1)[0]
        extension = file.rsplit('.', 1)[-1]

    else:
        filename = f"temp/{str(uuid4())}"
        extension = file.filename.rsplit('.', 1)[-1]

        file.save(f"{filename}.{extension}")
    
    if extension in ['mp4', 'avi', 'mkv', 'mov']:
        cap = VideoCapture(f"{filename}.{extension}")

        frame_count = int(cap.get(CAP_PROP_FRAME_COUNT))
        skip_frames = round(frame_count / 2)

        cap.set(CAP_PROP_POS_FRAMES, skip_frames)
        _, frame = cap.read()

        cap.release()
        
        imwrite(f"{filename}.png", frame)

        return f"{filename}.png", f"{filename}.{extension}"
    
    elif extension in ["png", "jpg", "jpeg", "gif"]:
        return f"{filename}.{extension}", f"{filename}.{extension}"
    
    else:
        return f"default_thumbnail.svg", f"{filename}.{extension}"