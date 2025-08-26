from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem


class VideoBackgroundView(QWidget):
    """
    Base View עם רקע וידאו בלופ ושכבת Overlay שקופה
    מסכים אחרים (LoginView, MainView) יורשים ממנו.
    """

    def __init__(self, video_path="client/assets/background.mp4", opacity=0.9):
        super().__init__()
        self.setMinimumSize(420, 300)

        # יצירת סצנה ווידאו
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(self.rect())
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QGraphicsView.NoFrame)
        self.view.setStyleSheet("background: transparent; border: none;")

        # פריט וידאו עם שקיפות
        self.video_item = QGraphicsVideoItem()
        self.video_item.setOpacity(opacity)
        self.scene.addItem(self.video_item)

        # נגן וידאו
        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_item)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.media_player.play()
        self.media_player.mediaStatusChanged.connect(self.handle_loop)

        # overlay שקוף לתוכן
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background: transparent;")
        self.layout = QVBoxLayout(self.overlay)
        self.layout.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        """וידאו יתפרס על כל המסך בעת שינוי גודל"""
        self.view.setGeometry(self.rect())
        self.overlay.setGeometry(self.rect())
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.video_item.setSize(self.rect().size())
        super().resizeEvent(event)

    def handle_loop(self, status):
        """וידאו יחזור בלופ אינסופי"""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()
