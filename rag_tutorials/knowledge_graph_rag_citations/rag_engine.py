import json
import hashlib
import re
from ollama import Client as OllamaClient
from data_models import Entity, Relationship, Citation, AnswerWithCitations

class GraphRAGEngine:
    def __init__(self, ollama_host, graph_manager):
        self.client = OllamaClient(host=ollama_host)
        self.graph = graph_manager

    def extract_and_index(self, text, doc_name, model="llama3.1"):
        """Extract entities/rels using LLM and sync to Neo4j."""
        prompt = f"Extract entities and relationships from text: {text}. Respond in JSON."
        resp = self.client.chat(model=model, messages=[{"role": "user", "content": prompt}], format="json")
        data = json.loads(resp['message']['content'])
        
        for e in data.get('entities', []):
            eid = hashlib.md5(f"{e['name']}_{doc_name}".encode()).hexdigest()[:8]
            self.graph.add_entity(Entity(eid, e['name'], e['type'], e['description'], doc_name, text[:150]))
            
        for r in data.get('relationships', []):
            self.graph.add_relationship(Relationship(r['source'], r['target'], r['type'], r['description'], doc_name))

    def generate_verifiable_answer(self, query, model="llama3.1"):
        """Run multi-hop traversal and generate cited answer."""
        trace = [f"🔍 Exploring graph for: {query}"]
        initial = self.graph.semantic_lookup(query)
        
        if not initial: return AnswerWithCitations("No data found.", [], trace)
        
        context_parts = []
        source_map = {}
        for i, ent in enumerate(initial[:3]):
            related = self.graph.find_related(ent['name'])
            for j, rel in enumerate(related):
                ref = f"[{len(context_parts)+1}]"
                context_parts.append(f"{ref} {rel['name']}: {rel['description']}")
                source_map[ref] = {"doc": rel['source'], "text": rel['chunk']}
        
        prompt = f"Answer query using context. Cite sources [N].\nContext: {' '.join(context_parts)}\nQuery: {query}"
        resp = self.client.chat(model=model, messages=[{"role": "user", "content": prompt}])
        answer = resp['message']['content']
        
        citations = []
        for ref in set(re.findall(r'\[(\d+)\]', answer)):
            key = f"[{ref}]"
            if key in source_map:
                citations.append(Citation(key, source_map[key]['doc'], source_map[key]['text'], 0.9, []))
                
        return AnswerWithCitations(answer, citations, trace + ["✅ Validated citations."])
