from cryptography.fernet import Fernet
keyFile = open("key.txt", "wb")
key = Fernet.generate_key()
keyFile.write(key)
keyFile.close()

