#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
skip() { echo -e "${YELLOW}[SKIP]${NC} $1"; }

is_valid_root_domain() {
    local domain="$1"
    local label_pattern='[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?'

    [ "${#domain}" -le 253 ] \
        && [[ "$domain" != www.* ]] \
        && [[ "$domain" =~ ^(${label_pattern}\.)+${label_pattern}$ ]]
}

is_valid_ipv4() {
    local ip="$1"
    local octet
    local -a octets

    [[ "$ip" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1
    IFS='.' read -r -a octets <<< "$ip"

    for octet in "${octets[@]}"; do
        ((10#$octet <= 255)) || return 1
    done
}

upsert_env() {
    local key="$1"
    local value="$2"

    if grep -q "^${key}=" .env; then
        sed -i "s|^${key}=.*|${key}=${value}|" .env
    else
        printf '%s=%s\n' "$key" "$value" >> .env
    fi
}

[ "$EUID" -ne 0 ] && { echo "Please run as root"; exit 1; }

while true; do
    read -r -p "Do you have a domain? [y/n]: " HAS_DOMAIN

    case "${HAS_DOMAIN,,}" in
        y|yes)
            USE_DOMAIN=true
            break
            ;;
        n|no)
            USE_DOMAIN=false
            break
            ;;
        *)
            warn "Enter y/yes or n/no."
            ;;
    esac
done

if [ "$USE_DOMAIN" = true ]; then
    while true; do
        read -r -p "Enter root domain (e.g. example.com): " ROOT_DOMAIN
        ROOT_DOMAIN="${ROOT_DOMAIN,,}"

        if is_valid_root_domain "$ROOT_DOMAIN"; then
            break
        fi

        warn "Enter a root domain without protocol, port, path, or www prefix."
    done

    WWW_DOMAIN="www.${ROOT_DOMAIN}"
    DEPLOY_HOST="$WWW_DOMAIN"
else
    while true; do
        read -r -p "Enter server IPv4 address (e.g. 203.0.113.10): " SERVER_IP

        if is_valid_ipv4 "$SERVER_IP"; then
            break
        fi

        warn "Enter a valid IPv4 address."
    done

    DEPLOY_HOST="$SERVER_IP"
fi

echo "=== Deploying to $DEPLOY_HOST ==="

# 1. System deps + Node.js 22.x
echo ">>> [1/6] System packages..."
apt-get update -qq && apt-get install -y -qq python3 python3-pip python3-venv nginx curl

# Install Node.js 22.x from NodeSource (Vite 8 requires Node >=20.19)
if command -v node &>/dev/null && node -e 'process.exit(parseFloat(process.version.slice(1)) < 20.19 ? 1 : 0)'; then
    skip "Node.js $(node -v) already meets requirements"
else
    echo "Installing Node.js 22.x from NodeSource..."
    # Remove conflicting system Node packages before upgrading
    apt-get remove -y -qq libnode-dev libnode72 nodejs npm 2>/dev/null || true
    curl -fsSL https://deb.nodesource.com/setup_22.x | DEBIAN_FRONTEND=noninteractive bash -
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
ADMIN_PATH=admin/
EOF
    log ".env created"
else
    skip ".env already exists"
fi

if [ "$USE_DOMAIN" = true ]; then
    upsert_env "ALLOWED_HOSTS" "$ROOT_DOMAIN,$WWW_DOMAIN,127.0.0.1,localhost"
    upsert_env "CSRF_TRUSTED_ORIGINS" "http://$ROOT_DOMAIN,http://$WWW_DOMAIN"
    upsert_env "CORS_ALLOWED_ORIGINS" "http://$ROOT_DOMAIN,http://$WWW_DOMAIN"
else
    upsert_env "ALLOWED_HOSTS" "$SERVER_IP,127.0.0.1,localhost"
    upsert_env "CSRF_TRUSTED_ORIGINS" "http://$SERVER_IP"
    upsert_env "CORS_ALLOWED_ORIGINS" "http://$SERVER_IP"
fi
log ".env host settings updated"

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

if [ "$USE_DOMAIN" = true ]; then
    sed \
        -e "s|PROJECT_DIR|$PROJECT_DIR|g" \
        -e "s|ROOT_DOMAIN|$ROOT_DOMAIN|g" \
        -e "s|WWW_DOMAIN|$WWW_DOMAIN|g" \
        "$PROJECT_DIR/deploy/nginx.conf" > /etc/nginx/sites-available/website
else
    sed \
        -e "s|PROJECT_DIR|$PROJECT_DIR|g" \
        -e "s|SERVER_IP|$SERVER_IP|g" \
        "$PROJECT_DIR/deploy/nginx.ip.conf" > /etc/nginx/sites-available/website
fi
ln -sf /etc/nginx/sites-available/website /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx
log "Nginx restarted"

chown -R www-data:www-data "$PROJECT_DIR/staticfiles"
chown www-data:www-data "$PROJECT_DIR" "$PROJECT_DIR"/db.sqlite3* 2>/dev/null || true

echo ""
echo "========================================"
log "Deploy complete!"
echo "  http://$DEPLOY_HOST"
echo "  http://$DEPLOY_HOST/zh-hans/admin/"
echo "========================================"
