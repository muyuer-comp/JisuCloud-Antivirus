import os
import shutil
import time

class QuarantineManager:
    """隔离区管理器"""
    
    def __init__(self):
        self.quarantine_dir = os.path.join(os.getcwd(), 'quarantine')
        self.quarantine_log = os.path.join(os.getcwd(), 'quarantine.log')
        self._init_quarantine()
    
    def _init_quarantine(self):
        """初始化隔离区"""
        if not os.path.exists(self.quarantine_dir):
            os.makedirs(self.quarantine_dir)
        
        if not os.path.exists(self.quarantine_log):
            with open(self.quarantine_log, 'w', encoding='utf-8') as f:
                pass
    
    def quarantine_file(self, file_path):
        """隔离文件"""
        try:
            if not os.path.exists(file_path):
                return False
            
            # 生成隔离文件名
            file_name = os.path.basename(file_path)
            quarantine_time = time.strftime('%Y%m%d_%H%M%S')
            quarantine_file = os.path.join(self.quarantine_dir, f"{quarantine_time}_{file_name}")
            
            # 移动文件到隔离区
            shutil.move(file_path, quarantine_file)
            
            # 记录隔离日志
            with open(self.quarantine_log, 'a', encoding='utf-8') as f:
                f.write(f"{quarantine_time},{file_name},{file_path},{quarantine_file}\n")
            
            return True
        except Exception:
            return False
    
    def restore_file(self, original_path):
        """恢复文件"""
        try:
            # 查找隔离文件
            quarantine_file = None
            with open(self.quarantine_log, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',', 3)
                    if len(parts) == 4 and parts[2] == original_path:
                        quarantine_file = parts[3]
                        break
            
            if not quarantine_file or not os.path.exists(quarantine_file):
                return False
            
            # 恢复文件
            shutil.move(quarantine_file, original_path)
            
            # 更新日志
            new_log_lines = []
            with open(self.quarantine_log, 'r', encoding='utf-8') as f:
                for line in f:
                    if original_path not in line:
                        new_log_lines.append(line)
            
            with open(self.quarantine_log, 'w', encoding='utf-8') as f:
                f.writelines(new_log_lines)
            
            return True
        except Exception:
            return False
    
    def delete_file(self, original_path):
        """删除隔离文件"""
        try:
            # 查找隔离文件
            quarantine_file = None
            with open(self.quarantine_log, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',', 3)
                    if len(parts) == 4 and parts[2] == original_path:
                        quarantine_file = parts[3]
                        break
            
            if quarantine_file and os.path.exists(quarantine_file):
                os.remove(quarantine_file)
            
            # 更新日志
            new_log_lines = []
            with open(self.quarantine_log, 'r', encoding='utf-8') as f:
                for line in f:
                    if original_path not in line:
                        new_log_lines.append(line)
            
            with open(self.quarantine_log, 'w', encoding='utf-8') as f:
                f.writelines(new_log_lines)
            
            return True
        except Exception:
            return False
    
    def get_quarantine_items(self):
        """获取隔离区项目"""
        items = []
        try:
            with open(self.quarantine_log, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(',', 3)
                    if len(parts) == 4:
                        items.append({
                            'quarantine_time': parts[0],
                            'file_name': parts[1],
                            'file_path': parts[2],
                            'quarantine_path': parts[3]
                        })
        except Exception:
            pass
        return items
    
    def empty_quarantine(self):
        """清空隔离区"""
        try:
            # 删除所有隔离文件
            for file in os.listdir(self.quarantine_dir):
                file_path = os.path.join(self.quarantine_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            # 清空日志
            with open(self.quarantine_log, 'w', encoding='utf-8') as f:
                pass
            
            return True
        except Exception:
            return False
