#!/usr/bin/env bash
set -euo pipefail

WANTED_VER="1.37"
CONF="/etc/inetsim/inetsim.conf"
BACKUP="/etc/inetsim/inetsim.conf.bak.$(date +%Y%m%d-%H%M%S)"

# Re-run with sudo if not root
if [[ $EUID -ne 0 ]]; then
  exec sudo -E bash "$0" "$@"
fi

echo "[*] Detecting Net::DNS version..."
CUR_VER="$(perl -MNet::DNS -e 'print $Net::DNS::VERSION' 2>/dev/null || echo "missing")"
echo "    Current Net::DNS: ${CUR_VER}"

needs_downgrade=false
if [[ "$CUR_VER" == "missing" ]]; then
  echo "    Net::DNS not found -> will install ${WANTED_VER}"
  needs_downgrade=true
else
  # Use dpkg version comparison if available; fallback to sort -V
  if command -v dpkg >/dev/null 2>&1; then
    if dpkg --compare-versions "$CUR_VER" ge "$WANTED_VER"; then
      # >= 1.37 -> downgrade to 1.37
      needs_downgrade=true
    fi
  else
    # Fallback comparison (>=)
    if [[ "$(printf '%s\n' "$WANTED_VER" "$CUR_VER" | sort -V | tail -n1)" == "$CUR_VER" ]]; then
      needs_downgrade=true
    fi
  fi
fi

if $needs_downgrade; then
  echo "[*] Installing prerequisites (cpanminus, build tools, SSL Perl libs)..."
  apt update
  apt install -y cpanminus build-essential libio-socket-ssl-perl libnet-ssleay-perl

  echo "[*] Downgrading/Installing Net::DNS@$WANTED_VER via cpanm..."
  # Force ensures site_perl overrides distro version; --notest zips through
  cpanm --notest --force "Net::DNS@${WANTED_VER}"
else
  echo "[*] Net::DNS (${CUR_VER}) is already below ${WANTED_VER}; no downgrade needed."
fi

echo "[*] Detecting primary IPv4 address..."
VM_IP="$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if ($i=="src"){print $(i+1); exit}}' || true)"
if [[ -z "${VM_IP}" ]]; then
  VM_IP="$(ip -4 addr show scope global up | awk '/inet /{print $2}' | cut -d/ -f1 | head -n1 || true)"
fi
if [[ -z "${VM_IP}" ]]; then
  echo "[-] Could not determine VM IPv4 address. Aborting."
  exit 1
fi
echo "    VM IPv4: ${VM_IP}"

echo "[*] Backing up INetSim config to ${BACKUP} ..."
cp -a "$CONF" "$BACKUP"

echo "[*] Updating INetSim config: service_bind_address and dns_default_ip ..."
# Ensure the two directives exist with desired values, replacing if present or appending if missing
if grep -Eq '^[#[:space:]]*service_bind_address[[:space:]]+' "$CONF"; then
  sed -i -E 's|^[#[:space:]]*service_bind_address[[:space:]].*|service_bind_address 0.0.0.0|' "$CONF"
else
  echo "service_bind_address 0.0.0.0" >> "$CONF"
fi

if grep -Eq '^[#[:space:]]*dns_default_ip[[:space:]]+' "$CONF"; then
  sed -i -E "s|^[#[:space:]]*dns_default_ip[[:space:]].*|dns_default_ip ${VM_IP}|" "$CONF"
else
  echo "dns_default_ip ${VM_IP}" >> "$CONF"
fi

# Optional but recommended on Kali: free port 53 from systemd-resolved
if systemctl is-active --quiet systemd-resolved; then
  echo "[*] Disabling systemd-resolved to free port 53 ..."
  systemctl disable --now systemd-resolved
fi

echo "[*] Enabling and restarting INetSim ..."
systemctl enable inetsim >/dev/null 2>&1 || true
systemctl restart inetsim

echo "[*] Checking port 53 listeners (DNS) ..."
if command -v ss >/dev/null 2>&1; then
  ss -tulpn | grep -E '(:53\s)' || true
else
  netstat -tulnp | grep -E '(:53\s)' || true
fi

echo
echo "[*] INetSim service status:"
systemctl --no-pager -l status inetsim || true

echo
echo "[✓] Done. If DNS still fails, re-run this script and share the output."
