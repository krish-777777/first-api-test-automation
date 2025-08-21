from typing import Optional, Any, Dict, List
from framework import config
from framework.logger import get_test_logger

logger = get_test_logger()

class GeminiClient:
    """
    Wrapper that tries the new 'google.genai' client first.
    Falls back to 'google.generativeai' if available.
    If no API key or imports fail, returns None from generate().
    """
    def __init__(self, model: str = None, api_key: Optional[str] = None):
        self.model = model or config.GEMINI_MODEL
        self.api_key = api_key or config.GOOGLE_API_KEY
        self._client = None
        self._mode = None  # "genai" or "generativeai" or None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not set; Gemini will be disabled (fallback will be used).")
            return
        # Try google.genai
        try:
            import google.genai as genai
            self._client = genai.Client(api_key=self.api_key)
            self._mode = "genai"
            logger.info("Using google.genai client.")
            return
        except Exception as e:
            logger.warning(f"google.genai unavailable: {e}")
        # Try google.generativeai
        try:
            import google.generativeai as genai_old
            genai_old.configure(api_key=self.api_key)
            self._client = genai_old
            self._mode = "generativeai"
            logger.info("Using google.generativeai client.")
            return
        except Exception as e:
            logger.warning(f"google.generativeai unavailable: {e}")
            self._client = None
            self._mode = None

    def generate_json(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        if not self._client or not self.api_key:
            return None
        try:
            if self._mode == "genai":
                # New client
                resp = self._client.models.generate_content(
                    model=self.model,
                    contents=[{"role": "system", "parts": [{"text": system_prompt}]},
                              {"role": "user", "parts": [{"text": user_prompt}]}],
                    config={"response_mime_type": "application/json"}
                )
                txt = resp.text
            else:
                # Old client
                model = self._client.GenerativeModel(self.model)
                resp = model.generate_content([system_prompt, user_prompt], generation_config={"response_mime_type": "application/json"})
                txt = resp.text
            import json
            return json.loads(txt)
        except Exception as e:
            logger.error(f"Gemini call failed: {e}")
            return None
