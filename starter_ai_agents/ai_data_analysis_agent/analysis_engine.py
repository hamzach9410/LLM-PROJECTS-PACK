import pandas as pd
import io

class AnalysisEngine:
    def analyze_dataset(self, analyst, integrator, data_source):
        """Orchestrate the analysis and research pipeline."""
        # Step 1: Internal Analysis
        analysis_report = analyst.run(f"Please analyze this data context: {data_source}")
        
        # Step 2: Contextual Research
        final_report = integrator.run(f"Data Findings: {analysis_report.content}\n\nProvide external context for these findings.")
        
        return analysis_report, final_report

    @staticmethod
    def load_csv(file_content):
        """Helper to load and preview CSV data."""
        try:
            df = pd.read_csv(io.StringIO(file_content))
            return df.head(10).to_string()
        except Exception as e:
            return f"Error reading CSV: {str(e)}"
