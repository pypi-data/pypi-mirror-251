CREATE OR REPLACE FUNCTION process_audit() RETURNS trigger AS $audit_trigger$
    DECLARE
        changes HSTORE;
        old_data HSTORE;
        operation_code INTEGER;
        changed_values_len INTEGER;
        user_id TEXT;
    BEGIN
        operation_code := 0;
        user_id := current_setting('libaudit.user_id', true);
        IF user_id IS NULL THEN
            user_id := 0;
        END IF;
        changes := NULL;
        old_data := NULL;

        IF (TG_OP = 'INSERT') THEN
            changes := HSTORE(NEW);
            operation_code := 1;
        ELSIF (TG_OP = 'UPDATE') THEN
            old_data := HSTORE(OLD);
            changes := HSTORE(NEW) - old_data;
            changed_values_len := array_length(akeys(changes),1);
            IF changed_values_len IS NOT NULL OR changed_values_len = 0 THEN
                operation_code := 2;
            END IF;
        ELSIF (TG_OP = 'DELETE') THEN
            old_data := HSTORE(OLD);
            operation_code := 3;
        END IF;

        IF operation_code != 0 THEN
            RAISE LOG '[AUDIT_LOG] % %.% % old data: (%), changes: (%).', TG_OP, TG_TABLE_SCHEMA, TG_TABLE_NAME, user_id, hstore_to_json(old_data), hstore_to_json(changes);
        END IF;
        RETURN NULL;
    END;
$audit_trigger$ LANGUAGE plpgsql;


-- Применение триггеров к таблицам
CREATE OR REPLACE FUNCTION apply_triggers() RETURNS void AS $body$
DECLARE
    target_table RECORD;
BEGIN
    FOR target_table IN
        SELECT table_name, table_schema
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    LOOP
        EXECUTE
           'DROP TRIGGER IF EXISTS audit_trigger ON ' ||
           target_table.table_schema || '.' || target_table.table_name;
        EXECUTE
            'CREATE TRIGGER audit_trigger AFTER INSERT OR UPDATE OR DELETE ON ' ||
            target_table.table_schema || '.' ||
            target_table.table_name || ' ' ||
            'FOR EACH ROW EXECUTE PROCEDURE process_audit()';
    END LOOP;
END
$body$
LANGUAGE plpgsql;

SELECT apply_triggers();
