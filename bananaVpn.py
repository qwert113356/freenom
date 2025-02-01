import requests, base64, json, uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

def rc4_decrypt(key, data):
    S, j, out = list(range(256)), 0, []
    for i in range(256): j = (j + S[i] + key[i % len(key)]) % 256; S[i], S[j] = S[j], S[i]
    i = j = 0
    for char in data: i = (i + 1) % 256; j = (j + S[i]) % 256; S[i], S[j] = S[j], S[i]; out.append(char ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header('Content-type', 'text/plain'); self.end_headers()
        r = requests.post('https://43.136.91.47:9000/auth/no_register', json={"device_id": uuid.uuid4().hex, "channel": 'normal'})
        decrypted_data = rc4_decrypt(b'RocketMaker', base64.b64decode(r.text)).decode('utf-8')
        self.wfile.write(requests.get(json.loads(decrypted_data)['data']['android_sub'][0]).text.encode('utf-8'))

HTTPServer(('0.0.0.0', 11505), MyHandler).serve_forever()