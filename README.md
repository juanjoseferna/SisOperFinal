# SisOperFinal
## 1. Instalar y configurar Nginx
Nos damos permisos de Super Usuario:
`sudo -s`
Actualizamos los paquetes del sistema:
`sudo apt update`
Instalamos Nginx:
`sudo apt install nginx`
Tenemos que comprobar que el Nginx este corriendo, tanto en el LocalHost como en la IP.

## 2. Instalar y configurar Apache, en otra maquina vitual
Instalamos Apache:
`sudo apt install apache2`
Nos metemos al LocalHost y verificamos que se este corriendo el apache y en la ip 
 


## 3. Instalacion y configuracion del Docker Compose
Instalamos Docker-compose
`sudo apt install docker-ce docker-compose -y`
Comprobamos que Docker este corriendo en la maquina:
`systemclt status docker`
Iniciamos el Docker-compose:
`docker-compose up -d`
Y verificamos el estado del Docker-compose (Debera estar en state Up)
`docker-compose ps`
Aqui verificamos que esta funcionando en el LocalHost y en el puerto 8000 y en la Ip en el mismo puerto

## 4. Configurar el reverse proxy

Configuramos el Nginx en la primera maquina virtual para que funcione como reverse proxy

`sudo nano /etc/nginx/sites-aviable/default`

Luego con nano editamos el archivo default
```cpp
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name _;

    location / {
        try_files $uri $uri/ = 404;
    }
    location / apache {
        proxy_pass http://10.80.5.117/;
        proxy_set_header host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    location / compose {
        proxy_pass http://10.80.5.179:8000/;
        proxy_set_header host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

```
Luego de hacer esto ya queda todo configurado y se puede acceder desde la maquina física a cualquiera de estos.