from neo4j import GraphDatabase
from data_models import Entity, Relationship
from typing import List, Dict

class KnowledgeGraphManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_graph(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def add_entity(self, entity: Entity):
        with self.driver.session() as session:
            session.run("""
                MERGE (e:Entity {id: $id})
                SET e.name = $name, e.type = $type, e.description = $desc,
                    e.source_doc = $doc, e.source_chunk = $chunk
            """, id=entity.id, name=entity.name, type=entity.entity_type, 
                desc=entity.description, doc=entity.source_doc, chunk=entity.source_chunk)

    def add_relationship(self, rel: Relationship):
        with self.driver.session() as session:
            session.run("""
                MATCH (a:Entity {name: $source})
                MATCH (b:Entity {name: $target})
                MERGE (a)-[r:RELATES_TO {type: $rel_type}]->(b)
                SET r.description = $desc, r.source_doc = $doc
            """, source=rel.source, target=rel.target, rel_type=rel.relation_type,
                desc=rel.description, doc=rel.source_doc)

    def find_related(self, name: str, hops=2) -> List[Dict]:
        with self.driver.session() as session:
            return [dict(r) for r in session.run(f"""
                MATCH path = (start:Entity)-[*1..{hops}]-(related:Entity)
                WHERE toLower(start.name) CONTAINS toLower($name)
                RETURN related.name as name, related.description as description,
                       related.source_doc as source, related.source_chunk as chunk,
                       [r in relationships(path) | r.description] as path_descriptions
                LIMIT 20
            """, name=name)]

    def semantic_lookup(self, query: str) -> List[Dict]:
        with self.driver.session() as session:
            return [dict(r) for r in session.run("""
                MATCH (e:Entity)
                WHERE e.name CONTAINS $q OR e.description CONTAINS $q
                RETURN e.name as name, e.description as description,
                       e.source_doc as source, e.source_chunk as chunk
                LIMIT 10
            """, q=query)]
