import subprocess

# Diccionario de rutas a programas
comandos = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vscode": r"C:\Users\TU_USUARIO\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "workbench": r"C:\Program Files\MySQL\MySQL Workbench 8.0 CE\MySQLWorkbench.exe",
    "wsp": "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
}

def ejecutar_programa(nombre: str) -> str:
    ruta = comandos.get(nombre)
    if not ruta:
        return "Programa no encontrado"
    try:
        if ruta.endswith("!App"):
            # Aplicación UWP
            subprocess.Popen(['explorer.exe', f"shell:appsFolder\\{ruta}"])
        else:
            # Aplicación tradicional
            subprocess.Popen(['cmd', '/c', 'start', '', ruta])
        return f"{nombre} abierto"
    except Exception as e:
        return f"Error al abrir {nombre}: {e}"
