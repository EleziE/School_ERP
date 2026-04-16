
                                                                                                                
<p align="center">Report Information </p>

These are some of the defaults that a person might need to know for a report on `reportlab`. Some measurements of pages or some other things that might help him to customize a report using `reportlab`, package of python.

## Installation


```bash
pip install reportlab
```

Run this command in the `venv` that you want to install it  

---
A4 page ***dimensions*** :

***x = 500px (max)***

***y = 810px (max)***

---
Default commands for every report:
 ```python
from reportlab.pdfgen import canvas 
# to import the canva where we will be writing on 


title = 'Document' # title of the pdf
filename = 'Document.pdf' # the '.pdf' so the file will be created as a pdf file 
text = 'My name is Bond ... James Bond'

pdf = canvas.Canvas(filename) # inside the brackets we enter the type of the document, or we call a variable that we have created prior that contains the type and name
pdf.setTitle(title) # title of the document 
pdf.drawString(x=270,y=770,text=text) # the text that we want to enter inspire the pg 





pdf.save() # to save all to customize that we have made 

 ```
