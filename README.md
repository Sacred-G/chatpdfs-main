# chatpdfs

## Introduction

Welcome to `chatpdfs-main`, a Streamlit app designed to provide an interactive experience with your PDF documents. By leveraging the OpenAI API, this app allows you to ask questions and get information from your PDFs as you view them. Perfect for researchers, students, and anyone who needs quick access to their PDF files.

## Features

- View PDF files within the app
- Interactive chat interface for document queries
- Integration with OpenAI API for advanced query capabilities
- Supports specific queries like "What is on page 5?" or "Search for the term XYZ"

## Prerequisites

- An OpenAI API key

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/sacred-g/chatpdfs-main.git
    ```

2. Navigate to the project directory and install the required packages:

    ```bash
    cd chatpdfs-main
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and populate it with your OpenAI API key:

    ```bash
    echo "OPENAI_API_KEY=your-api-key-here" > 
    ```

4. Run the app:

    ```bash
    streamlit run app.py
    ```

## How to Use

1. Open the app and enter your OpenAI API key when prompted.
2. Use the "Upload" button to upload your PDF document.
3. Once uploaded, you can view your PDF and interact with it via the chat interface.

## Contributing

If you'd like to contribute, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.