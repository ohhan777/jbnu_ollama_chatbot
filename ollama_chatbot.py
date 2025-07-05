import requests
import json

def chat_with_ollama():
    print("Ollama 챗봇에 오신 것을 환영합니다! (종료하려면 'exit' 입력)")
    url = "http://localhost:11434/api/chat"
    model = "gemma3:latest"  # 사용할 모델 이름, 필요에 따라 변경
    headers = {"Content-Type": "application/json"}
    messages = []
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("챗봇을 종료합니다.")
            break
        messages.append({"role": "user", "content": user_input})
        payload = {"model": model, "messages": messages}
        try:
            response = requests.post(url, json=payload, headers=headers, stream=True)
            response.raise_for_status()
            bot_message = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    content = data.get("message", {}).get("content", "")
                    bot_message += content
            if bot_message:
                print(f"Ollama: {bot_message}")
                messages.append({"role": "assistant", "content": bot_message})
            else:
                print("Ollama: (응답 없음)")
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    chat_with_ollama()
