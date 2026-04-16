from reportlab.pdfgen import canvas
# to import the canva where we will be writing on
from reportlab.lib import colors
# colors for the text


filename = 'Document.pdf' # the '.pdf' so the file will be created as a pdf file

document_title = 'Title'

title = 'Information' # title of the pdf
text = 'My name is Bond ... James Bond'
pdf = canvas.Canvas(filename) # inside the brackets we enter the type of the document, or we call a variable that we have created prior that contains the type and name

paragraf =pdf.beginText()


pdf.setFont('Times-Roman', 12)

pdf.setTitle(title) # title of the document

pdf.drawString(x=250,y=770,text=title) # the text that we want to enter inspire the pg

pdf.line(x1=25,y1=760,x2=570,y2=760) # to draw a line setting the beginning and the end of x and y

pdf.drawString(x=20,y=740,text=text) # the text that we want to enter inspire the pg

text_2 = pdf.beginText(30,680)
text_2.setFont('Times-Roman', 12)
text_2.setFillColor(colors.red)

for line in text:
    text_2.textLine(line)

pdf.drawText(text_2)

pdf.save() # to save all to customize that we have made