import cv2
from fps import FPS


class VideoPlayer:
    def __init__(self, source=0, dest=None):
        self._source = source
        self._dest = dest
        self._frame = None
        self._playing = False
        self._fps = FPS()

    def start(self):
        self._cap = cv2.VideoCapture(self._source)
        self._cap.set(3, 640)
        self._cap.set(4, 640)
        if self._dest is not None:
            width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
            height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
            fps = int(self._cap.get(cv2.CAP_PROP_FPS))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self._out = cv2.VideoWriter(
                self._dest, fourcc, fps, (width, height))
        self._playing = True
        self._fps.start()
        while self._playing:
            self.read_frame()
            self.process_frame()
            self.write_frame()
        self._fps.stop()
        print(self._fps.fps())

    def stop(self):
        self._playing = False
        self._cap.release()
        self._out.release()
        cv2.destroyAllWindows()

    def read_frame(self):
        ret, frame = self._cap.read()
        self._frame = frame
        self._fps.update()

    def process_frame(self):
        pass

    def write_frame(self):
        self.show_frame()
        if self._dest is not None:
            self.save_frame()

    def show_frame(self):
        cv2.imshow('Video', self._frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop()

    def save_frame(self):
        self._out.write(self._frame)


player = VideoPlayer(dest='vid.mp4')
player.start()
