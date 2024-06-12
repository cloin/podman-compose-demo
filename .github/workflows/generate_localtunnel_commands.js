const localtunnel = require('localtunnel');
const fs = require('fs');

(async () => {
  const webTunnel = await localtunnel({ port: 8080, subdomain: 'web1-8080' });
  const sshTunnel = await localtunnel({ port: 22, subdomain: 'ssh' });

  fs.writeFileSync('web_tunnel_url.txt', webTunnel.url);
  fs.writeFileSync('ssh_tunnel_url.txt', sshTunnel.url);

  webTunnel.on('close', () => {
    console.log('Web tunnel closed');
  });

  sshTunnel.on('close', () => {
    console.log('SSH tunnel closed');
  });
})();
