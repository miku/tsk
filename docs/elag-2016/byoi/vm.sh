#!/bin/sh

KEYFILE=`mktemp`
cat << EOF >> ${KEYFILE}
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAy3OLNAlXYVNtCaJuSZWgCGIu2hPH/uSXYvLOxqJGLDC6SNPv
S5+Oh/w1Or6FVvgrPlZE/d5fdSSmx6pHkPCE8zR7+BXvAib6tnBiaUD4EY2NZZ1p
zzLhxYNknvWdpDa4iVj3YElZ1IFxREMGUop6m0Rf4P2D+oi/Q32hYp0+F/5u/kf1
BJPNN/+fH3tf5PxdpOKj+4IfeOI0eyyIt7gerkcvdKC7fh40yuzyw687PmY0Tgo4
vEVHjs74of7uf8da3/mhi/blY/5NzmswgDfSFKVankn11YO+T7bn9RRMrknK3osU
QXr3bBGlTCePL0fy22ergACBP8XAd8aWIHTjgwIDAQABAoIBAGx4TOZQeKrmLMMv
O7e1s13k4u/YDhAC1gemRsI2cE1NKXR8sh9SkU5FFCgevb6Rj5SrsBrd/WzaPqVD
TuaipW95MwMgxo4SNCciogVV4yyQmKttkqUqjp6cn//0Gbkch6SKr1FBqkgXP0lS
psNJG3c+rBOrdjsTv01/ZJTMGvf09UspWS6AmBAhm4v32EKBC2Eif+tM6BNT2PtL
R/0cHXoXXoIsA9BXshgsLuqxHvl6Pvb5yU8hTsyaJdrrgRc6SdWq9raO5wrsLChC
yndxT+kdAHvR0u57HwcZfLC4Ptgt3YSN9Bfu2tSXhky14N2ERDGk+HVh46X/C35V
nIN8jekCgYEA/+iQ/gG082sP+4tAPOul9yuElQMjw9+1JMyY3CFf5estpzaO+Bsn
OxneLWaxpf2GlYv/fhu1unV5ndRiB8obnjMDXWKFN6GFftwegTxBIWjRq3kIEid7
D3ATQqbAB8YMBhrDhvCQ2r+cT9UPL83uxxjQIHZHrsIRl8J6pcg9ZX8CgYEAy4Ys
gswVZLkPs+Qnh2PqdTMGd9haOut6CFqxOG2MlLW60P3zPZW97y3KqXE9uQwGXhOp
lyM4LnniXBtYiypQwR+Lcsynr7H2oqz/TX1kNMKP5My/1gkPRfn9SAWPvh+PPFb3
2g5cFj6z5ZQT/K4lKUjM0lh1cj3puHB6DcZk6/0CgYEA+Y8sLnktpKBIws7Gg2Ju
xD7NGaApNbAob82SWEG3ynjxWXrMK8oXFPyh/XaDUdOOdrJDIxEUxNQhGLhwLRZ8
nmczJdOZBGpgzBkPKoq/HTyiE+2A4GteB+0M61fANxR8z0s0WJirOpfXcMbe+4iB
Den1tWKDfzpEe9GtV5SRwzMCgYBzWNTrQG0zi6r5ompA0oDz8XpN/AGPeRvNllDw
kS3mrmR1xCfSlIZ0AvjkNXjs4oLNWMl6DgzuUkfXOexh2xavjYhEBPdYnT0SD4gW
S+W5/Tb+Toi+7p2IZFmHMxe3gj10zjlkjVTlip38lIMLZ0tKbacf4+CUYcCPtreG
DRXvpQKBgCRDD4/Hcj8fraB2rkpm+Q8LW/rhzot2RAkWIPc1TPk2qArZQFPlcY9S
ZK3WgL7dQd0ut3ec6VlWZ71SE3mh9NnL362MAxbWMWFjSwv0ipimDaOfMbV8vyj5
kVplRxrzEc8nw1yrUdGFPlfGNTKZNTYFsVgQb/iDQFfN33l+VTOe
-----END RSA PRIVATE KEY-----
EOF
ssh -q -i ${KEYFILE} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 2200 byoi@localhost
rm -f ${KEYFILE}
