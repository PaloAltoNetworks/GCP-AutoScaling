#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
#temp=$(curl "http://metadata.google.internal/computeMetadata/v1/instance/zone" -H "Metadata-Flavor: Google")
#zone=$(basename $temp)
#apt-get update
#apt-get install -y apache2 
#ln -sf /etc/apache2/conf-available/serve-cgi-bin.conf /etc/apache2/conf-enabled/serve-cgi-bin.conf
#ln -sf /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load
#sudo mkdir -p /var/www/html/app1
#sudo cp /var/www/html/index.html /var/www/html/app1/index.html
#sudo sed  -i -e 's/Apache2 Debian Default Page/Apache2 APP1 Default Page/g' /var/www/html/app1/index.html
#sudo mkdir -p /var/www/html/app2
#sudo cp /var/www/html/index.html /var/www/html/app2/index.html
#sudo sed  -i -e 's/Apache2 Debian Default Page/Apache2 APP2 Default Page/g' /var/www/html/app2/index.html
#systemctl restart apache2

sudo echo '<html><head><title>Go PaloAlto Networks - GCP Autoscaling works!</title></head><body>Welcome to PaloAlto Networks</body></html>' > index.html

sudo python -m SimpleHTTPServer 80 &
