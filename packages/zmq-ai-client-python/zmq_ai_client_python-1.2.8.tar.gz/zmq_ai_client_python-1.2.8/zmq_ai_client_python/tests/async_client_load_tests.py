import asyncio
import random
import sys
import uuid

from zmq_ai_client_python import AsyncLlamaClient
from zmq_ai_client_python.schema import ChatCompletionRequest, Message, MessageRole, ChatCompletion

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

user_uuid = uuid.UUID("708bab67-64d2-4e7d-94b6-2b6e043d880c")

warmup_messages = [
    Message(role=MessageRole.system,
            content="A chat between a curious human and an artificial intelligence "
                    "assistant. The assistant gives helpful, detailed, and polite answers to the human's "
                    "questions."),
]

followup_messages = [
    Message(role=MessageRole.user, content='What was the name of the city.'),
    Message(role=MessageRole.user, content='What was the name of the country that I asked?'),
    Message(role=MessageRole.user, content=f'Tell me more about the capital of the country?'),
    Message(role=MessageRole.user, content=f'What is the population of the city in your answer?'),
    Message(role=MessageRole.user, content=f'What is the population of the country in the context?'),
    Message(role=MessageRole.user, content=f'What is the area of the country?')
]

countries = ["Germany", "Italy", "Spain", "Netherlands", "Switzerland", "Denmark", "Sweden", "Poland",
             "Czech Republic", "Greece", "Bulgaria", "Romania", "Ukraine", "United Kingdom"]

STOP = ["### Human:"]


async def send_conversation(client: AsyncLlamaClient, country: str):
    messages = warmup_messages + [
        Message(role=MessageRole.user, content=f'What is the capital of {country}?')
    ]

    questions = [f'What is the capital of {country}?']
    answers = []

    request = ChatCompletionRequest(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.8,
        n=2048,
        stop=STOP,
        user=user_uuid,
    )

    response: ChatCompletion = await client.send_chat_completion_request(request)
    print(f"** Question: {messages[len(warmup_messages)].content}'")
    session_uuid = response.key_values["session"]

    print(f"=== Session {session_uuid} is about {country} ===")
    answer = response.choices[0].message.content
    answers.append(answer)

    print(f"## Answer: {answer}")

    for message in followup_messages:
        questions.append(message.content)
        request = ChatCompletionRequest(
            model='gpt-3.5-turbo',
            messages=[message],
            temperature=0.8,
            n=1024,
            stop=STOP,
            user=user_uuid,
            key_values={"session": session_uuid}
        )

        response: ChatCompletion = await client.send_chat_completion_request(request)

        print(f"=== Session {session_uuid} is about {country} ===")
        print(f"** Question: {message.content}'")
        answer = response.choices[0].message.content
        answers.append(answer)
        print(f"## Answer: {answer}")

    return session_uuid, country, questions, answers


async def main():
    clients = []
    tasks = []

    for _ in range(4):
        client = AsyncLlamaClient('tcp://localhost:5555', timeout=360000)
        clients.append(client)
        country_index = random.randint(0, len(countries) - 1)
        country = countries[country_index]

        task = asyncio.create_task(send_conversation(client, country))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    for client in clients:
        client.close()

    for session_uuid, country, questions, answers in results:
        print(f"=== Session {session_uuid} Country {country} results ===")
        print(f"** Questions: {len(questions)}'")
        print(f"## Answers: {len(answers)}")


if __name__ == "__main__":
    asyncio.run(main())
