import pandas as pd
import io

class VisualisationEngine:
    def blueprint_visuals(self, specialist, designer, data_context):
        """Orchestrate the visualization design and narrative pipeline."""
        # Step 1: Design Recommendation
        viz_blueprint = specialist.run(f"Data Context: {data_context}")
        
        # Step 2: Storytelling
        narrative = designer.run(f"Viz Blueprint: {viz_blueprint.content}\n\nContext: {data_context}")
        
        return viz_blueprint, narrative

    @staticmethod
    def load_data_preview(file_content):
        """Helper to load and preview data."""
        try:
            df = pd.read_csv(io.StringIO(file_content))
            return df.head(10).to_string()
        except Exception as e:
            return f"Error reading data: {str(e)}"
