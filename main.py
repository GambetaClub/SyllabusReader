from pdf2txt import pdf2txt
def main():
    #main
    inPDFfile = 'syllabus1.pdf'
    outTXTFile = 'syllabus1.txt'
    pdf2txt(inPDFfile, outTXTFile)

if __name__ == "__main__":
    main()