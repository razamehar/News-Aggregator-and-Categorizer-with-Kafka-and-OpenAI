import json
import time
import logging
from confluent_kafka import Producer
from time import sleep
from dotenv import load_dotenv
from fetch_news import fetch_news
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Annotated, Literal

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class NewsTopic(BaseModel):
    topic: Annotated[Literal["General", "Politics", "Technology", "Sports", "Entertainment"], "Return topic of the news headline as either 'General', 'Politics', 'Technology', 'Sports', 'Entertainment'"]

def classify_news(title):
    model = ChatOpenAI(max_tokens=40)
    parser = PydanticOutputParser(pydantic_object=NewsTopic)

    prompt = PromptTemplate(
        template=""" 
        Please assign a topic to this news headline: "{title}"  
        Choose from: "General", "Politics", "Technology", "Sports", "Entertainment".  
        {format_instruction}
        """,
        input_variables=['title'],
        partial_variables={'format_instruction':parser.get_format_instructions()}   ,  # Example output
    )

    chain = prompt | model | parser
    result = chain.invoke({'title': title})
    return result.topic

def delivery_callback(err, msg):
    if err:
        logging.error(f"ERROR: Message failed delivery: {err}")
    else:
        logging.info(f"Produced event to topic {msg.topic()}: key = {msg.key().decode('utf-8'):12} value = {msg.value().decode('utf-8'):12}")

config = {
    'bootstrap.servers': 'localhost:50967',
    'retries': 2,
    'retry.backoff.ms': 1000,
    'acks': 'all'  # Fixed properties
}

producer = Producer(config)

while True:
    try:
        sources, titles, links, published_dates = fetch_news()
        for source, title, link, published_date in zip(sources, titles, links, published_dates):
            message = {
                "title": str(title),
                "source": str(source),
                "link": str(link),
            }

            topic = classify_news(title)
            producer.produce(topic, key=published_date.encode('utf-8'), value=json.dumps(message), callback=delivery_callback)

        # Process all messages before closing
        producer.poll(10000)
        producer.flush()
        time.sleep(5)

    except KeyboardInterrupt:
        logging.info("Shutting down producer...")
        break

    except Exception as e:
        logging.error(f"Exception while producing message: {e}")
        sleep(2)

producer.flush()