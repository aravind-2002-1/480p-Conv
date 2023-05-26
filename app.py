from flask import Flask, render_template, request
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode_decode', methods=['POST'])
def encode_decode():
    key = request.form['private_key']
    message = request.form['message']
    mode = request.form['mode']
    
    if mode == 'e':
        result = encode(key, message)
    elif mode == 'd':
        result = decode(key, message)
    else:
        result = 'Invalid Mode'
    
    return render_template('result.html', result=result)


# function to encode
def Encode(key, message):
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        encoded_char = (ord(message[i]) + ord(key_c)) % 65536
        enc.append(chr(encoded_char))

    encoded_str = "".join(enc)
    encoded_bytes = encoded_str.encode("utf-8")
    encoded_base64 = base64.urlsafe_b64encode(encoded_bytes).decode("utf-8")
    return encoded_base64

# function to decode
def Decode(key, message):
    dec = []
    decoded_base64 = base64.urlsafe_b64decode(message).decode("utf-8")
    for i in range(len(decoded_base64)):
        key_c = key[i % len(key)]
        decoded_char = (65536 + ord(decoded_base64[i]) - ord(key_c)) % 65536
        dec.append(chr(decoded_char))

    return "".join(dec)



if __name__ == '__main__':
    app.run(debug=True)
