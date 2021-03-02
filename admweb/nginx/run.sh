envsubst < /etc/nginx/conf.d/upstream.template.conf > /etc/nginx/conf.d/upstream.conf 
echo "*** BEGIN CONFIGS ***"
cat /etc/nginx/nginx.conf
cat /etc/nginx/conf.d/upstream.conf
cat /etc/nginx/conf.d/server.conf
echo "*** END CONFIGS ***"
nginx;

