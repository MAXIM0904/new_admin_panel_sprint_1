<h2>Перенос данных из SQLite в PosqreSQL</h2>

<h3>Для запуска проекта необходимо:</h3>
1. В в папке sqlite_to_postgres создать файл .env
2. Заполнить созданный файл со следующиеми параметрами PosqreSQL:

<p>DATABASE=name_database</p>
<p>DB_USER=user_database</p>
<p>DB_PASSWORD=password_database</p>
<p>HOST=host_database</p>
<p>PORT=port_database</p>

3.Запустить файл load_data.py командой 
<p>python load_data.py</p>

<h3>Результаты выполнения скрипта:</h3>
<p>После применения скрипта все фильмы, персоны и жанры появляются в PostgreSQL.</p>
<p>Все связи между записями сохранены.</p>
<p>Данные загружаются пачками по n записей.</p>
