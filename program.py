from openai import OpenAI
import os
import re


openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def ask_gpt(prompt: str) -> str:
  completion = openai_client.chat.completions.create(
    model = 'gpt-4o-mini',
    messages = [{
      'role': 'user',
      'content': prompt,
    }]
  )

  return completion.choices[0].message.content


if __name__ == '__main__':
  with open('article.txt') as file:
    article_html = ask_gpt('Convert the following article into HTML. Single lines should be headers, '
      'first one top level, others second level. Insert images before every second level '
      'header with <img src="image_placeholder.jpg"/> tags and include alt text as prompts '
      'for AI image generation. Output should be plain-text and include only content to be placed in '
      'the page body tag. Don\'t put the code in a code block. Here is the article:\n\n' + file.read())
  
  with open('artykul.html', 'w') as file:
    file.write(article_html)

  template_html = ask_gpt('Generate HTML template to display an article with h1, h2, p, em and img tags. '
    'Include minimalistic CSS styles and leave the body tag completely empty to paste the '
    'article. Output should be plain-text and include only the template code. Don\'t put the '
    'code in a code block.')
  
  with open('szablon.html', 'w') as file:
    file.write(template_html)
  
  with open('full.html', 'w') as file:
    body_pos = re.search('<body>', template_html).span()[1]

    file.write(
      template_html[:body_pos] +
      article_html +
      template_html[body_pos:]
    )
