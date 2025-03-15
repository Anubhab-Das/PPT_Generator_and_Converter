# 📌 PPT_Generator_and_Converter

🚀 AI-powered tool that converts PDFs into structured PowerPoint presentations using LLMs, FastAPI, and Streamlit. Supports automatic image fetching and minimal token usage for efficiency.

## 📖 Features

-  **Receive topics from user and create complete PPTs**
-  **Convert PDFs to PPT**: Extracts content from PDFs and structures it into well-formatted PowerPoint slides.
-  **AI-Generated Content**: Uses LLMs to generate slide text and structure efficiently.
-  **Image Handling**: Extracts images from PDFs or fetches relevant images using SerpAPI if needed.
-  **FastAPI Backend**: Provides a robust API to process PDF-to-PPT conversion requests.
-  **Streamlit Frontend**: User-friendly interface for seamless interaction.
-  **Optimized Token Usage**: Uses the GPT-4o mini model with minimal token consumption.

🎯**I've used a short prompt and haven't asked the LLM to make the PPT very visually appealing. This has been done to minimize token usage, but if you are ready to bear the forthcomings, you are free to use a better model and a more detailed prompt.**

## 🏗 Project Structure

```
📂 agent_catalog
├── 📄 api.py                 # FastAPI backend
├── 📄 app.py                 # Streamlit frontend
├── 📄 base_tool.py           # Abstract base class for tools
├── 📄 config.py              # Configuration settings
├── 📄 image_fetcher.py       # Image extraction and retrieval
├── 📄 langgraph_pipeline.py  # LangGraph-based pipeline
├── 📄 main.py                # Entry point
├── 📄 pdf_to_ppt_converter.py # PDF parsing and conversion logic
├── 📄 ppt_generator.py       # PPT generation logic
├── 📄 ppt_request.py         # Handles PPT request processing
├── 📄 register_tools.py      # Tool registration module
├── 📄 requirements.txt       # Dependencies
├── 📄 text_generation.py     # LLM-based text generation
├── 📄 tool_registry.py       # Manages available tools
│
├── 📂 assets                 # Stores template assets
├── 📂 output                 # Stores generated PPT files
├── 📂 templates              # PPT templates
├── 📂 uploads                # Stores uploaded PDFs
```

## 🚀 Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.10+
- pip
- PostgreSQL (for future database integration)

### Steps
```sh
# Clone the repository


# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Usage

### Running the Backend (FastAPI)
```sh
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
FastAPI will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Running the Frontend (Streamlit)
```sh
streamlit run app.py
```
The UI will be available at: [http://localhost:8501](http://localhost:8501)

## 📌 API Endpoints

- `POST /convert_pdf` → Upload a PDF and convert it into a PPT
- `GET /status/{job_id}` → Check the status of a conversion job
- `GET /download/{job_id}` → Download the generated PPT

## 🔧 Configuration
Modify `config.py` to set API keys and other parameters.

## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributing
Contributions are welcome! Please create a PR or open an issue for any suggestions.

## 📩 Contact
For any questions, reach out at anubhab.99d@gmail.com.
