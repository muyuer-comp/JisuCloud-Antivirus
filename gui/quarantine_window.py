from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from core.quarantine_manager import QuarantineManager

class QuarantineWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.quarantine_manager = QuarantineManager()
        self.load_quarantine_items()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("隔离区")
        title_label.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 18px; font-weight: bold; margin: 20px 0;")
        layout.addWidget(title_label)
        
        # 隔离区文件列表
        self.quarantine_list = QListWidget()
        self.quarantine_list.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.quarantine_list)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.restore_button = QPushButton("恢复选中文件")
        self.restore_button.clicked.connect(self.restore_selected)
        self.restore_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        button_layout.addWidget(self.restore_button)
        
        self.delete_button = QPushButton("删除选中文件")
        self.delete_button.clicked.connect(self.delete_selected)
        self.delete_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        button_layout.addWidget(self.delete_button)
        
        self.empty_button = QPushButton("清空隔离区")
        self.empty_button.clicked.connect(self.empty_quarantine)
        self.empty_button.setStyleSheet("font-family: 'Microsoft YaHei';")
        button_layout.addWidget(self.empty_button)
        
        layout.addLayout(button_layout)
        
        # 状态信息
        self.status_label = QLabel("隔离区状态: 就绪")
        self.status_label.setStyleSheet("font-family: 'Microsoft YaHei'; margin: 10px 0;")
        layout.addWidget(self.status_label)
        
    def load_quarantine_items(self):
        """加载隔离区项目"""
        self.quarantine_list.clear()
        quarantine_items = self.quarantine_manager.get_quarantine_items()
        
        if quarantine_items:
            for item in quarantine_items:
                list_item = QListWidgetItem(f"{item['file_name']} - {item['quarantine_time']}")
                list_item.setData(Qt.UserRole, item['file_path'])
                self.quarantine_list.addItem(list_item)
            self.status_label.setText(f"隔离区状态: 共 {len(quarantine_items)} 个文件")
        else:
            self.status_label.setText("隔离区状态: 空")
    
    def restore_selected(self):
        """恢复选中的文件"""
        selected_items = self.quarantine_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "提示", "请选择要恢复的文件")
            return
        
        for item in selected_items:
            file_path = item.data(Qt.UserRole)
            success = self.quarantine_manager.restore_file(file_path)
            if success:
                self.quarantine_list.takeItem(self.quarantine_list.row(item))
        
        QMessageBox.information(self, "成功", f"已恢复 {len(selected_items)} 个文件")
        self.load_quarantine_items()
    
    def delete_selected(self):
        """删除选中的文件"""
        selected_items = self.quarantine_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "提示", "请选择要删除的文件")
            return
        
        reply = QMessageBox.question(self, "确认", f"确定要删除选中的 {len(selected_items)} 个文件吗？",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for item in selected_items:
                file_path = item.data(Qt.UserRole)
                success = self.quarantine_manager.delete_file(file_path)
                if success:
                    self.quarantine_list.takeItem(self.quarantine_list.row(item))
            
            QMessageBox.information(self, "成功", f"已删除 {len(selected_items)} 个文件")
            self.load_quarantine_items()
    
    def empty_quarantine(self):
        """清空隔离区"""
        reply = QMessageBox.question(self, "确认", "确定要清空整个隔离区吗？此操作不可恢复。",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            success = self.quarantine_manager.empty_quarantine()
            if success:
                self.quarantine_list.clear()
                self.status_label.setText("隔离区状态: 空")
                QMessageBox.information(self, "成功", "隔离区已清空")
    
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
