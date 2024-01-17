import json
import re

import nbformat as nbf
import requests


def convert_notebook(input_text):
    url = "https://fintergpt.quantit.io/convert-notebook"
    data = {"input": input_text}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return json.loads(response.content)["result"]  # API 응답의 텍스트 반환
    else:
        raise Exception(f"API 요청 에러: {response.status_code}")


def create_notebook_from_text(text, title):
    blocks = re.split(r"(```[a-z]*\n[\s\S]*?\n```)", text)
    nb = nbf.v4.new_notebook()

    for block in blocks:
        if block.startswith("```python"):
            code = block.replace("```python\n", "").replace("```", "")
            nb["cells"].append(nbf.v4.new_code_cell(code))
        elif block.startswith("```markdown"):
            markdown = block.replace("```markdown\n", "").replace("```", "")
            nb["cells"].append(nbf.v4.new_markdown_cell(markdown))
        elif block.strip():
            nb["cells"].append(nbf.v4.new_markdown_cell(block))

    with open(title, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Notebook 파일 '{title}'이 성공적으로 생성되었습니다.")
    return nb


def create_notebook(input_text, title):
    try:
        text = convert_notebook(input_text)
        create_notebook_from_text(text, title)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    input_text = "volatility 전략 만들어줘"  # 원하는 입력 텍스트
    create_notebook(input_text, "sample.ipynb")
