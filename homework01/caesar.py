def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("")
    ''
    """
    ABS=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    abs=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    ciphertext = ""

    for el in plaintext:
        num = ord(el)
        if el in ABS:
            if num<ord('X'):
                num=ord(el)+3
            elif num>= ord('X'):
                num=num-23
        elif el in abs:
            if num<ord('x'):
                num=ord(el)+3
            elif num>=ord('x'):
                num=num-23
        ciphertext += chr(num)

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("")
    ''
    """
    ABS=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    abs=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    plaintext=""

    for el in ciphertext:
        num=ord(el)
        if el in ABS:
            if num>ord('C'):
                num=ord(el)-3
            elif num<=ord('C'):
                num=num+23
        elif el in abs:
            if num>ord('c'):
                num=ord(el)-3
            elif num<=ord('c'):
                num=num+23
        plaintext+=chr(num)        
    
    return plaintext
