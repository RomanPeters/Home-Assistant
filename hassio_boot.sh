line=$(sed "2q;d" /root/.bash_profile)

if [line != 'cd /config']; then
  echo 'cd /config' >> /root/.bash_profile;
fi

ln -s /config/.ssh/id_rsa /root/.ssh/id_rsa;
ln -s /config/.ssh/id_rsa.pub /root/.ssh/id_rsa.pub;
