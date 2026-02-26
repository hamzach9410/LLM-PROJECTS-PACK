import tempfile
import logging
from datetime import datetime
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf(file, chunk_size: int = 1000, chunk_overlap: int = 200) -> List:
    """
    Process an uploaded PDF file, split it into text chunks, and add metadata.
    
    Args:
        file: Streamlit UploadedFile object.
        chunk_size (int): Size of each text chunk.
        chunk_overlap (int): Overlap between consecutive chunks.
        
    Returns:
        List: List of LangChain Document objects.
    """
    try:
        logging.info(f"Processing PDF: {file.name}")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file.getvalue())
            loader = PyPDFLoader(tmp_file.name)
            documents = loader.load()
            
            # Add source metadata
            for doc in documents:
                doc.metadata.update({
                    "source_type": "pdf",
                    "file_name": file.name,
                    "timestamp": datetime.now().isoformat()
                })
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            chunks = text_splitter.split_documents(documents)
            logging.info(f"PDF {file.name} split into {len(chunks)} chunks.")
            return chunks
    except Exception as e:
        logging.error(f"PDF processing error for {getattr(file, 'name', 'unknown')}: {str(e)}")
        return []
