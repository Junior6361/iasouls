import sqlite3, datetime

con = sqlite3.connect("bot.db", check_same_thread=False)
con.execute("""CREATE TABLE IF NOT EXISTS servidores(
    guild_id INTEGER PRIMARY KEY, system_prompt TEXT, canais TEXT DEFAULT '')""")
con.execute("""CREATE TABLE IF NOT EXISTS uso(
    guild_id INTEGER, user_id INTEGER, dia TEXT, qtd INTEGER,
    PRIMARY KEY(guild_id, user_id, dia))""")

def get_config(guild_id):
    r = con.execute("SELECT system_prompt, canais FROM servidores WHERE guild_id=?", (guild_id,)).fetchone()
    return (r[0], [int(c) for c in (r[1] or "").split(",") if c]) if r else (None, [])

def set_prompt(guild_id, prompt):
    con.execute("""INSERT INTO servidores(guild_id, system_prompt) VALUES(?,?)
                   ON CONFLICT(guild_id) DO UPDATE SET system_prompt=excluded.system_prompt""", (guild_id, prompt))
    con.commit()

def set_canais(guild_id, canais):
    con.execute("""INSERT INTO servidores(guild_id, canais) VALUES(?,?)
                   ON CONFLICT(guild_id) DO UPDATE SET canais=excluded.canais""",
                (guild_id, ",".join(map(str, canais))))
    con.commit()

def pode_usar(guild_id, user_id, limite):
    if limite <= 0:
        return True
    dia = datetime.date.today().isoformat()
    r = con.execute("SELECT qtd FROM uso WHERE guild_id=? AND user_id=? AND dia=?",
                    (guild_id, user_id, dia)).fetchone()
    return not (r and r[0] >= limite)

def registrar_uso(guild_id, user_id):
    dia = datetime.date.today().isoformat()
    con.execute("""INSERT INTO uso VALUES(?,?,?,1)
                   ON CONFLICT(guild_id,user_id,dia) DO UPDATE SET qtd=qtd+1""",
                (guild_id, user_id, dia))
    con.commit()
