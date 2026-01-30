from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar, QListWidget, QListWidgetItem, QRadioButton, QGroupBox, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core.scan_engine import ScanEngine

class ScanThread(QThread):
    """扫描线程"""
    progress_updated = pyqtSignal(int)
    file_scanned = pyqtSignal(str)
    scan_completed = pyqtSignal(list)
    
    def __init__(self, scan_type, custom_path=None):
        super().__init__()
        self.scan_type = scan_type
        self.custom_path = custom_path
        
    def run(self):
        engine = ScanEngine()
        if self.scan_type == "quick":
            results = engine.quick_scan(self.progress_updated, self.file_scanned)
        elif self.scan_type == "full":
            results = engine.full_scan(self.progress_updated, self.file_scanned)
        elif self.scan_type == "custom" and self.custom_path:
            results = engine.custom_scan(self.custom_path, self.progress_updated, self.file_scanned)
        else:
            results = []
        self.scan_completed.emit(results)

class ScanWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.scan_thread = None
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("病毒扫描")
        title_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 18px; font-weight: bold; margin: 20px 0;")
        layout.addWidget(title_label)
        
        # 扫描类型选择
        scan_type_group = QGroupBox("扫描类型")
        scan_type_layout = QVBoxLayout(scan_type_group)
        
        self.quick_scan_radio = QRadioButton("快速扫描")
        self.full_scan_radio = QRadioButton("完整扫描")
        self.custom_scan_radio = QRadioButton("自定义扫描")
        
        self.quick_scan_radio.setChecked(True)
        
        scan_type_layout.addWidget(self.quick_scan_radio)
        scan_type_layout.addWidget(self.full_scan_radio)
        scan_type_layout.addWidget(self.custom_scan_radio)
        
        # 自定义扫描路径选择
        self.custom_path_button = QPushButton("选择路径")
        self.custom_path_button.clicked.connect(self.select_custom_path)
        self.custom_path_label = QLabel("未选择路径")
        self.custom_path_label.setStyleSheet("color: #666; font-size: 12px;")
        
        custom_path_layout = QHBoxLayout()
        custom_path_layout.addWidget(self.custom_path_button)
        custom_path_layout.addWidget(self.custom_path_label, 1)
        
        scan_type_layout.addLayout(custom_path_layout)
        layout.addWidget(scan_type_group)
        
        # 扫描按钮
        self.scan_button = QPushButton("开始扫描")
        self.scan_button.clicked.connect(self.start_scan)
        self.scan_button.setStyleSheet("font-family: 'Microsoft YaHei'; padding: 10px; font-size: 14px;")
        layout.addWidget(self.scan_button)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # 扫描状态
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("font-family: 'Microsoft YaHei'; margin: 10px 0;")
        layout.addWidget(self.status_label)
        
        # 扫描文件列表
        self.file_list_widget = QListWidget()
        self.file_list_widget.setMaximumHeight(200)
        layout.addWidget(self.file_list_widget)
        
        # 扫描结果
        self.result_label = QLabel("扫描结果: 暂无")
        self.result_label.setStyleSheet("font-family: 'Microsoft YaHei'; margin: 10px 0; font-weight: bold;")
        layout.addWidget(self.result_label)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        self.stop_button = QPushButton("停止扫描")
        self.stop_button.clicked.connect(self.stop_scan)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        
        self.quit_button = QPushButton("关闭")
        self.quit_button.clicked.connect(self.close)
        self.quit_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()
        button_layout.addWidget(self.quit_button)
        
        layout.addLayout(button_layout)
        
    def select_custom_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择扫描路径")
        if path:
            self.custom_path_label.setText(path)
            self.custom_scan_radio.setChecked(True)
    
    def start_scan(self):
        # 禁用按钮
        self.scan_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # 重置UI
        self.progress_bar.setValue(0)
        self.status_label.setText("正在扫描...")
        self.file_list_widget.clear()
        self.result_label.setText("扫描结果: 暂无")
        
        # 确定扫描类型
        if self.quick_scan_radio.isChecked():
            scan_type = "quick"
            custom_path = None
        elif self.full_scan_radio.isChecked():
            scan_type = "full"
            custom_path = None
        elif self.custom_scan_radio.isChecked():
            scan_type = "custom"
            custom_path = self.custom_path_label.text() if self.custom_path_label.text() != "未选择路径" else None
        
        if scan_type == "custom" and not custom_path:
            self.status_label.setText("请选择自定义扫描路径")
            self.scan_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            return
        
        # 创建并启动扫描线程
        self.scan_thread = ScanThread(scan_type, custom_path)
        self.scan_thread.progress_updated.connect(self.update_progress)
        self.scan_thread.file_scanned.connect(self.update_file_list)
        self.scan_thread.scan_completed.connect(self.scan_finished)
        self.scan_thread.start()
    
    def stop_scan(self):
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.terminate()
            self.status_label.setText("扫描已停止")
            self.scan_button.setEnabled(True)
            self.stop_button.setEnabled(False)
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_file_list(self, file_path):
        item = QListWidgetItem(file_path)
        self.file_list_widget.addItem(item)
        self.file_list_widget.scrollToBottom()
    
    def scan_finished(self, results):
        self.status_label.setText("扫描完成")
        self.scan_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if results:
            self.result_label.setText(f"扫描结果: 发现 {len(results)} 个威胁")
            # 显示威胁文件
            for threat in results:
                item = QListWidgetItem(f"[威胁] {threat}")
                item.setForeground(Qt.red)
                self.file_list_widget.addItem(item)
        else:
            self.result_label.setText("扫描结果: 未发现威胁")
    
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
            elif isinstance(widget, QListWidget):
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; {styles['list_widget']}")
            elif isinstance(widget, QProgressBar):
                widget.setStyleSheet(f"{styles['progress_bar']}")
                # 更新进度条填充颜色
                widget.setStyleSheet(f"QProgressBar::chunk {{ {styles['progress_bar_fill']} }}")
            elif isinstance(widget, QGroupBox):
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; {styles['group_box']}")
