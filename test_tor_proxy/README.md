#### Change IP:
```bash
ssh vm-100 './testing/env/bin/python3 ./testing/new_identity.py'
```

#### Show IP:
```bash
curl --socks5-hostname "192.168.56.10:9050" "http://ident.me/"
```
