from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from scripts import camera_manager, memory_manager, speaker_manager
import requests
import time

llm = Ollama(model="llama3", base_url="http://localhost:11434")

camera_prompt = PromptTemplate.from_template("""
Tu es un assistant personnel qui reconnaît les personnes filmées par la caméra.
Si tu reconnais {person}, rappelle-lui le dernier sujet de conversation :
{summary}
Formule une salutation naturelle et engageante.
""")

N8N_CAMERA_WEBHOOK = "http://raspberrypi:5678/webhook/camera_trigger"

def detect_and_greet():
    print("📸 Agent LangChain caméra actif...")
    while True:
        try:
            person = camera_manager.recognize_person()
            if not person:
                time.sleep(2)
                continue

            summary = memory_manager.summarize_conversation(person)
            prompt = camera_prompt.format(person=person, summary=summary)

            response = llm.invoke(prompt)
            speaker_manager.say(response)
            print(f"💬 Agent a salué {person} : {response}")

            requests.post(N8N_CAMERA_WEBHOOK, json={"person": person, "summary": summary, "response": response})
            time.sleep(10)

        except Exception as e:
            print(f"⚠️ Erreur caméra LangChain : {e}")
            time.sleep(5)

if __name__ == "__main__":
    detect_and_greet()
