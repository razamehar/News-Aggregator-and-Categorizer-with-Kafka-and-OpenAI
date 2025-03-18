from confluent_kafka import Consumer, KafkaException, KafkaError
import logging
import json
from dotenv import load_dotenv
import mysql.connector
import os


load_dotenv()

db_name = os.getenv("MYSQL_DB")
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")

conn = mysql.connector.connect(
    host="localhost",
    user=db_user,
    password=db_password,
    database=db_name,
    port=3306
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic TEXT,
    title TEXT,
    source TEXT,
    published_date DATE,
    link TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (link(255))
);
""")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == '__main__':

    config = {
        'bootstrap.servers': 'localhost:50967',
        'group.id': 'kafka-python-getting-started',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(config)

    topics = ["General", "Politics", "Technology", "Sports", "Entertainment"]

    consumer.subscribe(topics)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                logging.info("Waiting...")
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.info(f"End of partition reached: {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                else:
                    logging.error(f"ERROR: {msg.error()}")
            else:
                msg_value = msg.value().decode('utf-8')
                msg_dict = json.loads(msg_value)

                title = msg_dict.get("title", "")
                source = msg_dict.get("source", "")
                published_date = msg_dict.get("published_date", "")
                link = msg_dict.get("link", "")

                if not published_date:
                    published_date = None

                logging.info(f"Consumed event from topic {msg.topic()}: title = {title}, source = {source}, published_date = {published_date}, link = {link}")

                # Check if the news article already exists in the database
                cursor.execute("SELECT COUNT(*) FROM news WHERE link = %s", (link,))
                if cursor.fetchone()[0] == 0:

                    cursor.execute("""
                        INSERT INTO news (topic, title, source, published_date, link) 
                        VALUES (%s, %s, %s, %s, %s);
                    """, (msg.topic(), title, source, published_date, link))

                conn.commit()
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")
    except KafkaException as e:
        logging.error(f"Kafka Exception: {e}")
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error inserting into MySQL: {str(e)}")
    finally:
        consumer.close()
        cursor.close()
        conn.close()
