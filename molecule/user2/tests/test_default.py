import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_group(host):
    assert host.group("ansibletestgroup").exists
    assert host.group("ansibletestgroup").gid == 4000


def test_user(host):
    u = host.user("ansibletestuser")
    assert u.exists
    assert u.uid == 2222
    assert set(u.groups) == set(["ansibletestgroup", "users", "bin"])
    assert u.shell == "/bin/sh"


def test_profile(host):
    f = host.file("/home/ansibletestuser/.profile")
    assert b"alias ll='ls -lah'" in f.content
    assert b"alias cp='cp -iv'" in f.content


def test_public_key(host):
    cmd = "ssh-keygen -l -f /home/ansibletestuser/.ssh/authorized_keys"
    f = host.run_expect([0], cmd)
    assert "SHA256:O7S0HORdNGPbOBgqf1qTHqQ7N+9LkEzyUH8F6s0yz4c" in f.stdout
