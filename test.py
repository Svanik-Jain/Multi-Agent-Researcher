
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash-lite",  # Or "gemini-4-neon", "gemini-4-carbon", "gemini-3.5-flash-lite"
    input="Design a Postgres schema for multi-tenant webhook delivery with exponential retry.",
)

print(interaction.output_text)