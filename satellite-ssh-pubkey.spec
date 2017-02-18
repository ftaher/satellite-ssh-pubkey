Name:		satellite-ssh-pubkey
Version:	1.3
Release:	1
Summary:	Red Hat Satellite ssh public key - needed for remote execution

Group:		Development/Languages
License:	LGPLv2
URL:		https://access.redhat.com/articles/2464671
Source0:	https://codeload.github.com/ftaher/satellite-ssh-pubkey/tar.gz/%{version}

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:	curl,sed,grep,subscription-manager

%description
Red Hat Satellite ssh public key - needed for remote execution.
First this rpm will try to discovering the RHSM server hostname by running subscription-manager config
Then it will download this key from satellite web API and install it using the following command
curl -k https://${SATELLITE_HOSTNAME}:9090/ssh/pubkey >> ~/.ssh/authorized_keys

%post
### POST INSTALL
SATELLITE_HOSTNAME=$(subscription-manager config | egrep 'hostname = (.*)' -m 1 -o | cut -d " " -f 3)
SATELLITE_KEY=$(curl -s -k https://${SATELLITE_HOSTNAME}:9090/ssh/pubkey)
SATELLITE_HASH=$(echo $SATELLITE_KEY | cut -d' ' -f2)

if [ $SATELLITE_HOSTNAME == "" || SATELLITE_HASH == "" ]
then
	echo "Cound not find Red Hat Satellite address to connect to. Please make sure subscription-manager is registered to Red Hat Satellite before installing this package"
	exit 1
fi

# Always uninstall old keys if defferent
if [ -s /etc/rhsm/facts/satellite_public_key ]
then
	FILE_KEY=$(cat /etc/rhsm/facts/satellite_public_key)
	FILE_HASH=$(echo $SATELLITE_KEY | cut -d' ' -f2)

	if [ FILE_HASH != SATELLITE_HASH ]
	then
		FOUND=`grep -ic $FILE_HASH ~/.ssh/authorized_keys`

		if [ $FOUND != "0" ]
		then
		        # FOUND => MUST UNINSTALL IT NOW
		        echo "uninstalling satellite public key"
		        sed -e "s:$FILE_HASH:MARKED_TOBE_DELETE___:" -e "/MARKED_TOBE_DELETE___/ d"  ~/.ssh/authorized_keys > ~/.ssh/authorized_keys
			rm -f /etc/rhsm/facts/satellite_public_key
		fi
	fi
fi


FOUND=`grep -ic $SATELLITE_HASH ~/.ssh/authorized_keys`

if [ $FOUND != "0" ]
then
        # FOUND => IGNORE
        echo "Satellite public key is already installed"
else
        # Not found => Install it
        echo $SATELLITE_KEY > /etc/rhsm/facts/satellite_public_key
	mkdir -p ~/.ssh # making sure /root/.ssh exists
        echo $SATELLITE_KEY >> ~/.ssh/authorized_keys
fi
exit 0


%preun
if [ $1 -eq 0 ]
then 
	SATELLITE_KEY=$(cat /etc/rhsm/facts/satellite_public_key)
	SATELLITE_HASH=$(echo $SATELLITE_KEY | cut -d' ' -f2)

	FOUND=`grep -ic $SATELLITE_HASH ~/.ssh/authorized_keys`

	if [ $FOUND != "0" ]
	then
	        # FOUND => MUST UNINSTALL IT NOW
	        echo "uninstalling satellite public key"
	        sed -e "s:$SATELLITE_HASH:MARKED_TOBE_DELETE___:" -e "/MARKED_TOBE_DELETE___/ d"  ~/.ssh/authorized_keys > ~/.ssh/authorized_keys
		rm -f /etc/rhsm/facts/satellite_public_key
	else
	        # Not found => IGNORE
	        echo $SATELLITE_KEY > /etc/rhsm/facts/satellite_public_key
	        echo $SATELLITE_KEY >> ~/.ssh/authorized_keys
	fi
fi
exit 0

%files
%doc LICENSE

%changelog
* Thu Feb 18 2017 Feras Al Taher <feras@redhat.com> 1.3
- added a github source
- test for empty $SATELLITE_HASH and $SATELLITE_HOSTNAME
- uninstall previous old keys if changed by satellite
* Thu Feb 17 2017 Feras Al Taher <feras@redhat.com> 1.2
- chnage the name from foreman-ssh-pubkey-installer to satellite-ssh-pubkey
- upgrade bug: test $1 before proceeding with the uninstall
* Thu Feb 17 2017 Feras Al Taher <feras@redhat.com> 1.1
- test for empty $SATELLITE_HOSTNAME
- make sure /root/.ssh exists
* Thu Feb 16 2017 Feras Al Taher <feras@redhat.com> 1.0
- first release
