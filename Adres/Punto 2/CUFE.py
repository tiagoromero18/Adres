import os
import re
import sqlite3
import PyPDF2

def extract_cufe_from_pdf(pdf_path):
    cufe_pattern = re.compile(r"\b([0-9a-fA-F]\n*){95,100}\b", re.MULTILINE)
    cufe_found = None
    num_pages = 0
    
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages) #Extraemos el numero de paginas
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

            match = cufe_pattern.search(text) #buscamos un match del cufe con la expresion regular
            if match:
                cufe_found = match.group().replace("\n", "") 
    except Exception as e:
        print(f"Error procesando {pdf_path}: {e}")
    
    return num_pages, cufe_found


def save_to_db(data, db_path="facturas.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT,
            num_paginas INTEGER,
            cufe TEXT,
            peso_kb REAL
        )
    """
    )
    cursor.executemany("""
        INSERT INTO facturas (nombre_archivo, num_paginas, cufe, peso_kb)
        VALUES (?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close() 
    #Funcion sencilla para crear o añadir información a la tabla de SQLite 

def show_db_data(db_path="facturas.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facturas")
    rows = cursor.fetchall()
    conn.close()
    
    print("\nStored Data:")
    for row in rows:
        print(row)

    #Funcion que imprime los datos

def process_pdfs(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith(".PDF")]

    if not pdf_files:
        print("No hay archivos PDF en la ruta especificada.")
        return  # Sale si no encuentra pdfs en la la ruta

    extracted_data = []
    
    for pdf in pdf_files:
        pdf_path = os.path.join(directory, pdf)
        
        file_size = os.path.getsize(pdf_path) / 1024  # Convert to KB
        num_pages, cufe = extract_cufe_from_pdf(pdf_path)

        extracted_data.append((pdf, num_pages, cufe, file_size))
    
    save_to_db(extracted_data)
    print("Proceso completado. Datos almacenados en la base de datos.")
    show_db_data()

process_pdfs("facturas")

