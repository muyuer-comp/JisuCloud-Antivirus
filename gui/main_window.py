from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from gui.scan_window import ScanWindow
from gui.quarantine_window import QuarantineWindow
from gui.trust_window import TrustWindow
from gui.about_window import AboutWindow
from gui.update_window import UpdateWindow
from utils.theme_manager import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("极速云杀毒")
        self.setGeometry(100, 100, 900, 600)
        
        # 初始化主题管理器
        self.theme_manager = ThemeManager()
        
        # 创建主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # 创建侧边栏
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        
        # 标题
        title_label = QLabel("极速云杀毒")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 16px; font-weight: bold; margin: 20px 0;")
        sidebar_layout.addWidget(title_label)
        
        # 导航按钮
        self.nav_buttons = []
        nav_items = [
            ("主页", self.show_home),
            ("扫描", self.show_scan),
            ("隔离区", self.show_quarantine),
            ("信任区", self.show_trust),
            ("关于", self.show_about),
            ("在线更新", self.show_update)
        ]
        
        for text, callback in nav_items:
            button = QPushButton(text)
            button.clicked.connect(callback)
            button.setStyleSheet("font-family: 'Microsoft YaHei'; padding: 10px; text-align: left; margin: 5px 0;")
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)
        
        # 亮暗切换按钮
        self.theme_button = QPushButton("切换到暗色模式" if self.theme_manager.get_current_theme() == 'light' else "切换到亮色模式")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setStyleSheet("font-family: 'Microsoft YaHei'; padding: 10px; text-align: left; margin: 5px 0;")
        sidebar_layout.addWidget(self.theme_button)
        
        # 创建主内容区域
        self.stacked_widget = QStackedWidget()
        
        # 创建各个子窗口
        self.home_window = self.create_home_window()
        self.scan_window = ScanWindow()
        self.quarantine_window = QuarantineWindow()
        self.trust_window = TrustWindow()
        
        # 添加到堆叠窗口
        self.stacked_widget.addWidget(self.home_window)
        self.stacked_widget.addWidget(self.scan_window)
        self.stacked_widget.addWidget(self.quarantine_window)
        self.stacked_widget.addWidget(self.trust_window)
        
        # 组装布局
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget, 1)
        
        # 加载保存的主题设置
        self.update_theme()
        
    def create_home_window(self):
        """创建主页窗口"""
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)
        
        title = QLabel("欢迎使用 极速云杀毒")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 24px; font-weight: bold; margin: 50px 0;")
        
        status_label = QLabel("系统状态: 安全")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 16px; color: green; margin: 20px 0;")
        
        quick_scan_button = QPushButton("快速扫描")
        quick_scan_button.setStyleSheet("font-family: 'Microsoft YaHei'; padding: 15px; font-size: 14px;")
        quick_scan_button.clicked.connect(self.show_scan)
        
        layout.addWidget(title)
        layout.addWidget(status_label)
        layout.addWidget(quick_scan_button)
        layout.addStretch()
        
        return home_widget
    
    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.home_window)
    
    def show_scan(self):
        self.stacked_widget.setCurrentWidget(self.scan_window)
    
    def show_quarantine(self):
        self.stacked_widget.setCurrentWidget(self.quarantine_window)
    
    def show_trust(self):
        self.stacked_widget.setCurrentWidget(self.trust_window)
    
    def show_about(self):
        about_window = AboutWindow()
        about_window.exec_()
    
    def show_update(self):
        update_window = UpdateWindow()
        update_window.exec_()
    
    def toggle_theme(self):
        """切换主题"""
        # 切换主题
        new_theme = self.theme_manager.switch_theme()
        
        # 更新主题按钮文本
        self.theme_button.setText("切换到暗色模式" if new_theme == 'light' else "切换到亮色模式")
        
        # 更新窗口样式
        self.update_theme()
    
    def update_theme(self):
        """更新主题样式"""
        # 获取当前主题样式
        styles = self.theme_manager.get_theme_styles()
        
        # 更新主窗口样式
        self.setStyleSheet(styles['window'])
        
        # 更新侧边栏样式
        sidebar = self.centralWidget().layout().itemAt(0).widget()
        sidebar.setStyleSheet(styles['sidebar'])
        
        # 更新所有按钮样式
        for button in self.nav_buttons:
            button.setStyleSheet(f"font-family: 'Microsoft YaHei'; padding: 10px; text-align: left; margin: 5px 0; {styles['button']}")
        
        # 更新主题按钮样式
        self.theme_button.setStyleSheet(f"font-family: 'Microsoft YaHei'; padding: 10px; text-align: left; margin: 5px 0; {styles['button']}")
        
        # 更新当前显示窗口的样式
        current_widget = self.stacked_widget.currentWidget()
        if current_widget == self.home_window:
            self.update_home_theme()
        elif current_widget == self.scan_window:
            self.scan_window.update_theme()
        elif current_widget == self.quarantine_window:
            self.quarantine_window.update_theme()
        elif current_widget == self.trust_window:
            self.trust_window.update_theme()
    
    def update_home_theme(self):
        """更新主页主题样式"""
        styles = self.theme_manager.get_theme_styles()
        
        # 更新主页中的控件样式
        for i in range(self.home_window.layout().count()):
            widget = self.home_window.layout().itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; {styles['label']}")
            elif isinstance(widget, QPushButton):
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; padding: 15px; font-size: 14px; {styles['button']}")
