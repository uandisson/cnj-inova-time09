from pdf2image import convert_from_path
import xml.etree.ElementTree as ET

import PyPDF2
import requests
from urllib.request import Request, urlopen

from io import StringIO, BytesIO

import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from PIL import Image
import io

import ocr
from db import Connect

class Util():
    def __init__(self):
        print('Util init...')
        
    
    def pdfToImage(self, path, numProcesso, db:Connect):
        try:
            pages = convert_from_path(path, 500)

            x = 0
            for page in pages:
                if x == 0:
                    
                    fileName = '{0}-{1}.jpg'.format(numProcesso, x)
                    file = 'out/' + fileName
                    
                    page.save(file, 'JPEG')
                    rocr = ocr.checkIA(file)
                    
                    db = Connect()
                    db.insertPeticao([ numProcesso, fileName, file, rocr])

                x+=1
            
            return True if (x > 0) else False
        except Exception as errors:
            print(f"Error PDFtoImage: {errors}")
            return False

    def image_to_byte_array(self, image:Image):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format=image.format)
        imgByteArr = imgByteArr.getvalue()
    
        return imgByteArr
    
    def readXML(self, xmlstring, db):
        try:
            
            tree = ET.ElementTree(ET.fromstring(xmlstring))
            root = tree.getroot()

            ns = {
                ''   : 'http://www.cnj.jus.br/intercomunicacao-2.2.2',
                'ns' : 'http://www.cnj.jus.br/replicacao-nacional'
            }
            interface = tree.findall('ns:processo', namespaces=ns)

            for child in interface:
                numProcesso = ''
                for c in child.findall('dadosBasicos', ns):
                    numProcesso = c.get('numero')
                
                for c in child.findall('movimento', ns):
                    if int(c.get('identificadorMovimento')) == 1:
                        rota = c.find('peticao', ns).text
                        self.readPDF(rota, numProcesso, db)
                
            return True
        except Exception as errors:
            print(f"Error readXML: {errors}")
            return False
    
    def readPDF(self, path, numProcesso, db):
        url = path
        writer = PyPDF2.PdfFileWriter()

        remoteFile = urlopen(Request(url)).read()
        memoryFile = BytesIO(remoteFile)
        pdfFile = PyPDF2.PdfFileReader(memoryFile)

        for pageNum in range(pdfFile.getNumPages()):
                currentPage = pdfFile.getPage(pageNum)
                writer.addPage(currentPage)

        fileOut = "output.pdf"
        outputStream = open(fileOut,"wb")
        writer.write(outputStream)
        outputStream.close()
        Util.pdfToImage(self, fileOut, numProcesso, db)
