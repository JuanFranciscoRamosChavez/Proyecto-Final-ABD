import os
import glob
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# 1. Configuración de Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUPS_DIR = os.path.join(BASE_DIR, 'backups')
ENV_PATH = os.path.join(BASE_DIR, '.env')

# 2. Cargar Clave
load_dotenv(ENV_PATH)
key = os.getenv("BACKUP_ENCRYPTION_KEY")

def decrypt_backup():
    print("="*60)
    print(" UTILIDAD DE RESTAURACIÓN DATAMASK ETL")
    print("="*60)

    if not key:
        print(" ERROR CRÍTICO: No se encontró BACKUP_ENCRYPTION_KEY en .env")
        return

    # 3. Escanear carpeta
    if not os.path.exists(BACKUPS_DIR):
        print(f" La carpeta de respaldos no existe en:\n   {BACKUPS_DIR}")
        return

    files = glob.glob(os.path.join(BACKUPS_DIR, '*.sql.enc'))
    
    # Ordenar por fecha (más reciente al final)
    files.sort(key=os.path.getmtime)

    if not files:
        print(f"  No se encontraron archivos .sql.enc en:\n   {BACKUPS_DIR}")
        return

    # 4. Mostrar Menú
    print(f"\n Archivos encontrados en '{BACKUPS_DIR}':\n")
    for i, file_path in enumerate(files):
        filename = os.path.basename(file_path)
        print(f"   [{i+1}] {filename}")

    print("\n" + "-"*60)
    
    # 5. Selección de Usuario
    try:
        selection = input(f" Selecciona el número del archivo a restaurar (1-{len(files)}): ")
        index = int(selection) - 1
        
        if index < 0 or index >= len(files):
            print(" Selección inválida.")
            return
            
        target_file = files[index]
        target_filename = os.path.basename(target_file)
        
    except ValueError:
        print(" Por favor ingresa un número válido.")
        return

    # 6. Desencriptación
    output_file = os.path.join(BACKUPS_DIR, "restored_script.sql")
    
    try:
        print(f"\n Procesando: {target_filename}...")
        
        with open(target_file, 'rb') as f:
            encrypted_data = f.read()

        fernet = Fernet(key.encode())
        decrypted_data = fernet.decrypt(encrypted_data)

        with open(output_file, 'wb') as f:
            f.write(decrypted_data)

        print("\n ¡ÉXITO! Respaldo desencriptado correctamente.")
        print(f" Archivo generado: {output_file}")
        print(" Ahora puedes abrir este archivo en un Administrador de Base de Datos y ejecutarlo.")
        print("  IMPORTANTE: Borra 'restored_script.sql' al terminar por seguridad.")

    except Exception as e:
        print(f"\n Error al desencriptar: {e}")
        print("Posible causa: La clave en .env no coincide con la del respaldo.")

if __name__ == "__main__":
    decrypt_backup()