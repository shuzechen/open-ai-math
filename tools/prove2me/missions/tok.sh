#!/bin/bash
# Prints a valid Prove2Me access token, re-exchanging the API key when the cached token is older than 50 min.
# Reads credentials.json ({"api_key": "p2m_..."}) from the directory of this script. Only talks to https://prove2.me/api/v1.
D=$(cd "$(dirname "$0")" && pwd)
if [ -f "$D/token.json" ] && [ $(( $(date +%s) - $(stat -c %Y "$D/token.json") )) -lt 3000 ]; then
  python3 -c "import json;print(json.load(open('$D/token.json'))['access_token'])"; exit
fi
KEY=$(python3 -c "import json;print(json.load(open('$D/credentials.json'))['api_key'])")
curl -sS --retry 5 --retry-all-errors -X POST https://prove2.me/api/v1/agent/refresh -H "Content-Type: application/json" -d "{\"api_key\": \"$KEY\"}" > "$D/token.json"
python3 -c "import json;print(json.load(open('$D/token.json'))['access_token'])"
