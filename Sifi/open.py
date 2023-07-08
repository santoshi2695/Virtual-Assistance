import os
import openai
prompt = input("text:")
openai.api_key = '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'
response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.3,
                max_tokens=80,
            )
print(response.choices[0].text)