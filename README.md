# News Aggregator and Categorizer with Kafka and OpenAI

This project is a news aggregation and categorization system that pulls news from multiple sources using Google RSS feeds. The aggregated news is sent to **Apache Kafka** via a producer. Afterward, **OpenAI** is utilized to categorize each news article into predefined topics, including:

- **General**
- **Politics**
- **Technology**
- **Sports**
- **Entertainment**

The categorized news articles are then consumed by Kafka consumers and stored in either a **PostgreSQL** or **MySQL** database for easy retrieval and analysis.

## Features

- **News Aggregation**: Pulls news from various sources using Google RSS feeds.
- **Real-time Categorization**: Categorizes news articles into topics using OpenAI.
- **Kafka Integration**: News articles are sent to Kafka for streaming and processing.
- **Database Storage**: Categorized articles are stored in a PostgreSQL database for efficient querying.
  
## Use Cases

- **Journalists**: Helps journalists to quickly access categorized news from various sources.
- **Researchers**: Enables researchers to analyze news trends and topics based on categorized data.

## Requirements

Before setting up the project, ensure you have the following installed:

- **PostgreSQL** or **MySQL**: Databases to store the categorized news articles.
- **Docker Desktop**: For running Kafka and other containerized services locally.

## Setup Instructions

1. **Create a Virtual Environment**  
   Start by creating a virtual environment for managing dependencies:
   ```bash
   python -m venv venv
   ```
   
2. **Set Up Kafka**
   Follow the instructions in the Confluent Kafka Setup Guide to install and configure Kafka on your machine.

3. **Install Required Dependencies** 
   After Kafka setup, install all required Python packages listed in the requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Database Configuration**
Update the .env file with the correct database credentials (either for PostgreSQL or MySQL).
- Example .env for PostgreSQL:
  POSTGRES_DB=mydb
  POSTGRES_USER=your_user
  POSTGRES_PASSWORD=your_password

- Example .env for MySQL:
  MYSQL_DB=mydb
  MYSQL_USER=your_user
  MYSQL_PASSWORD=your_password

5. **Consumer Scripts**
There are two Kafka consumers to choose from based on your database preference:
- PostgreSQL Consumer: Consumes categorized news and stores it in a PostgreSQL database. Run the consumer for PostgreSQL:
   ```bash
   python consumer_postgres.py
   ```

- MySQL Consumer: Consumes categorized news and stores it in a MySQL database. Run the consumer for MySQL:
   ```bash
   python consumer_mysql.py
   ```

Both consumers will listen to Kafka, process the incoming news, categorize it using OpenAI, and store it in your selected database.

## License
This project is licensed under the Raza Mehar License. For further details, refer to the LICENSE.md file.

## Contact
If you have any questions or need clarification, feel free to reach out to Raza Mehar at raza.mehar@gmail.com.