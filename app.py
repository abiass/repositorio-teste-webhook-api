from flask import Flask, request, jsonify
import sqlite3
import json
import datetime
import os

DB_PATH = os.environ.get('DB_PATH', 'messages.db')

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            mtype TEXT,
            body TEXT,
            raw_json TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_message(sender, mtype, body, raw):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO messages (sender, mtype, body, raw_json, created_at) VALUES (?, ?, ?, ?, ?)',
        (
            sender,
            mtype,
            body,
            json.dumps(raw, ensure_ascii=False) if raw is not None else None,
            datetime.datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


@app.route('/webhook', methods=['POST'])
def webhook():
    if not request.is_json:
        return jsonify(error="Invalid payload"), 400

    data = request.get_json()
    print("Webhook recebido:", data)

    try:
        if data.get("object") == "whatsapp_business_account":
            entries = data.get("entry", [])
            for entry in entries:
                changes = entry.get("changes", [])
                for change in changes:
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for msg in messages:
                        sender = msg.get("from")
                        mtype = msg.get("type")
                        body = None
                        if mtype == "text":
                            body = msg.get("text", {}).get("body")
                        elif mtype == "image":
                            body = "<image>"
                        print(f"Mensagem recebida de {sender}: type={mtype} body={body}")
                        try:
                            save_message(sender, mtype, body, msg)
                        except Exception as e:
                            print("Erro ao salvar mensagem:", e)
            return jsonify(status="ok"), 200
    except Exception as e:
        print("Erro ao processar payload:", e)

    return jsonify(status="ignored"), 200


@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        limit = int(request.args.get('limit', 20))
    except ValueError:
        limit = 20

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, sender, mtype, body, raw_json, created_at FROM messages ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()

    results = []
    for r in rows:
        raw = None
        try:
            raw = json.loads(r[4]) if r[4] else None
        except Exception:
            raw = r[4]
        results.append({
            'id': r[0],
            'sender': r[1],
            'type': r[2],
            'body': r[3],
            'raw': raw,
            'created_at': r[5],
        })

    return jsonify(results), 200


if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if not request.is_json:
        from flask import Flask, request, jsonify
        import sqlite3
        import json
        import datetime
        import os

        DB_PATH = os.environ.get('DB_PATH', 'messages.db')

        app = Flask(__name__)


        def init_db():
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT,
                    mtype TEXT,
                    body TEXT,
                    raw_json TEXT,
                    created_at TEXT
                )
            ''')
            conn.commit()
            conn.close()


        def save_message(sender, mtype, body, raw):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                'INSERT INTO messages (sender, mtype, body, raw_json, created_at) VALUES (?, ?, ?, ?, ?)',
                (
                    sender,
                    mtype,
                    body,
                    json.dumps(raw, ensure_ascii=False) if raw is not None else None,
                    datetime.datetime.utcnow().isoformat(),
                ),
            )
            conn.commit()
            conn.close()


        @app.route('/webhook', methods=['POST'])
        def webhook():
            if not request.is_json:
                return jsonify(error="Invalid payload"), 400

            data = request.get_json()
            print("Webhook recebido:", data)

            # Tenta reconhecer o formato da WhatsApp Cloud API e persiste mensagens
            try:
                if data.get("object") == "whatsapp_business_account":
                    entries = data.get("entry", [])
                    for entry in entries:
                        changes = entry.get("changes", [])
                        for change in changes:
                            value = change.get("value", {})
                            messages = value.get("messages", [])
                            contacts = value.get("contacts", [])
                            for msg in messages:
                                sender = msg.get("from")
                                mtype = msg.get("type")
                                body = None
                                if mtype == "text":
                                    body = msg.get("text", {}).get("body")
                                elif mtype == "image":
                                    body = "<image>"
                                print(f"Mensagem recebida de {sender}: type={mtype} body={body}")
                                try:
                                    save_message(sender, mtype, body, msg)
                                except Exception as e:
                                    print("Erro ao salvar mensagem:", e)
                    return jsonify(status="ok"), 200
            except Exception as e:
                print("Erro ao processar payload:", e)

            # Caso não seja o formato esperado, apenas retorna 200
            return jsonify(status="ignored"), 200


        @app.route('/messages', methods=['GET'])
        def get_messages():
            # Retorna mensagens mais recentes; use ?limit=50 para ajustar
            try:
                limit = int(request.args.get('limit', 20))
            except ValueError:
                limit = 20

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT id, sender, mtype, body, raw_json, created_at FROM messages ORDER BY id DESC LIMIT ?', (limit,))
            rows = c.fetchall()
            conn.close()

            results = []
            for r in rows:
                raw = None
                try:
                    raw = json.loads(r[4]) if r[4] else None
                except Exception:
                    raw = r[4]
                results.append({
                    'id': r[0],
                    'sender': r[1],
                    'type': r[2],
                    'body': r[3],
                    'raw': raw,
                    'created_at': r[5],
                })

            return jsonify(results), 200


        if __name__ == '__main__':
            init_db()
            app.run(port=5000, debug=True)