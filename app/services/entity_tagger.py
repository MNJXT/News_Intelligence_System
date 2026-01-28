# # app/services/entity_tagger.py

# import re
# from typing import List, Dict

# from app.config.companies import COMPANIES


# class EntityTagger:
#     """
#     Tags articles with company entities using alias-based matching.
#     """

#     def __init__(self):
#         # Precompile regex patterns for efficiency
#         self.patterns: Dict[str, List[re.Pattern]] = {}

#         for company, aliases in COMPANIES.items():
#             self.patterns[company] = [
#                 re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
#                 for alias in aliases
#             ]

#     def tag(
#         self,
#         title: str,
#         description: str | None,
#         content: str | None,
#     ) -> List[str]:
#         """
#         Return list of matched company names.
#         """
#         text_parts = [
#             title or "",
#             description or "",
#             (content or "")[:2000],  # limit for efficiency
#         ]

#         combined_text = " ".join(text_parts)

#         matched_companies: List[str] = []

#         for company, patterns in self.patterns.items():
#             for pattern in patterns:
#                 if pattern.search(combined_text):
#                     matched_companies.append(company)
#                     break  # stop after first alias match

#         return matched_companies

# app/services/entity_tagger.py

from app.config.companies import COMPANIES


class EntityTagger:
    """
    Simple rule-based entity tagger.
    Matches company aliases in title, description, or content.
    """

    def tag(self, title: str, description: str, content: str):
        text = " ".join([
            title or "",
            description or "",
            content or "",
        ]).lower()

        matched = []

        for company, aliases in COMPANIES.items():
            for alias in aliases:
                if alias.lower() in text:
                    matched.append(company)
                    break

        return matched
