from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from functools import partial
from langchain import hub

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class GradeDocs(BaseModel):
    binary_score: str = Field(description="Relevance score 'yes' or 'no'")

class BlogGraphBuilder:
    def __init__(self, config, retriever):
        self.config = config
        self.retriever = retriever

    def grade_node(self, state):
        model = self.config.get_llm().with_structured_output(GradeDocs)
        prompt = PromptTemplate(
            template="Grade the relevance of this doc to the question. Yes/No. \nDoc: {context} \nQuestion: {question}",
            input_variables=["context", "question"]
        )
        chain = prompt | model
        last_msg = state["messages"][-1]
        res = chain.invoke({"question": state["messages"][0].content, "context": last_msg.content})
        return "generate" if res.binary_score.lower() == "yes" else "rewrite"

    def agent_node(self, state, tools):
        llm = self.config.get_llm().bind_tools(tools)
        return {"messages": [llm.invoke(state["messages"])]}

    def rewrite_node(self, state):
        llm = self.config.get_llm()
        msg = [HumanMessage(content=f"Rewrite this math/AI query for better retrieval: {state['messages'][0].content}")]
        return {"messages": [llm.invoke(msg)]}

    def generate_node(self, state):
        prompt = hub.pull("rlm/rag-prompt")
        chain = prompt | self.config.get_llm() | StrOutputParser()
        res = chain.invoke({"context": state["messages"][-1].content, "question": state["messages"][0].content})
        return {"messages": [res]}

    def build_graph(self, retriever_tool):
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", partial(self.agent_node, tools=[retriever_tool]))
        workflow.add_node("retrieve", retriever_tool) # ToolNode wrapper simplified
        workflow.add_node("rewrite", self.rewrite_node)
        workflow.add_node("generate", self.generate_node)
        
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", lambda s: "tools" if s["messages"][-1].tool_calls else END, {"tools": "retrieve", END: END})
        workflow.add_conditional_edges("retrieve", self.grade_node)
        workflow.add_edge("generate", END)
        workflow.add_edge("rewrite", "agent")
        return workflow.compile()
