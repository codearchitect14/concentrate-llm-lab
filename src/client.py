import asyncio
import json
import logging
import time
from typing import Any, Dict, Optional

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from src.config import settings

logger = logging.getLogger(__name__)


class ConcentrateAPIError(Exception):
    pass


class APIRequestError(ConcentrateAPIError):
    pass


class APIValidationError(ConcentrateAPIError):
    pass


class ConcentrateClient:

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.api_key = api_key or settings.concentrate_api_key
        self.base_url = (base_url or settings.concentrate_api_base_url).rstrip("/")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("API key is required. Set CONCENTRATE_API_KEY environment variable.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        logger.info(f"Initialized Concentrate client with base URL: {self.base_url}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
        reraise=True,
    )
    async def chat_completion(
        self,
        model: str,
        messages: list[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        stream: bool = False,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/responses/"

        model_name = model.split("/")[-1] if "/" in model else model
        
        input_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if content:
                if role == "system":
                    input_parts.append(f"System: {content}")
                elif role == "assistant":
                    input_parts.append(f"Assistant: {content}")
                else:
                    input_parts.append(content)
        
        input_text = "\n".join(input_parts)

        payload: Dict[str, Any] = {
            "model": model_name,
            "input": input_text,
            "temperature": temperature,
        }

        if max_tokens is not None:
            payload["max_output_tokens"] = max_tokens
        if top_p is not None:
            payload["top_p"] = top_p
        if stream:
            payload["stream"] = True

        logger.debug(f"Making request to {url} with model: {model}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()

                elapsed_time = time.time() - start_time
                result = response.json()

                output_text = result.get("output", result.get("text", result.get("content", "")))
                
                usage = result.get("usage", {})
                metrics = {
                    "latency_ms": round(elapsed_time * 1000, 2),
                    "prompt_tokens": usage.get("prompt_tokens", usage.get("input_tokens", 0)),
                    "completion_tokens": usage.get("completion_tokens", usage.get("output_tokens", 0)),
                    "total_tokens": usage.get("total_tokens", usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)),
                }

                formatted_result = {
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": output_text
                        }
                    }],
                    "usage": {
                        "prompt_tokens": metrics["prompt_tokens"],
                        "completion_tokens": metrics["completion_tokens"],
                        "total_tokens": metrics["total_tokens"]
                    },
                    "model": model,
                    "metrics": metrics,
                    "raw_response": result
                }

                logger.info(
                    f"Request completed in {metrics['latency_ms']}ms. "
                    f"Tokens: {metrics['total_tokens']}"
                )

                return formatted_result

        except httpx.HTTPStatusError as e:
            error_detail = f"HTTP {e.response.status_code}"
            try:
                error_body = e.response.json()
                error_detail += f": {error_body.get('error', {}).get('message', 'Unknown error')}"
            except Exception:
                error_detail += f": {e.response.text}"

            logger.error(f"API request failed: {error_detail}")
            raise APIRequestError(error_detail) from e

        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise APIRequestError(f"Request failed: {str(e)}") from e

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise APIRequestError(f"Unexpected error: {str(e)}") from e

    async def test_connection(self) -> bool:
        from src.config import OPENAI_MODELS

        try:
            test_model = OPENAI_MODELS[0] if OPENAI_MODELS else "openai/gpt-4o-mini"
            result = await self.chat_completion(
                model=test_model,
                messages=[{"role": "user", "content": "Say hello"}],
                max_tokens=10,
            )
            return "choices" in result and len(result["choices"]) > 0 and result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
