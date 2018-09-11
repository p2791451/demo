import os
import requests
import time


def main():
    child = pexpect.spawn('./mototerm 30.255.240.82')
    child.expect('cmd2k mode is off', timeout=20)
    child.sendline('osdiag rebootnow')
    time.sleep(3)
    os.system(
        "/Users/parkerfranks/Documents/GitHub/stb-tester-test-pack-charter/"
        "stbt_rig.py -v --node-id=stb-tester-00044b80f5f9 run tests/"
        "reboot_test.py::test_DVR_on_reboot > "
        "/Users/parkerfranks/Documents/results.txt")
    while True:
        if os.path.isfile("results.txt"):
            break


if __name__ == "__main__":
    main()
