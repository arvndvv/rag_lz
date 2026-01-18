from marker.converters.pdf import PdfConverter
import inspect

print(inspect.signature(PdfConverter.__call__))
