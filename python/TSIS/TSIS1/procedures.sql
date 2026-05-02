-- Добавить телефон к контакту по имени
CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name ILIKE p_name LIMIT 1;
    IF v_id IS NULL THEN
        RAISE NOTICE 'Контакт "%" не найден', p_name;
        RETURN;
    END IF;
    INSERT INTO phones(contact_id, phone, type) VALUES (v_id, p_phone, p_type);
END;
$$;

-- Переместить контакт в группу (создать группу если нет)
CREATE OR REPLACE PROCEDURE move_to_group(p_name VARCHAR, p_group VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_gid INTEGER;
BEGIN
    INSERT INTO groups(name) VALUES (p_group) ON CONFLICT(name) DO NOTHING;
    SELECT id INTO v_gid FROM groups WHERE name = p_group;
    UPDATE contacts SET group_id = v_gid WHERE name ILIKE p_name;
END;
$$;

-- Поиск по имени, email и всем телефонам
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, birthday DATE, grp VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name    ILIKE '%' || p_query || '%'
       OR c.email   ILIKE '%' || p_query || '%'
       OR p.phone   ILIKE '%' || p_query || '%';
END;
$$;

-- Постраничный вывод (из упражнения 8)
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, birthday DATE, grp VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    ORDER BY c.name
    LIMIT p_limit OFFSET p_offset;
END;
$$;
