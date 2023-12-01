from string import ascii_lowercase
from itertools import cycle


def simple_freq_analysis(msg: str):
    """
    - input : `msg (str)`
    - output : `deviation (int)` , more close to 0 `msg` is more likely to be English
    """

    msg = list(msg.lower())
    english_freq = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
    msg_freq = [100 * msg.count(s) / len(msg) for s in ascii_lowercase]
    return int(sum(((mf - ef) / ef) ** 2 for mf, ef in zip(msg_freq, english_freq)))


def symbol_analysis(msg: str):
    """
    - input : `msg (str)`
    - output : `deviation (int)` , the larger the more `msg` is likely to be English
    """

    msg = msg.lower()
    total = 0
    bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'st', 'or', 'te', 'es', 'is', 'ha', 'ou', 'it', 'to', 'ed', 'ti', 'ng', 'ar', 'se', 'al', 'nt', 'as', 'le', 've', 'of', 'me', 'hi', 'ea', 'ne', 'de', 'co', 'ro', 'll', 'ri', 'li', 'ra', 'io', 'be', 'el', 'ch', 'ic', 'ce', 'ta', 'ma', 'ur', 'om', 'ho', 'et', 'no', 'ut', 'si', 'ca', 'la', 'il', 'fo', 'us', 'pe', 'ot', 'ec', 'lo', 'di', 'ns', 'ge', 'ly', 'ac', 'wi', 'wh', 'tr', 'ee', 'so', 'un', 'rs', 'wa', 'ow', 'id', 'ad', 'ai', 'ss', 'pr', 'ct', 'we', 'mo', 'ol', 'em', 'nc', 'rt', 'sh', 'po', 'ie', 'ul', 'im', 'ts', 'am', 'ir', 'yo', 'fi', 'os', 'pa', 'ni', 'ld', 'sa', 'ay', 'ke', 'mi', 'na', 'oo', 'su', 'do', 'ig', 'ev', 'gh', 'bl', 'if', 'tu', 'av', 'pl', 'wo', 'ry', 'bu']
    trigrams = ['the', 'ing', 'and', 'ion', 'ent', 'hat', 'her', 'tio', 'tha', 'for', 'ter', 'ere', 'his', 'you', 'thi', 'ate', 'ver', 'all', 'ati', 'ith', 'rea', 'con', 'wit', 'are', 'ers', 'int', 'nce', 'sta', 'not', 'eve', 'res', 'ist', 'ted', 'ons', 'ess', 'ave', 'ear', 'out', 'ill', 'was', 'our', 'men', 'pro', 'com', 'est', 'ome', 'one', 'ect', 'ive', 'tin', 'hin', 'hav', 'ght', 'but', 'igh', 'ore', 'ain', 'str', 'oul', 'per', 'sti', 'ine', 'uld', 'ste', 'tur', 'man', 'oth', 'oun', 'rom', 'ble', 'nte', 'ove', 'ind', 'han', 'hou', 'whi', 'fro', 'use', 'der', 'ame', 'ide', 'ort', 'und', 'rin', 'cti', 'ant', 'hen', 'end', 'tho', 'art', 'red', 'lin']
    quadrigrams = ['that', 'ther', 'with', 'tion', 'here', 'ould', 'ight', 'have', 'hich', 'whic', 'this', 'thin', 'they', 'atio', 'ever', 'from', 'ough', 'were', 'hing', 'ment']
    for symbol in bigrams:
        total += msg.count(symbol) * 2
    for symbol in trigrams:
        total += msg.count(symbol) * 3
    for symbol in quadrigrams:
        total += msg.count(symbol) * 4
    return total


def caesar_decrypt(cipher: str, offset: int, charset: list):
    """
    - input : `cipher (str)`, `offset (int)`, `charset (list)`
    - output : `plain (str)`
    """
    return ''.join(charset[(charset.index(char) - offset) % len(charset)] for char in cipher)


def vigenere_decrypt(cipher: str, key: str, charset: list):
    """
    - input : `cipher (str)`, `key (str)`, `charset (list)`
    - output : `plain (str)`
    """
    key = cycle(charset.index(char) for char in key)
    return ''.join(charset[(charset.index(char) - next(key)) % 26] for char in cipher)


def rail_fence_decrypt(cipher: str, key: int):
    """
    - input : `cipher (str)`, `key (int)`
    - output : `plain (str)`
    """
    index_list = [[] for _ in range(key)]
    layer, down = 0, True
    for i in range(len(cipher)):
        index_list[layer].append(i)
        
        if layer == (key - 1):
            down = False
        
        if layer == 0:
            down = True
        
        if down:
            layer += 1
        else:
            layer -= 1
    index_list = sum(index_list, [])

    return ''.join(cipher[index_list.index(i)] for i in range(len(cipher)))


def crack_vigenere(cipher: str, charset: str):
    """
    - input : `cipher (str)`, `charset (str)` , `charset` will be `string.ascii_uppercase`/`string.ascii_lowercase`
    - output : `(key, keylength, plain) (str, int, str)`
    """

    def calc_keylength_list():
        correlation_list = [(keylength, calc_correlation(keylength)) for keylength in range(1, 100)]
        return [data[0] for data in sorted(correlation_list, key=lambda x: x[1], reverse=True)[:20]]

    def calc_correlation(keylength: str):
        correlation = 0
        for i in range(len(cipher) - keylength):
            if cipher[i] == cipher[i + keylength]:
                correlation += 1
        return correlation

    def keylength2key(keylength: str):
        caesar_cipher_group = []
        for i in range(keylength):
            caesar_cipher_group.append(''.join(cipher[j] for j in range(i, len(cipher), keylength)))

        key = []
        for caesar_cipher in caesar_cipher_group:
            val_list = [simple_freq_analysis(caesar_decrypt(caesar_cipher, i, charset)) for i in range(26)]
            key.append(val_list.index(min(val_list)))
        return ''.join(charset[k] for k in key)

    keylength_list = calc_keylength_list()
    key_list, plain_list = [], []
    for keylength in keylength_list:
        key = keylength2key(keylength)
        plain = vigenere_decrypt(cipher, key, charset)
        if plain in plain_list:
            idx = plain_list.index(plain)
            if key_list[idx][1] > keylength:
                key_list[idx] = (key, keylength)
        else:
            key_list.append((key, keylength))
            plain_list.append(plain)

    val_list = [symbol_analysis(plain) for plain in plain_list]
    idx = val_list.index(max(val_list))

    return key_list[idx][0], key_list[idx][1], plain_list[idx]
