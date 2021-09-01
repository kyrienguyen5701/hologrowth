server {
    listen 80;
    server_name tools.kekstudio.com;
    include /etc/nginx/mime.types;

    location / {
        # if ($request_method = 'OPTIONS') {
        #     add_header 'Access-Control-Allow-Origin' 'http://localhost:8080';
        #     add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        #     add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
        #     add_header 'Access-Control-Max-Age' 1728000;
        #     add_header 'Content-Type' 'text/plain; charset=utf-8';
        #     add_header 'Content-Length' 0;
        #     return 204;
        # }
        # if ($request_method = 'POST') {
        #     #add_header 'Access-Control-Allow-Origin' 'http://localhost:8080' always;
        #     add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        #     add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        #     add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;
        # }
        # if ($request_method = 'GET') {
        #     #add_header 'Access-Control-Allow-Origin' 'http://localhost:8080' always;
        #     add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        #     add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        #     add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;
        # }
        # Simple requests
        if ($request_method ~* "(GET|POST)") {
            add_header "Access-Control-Allow-Origin"  'http://localhost:8080';
        }

        # Preflighted requests
        if ($request_method = OPTIONS ) {
            add_header "Access-Control-Allow-Origin"  'http://localhost:8080';
            add_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS, HEAD";
            add_header "Access-Control-Allow-Headers" "Authorization, Origin, X-Requested-With, Content-Type, Accept";
            return 200;
        }
        proxy_intercept_errors on;
        proxy_pass http://127.0.0.1:8000;
        proxy_hide_header 'Access-Control-Allow-Origin';
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

server {
    listen 443 ssl;
    server_name tools.kekstudio.com;
    ssl_certificate /etc/letsencrypt/live/tools.kekstudio.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/tools.kekstudio.com/privkey.pem; # managed by Certbot


    location / {
        # if ($request_method = 'OPTIONS') {
        #     add_header 'Access-Control-Allow-Origin' 'http://localhost:8080';
        #     add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        #     add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
        #     add_header 'Access-Control-Max-Age' 1728000;
        #     add_header 'Content-Type' 'text/plain; charset=utf-8';
        #     add_header 'Content-Length' 0;
        #     return 204;
        # }
        # if ($request_method = 'POST') {
        #     add_header 'Access-Control-Allow-Origin' 'http://localhost:8080' always;
        #     add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        #     add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        #     add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;
        # }
        # if ($request_method = 'GET') {
        #     add_header 'Access-Control-Allow-Origin' 'http://localhost:8080' always;
        #     add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        #     add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        #     add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;
        # }
        # Simple requests
        if ($request_method ~* "(GET|POST)") {
            add_header "Access-Control-Allow-Origin"  'kyrienguyen5701.github.io/#/hologrowth';
        }

        # Preflighted requests
        if ($request_method = OPTIONS ) {
            add_header "Access-Control-Allow-Origin"  'kyrienguyen5701.github.io/#/hologrowth';
            add_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS, HEAD";
            add_header "Access-Control-Allow-Headers" "Authorization, Origin, X-Requested-With, Content-Type, Accept";
            return 200;
        }
        proxy_intercept_errors on;
        proxy_pass http://127.0.0.1:8000;
        # proxy_http_version 1.1;
        proxy_hide_header 'Access-Control-Allow-Origin';        
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Server $host;
        try_files $uri $uri/ =404;
    }
}
