'''
Business logic layer
It masks tasks to prompt templates
This is what to do layer
It looks up the summarize prompt template and combines it with user's text.
'''

from .llm_clients import generate

PROMPTS={
    "summarize": "Summarize the following text concisely in atleast 3 and atmost 5 bullet points.",
    "rewrite": "Rewrite the following text in clear and easy to understand proffesional tone.",
    "keypoints": "Extract the key points from the following text as numbered list.",
    "explain": "Explain the following concept in simple terms so that anyone can understand it."

}

def process_task(task:str,text:str)->dict:
    if task not in PROMPTS:
        raise ValueError(f"Unknown task:{task}. Available tasks:{list(PROMPTS.keys())}")

    result=generate(PROMPTS[task],text)

    return {
        "task":task,
        "content":result["content"],
        "tokens_used":result["tokens_used"]
    }