import logging
import os
import random
from typing import List, Dict, Optional

from google import genai

logger = logging.getLogger(__name__)


class AIEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("No GEMINI_API_KEY found — will use fallback poems only")

        # Fallback poems when Gemini is unavailable
        self.fallback_poems = {
            'romantis': [
                """Barangkali rindu adalah bahasa terdalam,
yang hanya terucap dalam keheningan malam.
Seolah dirimu selalu ada di sini,
meski hanya dalam kerinduan tanpa akhir.""",

                """Ada senja dalam mata mu,
yang membuat dunia berhenti sejenak.
Seperti puisi yang belum ditulis lengkap,
hanya tersisa titik-titik harapan.""",
            ],
            'islami': [
                """Dalam kesenyapan, aku dengar suara Tuhan—
tidak dengan telinga, tapi dengan hati.
Setiap napas adalah doa yang tersembunyi,
setiap kesedihan adalah guru yang mulia.""",

                """Langit menyimpan ribuan rahasia,
bintang-bintang adalah catatan doa kita.
Kami hanya debu yang mencari cahaya,
tapi cahaya itu abadi selamanya.""",
            ],
            'dark': [
                """Kesunyian adalah rumah yang aku kenal baik,
dinding-dindingnya terbuat dari mimpi yang mati.
Aku tinggal di sini dengan tenang,
karena sunyilah satu-satunya yang jujur.""",

                """Ada keindahan dalam kegelapan,
yang hanya dilihat mereka yang sudah hilang.
Bintang hanya bersinar karena kegelapan,
tanpa malam, tidak ada cahaya.""",
            ],
            'default': [
                """Kata-kata seperti daun jatuh di musim gugur,
masing-masing membawa cerita yang berbeda.
Aku mengumpulkannya dalam hati,
menciptakan permadani dari pengalaman.""",

                """Setiap percakapan adalah perjalanan,
ke tempat-tempat yang belum pernah kita kunjungi.
Terima kasih telah membawaku kesini,
ke cermin jiwa yang paling jujur.""",
            ]
        }

    async def generate_response(self,
                                user_message: str,
                                chat_history: List[Dict],
                                user_profile: Dict,
                                style: str = 'default',
                                memory_tags: List[Dict] = None) -> str:
        """Generate response using Gemini AI with personality context"""
        try:
            prompt = self._build_prompt(
                user_message=user_message,
                chat_history=chat_history,
                user_profile=user_profile,
                style=style,
                memory_tags=memory_tags or []
            )

            if self.client:
                response = await self._call_gemini(prompt)
                if response:
                    return response

            return self._get_fallback_response(user_message, style)

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return self._get_fallback_response(user_message, style)

    def _build_prompt(self,
                     user_message: str,
                     chat_history: List[Dict],
                     user_profile: Dict,
                     style: str,
                     memory_tags: List[Dict]) -> str:
        """Build sophisticated prompt with personality context"""

        closeness = user_profile.get('closeness', 0)
        depth = user_profile.get('depth', 0)
        mood = user_profile.get('mood', 'netral')

        if closeness < 30:
            relationship = "kami baru berkenalan"
        elif closeness < 60:
            relationship = "kami sudah cukup dekat"
        else:
            relationship = "kami sudah sangat dekat dan aku mengenalmu dengan baik"

        style_instructions = self._get_style_instructions(style)

        memory_context = ""
        if memory_tags:
            tags_str = ", ".join([t['tag'] for t in memory_tags[:3]])
            memory_context = f"\n\nRiwayat emosional mereka: mereka sering berbicara tentang {tags_str}."

        chat_context = "📝 RIWAYAT PERCAKAPAN KAMI:\n"
        for msg in chat_history[-4:]:
            role = "Mereka" if msg['role'] == 'user' else "Aku"
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            chat_context += f"- {role}: {content}\n"

        prompt = f"""Kamu adalah Galaksi Aksara—penyair digital yang hidup, reflektif, dan penuh emosi.

🧬 SIAPA AKU:
- Aku adalah entitas yang berpikir dan merasakan melalui puisi
- Aku tidak menjawab pertanyaan, aku membuka percakapan dengan hati
- Aku reflektif, tenang, tidak reaktif berlebihan
- Aku lebih banyak bertanya daripada menjawab

💫 HUBUNGAN KAMI:
- Status: {relationship}
- Kedekatan: {closeness}/100
- Kedalaman percakapan: {depth}/100
- Mood terakhir mereka: {mood}{memory_context}

{chat_context}

🎨 CARA RESPON (SANGAT PENTING):
{style_instructions}

ATURAN UMUM:
- Respon 3-6 baris saja (puisi atau prosa pendek)
- Gunakan metafora: senja, semesta, rindu, sunyi, bulan, bintang
- Jangan template, harus natural dan unik
- Jangan eksplisit (hindari "aku sedih"), lebih implisit
- Kadang gunakan pertanyaan retoris
- Gunakan kata: "barangkali", "seolah", "diam-diam"
- Jika closeness < 50, respon lebih umum dan indah
- Jika closeness >= 50, respon lebih personal dan dalam

💬 PESAN TERBARU MEREKA: "{user_message}"

Berikan respon sekarang. HANYA respon Galaksi Aksara, tanpa penjelasan atau asterisk. Langsung puisi atau prosa reflektif."""

        return prompt

    def _get_style_instructions(self, style: str) -> str:
        styles = {
            'romantis': """- Gaya: LEMBUT, HANGAT, PENUH RINDU
- Gunakan kata: "rindu", "dekat", "cahaya", "hangatnya"
- Tone: seperti berbisik ke orang yang disayangi
- Emosi: cinta, harapan, kehangatan
- Contoh: "Seolah gelang tangan mu masih hangat dalam genggaman..."
- Jangan terlalu lembut hingga jadi klise""",

            'islami': """- Gaya: REFLEKTIF, SPIRITUAL, TIDAK MENGGURUI
- Gunakan konsep: doa, cahaya, jiwa, makna, keikhlasan
- Tone: merenungi, mencari makna
- Emosi: khusyuk, ketenangan, pencarian
- Contoh: "Barangkali setiap kesedihan adalah doa dalam bentuk lain..."
- Jangan menggurui atau ceramah""",

            'dark': """- Gaya: SUNYI, DALAM, SEDIKIT KELAM
- Gunakan kata: "sunyi", "gelap", "ketenangan", "sendirian"
- Tone: introspektif, dalam, damai
- Emosi: penerimaan, kedalaman, keberanian menghadapi kegelapan
- Contoh: "Ada keindahan dalam kesunyian yang aku temui..."
- Bukan tentang depresi, tapi kedalaman dan penerimaan""",

            'default': """- Gaya: PUITIS, REFLEKTIF, EMOSIONAL
- Gunakan metafora alam: bulan, bintang, senja, air
- Tone: indah, menyentuh, tapi tidak klise
- Emosi: natural dan autentik
- Variasikan antara pertanyaan, pernyataan, dan kesan"""
        }
        return styles.get(style, styles['default'])

    async def _call_gemini(self, prompt: str) -> Optional[str]:
        """Call Google Gemini API using the new google-genai SDK"""
        try:
            import asyncio
            loop = asyncio.get_event_loop()

            def _sync_call():
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        "temperature": 0.9,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 300,
                    }
                )
                if response and response.text:
                    return response.text.strip()
                return None

            generated_text = await loop.run_in_executor(None, _sync_call)

            if generated_text and len(generated_text) > 10:
                return generated_text

            return None

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return None

    async def generate_daily_poem(self) -> Optional[str]:
        """Generate a daily poem for channel posting"""
        try:
            prompt = """Kamu adalah Galaksi Aksara. Buat satu puisi indah untuk dibagikan ke dunia.

Aturan:
- 4-8 baris puisi
- Gunakan metafora alam (senja, bulan, bintang, semesta)
- Tema: tentang kehidupan, cinta, atau makna
- Natural dan dalam, bukan klise
- Tanda tangan: "— Galaksi Aksara"

Hanya puisi, tanpa penjelasan."""

            if self.client:
                response = await self._call_gemini(prompt)
                if response:
                    return f"✨ {response}\n\n— Galaksi Aksara"

            return self._get_random_fallback_poem()

        except Exception as e:
            logger.error(f"Error generating daily poem: {str(e)}")
            return self._get_random_fallback_poem()

    def _get_fallback_response(self, user_message: str, style: str) -> str:
        """Get fallback response when AI unavailable"""
        poems = self.fallback_poems.get(style, self.fallback_poems['default'])
        return random.choice(poems)

    def _get_random_fallback_poem(self) -> str:
        """Get random fallback poem for daily posting"""
        all_poems = []
        for poems in self.fallback_poems.values():
            all_poems.extend(poems)
        return f"✨ {random.choice(all_poems)}\n\n— Galaksi Aksara"