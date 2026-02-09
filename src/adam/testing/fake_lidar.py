import os

class FakeSFTP:
    """
    A fake SFTP client for testing purposes. It simulates the behavior of an SFTP client by storing files in the current directory.
    """

    def __init__(self): 
        if not os.path.exists("C:/Lidar/System/Scan parameters/"):
            os.makedirs("C:/Lidar/System/Scan parameters/")
        if not os.path.exists("C:/Users/End User/DynScan/"):
            os.makedirs("C:/Users/End User/DynScan/")
        self.files = []
    def listdir(self, path): return os.listdir("." + path)
    def get(self, remote, local): open(local, "wb").write(self.files[remote])
    def put(self, local, remote): 
        with open("." + remote, "wb") as f:
            f.write(open(local, "rb").read())
        self.files += "." + remote
    def close(self):
        for file in self.files:
            os.remove(file)
        os.removedirs("C:/Lidar/System/Scan parameters/")
        os.removedirs("C:/Users/End User/DynScan/")
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): self.close()

class FakeSSHClient:
    """
    A fake SSH client for testing purposes. It simulates the behavior of an SSH client by providing a context manager that returns a FakeSFTP instance.
    """

    def __init__(self):
        self.sftp = FakeSFTP()
    def set_missing_host_key_policy(self, policy): pass
    def connect(self, ip_addr, username, password): print(f"Connected to {ip_addr} with username {username}")
    def open_sftp(self): return self.sftp
    def close(self): self.sftp.close()
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): self.close()

