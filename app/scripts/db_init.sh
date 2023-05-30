DB_PASS='admin123'
DIR='C:\Users\jtbec\Documents\code\python\prestonV_api\app\scripts'

"C:\Program Files\PostgreSQL\15\bin\psql.exe" -v user_passwd="${DB_PASS}" -U postgres -d postgres james_preston -f "${DIR}\db_create.sql"
