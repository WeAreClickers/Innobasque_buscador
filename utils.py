from openai import OpenAI

def call_openai(client, user_prompt: str, system_prompt: str, max_tokens: int) -> str:
    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            max_tokens=max_tokens
        )
    final_response = response.choices[0].message.content.strip()
    return final_response
