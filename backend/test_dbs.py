import psycopg2

print("=== CHECKING LOCAL POSTGRES ===")
try:
    conn = psycopg2.connect('postgresql://postgres:root@localhost:5432/queuehub')
    cur = conn.cursor()
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    tables = [r[0] for r in cur.fetchall()]
    print("Local tables:", tables)
    if 'users' in tables:
        cur.execute("SELECT count(*) FROM users")
        print("Local users count:", cur.fetchone()[0])
        cur.execute("SELECT email, role FROM users LIMIT 5")
        print("Sample users:", cur.fetchall())
    conn.close()
except Exception as e:
    print("Local error:", e)

print("\n=== CHECKING NEON POSTGRES ===")
try:
    url_direct = 'postgresql://neondb_owner:npg_6Ph2NuqUOLTR@ep-small-block-azceh5aa-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
    conn = psycopg2.connect(url_direct)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM users")
    print("Neon users count:", cur.fetchone()[0])
    conn.close()
except Exception as e:
    print("Neon error:", e)
