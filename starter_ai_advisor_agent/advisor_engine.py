import json
from datetime import datetime
from typing import Dict, Any, Optional
from agents_config import get_insurance_advisor_agent
from utils import setup_logger, extract_json, safe_number

logger = setup_logger(__name__)

class AdvisorEngine:
    """Orchestrates the advisory workflow: Math verification -> Market research."""
    
    def __init__(self, openai_key: str, firecrawl_key: str, e2b_key: str, model_id: str = "gpt-4o"):
        self.agent = get_insurance_advisor_agent(openai_key, firecrawl_key, e2b_key, model_id)
        
    def generate_assessment(self, profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Runs the full advisory pipeline."""
        try:
            logger.info("Initializing advisory assessment pipeline...")
            prompt = (
                "You will receive a JSON object describing the client's profile. Follow your workflow instructions to calculate coverage and surface suitable products.\n"
                f"Client profile JSON: {json.dumps(profile)}"
            )
            
            response = self.agent.run(prompt, stream=False)
            
            if response and response.content:
                parsed = extract_json(response.content)
                if parsed:
                    logger.info("Assessment generated successfully.")
                    return parsed
                else:
                    logger.warning("Agent output was not valid JSON.")
                    return {"raw_output": response.content, "error": "Invalid format"}
            else:
                raise ValueError("Agent returned empty response.")
                
        except Exception as e:
            logger.error(f"Advisory engine error: {e}")
            raise

def compute_local_math(profile: Dict[str, Any], real_rate: float) -> Dict[str, float]:
    """Replicate coverage math locally for UI verification."""
    income = safe_number(profile.get("annual_income"))
    years = max(0, int(profile.get("income_replacement_years", 0) or 0))
    total_debt = safe_number(profile.get("total_debt"))
    savings = safe_number(profile.get("available_savings"))
    existing_cover = safe_number(profile.get("existing_life_insurance"))

    if real_rate <= 0:
        discounted_income = income * years
        annuity_factor = float(years)
    else:
        annuity_factor = (1 - (1 + real_rate) ** (-years)) / real_rate if years else 0.0
        discounted_income = income * annuity_factor

    assets_offset = savings + existing_cover
    recommended = max(0.0, discounted_income + total_debt - assets_offset)

    return {
        "income": income,
        "years": int(years),
        "real_rate": real_rate,
        "annuity_factor": annuity_factor,
        "discounted_income": discounted_income,
        "debt": total_debt,
        "assets_offset": -assets_offset,
        "recommended": recommended,
    }
