import yaml
import os

podman_compose_path = os.getenv('PODMAN_COMPOSE_PATH')
ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')

with open(podman_compose_path, 'r') as file:
    podman_compose = yaml.safe_load(file)

ngrok_config = {
    'version': '2',
    'authtoken': ngrok_auth_token,
    'tunnels': {}
}

for service_name, service_data in podman_compose.get('services', {}).items():
    ports = service_data.get('ports', [])
    for port in ports:
        if ':' in port:
            internal_port, external_port = port.split(':')
            if not internal_port.startswith('127.0.0.1'):
                ngrok_config['tunnels'][f'{service_name}_{external_port}'] = {
                    'addr': external_port,
                    'proto': 'http',
                    'inspect': False
                }

with open('ngrok.yml', 'w') as file:
    yaml.dump(ngrok_config, file)
