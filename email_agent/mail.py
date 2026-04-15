from langgraph.graph import StateGraph,END,START
from llm import State
from agents import send_email_agent,reply_agent_emaiid,reply_agent_subject,human_opinion_analyser_agent,manager_agent,no_human_opinion_agent


graph_builder = StateGraph(State)
graph_builder.add_node("manager agent" , manager_agent)
graph_builder.add_node("autosend agent",no_human_opinion_agent)
graph_builder.add_node("opinion agent",human_opinion_analyser_agent)
graph_builder.add_node("send email" , send_email_agent)
graph_builder.add_node("subject agent" , reply_agent_subject)
graph_builder.add_node("emailid agent" , reply_agent_emaiid)


def router(state: State):
    print("DEBUG human_needed:", state["human_needed"], type(state["human_needed"]))
    
    if state["human_needed"]:   # ✅ correct boolean check
        s = input("Your Opinion (agree/disagree/unsure): ").strip().lower()
        state["human_opinion"] = s
        return "human"
    else:
        return "auto"
graph_builder.add_edge(START , "manager agent")
graph_builder.add_conditional_edges(
    "manager agent",
    router,
    {
        "human" : "opinion agent",
        "auto" : "autosend agent"
    }
)
graph_builder.add_edge("opinion agent","subject agent")
graph_builder.add_edge("autosend agent","subject agent")
graph_builder.add_edge("subject agent","emailid agent")
graph_builder.add_edge("emailid agent","send email")
graph_builder.add_edge("send email",END)

graph = graph_builder.compile()
state = {"history" : [] , "user_input" : "","content" : "" , "subject" : "" ,"to_email" : "","human_opinion" : False,"human_needed" : ""}
state = graph.invoke(state)
print(state["subject"],state["content"],state["to_email"],state["human_needed"])
   
    