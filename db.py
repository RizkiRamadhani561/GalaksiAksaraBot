import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path='galaxi_aksara.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User profile table (personality & relationship)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                closeness INTEGER DEFAULT 0,
                depth INTEGER DEFAULT 0,
                mood TEXT,
                style TEXT DEFAULT 'default',
                first_interaction DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_interaction DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Memory tags table (emotional themes)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                tag TEXT NOT NULL,
                weight INTEGER DEFAULT 1,
                first_mentioned DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_mentioned DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                preferred_style TEXT DEFAULT 'default',
                response_length TEXT DEFAULT 'medium',
                poetry_preference TEXT DEFAULT 'metaphorical'
            )
        ''')

        cursor.execute("PRAGMA table_info(user_preferences)")
        columns = {row[1] for row in cursor.fetchall()}
        if 'response_mode' not in columns:
            cursor.execute("ALTER TABLE user_preferences ADD COLUMN response_mode TEXT DEFAULT NULL")
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ========== USER MANAGEMENT ==========
    
    def init_user(self, user_id: int, username: str):
        """Initialize new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO user_profile (user_id, username)
                VALUES (?, ?)
            ''', (user_id, username))
            
            cursor.execute('''
                INSERT OR IGNORE INTO user_preferences (user_id)
                VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            logger.info(f"User {user_id} initialized")
        
        except Exception as e:
            logger.error(f"Error initializing user: {str(e)}")
        
        finally:
            conn.close()
    
    def user_exists(self, user_id: int) -> bool:
        """Check if user exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM user_profile WHERE user_id = ?', (user_id,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    
    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """Get user personality profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM user_profile WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None

    def get_user_preferences(self, user_id: int) -> Optional[Dict]:
        """Get user preference settings."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM user_preferences WHERE user_id = ?
        ''', (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def set_response_mode(self, user_id: int, response_mode: Optional[str]):
        """Persist the user's explicit response mode."""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO user_preferences (user_id, response_mode)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET response_mode = excluded.response_mode
            ''', (user_id, response_mode))
            conn.commit()
        except Exception as e:
            logger.error(f"Error setting response mode: {str(e)}")
        finally:
            conn.close()
    
    # ========== CHAT MANAGEMENT ==========
    
    def save_message(self, user_id: int, role: str, content: str):
        """Save chat message"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO chat_history (user_id, role, content)
                VALUES (?, ?, ?)
            ''', (user_id, role, content))
            
            # Update last interaction
            cursor.execute('''
                UPDATE user_profile
                SET last_interaction = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
        
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")
        
        finally:
            conn.close()
    
    def get_chat_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get recent chat history for context"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, content, timestamp FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Reverse to get chronological order
        return [dict(row) for row in reversed(rows)]
    
    # ========== PERSONALITY MANAGEMENT ==========
    
    def update_personality(self, user_id: int, closeness: int = None, 
                          depth: int = None, mood: str = None):
        """Update user personality metrics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            params = []
            
            if closeness is not None:
                updates.append("closeness = ?")
                params.append(min(closeness, 100))  # Cap at 100
            
            if depth is not None:
                updates.append("depth = ?")
                params.append(min(depth, 100))
            
            if mood is not None:
                updates.append("mood = ?")
                params.append(mood)
            
            if updates:
                params.append(user_id)
                query = f"UPDATE user_profile SET {', '.join(updates)} WHERE user_id = ?"
                cursor.execute(query, params)
                conn.commit()
        
        except Exception as e:
            logger.error(f"Error updating personality: {str(e)}")
        
        finally:
            conn.close()
    
    # ========== MEMORY TAGS ==========
    
    def add_memory_tag(self, user_id: int, tag: str, weight: int = 1):
        """Add or update emotional memory tag"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if tag exists
            cursor.execute('''
                SELECT id, weight FROM memory_tags
                WHERE user_id = ? AND tag = ?
            ''', (user_id, tag))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update weight and last_mentioned
                new_weight = min(existing['weight'] + weight, 100)
                cursor.execute('''
                    UPDATE memory_tags
                    SET weight = ?, last_mentioned = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (new_weight, existing['id']))
            else:
                # Insert new tag
                cursor.execute('''
                    INSERT INTO memory_tags (user_id, tag, weight)
                    VALUES (?, ?, ?)
                ''', (user_id, tag, weight))
            
            conn.commit()
        
        except Exception as e:
            logger.error(f"Error adding memory tag: {str(e)}")
        
        finally:
            conn.close()
    
    def get_memory_tags(self, user_id: int, limit: int = 5) -> List[Dict]:
        """Get top memory tags for user (for context)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tag, weight FROM memory_tags
            WHERE user_id = ?
            ORDER BY weight DESC, last_mentioned DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_all_memory_tags(self, user_id: int) -> List[str]:
        """Get all tags for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT tag FROM memory_tags
            WHERE user_id = ?
            ORDER BY last_mentioned DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [row['tag'] for row in rows]
    
    # ========== UTILITY ==========
    
    def cleanup_old_messages(self, days: int = 30):
        """Delete messages older than specified days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cursor.execute('''
                DELETE FROM chat_history
                WHERE timestamp < ?
            ''', (cutoff_date,))
            
            conn.commit()
            logger.info(f"Cleaned up messages older than {days} days")
        
        except Exception as e:
            logger.error(f"Error cleaning up messages: {str(e)}")
        
        finally:
            conn.close()
    
    def get_stats(self, user_id: int) -> Dict:
        """Get conversation statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) as total_messages FROM chat_history
            WHERE user_id = ?
        ''', (user_id,))
        
        total = cursor.fetchone()['total_messages']
        
        cursor.execute('''
            SELECT COUNT(*) as user_messages FROM chat_history
            WHERE user_id = ? AND role = 'user'
        ''', (user_id,))
        
        user_msgs = cursor.fetchone()['user_messages']
        
        conn.close()
        
        return {
            'total_messages': total,
            'user_messages': user_msgs,
            'bot_messages': total - user_msgs
        }
