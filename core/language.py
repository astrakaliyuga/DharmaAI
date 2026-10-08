import time
from deep_translator import GoogleTranslator
from core.logger import get_logger

logger = get_logger("core.language")

class LanguageHandler:
    """Telugu ↔ English + Romanized Telugu detection"""
    
    def __init__(self):
        self.telugu_to_english = GoogleTranslator(source='te', target='en')
        self.english_to_telugu = GoogleTranslator(source='en', target='te')
        self.last_request_time = 0
        self.min_interval = 2.0
        logger.info("LanguageHandler initialized")
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
    
    def detect_telugu(self, text: str) -> bool:
        """Telugu Unicode characters unayo ledo check chey"""
        for char in text:
            if '\u0c00' <= char <= '\u0c7f':
                return True
        return False
    
    def is_romanized_telugu(self, text: str) -> bool:
        """English letters tho Telugu (transliteration) unayo ledo check chey"""
        telugu_words = [
            'ela', 'unnav', 'unnava', 'nenu', 'nuvvu', 'nuvu', 'nuv',
            'dharmam', 'dharma', 'telugu', 'telus', 'enti', 'emiti', 'em',
            'chey', 'chestunna', 'chestunnav', 'matladu', 'matladuthunna',
            'kaliyuga', 'peru', 'per', 'sare', 'ledu', 'undi', 'unnadi',
            'bagunna', 'bagunnava', 'enduku', 'ekkada', 'eppudu', 'evaru',
            'emani', 'cheppu', 'cheppava', 'chudu', 'ra', 'ro', 'bro',
            'anna', 'akka', 'thammudu', 'chelli', 'amma', 'nanna',
            'enti', 'emiti', 'ela', 'ala', 'ila', 'kada', 'kadha',
            'avunu', 'kadu', 'ledhu', 'vundhi', 'vundi', 'unnav',
            'vasthunna', 'vasthunnav', 'velthunna', 'velthunnav',
            'thinnava', 'thinnav', 'thagava', 'thagav'
        ]
        words = text.lower().split()
        matches = sum(1 for word in words if word in telugu_words)
        return matches >= 1
    
    def to_english(self, telugu_text: str, max_retries: int = 5) -> str:
        for attempt in range(max_retries):
            self._rate_limit()
            try:
                result = self.telugu_to_english.translate(telugu_text)
                logger.info(f"TE→EN: {telugu_text[:30]}... → {result[:30]}...")
                return result
            except Exception as e:
                error_msg = str(e).lower()
                if "too many requests" in error_msg:
                    wait = 2 ** attempt
                    logger.warning(f"Rate limit, waiting {wait}s")
                    time.sleep(wait)
                else:
                    logger.error(f"Translation error: {e}")
                    return telugu_text
        return telugu_text
    
    def to_telugu(self, english_text: str, max_retries: int = 5) -> str:
        for attempt in range(max_retries):
            self._rate_limit()
            try:
                result = self.english_to_telugu.translate(english_text)
                logger.info(f"EN→TE: {english_text[:30]}... → {result[:30]}...")
                return result
            except Exception as e:
                error_msg = str(e).lower()
                if "too many requests" in error_msg:
                    wait = 2 ** attempt
                    logger.warning(f"Rate limit, waiting {wait}s")
                    time.sleep(wait)
                else:
                    logger.error(f"Translation error: {e}")
                    return english_text
        return english_text
