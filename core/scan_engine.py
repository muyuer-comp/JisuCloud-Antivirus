import os
import time
from utils.file_utils import get_system_directories

class ScanEngine:
    """扫描引擎"""
    
    def __init__(self):
        self.scan_count = 0
        self.threats_found = 0
        self.trust_paths = self._load_trust_paths()
    
    def _load_trust_paths(self):
        """加载信任路径"""
        try:
            with open('trust_paths.txt', 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    def _is_trusted(self, file_path):
        """检查文件是否在信任区"""
        for trust_path in self.trust_paths:
            if file_path.startswith(trust_path):
                return True
        return False
    
    def _scan_file(self, file_path):
        """扫描单个文件"""
        # 模拟病毒检测
        # 实际应用中，这里应该使用病毒特征库进行匹配
        threat_extensions = ['.virus', '.malware', '.trojan']
        for ext in threat_extensions:
            if file_path.endswith(ext):
                return True
        return False
    
    def quick_scan(self, progress_callback=None, file_callback=None):
        """快速扫描"""
        self.scan_count = 0
        self.threats_found = 0
        threats = []
        
        # 获取系统关键目录
        system_dirs = get_system_directories()
        total_files = self._count_files(system_dirs)
        scanned_files = 0
        
        for directory in system_dirs:
            if os.path.exists(directory):
                for root, _, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if not self._is_trusted(file_path):
                            self.scan_count += 1
                            scanned_files += 1
                            
                            # 更新进度
                            if progress_callback:
                                progress = int((scanned_files / total_files) * 100)
                                progress_callback.emit(min(progress, 100))
                            
                            # 回调文件信息
                            if file_callback:
                                file_callback.emit(file_path)
                            
                            # 扫描文件
                            if self._scan_file(file_path):
                                threats.append(file_path)
                                self.threats_found += 1
                            
                            # 模拟扫描延迟
                            time.sleep(0.01)
        
        return threats
    
    def full_scan(self, progress_callback=None, file_callback=None):
        """完整扫描"""
        self.scan_count = 0
        self.threats_found = 0
        threats = []
        
        # 获取所有驱动器
        drives = [f'{chr(c)}:' for c in range(65, 91) if os.path.exists(f'{chr(c)}:')]
        total_files = self._count_files(drives)
        scanned_files = 0
        
        for drive in drives:
            for root, _, files in os.walk(drive):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self._is_trusted(file_path):
                        self.scan_count += 1
                        scanned_files += 1
                        
                        # 更新进度
                        if progress_callback:
                            progress = int((scanned_files / total_files) * 100)
                            progress_callback.emit(min(progress, 100))
                        
                        # 回调文件信息
                        if file_callback:
                            file_callback.emit(file_path)
                        
                        # 扫描文件
                        if self._scan_file(file_path):
                            threats.append(file_path)
                            self.threats_found += 1
                        
                        # 模拟扫描延迟
                        time.sleep(0.001)
        
        return threats
    
    def custom_scan(self, path, progress_callback=None, file_callback=None):
        """自定义扫描"""
        self.scan_count = 0
        self.threats_found = 0
        threats = []
        
        if not os.path.exists(path):
            return threats
        
        total_files = self._count_files([path])
        scanned_files = 0
        
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if not self._is_trusted(file_path):
                    self.scan_count += 1
                    scanned_files += 1
                    
                    # 更新进度
                    if progress_callback:
                        progress = int((scanned_files / total_files) * 100)
                        progress_callback.emit(min(progress, 100))
                    
                    # 回调文件信息
                    if file_callback:
                        file_callback.emit(file_path)
                    
                    # 扫描文件
                    if self._scan_file(file_path):
                        threats.append(file_path)
                        self.threats_found += 1
                    
                    # 模拟扫描延迟
                    time.sleep(0.005)
        
        return threats
    
    def _count_files(self, paths):
        """计算文件数量"""
        count = 0
        for path in paths:
            if os.path.exists(path):
                for _, _, files in os.walk(path):
                    count += len(files)
        return max(count, 1)  # 避免除零错误
