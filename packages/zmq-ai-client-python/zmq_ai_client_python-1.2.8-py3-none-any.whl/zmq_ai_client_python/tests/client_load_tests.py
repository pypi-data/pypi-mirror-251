import random
import uuid

from zmq_ai_client_python import LlamaClient
from zmq_ai_client_python.schema import Message, MessageRole, ChatCompletionRequest, ChatCompletion


def main():
    client = LlamaClient('tcp://localhost:5555', timeout=360000)

    user_uuid = uuid.UUID("708bab67-64d2-4e7d-94b6-2b6e043d880c")

    chat_prompt_message = Message(role=MessageRole.system,
                                  content="A chat between a curious human and an artificial intelligence assistant. "
                                          "The assistant gives helpful, detailed, and polite answers to the human's "
                                          "questions.")
    title_prompt_message = Message(
        role=MessageRole.system,
        content="You are a helpful assistant. You generate a descriptive, short and meaningful title for the "
                "given conversation.")
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

    session_countries = {}

    # send initial messages for each session
    for _ in range(1):

        while True:
            country_index = random.randint(0, len(countries) - 1)
            country = countries[country_index]
            if country not in session_countries.values():
                break

        messages = [chat_prompt_message,
                    Message(role=MessageRole.user, content=f'What is the capital of {country}?')
                    ]

        chat_request = ChatCompletionRequest(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.8,
            n=2048,
            stop=STOP,
            user=user_uuid,
        )

        print(f"** Question: {messages[-1].content}'")

        chat_response: ChatCompletion = client.send_chat_completion_request(chat_request)
        session_uuid = chat_response.key_values["session"]
        session_countries[session_uuid] = country

        print(f"=== Session {session_uuid} is about {country} ===")
        answer = chat_response.choices[0].message.content

        print(f"## Answer: {answer}")

        test_title_generation = True

        if test_title_generation:
            # send title generation request
            title_messages = [title_prompt_message,
                              Message(role=MessageRole.user,
                                      content=f'Question: What is the capital of {country}? '
                                              f'Answer: {answer}')
                              ]

            title_request = ChatCompletionRequest(
                model='gpt-3.5-turbo',
                messages=title_messages,
                temperature=0.8,
                n=256,
                stop=STOP,
                key_values={"use_cache": False}

            )
            title_response: ChatCompletion = client.send_chat_completion_request(title_request)

            print(f'=== Session {chat_response.key_values["session"]} is about {country} ===')
            title_answer = title_response.choices[0].message.content
            print(f"** {title_answer}")

        # send each followup messages for each session
    for message in followup_messages:
        for session_uuid, country in session_countries.items():
            chat_request = ChatCompletionRequest(
                model='gpt-3.5-turbo',
                messages=[message],
                temperature=0.8,
                n=1024,
                stop=STOP,
                user=user_uuid,
                key_values={"session": session_uuid}
            )

            print(f"=== Session {session_uuid} is about {country} ===")
            print(f"** Question: {message.content}'")

            chat_response: ChatCompletion = client.send_chat_completion_request(chat_request)

            answer = chat_response.choices[0].message.content
            print(f"## Answer: {answer}")


if __name__ == "__main__":
    main()
