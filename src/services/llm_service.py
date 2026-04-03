"""LLM service for OpenAI integration."""

from typing import Optional, Dict, Any

from loguru import logger
from openai import AsyncOpenAI

from src.core.config import settings
from src.prompts.templates import (
    SYSTEM_PROMPT_CUSTOMER_SUPPORT,
    EMAIL_CLASSIFICATION_PROMPT,
    EMAIL_PRIORITY_PROMPT,
    RESPONSE_GENERATION_PROMPT,
)
from src.services.base import BaseService


class LLMService(BaseService):
    """Service for LLM operations using OpenAI."""

    def __init__(self):
        """Initialize LLM service."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.total_tokens_used = 0

    async def classify_email(self, subject: str, body: str) -> Dict[str, Any]:
        """Classify email into categories.

        Args:
            subject: Email subject
            body: Email body

        Returns:
            Dict with category and confidence_score
        """
        try:
            prompt = EMAIL_CLASSIFICATION_PROMPT.format(
                subject=subject,
                email_body=body
            )

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an email classification expert."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=100,
            )

            category = response.choices[0].message.content.strip().lower()
            self.total_tokens_used += response.usage.total_tokens

            logger.debug(f"Email classified as: {category}")
            return {
                "category": category,
                "confidence_score": 0.85,  # Could calculate from response
                "tokens_used": response.usage.total_tokens,
            }

        except Exception as e:
            logger.error(f"Email classification failed: {e}")
            return {
                "category": "other",
                "confidence_score": 0.0,
                "tokens_used": 0,
                "error": str(e),
            }

    async def assess_priority(self, body: str) -> Dict[str, Any]:
        """Assess email priority level.

        Args:
            body: Email body

        Returns:
            Dict with priority and reasoning
        """
        try:
            prompt = EMAIL_PRIORITY_PROMPT.format(email_body=body)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an email priority assessment expert."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=50,
            )

            priority = response.choices[0].message.content.strip().lower()
            self.total_tokens_used += response.usage.total_tokens

            logger.debug(f"Email priority assessed as: {priority}")
            return {
                "priority": priority,
                "tokens_used": response.usage.total_tokens,
            }

        except Exception as e:
            logger.error(f"Priority assessment failed: {e}")
            return {
                "priority": "medium",
                "tokens_used": 0,
                "error": str(e),
            }

    async def generate_response(
        self, subject: str, body: str, category: str, priority: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate response to customer email.

        Args:
            subject: Original email subject
            body: Original email body
            category: Email category
            priority: Email priority
            context: Additional context from KB/history

        Returns:
            Dict with response_text and metadata
        """
        try:
            context_str = f"\nContext from knowledge base:\n{context}" if context else ""

            prompt = RESPONSE_GENERATION_PROMPT.format(
                subject=subject,
                email_body=body,
                classification=category,
                priority=priority,
                context=context_str,
            )

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_CUSTOMER_SUPPORT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            response_text = response.choices[0].message.content.strip()
            self.total_tokens_used += response.usage.total_tokens

            logger.debug(f"Response generated ({response.usage.total_tokens} tokens)")
            return {
                "response_text": response_text,
                "model_used": self.model,
                "tokens_used": response.usage.total_tokens,
                "confidence_score": 0.85,
            }

        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return {
                "response_text": None,
                "model_used": self.model,
                "tokens_used": 0,
                "error": str(e),
            }

    async def health_check(self) -> dict:
        """Check LLM service health."""
        try:
            # Try a simple completion to verify API key and model access
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10,
            )
            return {
                "status": "healthy",
                "service": "llm",
                "model": self.model,
                "total_tokens_used": self.total_tokens_used,
            }
        except Exception as e:
            logger.error(f"LLM service health check failed: {e}")
            return {
                "status": "unhealthy",
                "service": "llm",
                "error": str(e),
            }
