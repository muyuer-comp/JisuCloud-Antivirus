from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # 标题
        title_label = QLabel("关于 极速云杀毒")
        title_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 20px; font-weight: bold; margin: 20px 0;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 版本信息
        version_label = QLabel("版本: 1.0.0")
        version_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 14px; margin: 10px 0;")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # 描述
        description_label = QLabel("极速云杀毒 是一款功能强大的安全扫描软件，提供全面的病毒检测和防护功能，保护您的计算机免受恶意软件的侵害。")
        description_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 14px; margin: 20px 0; line-height: 1.5;")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        layout.addWidget(description_label)
        
        # 功能列表
        features_label = QLabel("主要功能:")
        features_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 14px; font-weight: bold; margin: 10px 0;")
        features_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(features_label)
        
        features_list = [
            "快速扫描和完整扫描",
            "自定义扫描路径",
            "隔离区管理",
            "信任区管理",
            "在线更新"
        ]
        
        for feature in features_list:
            feature_label = QLabel(f"• {feature}")
            feature_label.setStyleSheet("font-family: 'Microsoft YaHei';")
            feature_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(feature_label)
        
        # 版权信息
        copyright_label = QLabel("© 2026 极速云安全. 保留所有权利。")
        copyright_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 12px; color: #666; margin: 30px 0;")
        copyright_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright_label)
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("font-family: 'Microsoft YaHei'; padding: 10px 20px; font-size: 14px;")
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
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
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; padding: 10px 20px; font-size: 14px; {styles['button']}")