from marker.converters.pdf import PdfConverter
import inspect

print(inspect.signature(PdfConverter.__init__))
# print(inspect.getdoc(PdfConverter.__init__))
