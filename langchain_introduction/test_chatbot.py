
from langchain.schema.messages import HumanMessage, SystemMessage

from chatbot import chat_model

system_messages_de = [
    """Sie sind ein Assistent, der sich mit Gesundheitsfragen auskennt. Beantworten Sie nur Fragen zu Gesundheitsthemen.""",
    """Sie sind ein Geschichtslehrer. Beantworten Sie nur Fragen zur Geschichte der Antike.""",
    """Sie sind ein Kryptohandel-Assistent. Beantworten Sie nur Fragen, die sich auf den Kryptohandel beziehen.""",
    """Sie sind ein Kryptohandel-Assistent. Beantworten Sie nur Fragen, die sich auf den Kryptohandel beziehen.""",
]

human_messages_de = [
    "Was ist Medicaid-Managed Care?",
    "Stellen Sie mir zehn Fragen zur Geschichte Roms.",
    "Was ist der vielversprechendste Weg, Ihre Investition um 10 % in einer Woche zu steigern?",
    "Was würde ein Kryptohändler auf die Frage antworten, wie man einen Nagel in die Wand schlägt?",
]

system_messages = {
    'en' : [
    """You're an assistant knowledgeable about healthcare. Only answer healthcare-related questions.""",
    """You are a history teacher. Only answer questions about the history of antiquity.""",
    """You are a Cryptotrading assistant. Only answer questions related to Cryptotrading.""",
    """You are a Cryptotrading assistant. Only answer questions related to Cryptotrading.""",
    ],
    'de' : [
    """Sie sind ein Assistent, der sich mit Gesundheitsfragen auskennt. Beantworten Sie nur Fragen zu Gesundheitsthemen.""",
    """Sie sind ein Geschichtslehrer. Beantworten Sie nur Fragen zur Geschichte der Antike.""",
    """Sie sind ein Kryptohandel-Assistent. Beantworten Sie nur Fragen, die sich auf den Kryptohandel beziehen.""",
    """Sie sind ein Kryptohandel-Assistent. Beantworten Sie nur Fragen, die sich auf den Kryptohandel beziehen.""",
    ],
}

human_messages = {
    'en' : [
    "What is Medicaid managed care?",
    "Ask me ten questions about the history of Rome.",
    "What is the most promising way to increase your investment by 10% in a week?",
    "What would a Cryptotrader answer to the question of how to hit a nail into the wall?",
    ],
    'de' : [
    "Was ist Medicaid-Managed Care?",
    "Stellen Sie mir zehn Fragen zur Geschichte Roms.",
    "Was ist der vielversprechendste Weg, Ihre Investition um 10 % in einer Woche zu steigern?",
    "Was würde ein Kryptohändler auf die Frage antworten wie man einen Nagel in die Wand schlägt?",
    ],
}

TEST_LANGUAGE = "en"
TEST_MESSAGE_INDEX = 1

messages = [
    SystemMessage(content=system_messages[TEST_LANGUAGE][TEST_MESSAGE_INDEX]),
    HumanMessage(content=human_messages[TEST_LANGUAGE][ TEST_MESSAGE_INDEX]),
]

print("System message: ", system_messages[TEST_LANGUAGE][TEST_MESSAGE_INDEX])
print("Human message: ", human_messages[TEST_LANGUAGE][TEST_MESSAGE_INDEX])

result = chat_model.invoke(messages)

print(result.content)

