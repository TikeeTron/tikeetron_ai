from app.chatbot.chain import agent

response = agent.invoke(
    {
        "messages": [
            (
                "system",
                "You are the Tikeetron Bot, designed to assist users with questions about events. Ensure that your responses are accurate and based on the provided passages.",
            ),
            (
                "human",
                "tell me more about Formula 1 Monaco Grand Prix",
            ),
        ],
    },
)

message = response["messages"][-1]
if message != None:
    print(message.content)
else:
    print("No response")
