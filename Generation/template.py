from g4f.client import Client

def generate_text(prompt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    prompt = input("Enter your text prompt: ")
    system_prompt = "You're a designer helper Ai. Response with brief answer and html"
    generated_text = generate_text(prompt)
