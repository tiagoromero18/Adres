from django.shortcuts import render
from .forms import UploadFileForm
import io
import re

def validate_file(request):
   if request.method == 'POST':
       form = UploadFileForm(request.POST, request.FILES)
       if form.is_valid():
           file = request.FILES['file']
           file_data = file.read().decode('utf-8')
           lines = file_data.splitlines()
           validation_results = []
           for row_num, line in enumerate(lines):
               values = line.split(',')
               if len(values) != 5:
                   validation_results.append(f'Error en la fila {row_num + 1}: número incorrecto de columnas.')
                   continue

               col1, col2, col3, col4, col5 = values

               if not re.match(r'^\d{3,10}$', col1):
                   validation_results.append(f'Error en la fila {row_num + 1}, columna 1: valor no válido.')
               if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', col2):
                   validation_results.append(f'Error en la fila {row_num + 1}, columna 2: correo electrónico no válido.')
               if col3 not in ('CC', 'TI'):
                   validation_results.append(f'Error en la fila {row_num + 1}, columna 3: valor no válido.')
               try:
                   if not (500000 <= int(col4) <= 1500000):
                       validation_results.append(f'Error en la fila {row_num + 1}, columna 4: valor fuera de rango.')
               except ValueError:
                   validation_results.append(f'Error en la fila {row_num + 1}, columna 4: valor no numérico.')

           if not validation_results:
               validation_results.append('Archivo validado con éxito.')

           return render(request, 'validator_app/result.html', {'results': validation_results})
   else:
       form = UploadFileForm()
   return render(request, 'validator_app/upload.html', {'form': form})
