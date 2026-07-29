from io import BytesIO
from docx import Document
from pypdf import PdfReader

from fastapi import UploadFile, HTTPException

class Parser:

    async def extract_text(self, file: UploadFile) -> str:
        if file.content_type == "application/pdf":
            return await self._extract_pdf(file)
        elif file.content_type in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"):
            return await self._extract_docx(file)
        elif file.content_type == "text/plain":
            return await self._extract_txt(file)
        raise HTTPException(status_code = 400, detail = "Unsupported file format")
    

    async def _extract_pdf(self, file: UploadFile) -> str:
        pdf_bytes = await file.read()
        
        try:
            doc = PdfReader(BytesIO(pdf_bytes))
            if doc.is_encrypted:
                raise HTTPException(status_code = 400, detail = "Password-protected PDFs are not supported")
            
            extracted_text = []
            for i, page in enumerate(doc.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(f"\n\n~~~~ PAGE {i} ~~~~\n\n"
                                        f"{page_text}")
                    
            text = "\n".join(extracted_text).strip()
            if not text:
                raise HTTPException(status_code = 400, detail = "No extractable text found in the uploaded file")
            
            return text
        
        except HTTPException:
            raise
        
        except Exception:
            raise HTTPException(status_code = 400, detail = "Invalid or corrupted PDF file")
    
    
    async def _extract_docx(self, file: UploadFile) -> str:
        docx_bytes = await file.read()
        
        try:
            doc = Document(BytesIO(docx_bytes))
            extracted_text = [paragraph.text for paragraph in doc.paragraphs]

            text = "\n".join(extracted_text).strip()
            if not text:
                raise HTTPException(status_code = 400, detail = "No extractable text found in the uploaded file")
            
            return text
        
        except HTTPException:
            raise
        
        except Exception:
            raise HTTPException(status_code = 400, detail = "Invalid or corrupted Word document")
    

    async def _extract_txt(self, file: UploadFile) -> str:
        txt_bytes = await file.read()

        try:
            text = txt_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code = 400, detail = "Only UTF-8 encoded text files supported")
        
        text = text.strip()
        if not text:
            raise HTTPException(status_code = 400, detail = "Text file empty")

        return text
