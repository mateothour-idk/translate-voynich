# auditar.py
import sys

try:
    import voynichdata
    print("¡ÉXITO PERFECTO! El archivo 'voynichdata.py' NO tiene errores de sintaxis y se puede importar.")
except SyntaxError as e:
    print(f"❌ ERROR DE SINTAXIS DETECTADO en la línea {e.lineno}:")
    print(f"Código con error: {e.text.strip() if e.text else 'No disponible'}")
    print(f"Detalle: {e.msg}")
except Exception as e:
    print(f"⚠️ Ocurrió otro tipo de error al importar: {e}")
