import json
import logging
import os
import random
import re
from pathlib import Path
from typing import List, Dict, Optional

from google import genai

logger = logging.getLogger(__name__)


class ResponseCache:
    def __init__(self, limit: int = 5):
        self.limit = limit
        self.recent_responses: Dict[int, List[str]] = {}

    def add_response(self, user_id: int, response: str):
        responses = self.recent_responses.setdefault(user_id, [])
        responses.append(response)
        if len(responses) > self.limit:
            del responses[:-self.limit]

    def get_recent(self, user_id: int) -> List[str]:
        return self.recent_responses.get(user_id, [])


class MetaforaBank:
    nature = [
        'pohon', 'air', 'api', 'udara', 'tanah', 'bunga',
        'batu', 'ombak', 'awan', 'angin', 'hujan', 'salju'
    ]

    time = [
        'senja', 'fajar', 'tengah malam', 'musim semi', 'musim gugur',
        'musim panas', 'musim dingin', 'subuh', 'siang', 'malam'
    ]

    emotion = [
        'cinta', 'duka', 'harapan', 'takut', 'rindu', 'bahagia',
        'sedih', 'marah', 'tenang', 'gelisah', 'lega', 'kesal'
    ]

    abstract = [
        'cahaya', 'kegelapan', 'bayangan', 'gema', 'visi', 'mimpi',
        'ingatan', 'harapan', 'kepastian', 'ketidakpastian'
    ]

    @staticmethod
    def get_diverse_metaphors(exclude_recent: Optional[List[str]] = None) -> Dict[str, str]:
        exclude = {item.lower() for item in (exclude_recent or [])}

        def pick(items: List[str]) -> str:
            choices = [item for item in items if item.lower() not in exclude]
            return random.choice(choices or items)

        return {
            'nature': pick(MetaforaBank.nature),
            'time': pick(MetaforaBank.time),
            'emotion': pick(MetaforaBank.emotion),
            'abstract': pick(MetaforaBank.abstract),
        }


class AIEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
        self.response_cache = ResponseCache()
        self.metafora_bank = MetaforaBank()

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("No GEMINI_API_KEY found — will use fallback poems only")

        # Fallback poems when Gemini is unavailable
        self.fallback_poems = self._load_fallback_poems()

    async def generate_response(self,
                                user_message: str,
                                chat_history: List[Dict],
                                user_profile: Dict,
                                style: str = 'default',
                                memory_tags: List[Dict] = None,
                                user_id: Optional[int] = None) -> str:
        """Generate response using Gemini AI with personality context"""
        try:
            recent_responses = self.response_cache.get_recent(user_id) if user_id is not None else []
            prompt = self._build_prompt(
                user_message=user_message,
                chat_history=chat_history,
                user_profile=user_profile,
                style=style,
                memory_tags=memory_tags or [],
                recent_responses=recent_responses,
            )

            if self.client:
                response = await self._call_gemini(prompt)
                if response:
                    if user_id is not None:
                        self.response_cache.add_response(user_id, response)
                    return response

            fallback = self._get_fallback_response(user_message, style, recent_responses)
            if user_id is not None:
                self.response_cache.add_response(user_id, fallback)
            return fallback

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            fallback = self._get_fallback_response(user_message, style)
            if user_id is not None:
                self.response_cache.add_response(user_id, fallback)
            return fallback

    def _build_prompt(self,
                     user_message: str,
                     chat_history: List[Dict],
                     user_profile: Dict,
                     style: str,
                     memory_tags: List[Dict],
                     recent_responses: Optional[List[str]] = None) -> str:
        """Build sophisticated prompt with personality context"""

        user_profile = user_profile or {}
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

        recent_context = ""
        recent_keywords = self._extract_recent_keywords(recent_responses or [])
        if recent_responses:
            previous_snippets = [
                resp.replace("\n", " ")[:120]
                for resp in recent_responses[-2:]
            ]
            if previous_snippets:
                recent_context = "\n\nRESPON TERAKHIR YANG HARUS DIHINDARI:\n- " + "\n- ".join(previous_snippets)

        metaphors = self.metafora_bank.get_diverse_metaphors(recent_keywords)

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
- Gunakan metafora segar dari bank ini: {metaphors['nature']}, {metaphors['time']}, {metaphors['emotion']}, {metaphors['abstract']}
- Jangan template, harus natural dan unik
- Jangan eksplisit (hindari "aku sedih"), lebih implisit
- Kadang gunakan pertanyaan retoris
- Gunakan kata: "barangkali", "seolah", "diam-diam"
- Jika closeness < 50, respon lebih umum dan indah
- Jika closeness >= 50, respon lebih personal dan dalam
{recent_context}

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
- Variasikan antara pertanyaan, pernyataan, dan kesan""",

            'melankoli': """- Gaya: SEDIH YANG INDAH
- Gunakan kata: "lirih", "retak", "sepi", "kenang"
- Tone: lembut, melambat, dan berlapis
- Emosi: duka yang tetap cantik
- Jangan dramatis berlebihan""",

            'hope': """- Gaya: PENUH HARAPAN
- Gunakan kata: "cahaya", "fajar", "mungkin", "tumbuh"
- Tone: hangat, optimistis, dan menenangkan
- Emosi: harapan, kemungkinan, pemulihan
- Jangan terkesan menggurui""",

            'mystery': """- Gaya: MISTERIUS
- Gunakan kata: "tersembunyi", "bayang", "isyarat", "rahasia"
- Tone: menggantung, mengundang tanya
- Emosi: penasaran, diam-diam, samar
- Jangan menjelaskan semuanya""",

            'contemplative': """- Gaya: DALAM PERENUNGAN
- Gunakan kata: "mengapa", "renung", "arti", "jejak"
- Tone: filosofis, tenang, dan terbuka
- Emosi: pencarian, pemahaman, keheningan
- Jangan terlalu padat"""
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
                        "temperature": 0.95,
                        "top_p": 0.98,
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
- Jangan meniru puisi sebelumnya; buat yang segar dan berbeda

Hanya puisi, tanpa penjelasan."""

            if self.client:
                response = await self._call_gemini(prompt)
                if response:
                    return f"✨ {response}\n\n— Galaksi Aksara"

            return self._get_random_fallback_poem()

        except Exception as e:
            logger.error(f"Error generating daily poem: {str(e)}")
            return self._get_random_fallback_poem()

    def _get_fallback_response(self, user_message: str, style: str, recent_responses: Optional[List[str]] = None) -> str:
        """Get fallback response when AI unavailable"""
        poems = self.fallback_poems.get(style, self.fallback_poems['default'])
        if recent_responses:
            recent_keywords = self._extract_recent_keywords(recent_responses)
            filtered = [
                poem for poem in poems
                if not any(keyword in poem.lower() for keyword in recent_keywords)
            ]
            if filtered:
                poems = filtered
        return random.choice(poems)

    def _get_random_fallback_poem(self, recent_responses: Optional[List[str]] = None) -> str:
        """Get random fallback poem for daily posting"""
        all_poems = []
        for poems in self.fallback_poems.values():
            all_poems.extend(poems)
        if recent_responses:
            recent_keywords = self._extract_recent_keywords(recent_responses)
            filtered = [
                poem for poem in all_poems
                if not any(keyword in poem.lower() for keyword in recent_keywords)
            ]
            if filtered:
                all_poems = filtered
        return f"✨ {random.choice(all_poems)}\n\n— Galaksi Aksara"

    def _load_fallback_poems(self) -> Dict[str, List[str]]:
        """Load fallback poems from JSON when available."""
        fallback_file = Path(__file__).with_name("fallback_poems.json")
        if fallback_file.exists():
            try:
                with fallback_file.open("r", encoding="utf-8") as handle:
                    data = json.load(handle)
                    if isinstance(data, dict) and data:
                        return data
                    logger.warning("fallback_poems.json is empty or invalid, using built-in fallback poems")
            except Exception as exc:
                logger.warning(f"Could not load fallback_poems.json: {exc}")

        return {
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
            ],
            'melankoli': [
                """Ada sedih yang tidak ingin pergi,
ia tinggal pelan di sudut-sudut hati.
Bukan untuk menyakiti,
hanya supaya kita belajar menjadi lebih lembut.""",
                """Senja yang jatuh pelan selalu tahu,
bahwa retak pun bisa memantulkan cahaya.
Barangkali begitu juga kita,
pernah patah, tapi tidak pernah benar-benar hilang.""",
            ],
            'hope': [
                """Pagi selalu datang tanpa banyak janji,
tapi cahaya tetap menemukan jalan.
Mungkin hari ini belum sempurna,
tapi ia masih bisa tumbuh menjadi baik.""",
                """Ada harapan yang kecil sekali,
namun cukup untuk menyalakan dada.
Seperti fajar yang tidak tergesa,
ia hanya datang, lalu menghangatkan.""",
            ],
            'mystery': [
                """Ada pintu yang tidak perlu dibuka,
karena rahasianya justru tinggal di sana.
Kita berjalan di tepi tanya,
dan diam menjadi jawaban paling jujur.""",
                """Bayang-bayang sering lebih sabar dari cahaya,
ia menunggu sampai kita siap melihat.
Barangkali hidup memang begitu,
selalu menyembunyikan makna di balik samar.""",
            ],
            'contemplative': [
                """Mengapa hati paling tenang justru sering paling ramai?
Mungkin karena ia sedang belajar mendengar.
Di antara jeda dan napas,
ada arti yang sedang tumbuh diam-diam.""",
                """Setiap langkah meninggalkan jejak,
tapi tidak semua jejak ingin dikenang.
Barangkali kita memang hidup,
untuk memahami apa yang tak selesai dijelaskan.""",
            ],
        }

    @staticmethod
    def _extract_recent_keywords(responses: List[str], limit: int = 8) -> List[str]:
        stopwords = {
            'dan', 'yang', 'di', 'ke', 'dari', 'untuk', 'pada', 'dalam', 'itu',
            'ini', 'aku', 'kamu', 'kami', 'mereka', 'tidak', 'akan', 'atau',
            'seperti', 'seolah', 'barangkali', 'tapi', 'bukan', 'karena'
        }
        words: List[str] = []
        for response in responses[-2:]:
            for word in re.findall(r"[A-Za-z]+", response.lower()):
                if len(word) < 4 or word in stopwords or word in words:
                    continue
                words.append(word)
                if len(words) >= limit:
                    return words
        return words
