#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
skip() { echo -e "${YELLOW}[SKIP]${NC} $1"; }

[ "$EUID" -ne 0 ] && { echo "Please run as root"; exit 1; }

echo -n "Enter server IP: "; read -r IP

echo "=== Deploying to $IP ==="

# 1. System deps + Node.js 22.x
echo ">>> [1/6] System packages..."
apt-get update -qq && apt-get install -y -qq python3 python3-pip python3-venv nginx curl

# Install Node.js 22.x from NodeSource (Vite 8 requires Node >=20.19)
if command -v node &>/dev/null && node -e 'process.exit(+process.version.slice(1) < 20.19 ? 1 : 0)'; then
    skip "Node.js $(node -v) already meets requirements"
else
    echo "Installing Node.js 22.x from NodeSource..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
    apt-get install -y -qq nodejs
    log "Node.js $(node -v) installed"
fi
npm config set registry https://registry.npmmirror.com
log "System ready"

# 2. Directories
echo ">>> [2/6] Directories..."
mkdir -p /var/log/gunicorn "$PROJECT_DIR/media" "$PROJECT_DIR/logs"
chown -R www-data:www-data /var/log/gunicorn "$PROJECT_DIR/logs"
log "Done"

# 3. Python venv — skip if already set up
if [ -d "$PROJECT_DIR/venv" ]; then
    skip "venv exists, skipping creation"
else
    echo ">>> [3/6] Python venv..."
    cd "$PROJECT_DIR"
    python3 -m venv venv
    . venv/bin/activate
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip -q
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt -q
    deactivate
    log "Done"
fi

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
ADMIN_PATH=admin/
EOF
    log ".env created"
else
    skip ".env already exists"
fi
chmod 600 .env
chown www-data:www-data .env

. venv/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
deactivate
log "Django ready"

# 6. Services
echo ">>> [6/6] Services..."
sed "s|PROJECT_DIR|$PROJECT_DIR|g" "$PROJECT_DIR/deploy/systemd/gunicorn.service" > /etc/systemd/system/gunicorn.service
systemctl daemon-reload
systemctl enable gunicorn --now
log "Gunicorn started"

sed "s|PROJECT_DIR|$PROJECT_DIR|g" "$PROJECT_DIR/deploy/nginx.conf" > /etc/nginx/sites-available/website
ln -sf /etc/nginx/sites-available/website /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx
log "Nginx restarted"

chown -R www-data:www-data "$PROJECT_DIR/staticfiles"
chown www-data:www-data "$PROJECT_DIR" "$PROJECT_DIR"/db.sqlite3* 2>/dev/null || true

echo ""
echo "========================================"
log "Deploy complete!"
echo "  http://$IP"
echo "  http://$IP/zh-hans/admin/"
echo "========================================"
