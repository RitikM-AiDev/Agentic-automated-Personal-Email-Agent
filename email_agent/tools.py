from langchain.tools import BaseTool,tool
from pydantic import BaseModel,Field
import os
import sys
import subprocess
from typing import Type

class send_reply_tool_Schema(BaseModel):
    subject: str = Field(..., description="Subject of the reply email without Re:")
    content: str = Field(..., description="Content of the reply email")
    to_email: str = Field(..., description="reply email address")
@tool
def send_email_tool(subject : str, content : str, to_email : str):
        """
        Sends an email to the specified address with the given subject and content.
        """
        run = subprocess.run([sys.executable,"send_email.py",subject,content,to_email],text=True,capture_output=True)
        if run.returncode == 0:
            status = "Success"
        else:
            status = "Failed"
        print(run.stdout)

        return {
        "status": status,
        "stdout": run.stdout,
        "stderr": run.stderr
    }
        