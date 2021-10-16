from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
def pdf2txt(inPDFfile, outTXTFile):
    inFile = open(inPDFfile, 'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
    interpreter = PDFPageInterpreter(resMgr, TxtConverter)
    
    #process each page in pdf file
    for page in PDFPage.get_pages(inFile):
        interpreter.process_page(page)

    txt = retData.getvalue()
    #save output data to a text file
    with open(outTXTFile, 'w') as f:
        f.write(txt)
