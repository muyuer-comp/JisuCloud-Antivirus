import os

class TrustManager:
    """信任区管理器"""
    
    def __init__(self):
        self.trust_file = os.path.join(os.getcwd(), 'trust_paths.txt')
        self._init_trust()
    
    def _init_trust(self):
        """初始化信任区"""
        if not os.path.exists(self.trust_file):
            with open(self.trust_file, 'w', encoding='utf-8') as f:
                pass
    
    def add_to_trust(self, path):
        """添加到信任区"""
        try:
            if not os.path.exists(path):
                return False
            
            # 检查是否已经在信任区
            if self._is_in_trust(path):
                return False
            
            # 添加到信任区
            with open(self.trust_file, 'a', encoding='utf-8') as f:
                f.write(f"{path}\n")
            
            return True
        except Exception:
            return False
    
    def remove_from_trust(self, path):
        """从信任区移除"""
        try:
            # 读取所有信任路径
            trust_paths = self.get_trust_items()
            
            # 移除指定路径
            if path in trust_paths:
                trust_paths.remove(path)
                
                # 写回文件
                with open(self.trust_file, 'w', encoding='utf-8') as f:
                    for trust_path in trust_paths:
                        f.write(f"{trust_path}\n")
                
                return True
            
            return False
        except Exception:
            return False
    
    def get_trust_items(self):
        """获取信任区项目"""
        try:
            with open(self.trust_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception:
            return []
    
    def _is_in_trust(self, path):
        """检查路径是否在信任区"""
        trust_paths = self.get_trust_items()
        return path in trust_paths
    
    def clear_trust(self):
        """清空信任区"""
        try:
            with open(self.trust_file, 'w', encoding='utf-8') as f:
                pass
            return True
        except Exception:
            return False
