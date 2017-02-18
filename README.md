# satellite-ssh-pubkey
Red Hat Satellite ssh public key - needed for remote execution

This rpm will First try to discovering the RHSM server hostname by running subscription-manager config
Then it will download this key from satellite web API and install it using the following command
curl -k https://${SATELLITE_HOSTNAME}:9090/ssh/pubkey >> ~/.ssh/authorized_keys
