from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core.update_manager import UpdateManager

class UpdateThread(QThread):
    """更新线程"""
    progress_updated = pyqtSignal(int)
    update_completed = pyqtSignal(bool, str)
    
    def run(self):
        update_manager = UpdateManager()
        try:
            success, message = update_manager.check_and_update(self.progress_updated)
            self.update_completed.emit(success, message)
        except Exception as e:
            self.update_completed.emit(False, str(e))

class UpdateWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_thread = None
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("在线更新")
        title_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 18px; font-weight: bold; margin: 20px 0;")
        layout.addWidget(title_label)
        
        # 当前版本信息
        self.version_label = QLabel("当前版本: 1.0.0")
        self.version_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 14px; margin: 10px 0;")
        layout.addWidget(self.version_label)
        
        # 检查更新按钮
        self.check_update_button = QPushButton("检查更新")
        self.check_update_button.clicked.connect(self.check_update)
        self.check_update_button.setStyleSheet("font-family: 'Microsoft YaHei'; padding: 10px; font-size: 14px;")
        layout.addWidget(self.check_update_button)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 状态信息
        self.status_label = QLabel("更新状态: 就绪")
        self.status_label.setStyleSheet("font-family: 'Microsoft YaHei'; margin: 10px 0;")
        layout.addWidget(self.status_label)
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("font-family: 'Microsoft YaHei'; padding: 10px; font-size: 14px;")
        layout.addWidget(close_button)
        
    def check_update(self):
        """检查更新"""
        self.check_update_button.setEnabled(False)
        self.status_label.setText("正在检查更新...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 创建并启动更新线程
        self.update_thread = UpdateThread()
        self.update_thread.progress_updated.connect(self.update_progress)
        self.update_thread.update_completed.connect(self.update_finished)
        self.update_thread.start()
    
    def update_progress(self, value):
        """更新进度"""
        self.progress_bar.setValue(value)
    
    def update_finished(self, success, message):
        """更新完成"""
        self.check_update_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.status_label.setText("更新状态: 已更新到最新版本")
        else:
            QMessageBox.warning(self, "失败", message)
            self.status_label.setText("更新状态: 更新失败")
    
    def update_theme(self):
        """更新主题样式"""
        from utils.theme_manager import ThemeManager
        theme_manager = ThemeManager()
        styles = theme_manager.get_theme_styles()
        
        # 更新窗口样式
        self.setStyleSheet(styles['window'])
        
        # 更新所有标签样式
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; {styles['label']}")
            elif isinstance(widget, QPushButton):
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; padding: 10px; font-size: 14px; {styles['button']}")
            elif isinstance(widget, QProgressBar):
                widget.setStyleSheet(f"{styles['progress_bar']}")
                # 更新进度条填充颜色
                widget.setStyleSheet(f"QProgressBar::chunk {{ {styles['progress_bar_fill']} }}")
