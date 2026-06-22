import logging
from typing import List, Dict, Optional
from db import Database

logger = logging.getLogger(__name__)

class PersonalityEngine:
    def __init__(self, db: Database):
        self.db = db
        
        # Emotional keywords untuk deteksi mood dan tag
        self.emotion_keywords = {
            'lelah': ['lelah', 'capek', 'kecapekan', 'mengantuk', 'tidak kuat'],
            'sedih': ['sedih', 'duka', 'menangis', 'hati sakit', 'patah hati', 'dukha'],
            'rindu': ['rindu', 'merindukan', 'kangen', 'absen', 'hilang'],
            'bahagia': ['bahagia', 'senang', 'gembira', 'suka', 'asyik', 'menyenangkan'],
            'takut': ['takut', 'khawatir', 'cemas', 'gelisah', 'panik'],
            'marah': ['marah', 'kesal', 'benci', 'jengkel', 'muak'],
            'cinta': ['cinta', 'sayang', 'kasih', 'mencintai', 'tulus'],
            'kehilangan': ['hilang', 'pergi', 'meninggal', 'kepergian', 'ditinggal'],
            'kebingungan': ['bingung', 'tidak tahu', 'ragu', 'galau', 'bimbang'],
            'harapan': ['harap', 'impian', 'mimpi', 'ingin', 'berharap', 'cita-cita'],
            'kesunyian': ['sunyi', 'sepi', 'sendirian', 'kesepian', 'seorang diri'],
            'dalam': ['dalam', 'mendalam', 'kompleks', 'rumit', 'berlapis'],
            'spiritual': ['doa', 'iman', 'tuhan', 'ruhani', 'jiwa', 'atman'],
            'alam': ['alam', 'senja', 'bulan', 'bintang', 'langit', 'semesta', 'galaksi'],
        }
        
        # Depth increase keywords (percakapan yang semakin dalam)
        self.depth_keywords = [
            'mengapa', 'bagaimana', 'apa arti', 'filosofi', 'makna',
            'diri', 'jiwa', 'hati', 'perasaan', 'pikiran', 'batin'
        ]
    
    def analyze_and_update(self, user_id: int, message: str):
        """Analyze user message and update personality"""
        profile = self.db.get_user_profile(user_id)
        
        if not profile:
            return
        
        # Get current values
        closeness = profile['closeness']
        depth = profile['depth']
        
        # Analyze message
        message_lower = message.lower()
        
        # 1. Detect emotions and add memory tags
        detected_emotions = self._detect_emotions(message_lower)
        for emotion in detected_emotions:
            self.db.add_memory_tag(user_id, emotion, weight=2)
        
        # 2. Update mood based on primary emotion
        if detected_emotions:
            primary_mood = detected_emotions[0]
        else:
            primary_mood = profile['mood']
        
        # 3. Increase closeness (every message increases it slightly)
        # More increase if message is longer or deeper
        closeness_increase = self._calculate_closeness_increase(message)
        new_closeness = min(closeness + closeness_increase, 100)
        
        # 4. Increase depth if message contains deep topics
        depth_increase = self._calculate_depth_increase(message_lower)
        new_depth = min(depth + depth_increase, 100)
        
        # 5. Update database
        self.db.update_personality(
            user_id,
            closeness=new_closeness,
            depth=new_depth,
            mood=primary_mood
        )
        
        logger.info(f"User {user_id}: closeness={new_closeness}, depth={new_depth}, mood={primary_mood}")
    
    def _detect_emotions(self, message: str) -> List[str]:
        """Detect emotions from message"""
        detected = []
        
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    detected.append(emotion)
                    break  # Don't add same emotion twice
        
        return detected
    
    def _calculate_closeness_increase(self, message: str) -> int:
        """Calculate closeness increase based on message length and content"""
        # Base increase
        increase = 2
        
        # Extra increase for longer messages (sign of engagement)
        if len(message) > 50:
            increase += 1
        if len(message) > 100:
            increase += 1
        
        # Extra for emotional content
        emotions = self._detect_emotions(message.lower())
        if emotions:
            increase += 2
        
        # Extra for questions (sign of engagement)
        if '?' in message:
            increase += 1
        
        return increase
    
    def _calculate_depth_increase(self, message: str) -> int:
        """Calculate depth increase based on complexity"""
        increase = 0
        
        # Check for depth keywords
        for keyword in self.depth_keywords:
            if keyword in message:
                increase += 1
        
        # Extra for multiple sentences (sign of elaboration)
        sentences = message.split('.')
        if len(sentences) > 2:
            increase += 1
        
        return increase
    
    def get_relationship_description(self, closeness: int) -> str:
        """Get human-readable relationship description"""
        if closeness < 15:
            return "Kami baru saja berkenalan 🌱"
        elif closeness < 35:
            return "Kepercayaan mulai tumbuh 🌿"
        elif closeness < 55:
            return "Kami sudah cukup dekat 🌸"
        elif closeness < 80:
            return "Hubungan kita sudah dalam 🌺"
        else:
            return "Aku mengenalmu dengan sangat baik 🌙"
    
    def get_response_tone(self, profile: Dict) -> str:
        """Determine response tone based on relationship"""
        closeness = profile.get('closeness', 0)
        
        if closeness < 30:
            return "formal_poetic"  # More formal, less personal
        elif closeness < 60:
            return "warm_poetic"    # Warm but still reserved
        else:
            return "intimate_poetic"  # Very personal, intimate
    
    def should_use_memory_reference(self, profile: Dict) -> bool:
        """Decide if we should reference previous conversations"""
        closeness = profile.get('closeness', 0)
        return closeness > 40  # Only after some closeness established
    
    def get_personality_prompt_addition(self, profile: Dict, 
                                       memory_tags: List[Dict]) -> str:
        """Build personality context for AI prompt"""
        closeness = profile.get('closeness', 0)
        depth = profile.get('depth', 0)
        mood = profile.get('mood', 'netral')
        
        # Convert to adjectives
        if closeness > 70:
            closeness_desc = "sangat dekat"
        elif closeness > 40:
            closeness_desc = "cukup akrab"
        else:
            closeness_desc = "baru berkenalan"
        
        # Build tag context
        tags_context = ""
        if memory_tags:
            tags_list = ", ".join([f"'{t['tag']}'" for t in memory_tags[:3]])
            tags_context = f"\n- Tema emosional yang sering mereka bicarakan: {tags_list}"
        
        prompt_addition = f"""
🧬 KONTEKS HUBUNGAN KAMI:
- Tingkat kedekatan: {closeness_desc} (nilai: {closeness}/100)
- Kedalaman percakapan: {depth}/100
- Mood terakhir mereka: {mood}{tags_context}
"""
        
        return prompt_addition
