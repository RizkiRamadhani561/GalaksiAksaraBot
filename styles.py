import logging
from typing import Dict, Optional
from db import Database

logger = logging.getLogger(__name__)

class StyleManager:
    """Manage user style preferences (in-memory cache + DB persistence)"""
    
    def __init__(self, db: Optional[Database] = None):
        # In-memory cache for current session
        self.user_styles: Dict[int, str] = {}
        self.db = db
        
        # Default style
        self.default_style = 'default'
        
        # Valid styles
        self.valid_styles = [
            'romantis',
            'islami',
            'dark',
            'default',
            'melankoli',
            'hope',
            'mystery',
            'contemplative',
        ]
    
    def set_user_style(self, user_id: int, style: str) -> bool:
        """Set user's preferred style"""
        if style not in self.valid_styles:
            logger.warning(f"Invalid style: {style}")
            return False
        
        self.user_styles[user_id] = style
        logger.info(f"User {user_id} style changed to {style}")
        return True
    
    def get_user_style(self, user_id: int) -> str:
        """Get user's current style"""
        return self.user_styles.get(user_id, self.default_style)
    
    def reset_style(self, user_id: int):
        """Reset user style to default"""
        if user_id in self.user_styles:
            del self.user_styles[user_id]
        logger.info(f"User {user_id} style reset to default")
    
    def is_valid_style(self, style: str) -> bool:
        """Check if style is valid"""
        return style in self.valid_styles
    
    def get_all_styles(self) -> list:
        """Get all available styles"""
        return self.valid_styles
    
    def get_style_description(self, style: str) -> str:
        """Get human-readable description of style"""
        descriptions = {
            'romantis': '💕 Lembut, hangat, penuh rindu dan cinta',
            'islami': '🌙 Reflektif, spiritual, penuh makna',
            'dark': '🌑 Sunyi, dalam, kedalaman dan penerimaan',
            'default': '✨ Puitis, reflektif, dan autentik',
            'melankoli': '💔 Sedih yang indah, lembut, dan reflektif',
            'hope': '✨ Penuh harapan, hangat, dan menatap cahaya',
            'mystery': '🌫️ Misterius, penuh tanya, dan mengundang penasaran',
            'contemplative': '🤔 Dalam perenungan, filosofis, dan tenang',
        }
        return descriptions.get(style, 'Gaya tidak diketahui')
