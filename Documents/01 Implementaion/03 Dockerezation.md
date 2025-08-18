## 1. Check Docker Version  
```bash
$ docker --version
Docker version 28.3.2, build 578ccf6
```  

## 2. MYSQL initialazation  
```bash
docker run --name HEC-RAS_FLOOD -e MYSQL_ROOT_PASSWORD=hecras -e MYSQL_DATABASE=flood_data -p 3307:3306 -d mysql:8.0
```  

## 3. Check running process  
```bash
$ docker ps
CONTAINER ID   IMAGE       COMMAND                  CREATED          STATUS          PORTS                                         NAMES
8d8fc26b557c   mysql:8.0   "docker-entrypoint.s…"   18 seconds ago   Up 16 seconds   0.0.0.0:3307->3306/tcp, [::]:3307->3306/tcp   HEC-RAS_FLOOD
```  

## 4. Access the MySQL shell inside the container  
```bash
docker exec -it HEC-RAS_FLOOD mysql -uroot -p
```  
#### Output:  
```console
$ docker exec -it HEC-RAS_FLOOD mysql -uroot -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.43 MySQL Community Server - GPL

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its  
affiliates. Other names may be trademarks of their respective      
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```  

## 5. Create a dedicated user and grant privileges to the flood_data database  
#### Output:  
```console
mysql> CREATE USER 'ganesh'@'%' IDENTIFIED BY 'hecras';
RANT ALL PRIVILEGES ON flood_data.* TO 'ganesh'@'%';
FLUSH PRIVILEGES;
EXIT;Query OK, 0 rows affected (0.18 sec)

mysql> GRANT ALL PRIVILEGES ON flood_data.* TO 'ganesh'@'%';
Query OK, 0 rows affected (0.01 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)

```  
Connection String  
```txt
DATABASE_URI="mysql+pymysql://ganesh:hecras@localhost:3307/flood_data"
```  
App\backend-flask-app\.env
```env
# Backend/.env
FLASK_APP=app.py
FLASK_ENV=development
# Add a placeholder for your database URI, we'll configure this properly later
DATABASE_URI="mysql+pymysql://ganesh:hecras@localhost:3307/flood_data"
# For production, you'd add a secret key too:
# SECRET_KEY="your_super_secret_key_here"
```  
## 6. Create table  
```bash
USE flood_data;
```  
```bash
CREATE TABLE alert_thresholds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    parameter VARCHAR(100) NOT NULL,
    threshold_value DECIMAL(10, 2) NOT NULL,
    threshold_unit VARCHAR(50),
    threshold_type ENUM('above', 'below') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```  
verify  
#### Output:  
```console
mysql> show tables;
+----------------------+
| Tables_in_flood_data |
+----------------------+
| alert_thresholds     |
+----------------------+
1 row in set (0.01 sec)
```  
#### Output:  
```console
mysql> DESCRIBE alert_thresholds;
+-----------------+-----------------------+------+-----+-------------------+-----------------------------------------------+
| Field           | Type                  | Null | Key | Default           | Extra                                         |
+-----------------+-----------------------+------+-----+-------------------+-----------------------------------------------+
| id              | int                   | NO   | PRI | NULL              | auto_increment                                |
| location_name   | varchar(255)          | NO   |     | NULL              |                                               |
| parameter       | varchar(100)          | NO   |     | NULL              |                                               |
| threshold_value | decimal(10,2)         | NO   |     | NULL              |                                               |
| threshold_unit  | varchar(50)           | YES  |     | NULL              |                                               |
| threshold_type  | enum('above','below') | NO   |     | NULL              |                                               |
| is_active       | tinyint(1)            | YES  |     | 1         
        |                                               |
| created_at      | timestamp             | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
| updated_at      | timestamp             | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
+-----------------+-----------------------+------+-----+-------------------+-----------------------------------------------+
9 rows in set (0.01 sec)
```   
```bash
EXIT;
```  