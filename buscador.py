import psycopg2
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
DB_NAME = os.getenv('POSTGRES_DB')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Parámetros de conexión para PostgreSQL (ajusta según tu entorno)
db_params = {
    'host': 'localhost',
    'port': 5432,
    'dbname': DB_NAME,
    'user': USER,
    'password': PASSWORD
}

def buscar_soluciones(query_text, empresa_id=None, limite=20):
    """
    Busca soluciones similares usando similitud coseno
    
    Args:
        query_text (str): Texto de búsqueda
        empresa_id (int): ID de la empresa
        limite (int): Número máximo de resultados
    
    Returns:
        list: Lista de tuplas (id, nombre, descripcion, similitud)
    """
    
    try:
        tiempo_inicio_total = time.time()
        
        # 1. Conectar a la base de datos
        tiempo_inicio_conexion = time.time()
        
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        tiempo_conexion = time.time() - tiempo_inicio_conexion

        # 2. Si la empresa esta logeada, se obtienen las caracteristicas de la empresa para el filtro
        tiempo_inicio_query_empresa = time.time()

        if empresa_id:
            cursor.execute("""
                SELECT name,sector_id, employees_range, postcode_id FROM empresas_es WHERE id = %s
            """, (empresa_id,))
            empresa = cursor.fetchone()

        tiempo_query_empresa = time.time() - tiempo_inicio_query_empresa

        # 3. Convertir texto a vector
        tiempo_inicio_vector = time.time()
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.embeddings.create(
            input=query_text,
            model="text-embedding-3-large"
        )
        query_vector = response.data[0].embedding
        
        tiempo_vector = time.time() - tiempo_inicio_vector
    
        # 4. Buscar en la base de datos
        tiempo_inicio_busqueda = time.time()
        
        cursor.execute("""
            SELECT 
                id,
                name,
                1 - (description_embed <=> %s::vector) as similitud,
                prioridad
            FROM soluciones_es 
            WHERE description_embed IS NOT NULL
            ORDER BY description_embed <=> %s::vector
            LIMIT %s
        """, (query_vector, query_vector, limite))

        resultados = cursor.fetchall()

        # Si prioridad está informado a 1, se le suma 0.05 al score de similitud
        resultados_modificados = []
        for fila in resultados:
            id, name, similitud, prioridad = fila
            if prioridad == 1:
                similitud += 0.05
            resultados_modificados.append((id, name, similitud, prioridad))
        # Reordenar de mayor a menor score (similitud)
        resultados_modificados.sort(key=lambda x: x[2], reverse=True)
        resultados = resultados_modificados

        tiempo_busqueda = time.time() - tiempo_inicio_busqueda
        
        # 5. Mostrar resultados
        print(f"\n🔍 RESULTADOS ({len(resultados)} encontrados):")
        for i, (id, name, similitud, prioridad) in enumerate(resultados, 1):
            prio_str = "  >>> PRIO <<<" if prioridad == 1 else ""
            print(f"{i}. [{id}] {name} (Similitud: {similitud*100:.1f}%) {prio_str}")

        # 6. Mostrar filtros
        print("\n🎛️  FILTROS UTILIZADOS:")
        if empresa_id and empresa:
            nombre_empresa = empresa[0] if empresa[0] else "Desconocido"
            sector_id = empresa[1] if empresa[1] is not None else "No especificado"
            employees_range = empresa[2] if empresa[2] is not None else "No especificado"
            postcode_id = empresa[3] if empresa[3] is not None else "No especificado"
            print(f"   • Empresa: {nombre_empresa} (ID: {empresa_id})")
            print(f"   • Sector ID: {sector_id}")
            print(f"   • Rango de empleados ID: {employees_range}")
            print(f"   • Código postal ID: {postcode_id}")
        else:
            print("   • Sin filtros de empresa (búsqueda general)")
        
        # 7. Resumen de tiempos
        tiempo_total = time.time() - tiempo_inicio_total
        print(f"\n⏱️  RESUMEN DE TIEMPOS:")
        print(f"   • Conexión a BD: {tiempo_conexion:.2f}s")
        print(f"   • Query empresa: {tiempo_query_empresa:.2f}s")
        print(f"   • Generación de vector: {tiempo_vector:.2f}s")
        print(f"   • Búsqueda en BD: {tiempo_busqueda:.2f}s")
        print(f"   • TOTAL: {tiempo_total:.2f}s")
        
        return resultados
        
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

buscar_soluciones("inteligencia artificial industrial", 1052)