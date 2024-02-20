#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static

# install nginx
sudo apt-get update
sudo apt-get install nginx -y

# create necessary folders
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

webpage='<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>'
echo "$webpage" > /data/web_static/releases/test/index.html

symlink="/data/web_static/current"

if [ -L "$symlink" ]; then
  rm "$symlink"
fi
ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -hR "ubuntu:ubuntu" /data

# handle hbnb_static
hbnb_static="\n\
        location /hbnb_static {\n\
                alias /data/web_static/current/;\n\
        }"
config="/etc/nginx/sites-available/default"
sudo sed -i "/server_name _;/a\ $hbnb_static" "$config"

#restart nginx
sudo service nginx restart
