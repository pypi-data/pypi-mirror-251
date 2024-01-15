# cyber-security-Ai
cyber security Ai python homework

# interipport package
use python to do some cyber security Ai work.
check the internet connect by google.com, github.com, pypi.org
get public ip and get host ip 
check open ports which is using 
it works on win32 And maybe work well on server too

# How to install interipport
$ pip install interipport

# How to run interipport
$ interipport 

$ interipport <ip port[0] port[1]>

# showcase
    $interipport 
    ~be like
    http://www.google.com response status code: 200
    http://www.github.com response status code: 200
    http://pypi.org response status code: 200
    host_ip 192.168.3.5
    public_ip60.199.119.197

    $interipport <ip port[0] port[1]>
    ~be like
    $interipport "127.0.0.1" 6000 6006
    http://www.google.com response status code: 200
    http://www.github.com response status code: 200
    http://pypi.org response status code: 200
    host_ip 192.168.3.2
    public_ip 60.199.119.197
    The occupied port number
    6006
