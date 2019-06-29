def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    alphabet= 'abcdefghijklmnopqrstuvwxyz'
    ciphertext=""
    key=keyword.lower() 
    for i in range (len(plaintext)):
        a=ord(plaintext[i])
        b=alphabet.find(key[i%len(key)])
        c=a+b
        if 65<=a<=90:
            if c<=90:
                ciphertext+=chr(c)
            elif c>90:
                ciphertext+=chr(c-26)
        if 97<=a<=122:
            if c<=122:
                ciphertext+=chr(c)
            elif a+b>122:
                ciphertext+=chr(c-26)

    return ciphertext



def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    alphabet= 'abcdefghijklmnopqrstuvwxyz'
    plaintext=""
    key=keyword.lower() 
    for i in range (len(ciphertext)):
        a=ord(ciphertext[i])
        b=alphabet.find(key[i%len(key)])
        c=a-b
        if 65<=a<=90:
            if 65<=c<=90:
                plaintext+=chr(c)
            elif c<65:
                plaintext+=chr(c+26)
        if 97<=a<=122:
            if 97<=c<=122:
                plaintext+=chr(c)
            elif 90<c<97:
                plaintext+=chr(c+26)

    return plaintext
