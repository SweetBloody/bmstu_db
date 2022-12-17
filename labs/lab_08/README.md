В папке nifi_img лежат примеры создания структуры NiFi.

Чтобы настроить драйвер для подключения к базе данных:
- положить файл postgresql-42.5.1.jar в папку ./lab/nifi/database_repository
- в настройках NiFi контроллера DBCPConnectionPool в поле Database Driver Location указать /opt/nifi/nifi-current/database_repository/postgresql-42.5.1.jar