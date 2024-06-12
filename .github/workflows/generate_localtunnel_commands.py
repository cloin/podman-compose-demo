import yaml
import os

podman_compose_path = os.getenv('PODMAN_COMPOSE_PATH')

with open(podman_compose_path, 'r') as file:
    podman_compose = yaml.safe_load(file)

localtunnel_commands = []
localtunnel_password_commands = []

for service_name, service_data in podman_compose.get('services', {}).items():
    ports = service_data.get('ports', [])
    for port in ports:
        if ':' in port:
            internal_port, external_port = port.split(':')
            if not internal_port.startswith('127.0.0.1'):
                subdomain = f"{service_name}-{external_port}".replace('_', '-')
                localtunnel_commands.append(f"lt --port {external_port} --subdomain {subdomain} &")
                localtunnel_password_commands.append(f"curl --silent https://loca.lt/{subdomain}password")

localtunnel_commands.append("lt --port 22 --subdomain ssh &")
localtunnel_password_commands.append("curl --silent https://loca.lt/sshpassword")

with open('localtunnel_commands.sh', 'w') as file:
    file.write("#!/bin/bash\n")
    for command in localtunnel_commands:
        file.write(f"{command}\n")

with open('localtunnel_password_commands.sh', 'w') as file:
    file.write("#!/bin/bash\n")
    for command in localtunnel_password_commands:
        file.write(f"{command}\n")

print("LocalTunnel commands and password retrieval commands generated.")
