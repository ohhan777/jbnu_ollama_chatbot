import requests
import json
import time

def chat_with_ollama():
    print("Ollama 챗봇에 오신 것을 환영합니다! (종료하려면 'exit' 입력)")
    url = "http://localhost:11434/api/chat"
    model = "gemma3:latest"
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
            
            print("Ollama: ", end="", flush=True)
            bot_message = ""
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        content = data.get("message", {}).get("content", "")
                        
                        if content:
                            for char in content:  # 글자 하나씩 출력 (타이핑 효과)
                                print(char, end="", flush=True)
                                time.sleep(0.01)  # 20ms 딜레이
                            bot_message += content
                        
                        if data.get("done", False):
                            break
                            
                    except json.JSONDecodeError:
                        continue
            
            print()  # 줄바꿈
            
            if bot_message:
                messages.append({"role": "assistant", "content": bot_message})
            else:
                print("(응답 없음)")
                
        except KeyboardInterrupt:
            print("\n응답 중단됨")
            break
        except Exception as e:
            print(f"\n오류 발생: {e}")

if __name__ == "__main__":
    chat_with_ollama()