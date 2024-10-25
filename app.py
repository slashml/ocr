import streamlit as st
import os
import asyncio
from tempfile import NamedTemporaryFile
from pyzerox import zerox
import fitz 
st.set_page_config(layout="wide")


async def do_ocr(file_path):
    model = "gpt-4o-mini"
    select_pages = None
    output_dir = "./"
    custom_system_prompt = None
    result = await zerox(file_path=file_path, model=model, output_dir=output_dir, 
                        custom_system_prompt=custom_system_prompt, select_pages=select_pages)
    return result

def format_content(content):
    """Format the content in a readable way"""
    if isinstance(content, str):
        formatted = content.replace('\\n', '\n').replace('\\t', '\t')
        return formatted
    return content

def extract_content(result):
    """Extract just the content from the pages"""
    if hasattr(result, 'pages'):
        contents = []
        for page in result.pages:
            if hasattr(page, 'content'):
                contents.append(page.content)
        return '\n'.join(contents)
    return str(result)

def display_pdf(file_path):
    """Display PDF preview"""
    try:
        doc = fitz.open(file_path)
        for page_num in range(min(len(doc), 5)):  # Show first 5 pages max
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))  # Reduced scale for preview
            st.image(pix.tobytes(), caption=f"Page {page_num + 1}", use_column_width=True)
        doc.close()
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")


st.title("PDF OCR Tool")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with st.container():
        
        left_col, right_col = st.columns([1, 1])

        with left_col:
            st.subheader("Upload and Preview")
            
            with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                preview_path = tmp_file.name
                
            
            st.write("PDF Preview:")
            display_pdf(preview_path)
            
            analyze_button = st.button("Analyze PDF")

        with right_col:
            st.subheader("Analysis Results")
            if 'analyze_button' in locals() and analyze_button:
                
                with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    file_path = tmp_file.name
                
                with st.spinner("Analyzing ..."):
                    result = asyncio.run(do_ocr(file_path))
                
                tab1, tab2, tab3 = st.tabs(["Formatted Output", "Raw Output", "JSON Output"])
                
                with tab1:
                    st.markdown("### Formatted Content")
                    formatted_content = format_content(extract_content(result))
                    st.markdown(formatted_content)
                
                with tab2:
                    st.markdown("### Raw Output")
                    st.code(str(result), language="python")
                
                with tab3:
                    st.markdown("### JSON Output")
                    if hasattr(result, '__dict__'):
                        json_data = {
                            "pages": [{
                                "page": idx + 1,
                                "content": page.content if hasattr(page, 'content') else str(page),
                                "contentLength": len(str(page))
                            } for idx, page in enumerate(result.pages)] if hasattr(result, 'pages') else [],
                            "fileName": getattr(result, 'file_name', ''),
                            "inputTokens": getattr(result, 'input_tokens', 0),
                            "outputTokens": getattr(result, 'output_tokens', 0),
                            "completionTime": getattr(result, 'completion_time', 0)
                        }
                        st.json(json_data)
                    else:
                        st.json({"error": "Could not convert result to JSON format"})

                # Clean up the temporary files
                os.unlink(file_path)
                if 'preview_path' in locals():
                    os.unlink(preview_path)
else:
    st.info("Upload a PDF file to start analysis.")

st.markdown("""
    <style>
        .css-18e3th9 {
            padding: 0 1rem; /* Adjust padding for a more full-width view */
        }
        .css-1d391kg {
            min-height: 100vh;
        }
    </style>
""", unsafe_allow_html=True)
