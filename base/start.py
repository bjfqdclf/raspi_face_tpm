import sys, os
if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    sys.path.append("..")
    from face_recognition.face_detect import FaceServer
    face_obj = FaceServer(path)
    face_obj.face_start()
