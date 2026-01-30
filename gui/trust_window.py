from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from core.trust_manager import TrustManager

class TrustWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.trust_manager = TrustManager()
        self.load_trust_items()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("信任区")
        title_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 18px; font-weight: bold; margin: 20px 0;")
        layout.addWidget(title_label)
        
        # 添加信任项按钮
        add_button_layout = QHBoxLayout()
        
        self.add_file_button = QPushButton("添加文件")
        self.add_file_button.clicked.connect(self.add_file)
        self.add_file_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        add_button_layout.addWidget(self.add_file_button)
        
        self.add_folder_button = QPushButton("添加文件夹")
        self.add_folder_button.clicked.connect(self.add_folder)
        self.add_folder_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        add_button_layout.addWidget(self.add_folder_button)
        
        layout.addLayout(add_button_layout)
        
        # 信任区列表
        self.trust_list = QListWidget()
        self.trust_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.trust_list)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.remove_button = QPushButton("移除选中项")
        self.remove_button.clicked.connect(self.remove_selected)
        self.remove_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        button_layout.addWidget(self.remove_button)
        
        self.clear_button = QPushButton("清空信任区")
        self.clear_button.clicked.connect(self.clear_trust)
        self.clear_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # 状态信息
        self.status_label = QLabel("信任区状态: 就绪")
        self.status_label.setStyleSheet("font-family: 'Microsoft YaHei'; margin: 10px 0;")
        layout.addWidget(self.status_label)
        
    def load_trust_items(self):
        """加载信任区项目"""
        self.trust_list.clear()
        trust_items = self.trust_manager.get_trust_items()
        
        if trust_items:
            for item in trust_items:
                list_item = QListWidgetItem(item)
                self.trust_list.addItem(list_item)
            self.status_label.setText(f"信任区状态: 共 {len(trust_items)} 个项目")
        else:
            self.status_label.setText("信任区状态: 空")
    
    def add_file(self):
        """添加文件到信任区"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            success = self.trust_manager.add_to_trust(file_path)
            if success:
                self.trust_list.addItem(file_path)
                QMessageBox.information(self, "成功", "文件已添加到信任区")
                self.load_trust_items()
            else:
                QMessageBox.warning(self, "失败", "文件已在信任区中")
    
    def add_folder(self):
        """添加文件夹到信任区"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            success = self.trust_manager.add_to_trust(folder_path)
            if success:
                self.trust_list.addItem(folder_path)
                QMessageBox.information(self, "成功", "文件夹已添加到信任区")
                self.load_trust_items()
            else:
                QMessageBox.warning(self, "失败", "文件夹已在信任区中")
    
    def remove_selected(self):
        """移除选中的信任项"""
        selected_items = self.trust_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "提示", "请选择要移除的项目")
            return
        
        for item in selected_items:
            trust_path = item.text()
            self.trust_manager.remove_from_trust(trust_path)
            self.trust_list.takeItem(self.trust_list.row(item))
        
        QMessageBox.information(self, "成功", f"已移除 {len(selected_items)} 个项目")
        self.load_trust_items()
    
    def clear_trust(self):
        """清空信任区"""
        reply = QMessageBox.question(self, "确认", "确定要清空整个信任区吗？",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.trust_manager.clear_trust()
            self.trust_list.clear()
            self.status_label.setText("信任区状态: 空")
            QMessageBox.information(self, "成功", "信任区已清空")
    
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
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; {styles['button']}")
            elif isinstance(widget, QListWidget):
                widget.setStyleSheet(f"font-family: 'Microsoft YaHei'; {styles['list_widget']}")
