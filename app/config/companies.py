# app/config/companies.py

from typing import Dict, List

# Chosen Test Set: Global IT Companies
COMPANIES: Dict[str, List[str]] = {
    "Microsoft": ["microsoft", "msft", "windows", "azure"],
    "Google": ["google", "alphabet", "googl", "google sheets"],
    "Apple": [
    "apple inc",
    "apple’s",
    "iphone",
    "ipad",
    "mac",
    "ios",
    "siri",
    ],
    "Meta": ["meta", "facebook", "instagram", "whatsapp", "ray-ban"],
    # "Microsoft": [
    #     "Microsoft",
    #     "MSFT",
    #     "Microsoft Corp",
    #     "Microsoft Corporation",
    # ],
    # "Google": [
    #     "Google",
    #     "Alphabet",
    #     "Alphabet Inc",
    #     "Google LLC",
    # ],
    # "Apple": [
    #     "Apple",
    #     "AAPL",
    #     "Apple Inc",
    # ],
    # "Meta": [
    #     "Meta",
    #     "Facebook",
    #     "Meta Platforms",
    #     "Meta Platforms Inc",
    #],
}
