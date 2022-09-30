def validateHMAC():
    import hmac
    import hashlib
    import base64
    file = open("payload.txt", "rb") # Read the payload from a file named payload.txt
    payload = file.read()
    secret = "4+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxuE=" # Replace this value with your own secret
    signature = "e4xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxhg=" # Replace this value with your own signature

    hashBytes = hmac.new(str.encode(secret), msg=payload, digestmod=hashlib.sha256).digest()
    base64Hash = base64.b64encode(hashBytes)
    return hmac.compare_digest(str.encode(signature), base64Hash)

print(validateHMAC())