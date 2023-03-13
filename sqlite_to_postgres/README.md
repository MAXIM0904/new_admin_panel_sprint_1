Перенос данных из SQLite в PosqreSQL

Для запуска проекта необходимо:
1. В в папке sqlite_to_postgres создать файл .env
2. Заполнить созданный файл со следующиеми параметрами PosqreSQL:
<p>DATABASE=name_database</p>
<p>DB_USER=user_database</p>
<p>DB_PASSWORD=password_database</p>
<p>HOST=host_database</p>
<p>PORT=port_database</p>

Запустить файл load_data.py командой 
<p>python load_data.py</p>

Результаты выполнения скрипта:
- После применения скрипта все фильмы, персоны и жанры появляются в PostgreSQL.  
- Все связи между записями сохранены. 
- Данные загружаются пачками по n записей.
