import hashlib
import sys
import time
from termcolor import colored


def hash(hashMode: str, wordlistPassword: str) -> str:
    if hashMode == 'md5':
        return hashlib.md5(wordlistPassword.encode()).hexdigest()
    elif hashMode == 'sha256':
        return hashlib.sha256(wordlistPassword.encode()).hexdigest()
    elif hashMode == 'sha512':
        return hashlib.sha512(wordlistPassword.encode()).hexdigest()
    # elif hashMode == 'scrypt':
    #     return hashlib.scrypt(wordlistPassword.encode()).hexdigest()
    else:
        print(colored("[-] Hash mode invalid..", "red"))

def auto_detectHash(targetHash: str) -> str:
    if len(targetHash) == len(hash(hashMode='md5', wordlistPassword='0')):
        return 'md5'
    elif len(targetHash) == len(hash(hashMode='sha256', wordlistPassword='0')):
        return 'sha256'
    elif len(targetHash) == len(hash(hashMode='sha512', wordlistPassword='0')):
        return 'sha512'
    else:
        print(colored("[-] Could not identify hash..", "red"))

def hashbreak(hashPath: str, wordlistPath: str, hashMode=None , threads=0, verbose=False) -> str:
    print(colored("[+] Initiating hash cracking process..", "green"))

    targetHash = open(hashPath, 'r')
    targetHash = targetHash.read().strip()
    
    if hashMode == None: #If no hash input
        print(colored("[WARNING] Hash mode is being auto detected..", "yellow"))
        hashMode = auto_detectHash(targetHash=targetHash)
        print(colored(f"[+] Hash mode {hashMode} identified.", "green"))


    if len(targetHash) == len(hash(hashMode=hashMode, wordlistPassword='0')):  # compare length with the hash to proceed
        print(colored("[+] Opening wordlist..", "green"))
        with open(wordlistPath, 'r', encoding='latin-1') as wordlist:
            print(colored("[+] Cracking hash..", "green"))
            for word in wordlist:
                wordlistPassword = word.strip()
                wordlistPasswordHash = hash(hashMode=hashMode, wordlistPassword=wordlistPassword)  # Where hashing happens
                if verbose == True:
                    print(f' \rTrying -> {wordlistPasswordHash}:{wordlistPassword}', end='')

                if wordlistPasswordHash == targetHash:  # Compares the hash
                    print(colored(f"\n[+] Password found -> {wordlistPassword}.", "green"))
                    return wordlistPassword # Breaks out of loop and returns value
                
                time.sleep(threads)
                
    else:
        print(colored(f"[-] Hash input invalid..", "red"))


#Debug
if __name__ == '__main__':
    try:
        hashbreak(wordlistPath=sys.argv[1], hashPath=sys.argv[2], hashMode=sys.argv[3])
    except:
        try:
            hashbreak(wordlistPath=sys.argv[1], hashPath=sys.argv[2])
        except Exception as error:
            print(error)
            print('Usage - python hashbreaker.py {hash path} {hash mode} {wordlist path}')
            