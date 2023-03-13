Перенос данных из SQLite в PosqreSQL

Для запуска проекта необходимо:
1. В в папке sqlite_to_postgres создать файл .env
2. Заполнить созданный файл со следующиеми параметрами PosqreSQL:
DATABASE=name_database/n
DB_USER=user_database
DB_PASSWORD=password_database
HOST=host_database
PORT=port_database

Запустить файл load_data.py командой 
python load_data.py

Результаты выполнения скрипта:
- После применения скрипта все фильмы, персоны и жанры появляются в PostgreSQL.  
- Все связи между записями сохранены. 
- Данные загружаются пачками по n записей.
