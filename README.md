# satellite-ssh-pubkey
Red Hat Satellite ssh public key - needed for remote execution

RPM Download
============
https://github.com/ftaher/satellite-ssh-pubkey/releases/download/1.3/satellite-ssh-pubkey-1.3-1.noarch.rpm

This rpm will First try to discovering the RHSM server hostname by running subscription-manager config
Then it will download this key from satellite web API and install it using the following command
curl -k https://${SATELLITE_HOSTNAME}:9090/ssh/pubkey >> ~/.ssh/authorized_keys
