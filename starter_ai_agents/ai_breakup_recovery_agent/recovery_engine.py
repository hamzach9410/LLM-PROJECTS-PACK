import os

class RecoveryEngine:
    def process_emotional_state(self, counselor, strategist, user_input: str):
        """Orchestrate the interaction between empathy and practical wellness."""
        # Step 1: Counselor provides empathetic response
        counseling_session = counselor.run(user_input)
        
        # Step 2: Strategist provides actionable advice based on the session
        wellness_plan = strategist.run(f"User Input: {user_input}\nCounselor Response: {counseling_session.content}")
        
        return counseling_session, wellness_plan
