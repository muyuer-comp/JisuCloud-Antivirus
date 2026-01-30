import os
import os.path


def get_system_directories():
    """获取系统关键目录"""
    system_dirs = []
    
    # 获取用户目录
    user_profile = os.environ.get('USERPROFILE', '')
    if user_profile:
        # 添加用户目录下的关键文件夹
        user_dirs = [
            os.path.join(user_profile, 'Desktop'),
            os.path.join(user_profile, 'Downloads'),
            os.path.join(user_profile, 'Documents'),
            os.path.join(user_profile, 'Pictures'),
            os.path.join(user_profile, 'Music'),
            os.path.join(user_profile, 'Videos')
        ]
        system_dirs.extend([d for d in user_dirs if os.path.exists(d)])
    
    # 获取系统目录
    system_root = os.environ.get('SYSTEMROOT', 'C:\\Windows')
    if os.path.exists(system_root):
        system_dirs.append(system_root)
    
    # 获取程序文件目录
    program_files = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
    if os.path.exists(program_files):
        system_dirs.append(program_files)
    
    program_files_x86 = os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')
    if os.path.exists(program_files_x86):
        system_dirs.append(program_files_x86)
    
    return system_dirs


def get_file_info(file_path):
    """获取文件信息"""
    try:
        if not os.path.exists(file_path):
            return None
        
        file_info = {
            'name': os.path.basename(file_path),
            'path': file_path,
            'size': os.path.getsize(file_path),
            'mtime': os.path.getmtime(file_path)
        }
        return file_info
    except Exception:
        return None


def is_valid_file(file_path):
    """检查文件是否有效"""
    try:
        return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
    except Exception:
        return False
