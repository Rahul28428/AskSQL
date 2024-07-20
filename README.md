# SQL Query Retriever with Google Gemini Pro LLM

This project provides a Streamlit web application that allows users to interact with an SQLite database by asking questions in English. The application utilizes Google Gemini Pro LLM to convert these questions into SQL queries, execute them on the database, and display the results.

## Features

- Upload SQLite database files and configure table names and column names.
- Ask questions about the data and get corresponding SQL queries.
- Retrieve and display query results in a user-friendly format.

## Technologies Used

- **Streamlit**: Framework for building interactive web applications.
- **Google Gemini Pro LLM**: For generating SQL queries from English questions.
- **SQLite**: Database used for storing and querying data.
- **LangChain**: To handle conversation and prompt management.
- **Pandas**: For displaying query results in a tabular format.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Rahul28428/AskSQL-Intelligent-SQL-Query-Generator.git
    cd yourrepository
    ```

2. Install the required packages:
    ```bash
    pip install streamlit google-generativeai langchain langchain-google-genai pandas python-dotenv
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory of the project and add your Google Gemini API key:
    ```
    GOOGLE_API_KEY=your_google_api_key
    ```

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open the web app in your browser. The application will be available at `http://localhost:8501`.

3. In the sidebar, upload your SQLite database file and provide the table name and column names.

4. Ask questions about the data. The app will convert your questions into SQL queries and display the results.

## Code Explanation

- **app.py**: The main script for the Streamlit application. It handles user inputs, interacts with Google Gemini Pro LLM to generate SQL queries, executes these queries on the provided SQLite database, and displays the results.

    - `get_gemini_response(question, prompt)`: Uses Google Gemini Pro LLM to generate SQL queries based on the user’s question and prompt.
    - `read_sql_query(sql, db)`: Executes the generated SQL query on the SQLite database and retrieves the results.
    - `prompt_template`: Defines how the questions should be translated into SQL queries.

## Contributing

Feel free to fork the repository, make changes, and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please reach out to [your-rahulbarodia28@gmail.com](mailto:rahulbarodia28@gmail.com).

