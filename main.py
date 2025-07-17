import cv2
from src.video_capture import VideoCapture
from src.face_detector import FaceDetector
import config

def main():
    face_detector = FaceDetector(
        cascade_file_path=config.CASCADE_FILE_PATH,
        scale_factor=config.SCALE_FACTOR
    )

    with VideoCapture(0) as video_capture:
        while True:
            # 1. Read a frame
            success, frame = video_capture.read_frame()
            if not success:
                break

            # 2. Detect faces (gets coordinates)
            faces = face_detector.detect_faces(frame)

            # 3. Draw rectangles and text on the frame
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            face_count_text = f"Faces detected: {len(faces)}"
            cv2.putText(frame, face_count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # 4. Display the modified frame
            cv2.imshow(config.WINDOW_NAME, frame)

            # 5. Check for stop key
            if cv2.waitKey(1) & 0xFF == ord(config.STOP_KEY):
                break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
