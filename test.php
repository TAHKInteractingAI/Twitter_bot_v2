server {
listen 80;
server_name 3.107.4.24; # Thay thế bằng địa chỉ IP công khai của EC2 Instance hoặc tên miền của bạn

access_log /var/log/nginx/reverse_proxy.access.log;
error_log /var/log/nginx/reverse_proxy.error.log;

location /myweb/ {
proxy_pass http://54.252.184.182/; # Chuyển tiếp yêu cầu tới backend
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

# Xử lý các trường hợp redirect
proxy_redirect http://54.252.184.182/ /myweb/;
}

location = /favicon.ico { log_not_found off; access_log off; }
location = /robots.txt { log_not_found off; access_log off; }

# Deny access to hidden files
location ~ /\.ht {
deny all;
}
}

cd /var/www/html
sudo nano wp-config.php

define('WP_HOME', 'http://3.107.4.24');
define('WP_SITEURL', 'http://3.107.4.24');




server {
listen 80;
server_name 3.107.4.24;

access_log /var/log/nginx/reverse_proxy.access.log;
error_log /var/log/nginx/reverse_proxy.error.log;

location /myweb/ {
proxy_pass http://54.252.184.182/;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
}

location /myweb/wp-admin/ {
proxy_pass http://54.252.184.182/wp-admin/;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
}

location /myweb/shop/ {
proxy_pass http://54.252.184.182/shop/;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
}

# Cấu hình bảo vệ an ninh
location ~ /\.ht {
deny all;
}

location = /favicon.ico { log_not_found off; access_log off; }
location = /robots.txt { log_not_found off; access_log off; }
}



erver {
listen 80;
server_name 3.107.4.24;

location /myweb/ {
proxy_pass http://54.252.184.182/ ;
}

location /myweb/shop/ {
proxy_pass http://54.252.184.182/shop/ ;
}

location /myweb/cart/ {
proxy_pass http://54.252.184.182/cart/ ;
}

location /myweb/wp-admin/ {
proxy_pass http://54.252.184.182/wp-admin/ ;
}
}


sudo apt update
sudo apt install mysql-server


sudo mysql_secure_installation


sudo mysql -u root -p
mysql> CREATE DATABASE test CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
mysql> CREATE USER thanh IDENTIFIED BY 'Thanh12345@';
mysql> GRANT ALL PRIVILEGES ON test.* TO 'thanh';
mysql> FLUSH PRIVILEGES;
mysql> EXIT;


sudo apt install php-curl php-gd php-mbstring php-xml php-xmlrpc php-soap php-intl php-zip
sudo apt-get install php8.3 php8.3-fpm


wget https://wordpress.org/latest.tar.gz
tar -xzvf latest.tar.gz
sudo mv wordpress/* .
sudo rm -rf wordpress


sudo apt update
sudo apt install nginx

sudo systemctl enable nginx

sudo nano /etc/nginx/sites-available/wordpress

sudo ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/

sudo nginx -t

sudo systemctl restart nginx

sudo apt update
sudo apt install git

cd /var/www/html
git init
git remote add origin https://github.com/Rangdog/WP-and-WOO2.git
git add .
git push -u origin main

sudo apt update
sudo apt install nginx

sudo nano /etc/nginx/sites-available/reverse_proxy.conf


server {
listen 80;
server_name 3.107.4.24;

location /myweb/ {
proxy_pass http://54.252.184.182/ ;
}
}

sudo ln -s /etc/nginx/sites-available/reverse_proxy.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx