"""
Lab 1c: AI Workbench CLI v1
A menu driven CLI application with 4 AI tasks
Demonstrates: separation of prompts from logic, function resuse, user interaction loop.

Architecture
User input-->Task Selection-->Prompt Template-->LLM API-->Fromatted Response

This architecture becomes a REST API in Week 2

"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError

# to make sure the encoding UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()  # load the environment variables

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL= os.getenv("OPENAI_MODEL","gpt-4.1-mini")

#--PROMPT TEMPLATES--

TASKS= {
    "1":{
        "name":"Summarize",
        "prompt":"You are a concise summarizer. Summarize the user's text in 3-5 clear bullet points. Focus on most important information."
    },
    "2":{
            "name":"Rewrite",
            "prompt":"You are a professional editor. Rewrite the user's text in clear, professional tone. Keep the original intent in the text all the while improving clarity, readability and messaging."
        },
    "3":{
            "name":"Key points",
            "prompt":"Act as an analyst and from the user's text extract clear key points in a numbered list with each point of max one sentence."
        },
    "4":{
                "name":"Explain",
                "prompt":"Act as a patient teacher and explain user's text in simple to understand terms so that a non-expert can understand the topic. You can use analogies where needed"
            }    
}


def call_llm(system_prompt:str,user_text:str) -> dict:
    """
    Call the LLM with a system prompt and a user text,
    It would return a dictionary 'content','tokens consumed and 'model used' as keys
    """

    try:
        response=client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_text}
            ],
            temperature=0.3,
            max_tokens=500
        )

        return {
            "content":response.choices[0].message.content,
            "tokens":response.usage.total_tokens,
            "model":response.model}

    except AuthenticationError:
        return {
                    "content":"Error: Invalid API Key. Check your .env file",
                    "tokens":0,
                    "model":"N/A"
                }

    except RateLimitError:
            return {
                        "content":"Error: Rate Limit Error. Wait a moment and try again.",
                        "tokens":0,
                        "model":"N/A"
                    }
    except APIConnectionError:
            return {
                        "content":"Error: Cannot Connect to OpenAI. Check your internet connection.",
                        "tokens":0,
                        "model":"N/A"
                        }

def display_menu():
    print("\n|----------------------------|")
    print("|     AI WORKBENCH CLI V1     |")
    print("|-----------------------------|")

    for key in TASKS:  
         print(f"|{key}. {TASKS[key]['name']:<32}|")  #TASKS["1"]['name']=Summarize

    print("|-----------------------------|")
    print("|          q. Quit            |")
    print("|-----------------------------|")


def get_user_text() ->str:
    print("\n Paste your text below")
    print("(Press Enter on an empty line to submit)")
    print(" "+"-"*36)
    lines=[]

    while True:
        try:
            line=input(" | ")
        except EOFError:
             break
        if line=="":
            if lines:
                break
        else:
            lines.append(line)

    return "\n".join(lines) 
             
        
def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("|-----------------------------||")
        print("| ERROR: OPENAI_API_KEY not set|")
        print("|      ADD YOUR API KEY        |")
        print("|        RUN AGAIN             |")
        print("|------------------------------|")
        sys.exit(1)

    print("\n Welcome to AI Workbench!")
    print(f" Model:{MODEL}")
    print(f" Tasks available:{len(TASKS)}")

    session_tokens=0

    while True:
        display_menu()
        choice=input("\n Select a task (1-4 or q)): ").strip()

        if choice.lower()=="q":
            print(f"\n Session total: {session_tokens} token used")
            print(" Goodbye!\n")
            break
        if choice not in TASKS:
            print(" Invalid choice. Enter 1-4 or q.")
            continue

        task=TASKS[choice]
        print(f"\n --> Task: {task['name']}")
        user_text=get_user_text()

        print(f"\n Processing({task['name']})....")
        result=call_llm(task['prompt'],user_text)

        print(f"\n {'-'*38}")
        print(f" Result({task['name']}):")
        print(f" {'-'*38}")
        print()

        for line in result['content'].split("\n"):
            print(f" {line}")
        print()
        print(f" {'-'*38}")
        print(f" Tokens: {result['tokens']} | Model: {result['model']}")
        print(f" {'-'*38}")

        session_tokens+=result['tokens']

if __name__=="__main__":
    main()
             

