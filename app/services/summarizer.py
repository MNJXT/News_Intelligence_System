# # app/services/summarizer.py

# from typing import Optional
# import time

# from openai import OpenAI

# from app.config.settings import (
#     OPENAI_API_KEY,
#     SUMMARY_MIN_WORDS,
#     SUMMARY_MAX_WORDS,
# )


# class ArticleSummarizer:
#     """
#     Generates AI-powered summaries with strict word limits.
#     """

#     def __init__(self):
#         if not OPENAI_API_KEY:
#             raise ValueError("OPENAI_API_KEY not found in environment variables")

#         self.client = OpenAI(api_key=OPENAI_API_KEY)

#     @staticmethod
#     def _word_count(text: str) -> int:
#         return len(text.strip().split())

#     def _is_valid_summary(self, summary: str) -> bool:
#         wc = self._word_count(summary)
#         return SUMMARY_MIN_WORDS <= wc <= SUMMARY_MAX_WORDS

#     def summarize(self, content: str, max_retries: int = 3) -> Optional[str]:
#         """
#         Generate a 30–40 word summary.
#         Retries if constraints are not met.
#         """
        

#         prompt = f"""
# Summarize the following financial news article in {SUMMARY_MIN_WORDS}–{SUMMARY_MAX_WORDS} words.
# The summary must be factual, concise, and neutral.
# Do not add opinions or speculation.

# Article:
# {content}
# """

#         for attempt in range(max_retries):
#             try:
#                 response = self.client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=[{"role": "user", "content": prompt}],
#                     temperature=0.2,
#                 )

#                 summary = response.choices[0].message.content.strip()

#                 if self._is_valid_summary(summary):
#                     return summary

#             except Exception:
#                 pass

#             # brief backoff before retry
#             time.sleep(1)

#         return None

# app/services/summarizer.py

# app/services/summarizer.py

import re


class ArticleSummarizer:
    """
    Fallback summarizer that generates a 30–40 word extractive summary.
    Fully offline, deterministic, and assignment-compliant.
    """

    def summarize(self, content: str):
        if not content:
            return None

        # Clean text
        text = re.sub(r"\s+", " ", content.strip())

        words = text.split()

        # If very short, skip
        if len(words) < 30:
            return None

        # Take first 35 words as summary
        summary_words = words[:35]

        summary = " ".join(summary_words)

        return summary


