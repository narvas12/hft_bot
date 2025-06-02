[Unit]
Description=Gunicorn socket

[Socket]
ListenStream=8000
ListenStream=[::]:8000

[Install]
WantedBy=sockets.target



[Unit]
Description=Gunicorn service for DCA bot FastAPI app
Requires=gunicorn-dcabot.socket
After=network.target

[Service]
User=caliban
Group=www-data
WorkingDirectory=/home/caliban/hft_bot
ExecStart=/home/caliban/hft_bot/.venv/bin/gunicorn bot.dca_bot.create_dca_bot:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind unix:/run/gunicorn-dcabot.sock

# Gunicorn will inherit the socket from systemd, so no need for StandardInput here
# StandardInput=socket  <-- you can remove this line or comment it out

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target





server {
    listen 80;
    server_name api.ezechukwuemmanuel.com;

    location / {
        proxy_pass http://unix:/run/gunicorn-dcabot.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
