import csv, json
from connect import get_conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    for fname in ("schema.sql", "procedures.sql"):
        with open(fname) as f:
            cur.execute(f.read())
    conn.commit(); cur.close(); conn.close()
    print("БД инициализирована.")


def add_contact(name, email=None, birthday=None, group=None):
    conn = get_conn(); cur = conn.cursor()
    gid = None
    if group:
        cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT(name) DO NOTHING", (group,))
        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        gid = cur.fetchone()[0]
    cur.execute("INSERT INTO contacts(name,email,birthday,group_id) VALUES(%s,%s,%s,%s) RETURNING id",
                (name, email, birthday, gid))
    cid = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return cid

def add_phone_py(contact_id, phone, ptype="mobile"):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,%s)", (contact_id, phone, ptype))
    conn.commit(); cur.close(); conn.close()


def search(query):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows


def filter_by_group(group_name, sort_by="name"):
    allowed = {"name": "c.name", "birthday": "c.birthday", "date": "c.created"}
    order = allowed.get(sort_by, "c.name")
    conn = get_conn(); cur = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        WHERE g.name ILIKE %s
        ORDER BY {order}
    """, (group_name,))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows


def paginate(page_size=5):
    offset = 0
    while True:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_page(%s,%s)", (page_size, offset))
        rows = cur.fetchall(); cur.close(); conn.close()
        if not rows:
            print("Контакты закончились."); break
        print_contacts(rows)
        cmd = input("next/prev/quit: ").strip().lower()
        if cmd == "next":   offset += page_size
        elif cmd == "prev": offset = max(0, offset - page_size)
        else: break

def export_json(filename="contacts.json"):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email,
               c.birthday::text, g.name as grp
        FROM contacts c LEFT JOIN groups g ON g.id=c.group_id
    """)
    contacts = []
    for row in cur.fetchall():
        cid, name, email, bday, grp = row
        cur2 = conn.cursor()
        cur2.execute("SELECT phone,type FROM phones WHERE contact_id=%s", (cid,))
        phones = [{"phone": p, "type": t} for p, t in cur2.fetchall()]
        cur2.close()
        contacts.append({"name": name, "email": email, "birthday": bday,
                          "group": grp, "phones": phones})
    cur.close(); conn.close()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    print(f"Экспортировано {len(contacts)} контактов в {filename}")


def import_json(filename="contacts.json"):
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
    conn = get_conn(); cur = conn.cursor()
    for c in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (c["name"],))
        exists = cur.fetchone()
        if exists:
            ans = input(f'Дубликат "{c["name"]}". Перезаписать? (y/n): ')
            if ans.lower() != "y":
                continue
            cur.execute("DELETE FROM contacts WHERE id=%s", (exists[0],))
        cid = add_contact(c["name"], c.get("email"), c.get("birthday"), c.get("group"))
        for ph in c.get("phones", []):
            add_phone_py(cid, ph["phone"], ph.get("type", "mobile"))
    conn.commit(); cur.close(); conn.close()
    print("Импорт завершён.")


def import_csv(filename="contacts.csv"):
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = add_contact(row["name"], row.get("email") or None,
                              row.get("birthday") or None, row.get("group") or None)
            if row.get("phone"):
                add_phone_py(cid, row["phone"], row.get("type", "mobile"))
    print("CSV импортирован.")


def print_contacts(rows):
    if not rows:
        print("Ничего не найдено."); return
    print(f"{'ID':<4} {'Имя':<20} {'Email':<25} {'День рожд.':<12} {'Группа'}")
    print("-" * 70)
    for r in rows:
        print(f"{r[0]:<4} {str(r[1]):<20} {str(r[2] or ''):<25} {str(r[3] or ''):<12} {r[4] or ''}")

def menu():
    init_db()
    while True:
        print("""
=== Телефонная книга ===
1. Добавить контакт
2. Поиск (имя / email / телефон)
3. Фильтр по группе
4. Листать контакты (пагинация)
5. Добавить телефон к контакту
6. Переместить в группу
7. Импорт CSV
8. Экспорт JSON
9. Импорт JSON
0. Выход""")
        ch = input("Выбор: ").strip()

        if ch == "1":
            name = input("Имя: ")
            email = input("Email (Enter пропустить): ") or None
            bday = input("День рождения YYYY-MM-DD (Enter пропустить): ") or None
            group = input("Группа (Family/Work/Friend/Other): ") or None
            cid = add_contact(name, email, bday, group)
            phone = input("Телефон: ")
            ptype = input("Тип (home/work/mobile): ") or "mobile"
            add_phone_py(cid, phone, ptype)
            print("Добавлено!")

        elif ch == "2":
            q = input("Запрос: ")
            print_contacts(search(q))

        elif ch == "3":
            grp = input("Группа: ")
            sort = input("Сортировка (name/birthday/date): ") or "name"
            print_contacts(filter_by_group(grp, sort))

        elif ch == "4":
            paginate()

        elif ch == "5":
            name = input("Имя контакта: ")
            phone = input("Телефон: ")
            ptype = input("Тип (home/work/mobile): ") or "mobile"
            conn = get_conn(); cur = conn.cursor()
            cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
            conn.commit(); cur.close(); conn.close()
            print("Телефон добавлен.")

        elif ch == "6":
            name = input("Имя контакта: ")
            grp = input("Новая группа: ")
            conn = get_conn(); cur = conn.cursor()
            cur.execute("CALL move_to_group(%s,%s)", (name, grp))
            conn.commit(); cur.close(); conn.close()
            print("Перемещено.")

        elif ch == "7":
            fn = input("Файл CSV (contacts.csv): ") or "contacts.csv"
            import_csv(fn)

        elif ch == "8":
            fn = input("Файл JSON (contacts.json): ") or "contacts.json"
            export_json(fn)

        elif ch == "9":
            fn = input("Файл JSON (contacts.json): ") or "contacts.json"
            import_json(fn)

        elif ch == "0":
            break

if __name__ == "__main__":
    menu()
