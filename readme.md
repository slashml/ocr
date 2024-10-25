# OCR tool for PDFs

## Easily parse the text in your pdf -- even if it's images.

Provides output in 3 formats:

1. Structured
2. Raw
3. JSON

## Set up

1. Clone the repository:
   ```
   git clone repo_link
   ```


2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Setting up Poppler -- This is required.

   You need to have poppler installed on your machine and added in path (system environment variables)

   Go to this link: https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.08.0-0

   Download the zip file, extract it, go to the bin folder isnide it, copy teh path and add it to your env variables.

5. Set your OPENAI_API_KEY
    ```
     export OPENAI_API_KEY=your_api_key_here     
    ```
    or 
    ```
     set OPENAI_API_KEY=your_api_key_here
    ```

## Usage

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Upload your pdf document and see the result in 3 formats: Structured, Raw, and JSON.
