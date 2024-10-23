import yaml
import os
import json

# Read environment variables
podman_compose_path = os.getenv('PODMAN_COMPOSE_PATH')
ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')
stack_name = os.getenv('STACK_NAME')

# Read Podman Compose configuration
with open(podman_compose_path, 'r') as file:
    podman_compose = yaml.safe_load(file)

# Create the ngrok configuration
ngrok_config = {
    'version': '2',
    'authtoken': ngrok_auth_token,
    'tunnels': {}
}

# Add tunnels for each service defined in the Podman Compose file
for service_name, service_data in podman_compose.get('services', {}).items():
    ports = service_data.get('ports', [])
    for port in ports:
        if ':' in port:
            internal_port, external_port = port.split(':')
            if not internal_port.startswith('127.0.0.1'):
                tunnel_name = f'{stack_name}_{service_name}_{external_port}'
                ngrok_config['tunnels'][tunnel_name] = {
                    'addr': external_port,
                    'proto': 'http',
                    'inspect': False
                }

# Add an SSH tunnel configuration
ngrok_config['tunnels'][f'{stack_name}_ssh'] = {
    'addr': '22',
    'proto': 'tcp',
    'inspect': False
}

# Write the ngrok configuration to 'ngrok.yml'
with open('ngrok.yml', 'w') as file:
    yaml.dump(ngrok_config, file)

# Generate a JSON file with tunnel information for reference
tunnel_info = {tunnel_name: tunnel['addr'] for tunnel_name, tunnel in ngrok_config['tunnels'].items()}
with open('tunnel_info.json', 'w') as file:
    json.dump(tunnel_info, file)

print('Ngrok configuration written to ngrok.yml')
