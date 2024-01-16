import requests

def convert_notebook(input_text):
    url = "http://172.30.1.154:8000/convert-notebook"  # FastAPI 서버의 주소 및 엔드포인트
    data = {"input": input_text}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()["result"]
        return result
    else:
        return f"Error: {response.status_code}"

# 예제 사용
if __name__ == "__main__":
    input_text = "volatility 전략 만들어줘"  # 원하는 입력 텍스트
    result = convert_notebook(input_text)
    print("결과:", result)
