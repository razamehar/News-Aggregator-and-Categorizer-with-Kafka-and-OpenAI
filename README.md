# News Aggregator and Categorizer with Kafka and OpenAI

This project is a news aggregation and categorization system that pulls news from multiple sources using Google RSS feeds. The aggregated news is sent to **Apache Kafka** via a producer. Afterward, **OpenAI** is utilized to categorize each news article into predefined topics, including:

- **General**
- **Politics**
- **Technology**
- **Sports**
- **Entertainment**

The categorized news articles are then consumed by a Kafka consumer and stored in a **PostgreSQL** database for easy retrieval and analysis.

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

- **PostgreSQL**: Database to store the categorized news articles.
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
   
## License
This project is licensed under the Raza Mehar License. For further details, refer to the LICENSE.md file.

## Contact
If you have any questions or need clarification, feel free to reach out to Raza Mehar at raza.mehar@gmail.com.