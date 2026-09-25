import http.server
import socketserver
import socket
import ssl
import threading
import os
import subprocess

HTTP_PORT = 8000
HTTPS_PORT = 8443

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def ensure_ssl_certs(local_ip):
    cert_file = "cert.pem"
    key_file = "key.pem"
    if not (os.path.exists(cert_file) and os.path.exists(key_file)):
        print("⚙️  Generating local self-signed SSL certificate for HTTPS...")
        cnf_path = r"C:\Program Files\Git\usr\ssl\openssl.cnf"
        cmd = [
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", key_file, "-out", cert_file,
            "-days", "365", "-nodes",
            "-subj", f"/CN={local_ip}"
        ]
        if os.path.exists(cnf_path):
            cmd.extend(["-config", cnf_path])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Local SSL certificate generated.")
    return cert_file, key_file

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable caching so changes appear immediately
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        # Clean terminal output for connected devices
        client_ip = self.client_address[0]
        req_line = args[0] if len(args) > 0 else ""
        status_code = args[1] if len(args) > 1 else ""
        # Only log main page requests to keep console readable
        if any(ext in req_line for ext in ['.html', '.mp4', '.mind']):
            print(f"  [REQ from {client_ip}] {req_line} -> {status_code}")

local_ip = get_local_ip()
cert_file, key_file = ensure_ssl_certs(local_ip)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

# HTTP Server Thread
def run_http():
    with ReusableTCPServer(("0.0.0.0", HTTP_PORT), CustomHandler) as httpd:
        httpd.serve_forever()

# HTTPS Server Thread
def run_https():
    with ReusableTCPServer(("0.0.0.0", HTTPS_PORT), CustomHandler) as httpsd:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        httpsd.socket = context.wrap_socket(httpsd.socket, server_side=True)
        httpsd.serve_forever()

t_http = threading.Thread(target=run_http, daemon=True)
t_https = threading.Thread(target=run_https, daemon=True)

t_http.start()
t_https.start()

print("=" * 70)
print("  [*] MindAR Local Dual-Server Started (HTTP + HTTPS)")
print("=" * 70)
print("  [PC / Desktop]:")
print(f"     * Poster & Live QR Generator:  http://localhost:{HTTP_PORT}/poster.html")
print(f"     * WebAR Experience:            http://localhost:{HTTP_PORT}/index.html")
print(f"     * Targets Compiler:            http://localhost:{HTTP_PORT}/compiler.html")
print("-" * 70)
print("  [Phone on Same Wi-Fi Network]:")
print(f"     -> https://{local_ip}:{HTTPS_PORT}/index.html")
print()
print("  [!] FIRST TIME CONNECTING ON PHONE (Self-Signed SSL):")
print("     Mobile browsers require HTTPS for camera access. Because this is a")
print("     local self-signed certificate, your phone browser will show a warning:")
print("     - iOS Safari:     Tap 'Show Details' -> Tap 'visit this website'.")
print("     - Android Chrome: Tap 'Advanced'     -> Tap 'Proceed to (unsafe)'.")
print("     Then tap 'Allow' when prompted for Camera permissions!")
print("-" * 70)
print("  [Option B] Instant Tunnel (Zero SSL warnings on phone):")
print(f"     Run in a separate terminal:  npx localtunnel --port {HTTP_PORT}")
print("=" * 70)
print("  Server is active. Press Ctrl+C to stop.\n")

try:
    threading.Event().wait()
except KeyboardInterrupt:
    print("\nShutting down servers...")

