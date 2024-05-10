#!/bin/bash

TUNNEL_ENDPOINT=${TUNNEL_ENDPOINT:-http://tunnel:4040}

while [[ "$(curl -s -o /dev/null -w '%{http_code}' "${TUNNEL_ENDPOINT}/status")" != "200" ]]; do
    echo "Waiting for tunnel..."
    sleep 1
done
WS_ENDPOINT=$(curl --silent "${TUNNEL_ENDPOINT}/start" | python -c "import sys, json; print(json.load(sys.stdin)['url'])" | sed -rn 's#https?://([^/]+).*#\1#p')
echo "fetched hostname and port [$WS_ENDPOINT]"

exec "$@"  --externalhostandport ${WS_ENDPOINT}
