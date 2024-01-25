#!/bin/python
import base64
import hashlib

gwconfigMD5 = 'RTfG0MzhkEjVmZ6nnK7uAQ=='
gwconfig = '{"code":"000000","descrition":"success","data":{"lora":{"freq":910300000,"dr":3,"power":20},"firm":{"ver":"0107","url":"http://www.yosmart.com/firmrepo/NotValidNow.bin"},"deviceId":"d88b4c1603026f25","ota":{"time":"01:00"},"svr":{"mqtt":{"url":"mqtt://mq-yl-gw.yosmart.com:8001","pwd":"1bf6556c9cbabe4c197c328f0a1d903d","tpkfix":"ylgw470"}}},"messageKey":null}'

gwconfigMD5_base64_decoded = base64.b64decode(gwconfigMD5)
gwconfig_generated_bytes = bytes.fromhex(hashlib.md5(gwconfig.encode()).hexdigest())

gwconfig_generated_encoded = base64.b64encode(gwconfig_generated_bytes)

print('gwconfigMD5                  = "{}"'.format(gwconfigMD5))
print('gwconfig_generated_encoded   = "{}"'.format(gwconfig_generated_encoded.decode('utf-8')))
