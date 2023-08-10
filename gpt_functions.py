import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

MODEL = "gpt-3.5-turbo"

def link_describe(text):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a laconic assistant. You reply with brief, concise answers."},
            {"role": "user", "content": "I am going to paste the body text of a web page and I want you to give a one-sentence description of what the page is for."},
            {"role": "assistant", "content": "Okay, paste the text from a web page in your response and I will describe the purpose of the web page in one sentence. Start with the words 'This resource' or 'This tool'."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )

    return (response['choices'][0]['message']['content'])


def long_describe(text):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a neutral, laconic writer. You write concise, neutral articles that are not persuasive, in 250 words or less."},
            {"role": "user", "content": "I am going to paste the body text of a web page for a resource or article and I want you to write a short, non-persuasive article describing it in 250 words or less, that outlines the purpose of the resource or article and its main features. Start with the words 'This resource' or 'This tool'."},
            {"role": "assistant", "content": "Okay, please show me the web page for the resource / article I should write about. I will not include copyright information or contact details."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )

    return (response['choices'][0]['message']['content'])

def short_describe(text):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a neutral, laconic writer. You write concise, neutral articles that are not persuasive, in 150 words or less."},
            {"role": "user", "content": "I am going to paste the body text from a web page for a resource or article and I want you to write a short, laconic article describing the resource or article that the web page is for in 150 words or less, that outlines the purpose of the resource or article and its main features."},
            {"role": "assistant", "content": "Okay, please show me the web page for the resource / article I should write about. I will not include copyright information or contact details."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )

    return (response['choices'][0]['message']['content'])
