#!/bin/bash
set -e

PROJECT_DIR="/home/www/BlogWebsite"

# Color
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
log()  { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

[ "$EUID" -ne 0 ] && { echo "Please run as root"; exit 1; }

# Server IP
echo -n "Enter server IP: "; read -r IP

echo "=== Deploying to $IP ==="

# 1. System deps
echo ">>> [1/6] System packages..."
apt-get update -qq && apt-get install -y -qq python3 python3-pip python3-venv nginx nodejs npm curl
npm config set registry https://registry.npmmirror.com
log "Done"

# 2. Directories
echo ">>> [2/6] Directories..."
mkdir -p /var/log/gunicorn "$PROJECT_DIR/media"
chown -R www-data:www-data /var/log/gunicorn
log "Done"

# 3. Python venv
echo ">>> [3/6] Python venv..."
cd "$PROJECT_DIR"
if [ -d venv ]; then warn "venv exists, skip"; else python3 -m venv venv; fi
. venv/bin/activate
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip -q
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt -q
deactivate
log "Done"

# 4. Frontend
echo ">>> [4/6] Frontend build..."
cd "$PROJECT_DIR/frontend"
npm install --silent && npm run build
log "Done"

# 5. .env + Django
echo ">>> [5/6] Django setup..."
cd "$PROJECT_DIR"
if [ ! -f .env ]; then
    KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    cat > .env << EOF
SECRET_KEY=$KEY
DEBUG=False
ALLOWED_HOSTS=$IP,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://$IP
CORS_ALLOWED_ORIGINS=http://$IP
EOF
fi
chmod 600 .env
chown www-data:www-data .env
log ".env ready"

. venv/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
deactivate
log "Django ready"

# 6. Services
echo ">>> [6/6] Services..."
cp "$PROJECT_DIR/deploy/systemd/gunicorn.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable gunicorn --now

cp "$PROJECT_DIR/deploy/nginx.conf" /etc/nginx/sites-available/website
ln -sf /etc/nginx/sites-available/website /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

chown -R www-data:www-data "$PROJECT_DIR/staticfiles"
chown www-data:www-data "$PROJECT_DIR"

echo ""
echo "========================================"
log "Deploy complete!"
echo "  http://$IP"
echo "  http://$IP/zh-hans/admin/"
echo "========================================"
