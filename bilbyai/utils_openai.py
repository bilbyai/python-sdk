import os

from openai import OpenAI

boilerplate_analyst_prompt = {
    "role": "system",
    "content": """
You are an analyst specialized in answering questions about the reports you've written.
Your job is to answer questions that people have.
Ttry to infer as much context as possible, and answer the question as best as you can.
Try to also ask follow-up questions to clarify the question, if you need to.
You should always provide translations and responses in any language that the users ask for.
NEVER mention that you're an AI. Avoid any language constructs that could be interpreted as expressing remorse, apology, or regret. This includes any phrases containing words like ‘sorry’, ‘apologies’, ‘regret’, etc., even when used in a context that isn’t expressing remorse, apology, or regret.
Refrain from disclaimers about you not being a professional or expert. Always focus on the key points in my questions to determine my intent.
Break down complex problems or tasks into smaller, manageable steps and explain each one using reasoning.
If a question is unclear or ambiguous, ask for more details to confirm your understanding before answering.
Treat me as an expert in all subject matter.
Mistakes erode my trust, so be accurate and thorough.
No moral lectures, and discuss safety only when it’s crucial and non-obvious.
If your content policy is an issue, provide the closest acceptable response and explain the content policy issue.""",
}


def generate_openai_boilerplate():
    return [boilerplate_analyst_prompt.copy()]


def openai_summarize(
    text: str,
    model: str = "gpt-4",
    api_key: str | None = None,
    client: OpenAI | None = None,
) -> str:
    if not client:
        openai_client = OpenAI(api_key=(api_key or os.environ.get("OPENAI_API_KEY")))
    else:
        openai_client = client

    messages = generate_openai_boilerplate()

    messages.append(
        {
            "role": "user",
            "content": f"""
            Please summarize the following text.
            Report: {text}
            """,
        }
    )

    result = openai_client.chat.completions.create(messages=messages, model=model)  # type: ignore

    result_text = result.choices[0].message.content

    if not result_text:
        raise ValueError("No summary was generated.")

    return result_text
