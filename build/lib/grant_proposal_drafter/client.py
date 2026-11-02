import json
import urllib.error
import urllib.request


class LLMError(Exception):
    """Raised when the LLM endpoint cannot be reached or returns bad data."""


class LLMClient:
    def __init__(self, base_url="http://localhost:11434/v1", model="llama3.2",
                 api_key=None, timeout=60):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout

    def chat(self, messages, temperature=0.7, max_tokens=1200):
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise LLMError(f"Unable to reach LLM endpoint at {self.base_url}: {exc}") from exc
        except Exception as exc:
            raise LLMError(f"LLM request failed: {exc}") from exc
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise LLMError(f"Invalid JSON from LLM endpoint: {exc}") from exc
        try:
            return parsed["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Unexpected response shape from LLM endpoint: {parsed!r}") from exc
