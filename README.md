# Tikeetron AI (Python FastAPI)

This is the AI backend for **Tikeetron**, an AI-first event marketplace app that uses FastAPI for managing AI functionalities such as event recommendations, ticketing assistance, and real-time user interaction. The AI system is powered by **Llama3**, utilizing Retrieval-Augmented Generation (RAG) with MongoDB vectors for data retrieval. The backend also interacts with the blockchain and serves as the core engine for the app's AI assistant.

## Features
- **AI-Powered Event Recommendations**: Provide personalized event recommendations to users based on historical data and preferences.
- **Real-Time Ticketing Assistance**: Users can ask the AI about their tickets, event details, and manage ticket transfers.
- **Integration with MongoDB**: Store event and ticket information as vectors for efficient retrieval and ranking of results.
- **FastAPI Framework**: Lightweight and fast API framework to handle AI interactions.
  
## Core Dependencies

The Tikeetron AI backend relies on the following core dependencies for efficient functionality:

### 1. **LangChain**  
   LangChain is used to build and manage complex language model pipelines. It helps us handle natural language understanding (NLU), event recommendations, and interactions with the AI assistant.
   
   - **Use Case**: Managing the conversation flow and decision-making for AI-powered features in the app.

### 2. **LangChain-GROQ**  
   This extends LangChain's capabilities by adding integration with **GROQ**, a high-performance hardware and software stack for accelerated AI workloads. It enhances the speed and efficiency of running language models like Llama3.
   
   - **Use Case**: Enhancing the inference speed and performance of our AI models when processing complex queries from users.
   
### 3. **PyMongo**  
   **PyMongo** allows us to interact with MongoDB, which stores all the event and ticket metadata as vectorized information for retrieval-augmented generation (RAG).
   
   - **Use Case**: Storing and retrieving event data efficiently, enabling fast AI query results based on user input.

### 4. **LangGraph**  
   **LangGraph** is used for building conversational agents and knowledge graphs. This allows us to structure and link event data, ticket information, and user interaction histories for more context-aware AI responses.
   
   - **Use Case**: Building a knowledge graph of event data and user preferences for improved AI-powered event recommendations.

## Installation

To set up the Tikeetron AI backend, follow these steps:

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/TikeeTron/tikeetron_ai.git
   cd tikeetron-ai-backend
   ```

2. **Install Dependencies**  
   Install the required Python packages listed in `requirements.txt`:
3. **Set Up MongoDB**  
   - Ensure that MongoDB is up and running. The AI system interacts with MongoDB to retrieve and store vectorized data.
   - Create a MongoDB database for event and ticket storage.

4. **Run the FastAPI Server**  
   Start the FastAPI server to handle AI interactions:
   ```bash
   uvicorn main:app --reload
   ```

5. **Environment Variables**  
   Make sure to configure the example environment variables

## AI Architecture

The Tikeetron AI backend uses a combination of:
- **Llama3** for language understanding.
- **Retrieval-Augmented Generation (RAG)** for retrieving context-relevant information from MongoDB vector data.
- **FastAPI** to serve AI interactions at scale.
- **LangChain** and **LangGraph** for building conversation flows and linking knowledge across event datasets.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

For more information about the AI assistant and its integration with the Tikeetron mobile app, refer to our [White Paper](https://docs.tikeetron.cloud).