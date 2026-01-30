import os
import json

class ThemeManager:
    """主题管理器"""
    
    def __init__(self):
        self.theme_file = os.path.join(os.getcwd(), 'theme_settings.json')
        self.current_theme = 'light'  # 默认亮色主题
        self._load_theme()
        self._init_themes()
    
    def _init_themes(self):
        """初始化主题样式"""
        self.themes = {
            'light': {
                'window': 'background-color: #ffffff; color: #000000;',
                'sidebar': 'background-color: #f0f0f0; color: #000000;',
                'button': 'background-color: #e0e0e0; color: #000000; border: 1px solid #cccccc;',
                'button_hover': 'background-color: #d0d0d0;',
                'list_widget': 'background-color: #ffffff; color: #000000; border: 1px solid #cccccc;',
                'progress_bar': 'background-color: #e0e0e0;',
                'progress_bar_fill': 'background-color: #4CAF50;',
                'group_box': 'background-color: #f9f9f9; color: #000000;',
                'label': 'color: #000000;',
                'status_label': 'color: #666666;'
            },
            'dark': {
                'window': 'background-color: #2d2d2d; color: #ffffff;',
                'sidebar': 'background-color: #202020; color: #ffffff;',
                'button': 'background-color: #3d3d3d; color: #ffffff; border: 1px solid #4d4d4d;',
                'button_hover': 'background-color: #4d4d4d;',
                'list_widget': 'background-color: #2d2d2d; color: #ffffff; border: 1px solid #4d4d4d;',
                'progress_bar': 'background-color: #3d3d3d;',
                'progress_bar_fill': 'background-color: #4CAF50;',
                'group_box': 'background-color: #262626; color: #ffffff;',
                'label': 'color: #ffffff;',
                'status_label': 'color: #aaaaaa;'
            }
        }
    
    def _load_theme(self):
        """加载主题设置"""
        try:
            if os.path.exists(self.theme_file):
                with open(self.theme_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get('theme', 'light')
        except Exception:
            pass
    
    def save_theme(self):
        """保存主题设置"""
        try:
            with open(self.theme_file, 'w', encoding='utf-8') as f:
                json.dump({'theme': self.current_theme}, f)
        except Exception:
            pass
    
    def switch_theme(self):
        """切换主题"""
        if self.current_theme == 'light':
            self.current_theme = 'dark'
        else:
            self.current_theme = 'light'
        self.save_theme()
        return self.current_theme
    
    def get_current_theme(self):
        """获取当前主题"""
        return self.current_theme
    
    def get_theme_styles(self, theme=None):
        """获取主题样式"""
        if theme is None:
            theme = self.current_theme
        return self.themes.get(theme, self.themes['light'])
    
    def get_style(self, widget_type, theme=None):
        """获取指定控件的样式"""
        styles = self.get_theme_styles(theme)
        return styles.get(widget_type, '')
