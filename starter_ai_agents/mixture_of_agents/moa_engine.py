import asyncio
from together import AsyncTogether
import os

class MOAEngine:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.async_client = AsyncTogether(api_key=api_key)

    async def run_reference_model(self, model: str, user_prompt: str):
        """Invoke a single reference model."""
        response = await self.async_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
            max_tokens=512,
        )
        return model, response.choices[0].message.content

    async def get_reference_responses(self, models, user_prompt: str):
        """Fetch responses from all reference models concurrently."""
        tasks = [self.run_reference_model(model, user_prompt) for model in models]
        return await asyncio.gather(*tasks)

    def aggregate_responses(self, aggregator_agent, reference_responses, user_prompt: str):
        """Use the aggregator agent to synthesize the final response."""
        context = "\n\n".join([f"--- Model: {m} ---\n{r}" for m, r in reference_responses])
        full_prompt = f"User Question: {user_prompt}\n\nCandidate Responses:\n{context}"
        
        return aggregator_agent.run(full_prompt)
