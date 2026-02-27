from typing import Dict, Any
from agents_config import get_news_collector, get_summary_writer, get_trend_analyzer
from agno.run.agent import RunOutput

class AnalysisEngine:
    """Orchestrates the multi-agent startup trend analysis workflow."""
    
    def __init__(self, api_key: str, model_id: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model_id = model_id
        
    async def run_analysis(self, topic: str, progress_callback=None) -> Dict[str, Any]:
        """Runs the 3-stage market analysis pipeline."""
        
        # Stage 1: Collection
        if progress_callback: progress_callback("🔍 Stage 1: Gathering Market Intelligence...")
        collector = get_news_collector(self.api_key, self.model_id)
        news_res: RunOutput = collector.run(f"Collect recent news and market reports on {topic}")
        raw_news = news_res.content
        
        # Stage 2: Synthesis
        if progress_callback: progress_callback("📝 Stage 2: Synthesizing Industry Signals...")
        summarizer = get_summary_writer(self.api_key, self.model_id)
        summary_res: RunOutput = summarizer.run(f"Summarize these market signals:\n{raw_news}")
        summaries = summary_res.content
        
        # Stage 3: Strategic Insight
        if progress_callback: progress_callback("📈 Stage 3: Generating Startup Opportunities...")
        analyzer = get_trend_analyzer(self.api_key, self.model_id)
        trend_res: RunOutput = analyzer.run(f"Analyze trends and propose startups based on these summaries:\n{summaries}")
        
        return {
            "topic": topic,
            "raw_news": raw_news,
            "summaries": summaries,
            "analysis": trend_res.content
        }
