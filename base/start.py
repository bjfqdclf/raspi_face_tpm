import sys
if __name__ == '__main__':
    sys.path.append("..")
    from face_recognition.face_detect import FaceServer
    face_obj = FaceServer()
    face_obj.face_start()

