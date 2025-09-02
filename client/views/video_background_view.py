# client/views/video_background_view.py
import cv2
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap, QPainter

"""
    מחלקה שמציגה וידאו כרקע חלון.
    - טוענת מראש את כל הפריימים של הווידאו לזיכרון → הקרנה חלקה ללא הבהובים.
    - מתאימה את הווידאו לגודל החלון ('cover') תוך שמירה על יחס ממדים.
    - משתמשת ב־QTimer כדי להקרין פריימים לפי ה־
    FPS.
"""
class VideoBackgroundView(QWidget):

    def __init__(self, video_path="client/assets/background.mp4", fps_override=None, max_frames=None):

        super().__init__()
        # מבטלים ניקוי רקע מצד המערכת ומציירים אטום
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setMinimumSize(420, 300)

        # מצב נוכחי
        self._pixmaps: list[QPixmap] = []
        self._frame_idx = 0
        # גרסה מוקטנת/מוגדלת לפי גודל החלון
        self._scaled_cache: list[QPixmap] = []  

        # טען מראש את כל הפריימים
        self.fps = self._preload_video(video_path, fps_override, max_frames)
        self.interval_ms = max(1, int(1000 / self.fps))

        # אם משום מה לא נטען דבר — נגדיר שחור קבוע
        if not self._pixmaps:
            black = QPixmap(16, 16); black.fill(Qt.black)
            self._pixmaps = [black]
            self._scaled_cache = [black]

        # טיימר הקרנה
        self.timer = QTimer(self)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.timeout.connect(self._tick)
        self.timer.start(self.interval_ms)


    # ---------- טעינה מראש -----------
    # טוען את כל הפריימים של הווידאו לזיכרון
    def _preload_video(self, path, fps_override, max_frames):

        cap = cv2.VideoCapture(path)
        # אם לא מצליחים לפתוח, מחזירים ברירת מחדל
        if not cap.isOpened():
            return 30.0

        # קצב פריימים
        src_fps = float(cap.get(cv2.CAP_PROP_FPS) or 30.0)
        fps = float(fps_override) if fps_override else src_fps

        # תיקון קל למקרים בעייתיים
        if not fps_override and fps > 59.94:
            fps = 59.94
        if not fps_override and 29.97 < fps <= 60:
            fps = 29.95

        # טעינת פריימים ללולאה
        count = 0
        self._pixmaps.clear()
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            p = self._mat_to_pixmap(frame)
            self._pixmaps.append(p)
            count += 1
            if max_frames is not None and count >= max_frames:
                break

        cap.release()

        # בניית קאש סקלד
        self._scaled_cache = [self._scale_to_cover(p) for p in self._pixmaps]
        return fps or 30.0


    # ---------- המרות/סקייל -----------
    #
    def _mat_to_pixmap(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(qimg)

    def _scale_to_cover(self, pix: QPixmap):
        tw, th = max(1, self.width()), max(1, self.height())
        return pix.scaled(tw, th, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

    #אם הגודל השתנה — מייצרים מחדש את הקאש הסקלד
    def _rescale_cache(self):
        if not self._pixmaps:
            return
        tw, th = max(1, self.width()), max(1, self.height())
        if (self._scaled_cache 
            and self._scaled_cache[0].width() == tw 
            and self._scaled_cache[0].height() == th):
            return  
        self._scaled_cache = [self._scale_to_cover(p) for p in self._pixmaps]

    # ---------- לולאת הקרנה -----------
    # כל פעם שהטיימר מתקתק
    def _tick(self):

        if not self._scaled_cache:
            return
        self._frame_idx = (self._frame_idx + 1) % len(self._scaled_cache)
        self.update()

    # ---------- אירועי Qt -----------
    # ציור הפריימים
    def paintEvent(self, event):

        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)
        if not self._scaled_cache:
            return
        pix = self._scaled_cache[self._frame_idx]
        if not pix.isNull():
            painter.drawPixmap(0, 0, pix)

    # כאשר גודל החלון משתנה
    def resizeEvent(self, e):

        self._rescale_cache()
        self.update()
        super().resizeEvent(e)

    # עצירת הטיימר בעת סגירת החלון
    def closeEvent(self, e):
        
        try:
            if self.timer.isActive():
                self.timer.stop()
        except Exception:
            pass
        super().closeEvent(e)
