import sqlite3

DB_PATH = "app/database/controlDB.db"

def listar_apps():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, route, status FROM app")
    apps = cursor.fetchall()
    conn.close()
    return apps

def listar_apps_activas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, route, status FROM app WHERE status = 1")
    rows = cursor.fetchall()
    conn.close()
    apps = [{"id": r[0], "name": r[1], "route": r[2], "status": r[3]} for r in rows]
    print(apps)
    return apps

def obtener_app(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, route, status FROM app WHERE id = ?", (id,))
    app = cursor.fetchone()
    conn.close()
    return app

def agregar_app(name: str, route: str, status: int = 1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO app (name, route, status) VALUES (?, ?, ?)", (name, route, status))
    conn.commit()
    conn.close()

def actualizar_app(id: int, name: str, route: str, status: int = 1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE app SET name = ?, route = ?, status = ? WHERE id = ?", (name, route, status, id))
    conn.commit()
    conn.close()

def eliminar_app(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM app WHERE id = ?", (id,))
    conn.commit()
    conn.close()
