from agno.media import Image as AgnoImage
from agno.run.agent import RunOutput
from agents_config import get_medical_agent, DIAGNOSTIC_PROMPT
from utils import setup_logger

logger = setup_logger(__name__)

class ImagingEngine:
    """Orchestrates medical image analysis using Gemini vision models."""
    
    def __init__(self, api_key: str, model_id: str = "gemini-2.0-flash-exp"):
        self.agent = get_medical_agent(api_key, model_id)
        
    def analyze_image(self, image_path: str) -> str:
        """Runs the diagnostic analysis for a given image path."""
        try:
            logger.info(f"Starting analysis for image: {image_path}")
            agno_image = AgnoImage(filepath=image_path)
            
            response: RunOutput = self.agent.run(
                DIAGNOSTIC_PROMPT,
                images=[agno_image]
            )
            
            if response and response.content:
                logger.info("Analysis completed successfully.")
                return response.content
            else:
                raise ValueError("AI agent returned empty content.")
                
        except Exception as e:
            logger.error(f"Analysis orchestration error: {e}")
            raise
