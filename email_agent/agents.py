from langchain.messages import HumanMessage,AIMessage,SystemMessage
import os 
from tools import send_email_tool
from llm import llm,State
import sys
email_id = sys.argv[1]
content = sys.argv[2]


def manager_agent(state : State):
    """
    This is agent is manager agent which will decide wheather 
    email reply needs human opinion or not needed
    """
    messages = [
    SystemMessage(content="""
Decide whether this email requires a human reply.

Return true if:
- There is any date, deadline, timeline, or time-bound request
- The sender expects confirmation, response, or action
- It references meetings, follow-ups, or ongoing work
- It involves decisions, approvals, or dependencies

Return false only if:
- The email is purely informational and does not expect a reply

Be smart and interpret meaning, not just exact words.

Output ONLY:
true or false
"""),
    HumanMessage(content=state["user_input"])
]
    result = llm.invoke(messages)
    return {
        "history" : [result],
        "human_needed" : result.content
    }


def human_opinion_analyser_agent(state : State):
    """
    This will craete content for email 
    and it will ensure that it is related to
    human opinion where human opinion is needed.
    """
    messages = [
    SystemMessage(content=SystemMessage(content="""
Write a reply email.

STRICT RULES:
- Only write the email body (NO subject line)
- Do NOT include words like "Subject:" anywhere
- Extract recipient name from email ID:
  Example: shadhanan.project@gmail.com → Shadhanan
- Replace placeholders like [Sender Name] with actual name
- Do NOT include the email ID anywhere in the body
- Keep it natural and human-like
-You should not hallocinate only reply based on human opinion because he is the one who will actually reply.

Format:
Hi <Name>,

<message>

Best regards,
Ritik M
""")),
    HumanMessage(content=f"{state["human_opinion"]} and emailid : {email_id} and email content : {state['content']}")
]
    result = llm.invoke(messages)
    return {
        "history" : [result],
        "content" : result.content
    }


def no_human_opinion_agent(state : State):
    messages = [
    SystemMessage(content="""
Write a reply email.
STRICT RULES:
- Only write the email body (NO subject line)
- Do NOT include words like "Subject:" anywhere
- Extract recipient name from email ID:
  Example: shadhanan.project@gmail.com → Shadhanan
- Replace placeholders like [Sender Name] with actual name
- Do NOT include the email ID anywhere in the body
- Keep it natural and human-like
Format:
Hi <Name>,
<message>
Best regards,
Ritik M
"""),
             HumanMessage(content=state["user_input"])
            ]
    result = llm.invoke(messages)
    return {
        "history" : [result],
        "content" : result.content
    }
def reply_agent_subject(state : State):
    """
    This the the agent which helps 
    in analysing the data given by 
    analyser agent and it writes a 
    subject to the mail based on the analysis
    """
    messages = [
        SystemMessage(content="""
           Analyze the email content provided by the user and generate a concise, relevant reply email subject. The subject must be:
            Directly based on the analysis of the user’s message
            Maximum 8 words
            Clear, structured, and professional
            Do not include “Re:” or any extra text
            Only provide the subject line, nothing else"""),
            HumanMessage(content=f"""
            can you write a reply subject alone for mail and users message is {content}""")
    ]
    result = llm.invoke(messages)
    print(result.content)
    return {
        "history": [result],
        "subject" : result.content
    }
def reply_agent_emaiid(state : State):
    """
    This the the agent which helps 
    extrating email from user input
    """
    messages = [
        SystemMessage(content="""
            Your work is to analyse the data given by user and extract email id from the input
            only give email id as output no explanation and no extra any addings
            There is a possiblitiy of two email so i need only sender email so analyse carefully
             """),
            HumanMessage(content=f"""
            can you extract me email id and user input is : {email_id}""")
    ]
    result = llm.invoke(messages)
    print(result.content)
    return {
        "history": [result],
        "to_email" : result.content.strip()
    }
# def reply_agent_content(state : State):
#     """
#     This the the agent which helps 
#     in analysing the data given by 
#     analyser agent and it writes a 
#     reply letter based on the analysis
#     """
#     messages = [
#         SystemMessage(content=f"""
#             Analyze the email content provided by the user and generate a reply email content that is:
#             Directly based on the user’s message
#             Neat, structured, and reads like a natural human conversation
#             Do not include any subject line or extra text
#             Extract the recipient’s name from {email_id} and address them directly in the reply
#                 Always sign off as Ritik M
#                 Only provide the content, nothing else"""),
#             HumanMessage(content=f"""
#             can you write a reply mail based on analysis : {state['history'][-1].content} and
#             users message is {content}""")
#     ]
#     result = llm.invoke(messages)
#     print(result.content)
#     return {
#         "history": [result],
#         "content" : result.content
#     }

def send_email_agent(state : State):
    """
    This the the agent which helps 
    in sending mails to people with
    subject and content
    """
    print("sending email")
    tool_input = {
    "subject": state["subject"],
    "content": state["content"],
    "to_email": state["to_email"],
}
    send_email_tool.run(
        tool_input=tool_input   
    )
    return state