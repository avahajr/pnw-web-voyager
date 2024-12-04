"""
An early-stage, text-based web navigator built with GPT4. 

This is what I tried before implementing WebVoyager, which is structured
more thoughtfully and worked much better.
"""

from dotenv import load_dotenv
import os

from openai import OpenAI
from bs4 import BeautifulSoup

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
system_msg = """You are trying to help the user decide where to click on a webpage.
                The user is looking to opt-out of data collection for the website they are currently on."""


def load_html_as_string_without_head(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_string = file.read()

    soup = BeautifulSoup(html_string, "html.parser")
    if soup.head:
        soup.head.decompose()  # Remove the <head> section
    return str(soup)


# Usage
html_content = load_html_as_string_without_head("linkedin.html")
print(html_content)
print("loading html...")
assistant_msg = load_html_as_string_without_head("linkedin.html")
print("done.")

user_message = "I want to opt-out of data collection. Where should I click on this webpage? Based on the provided webpage only and NO prior information, retrieve click targets that might lead to opt-out of data collection. Return HTML chunks where I should click."

print("asking chatgpt...")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": assistant_msg},
    ],
)

print("done.")
print(response.choices[0].message)
