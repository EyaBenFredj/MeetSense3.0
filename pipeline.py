from transcription.transcriber import transcribe
from tools.acronym_tool import get_acronym_tool

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

def run_pipeline(audio_path: str):
    print("[🎙️] Transcribing meeting audio...")
    transcript = transcribe(audio_path)
    print("[📝] Transcript:\n", transcript)

    # Load your tool
    tools = [get_acronym_tool()]

    # Use GPT-3.5 if you still want it (but no embeddings here)
    llm = ChatOpenAI(temperature=0)  # This is still free on API key — works for now

    # Initialize agent with the tool
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # The prompt uses the acronym tool when needed
    prompt = (
        f"This is a meeting transcript:\n{transcript}\n\n"
        f"Use the AcronymLookup tool to explain any acronyms."
    )

    response = agent.run(prompt)
    print("\n🤖 Final Response:\n", response)

if __name__ == "__main__":
    run_pipeline("transcription/my_voice.wav")
