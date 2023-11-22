# SisOperFinal
## 1. Instalar y configurar Nginx
Nos damos permisos de Super Usuario:

```
sudo -s
```

Actualizamos los paquetes del sistema:

```
sudo apt update
```

Instalamos Nginx:

```
sudo apt install nginx
```

Tenemos que comprobar que el Nginx este corriendo, tanto en el LocalHost como en la IP.

## 2. Instalar y configurar Apache, en otra maquina vitual
Instalamos Apache:

```
sudo apt install apache2
```

Nos metemos al LocalHost y verificamos que se este corriendo el apache y en la ip 
 


## 3. Instalacion y configuracion del Docker Compose
Instalamos Docker-compose

```
sudo apt install docker-ce docker-compose -y
```

Comprobamos que Docker este corriendo en la maquina:

```
systemclt status docker
```

Iniciamos el Docker-compose:

```
docker-compose up -d
```

Y verificamos el estado del Docker-compose (Debera estar en state Up)

```
docker-compose ps
```

Aqui verificamos que esta funcionando en el LocalHost y en el puerto 8000 y en la Ip en el mismo puerto

## 4. Configurar el reverse proxy

Configuramos el Nginx en la primera maquina virtual para que funcione como reverse proxy

```
sudo nano /etc/nginx/sites-aviable/default
```

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

## 5. Configurar 4ta maquina virtual

Instalamos SSH con:

```
sudo apt install ssh
```

Instalamos PDSH:

```
sudo apt install pdsh
```

Con nano abrimos el archivo de Bashrc:

```
sudo nano .bashrc
```

Una vez en nano, agregamos la siguiente linea de comandos al final del archivo

```
expo PDSH_RCMD_TYPE=ssh
```

Generamos una clave ssh:

```
ssh-keygen - t rsa - P ""
```

Clonamos la clave en las claves autorizadas (authorized_keys):

```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/autorized_keys
```

Instalamos JAVA 8:

```
sudo apt install openjdk-8-jdk
```

Instalamods Hadoop:

```
sudo wget -P ~ https://mirrors.sonic.net/apache/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz
```

Descomprimimos el archivo.

```
tar xzf hadoop-3.2.1.tar.gz
```

Configuramos el hadoop para el path de Java en el entorno virtual de Hadoop:

```
sudo nano ~/hadoop/etc/hadoop/hadoop-env.sh
```

Luego cambiamos la linea que empiece con JAVA_HOME:

```
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

Movemos el directorio hadoop a nuestro archivo local de usuario:

```
sudo mv hadoop /usr/local/hadoop
```

Configuraramos la ruta de hadoop


```
sudo nano /etc/environment
```

Y reemplazamos la linea PATH con:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/hadoop/bin:/usr/local/hadoop/sbin"
JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/jre"
```

Crear un usuario específico para Hadoop;

```
sudo adduser h-user
```

Ahora debe otorgar permisos a este usuario para trabajar dentro de la carpeta de hadoop:

```
sudo usermod -aG hadoopuser h-user
sudo chown h-user:root -R /usr/local/hadoop/
sudo chmod g+rwx -R /usr/local/hadoop/
sudo adduser h-user sudo
```

Clonar la máquina principal para crear dos máquinas secundarias y cambiamps el hostname.

```
sudo nano /etc/hosts
```

En cada maquina clonada, si es principal escribimos `h-primary` y para las otras `h-secundary1` y `h-secundary2`.
Identificamos cada IP con:

```
ip addr
```

Ahora cambiamos el archivo de host en todas las maquinas

```
sudo nano /etc/hosts
```

Y agregue la identificación de otra máquina, con IP - `h-primary`,  `h-secundary1` o `h-secundary2`.

Cambiamos de usuario:

```
su - h-user
```

Ahora necesitas generar una clave ssh para este usuario:

```
ssh-keygen -t rsa -P ""
```

Clonamos la clave en las claves autorizadas (authorized_keys):

```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

Ahora probamos la conexión ssh de las maquinas:

```
ssh h-user@h-primary
ssh h-user@h-secundary1
ssh h-user@h-secundary2
```

Ahora tenemos que configurar hadoop para que funcione en un clúster. Para eso, necesitamos editar los siguientes archivos en la carpeta `/usr/local/hadoop/etc/hadoop/`:

```
sudo nano /usr/local/hadoop/etc/hadoop/core-site.xml
```

Y agregamos el siguiente codigo

```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://h-primary:9000</value>
    </property>
</configuration>
```

```
sudo nano /usr/local/hadoop/etc/hadoop/hdfs-site.xml
```

Y luego agregue a la configuración del archivo:

```
<property>
<name>dfs.namenode.name.dir</name><value>/usr/local/hadoop/data/nameNode</value>
</property>
<property>
<name>dfs.datanode.data.dir</name><value>/usr/local/hadoop/data/dataNode</value>
</property>
<property>
<name>dfs.replication</name>
<value>2</value>
</property>
```

Agregue las máquinas secundarias al archivo de trabajadores: (solo en la primaria)

```
sudo nano /usr/local/hadoop/etc/hadoop/workers
```

Y agregamos las maquinas secundarias

```
h-secundary1
h-secundary2
```

Copie configuraciones en máquinas secundarias:

```
scp /usr/local/hadoop/etc/hadoop/* 
h-secondary1:/usr/local/hadoop/etc/hadoop/
scp /usr/local/hadoop/etc/hadoop/* 
h-secondary2:/usr/local/hadoop/etc/hadoop/
```

Formateo e inicio del sistema HDFS (solo primario)

```
source /etc/environment
```

Luego formatee el sistema hdfs con:

```
hdfs namenode -format
```

Asegúrese de que su archivo .bashrc esté configurado:

```
sudo nano .bashrc
```

Y verifique si al final del archivo tiene la siguiente ruta:

```
export PDSH_RCMD_TYPE=ssh
```

Actualiza los cambios:

```
source ~/.bashrc
```

Cuando finalicen estas operaciones, inicie el servicio:

```
start-dfs.sh
```

Para comprobar si todas las máquinas están utilizando los recursos correctos, utilice:

```
jps
```

Para configurar el hilo, debe comenzar a exportar todas las rutas: (en la primaria)

```
export HADOOP_HOME="/usr/local/hadoop"
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
```

Ahora simplemente cambia la configuración del hilo en ambos secundarios:

```
sudo nano /usr/local/hadoop/etc/hadoop/yarn-site.xml
```

Y luego agregue las siguientes configuraciones:

```
<property>
<name>yarn.resourcemanager.hostname</name>
<value>h-primary</value>
</property>
```

Para iniciar el uso del servicio Yarn:

```
start-yarn.sh
```

Para tener acceso a la herramienta de administración de Yarn, use su navegador para acceder a la IP principal en el puerto 8088