# By Tedezed
# https://www.saltycrane.com/blog/2011/10/python-gnupg-gpg-example/
# https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/ApiextensionsV1beta1Api.md

import gnupg, random, string, re, json
from kubernetes import client, config
from os import path, getlogin, system, getuid, environ
from sys import argv

class cronjob():

    def randomStringDigits(self, stringLength=6):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

    def createKey(self, keyfile, email, password, keylen=1024, keytype='RSA'):
        print("Be patient...")
        input_data = self.gpg.gen_key_input(
            key_type=keytype,
            key_length=keylen,
            name_email=email,
            passphrase=password)
        key = self.gpg.gen_key(input_data)
        print("Key: ", key)
        self.export_nut(keyfile, str(key.fingerprint))

    def exportKey(self, keyfile, key):
        ascii_armored_public_keys = self.gpg.export_keys(key)
        ascii_armored_private_keys = self.gpg.export_keys(key, secret=True)
        with open("%s.pub" % keyfile, 'w') as f:
            f.write(ascii_armored_public_keys)
        with open("%s.key" % keyfile, 'w') as f:
            f.write(ascii_armored_private_keys)

    def importKey(self, keyfile):
        key_data = open(keyfile).read()
        import_result = self.gpg.import_keys(key_data)
        print(import_result.results)

    def encryptText(self, email, text_to_encrypt):
        encrypted_data = self.gpg.encrypt(text_to_encrypt, email)
        encrypted_string = str(encrypted_data)
        #print('ok: ', encrypted_data.ok)
        #print('status: ', encrypted_data.status)
        #print('stderr: ', encrypted_data.stderr)
        #print('unencrypted_string: ', text_to_encrypt)
        #print('encrypted_string: ', encrypted_string)
        return str(encrypted_string)

    def dencryptText(self, password, encrypted_string):
        decrypted_data = self.gpg.decrypt(encrypted_string, passphrase=password)
        #print('ok: ', decrypted_data.ok)
        #print('status: ', decrypted_data.status)
        #print('stderr: ', decrypted_data.stderr)
        #print('decrypted string: ', decrypted_data.data)
        return str(decrypted_data.data)

    def away(self):
        public_keys = self.gpg.list_keys()
        #re.findall("[a-zA-Z0-9_.-]*@[a-zA-Z0-9_.-]*",gpg.list_keys()[0]["uids"][0])
        for key in self.gpg.list_keys():
            for uid in key.get("uids", False):
                if uid:
                    email = re.findall("[a-zA-Z0-9_.-]*@[a-zA-Z0-9_.-]*", uid)
                    self.nut_list.append(self.encryptText(email, self.randomStringDigits(self.len_password)))
        #print(self.dencryptText('1234567890',self.nut_list[0]))
        self.nuts["nuts"] = self.nut_list
        with open('%s/nuts.json' % self.squirrel_away, 'w') as outfile:  
            json.dump(self.nuts, outfile)

    def rotation(self):
        squirrel = sqrl()
        #squirrel.createKey('mykeyfile', 'juanmanuel.torres@aventurabinaria.es', '1234567890')
        squirrel.importKey('mykeyfile.pub')
        print(squirrel.listKey)
        secret_text = squirrel.encryptText('juanmanuel.torres@aventurabinaria.es', squirrel.randomStringDigits(22))
        print(secret_text)
        print(squirrel.dencryptText('1234567890', secret_text))

    # def rotation(self):
    #     squirrel = sqrl()
    #     #squirrel.createKey('mykeyfile', 'juanmanuel.torres@aventurabinaria.es', '1234567890')
    #     squirrel.importKey('mykeyfile.pub')
    #     print(squirrel.listKey)
    #     secret_text = squirrel.encryptText('juanmanuel.torres@aventurabinaria.es', squirrel.randomStringDigits(22))
    #     print(secret_text)
    #     print(squirrel.dencryptText('1234567890', secret_text))

# def old():
#     squirrel = sqrl()
#     #squirrel.createNut('mykeyfile', 'juanmanuel.torres@aventurabinaria.es', '1234567890')
#     squirrel.importNut('mykeyfile.pub')
#     print(squirrel.listNuts)
#     secret_text = squirrel.encryptText('juanmanuel.torres@aventurabinaria.es', squirrel.randomStringDigits(22))
#     print(secret_text)
#     print(squirrel.dencryptText('1234567890', secret_text))


# def main():
#     squirrel = sqrl()
#     squirrel.away()

# if __name__ == '__main__':
#     # Start
#     main()