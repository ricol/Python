#!/usr/bin/env python
#-*- coding: utf-8 -*-

class CaesarCipher:

    MAX = 26

    def __init__(self, shift):
        encoder = [None] * self.MAX
        decoder = [None] * self.MAX
        for k in range(self.MAX):
            encoder[k] = chr((k + shift) % self.MAX + ord('A'))
            decoder[k] = chr((k - shift) % self.MAX + ord('A'))
        self._forward = ''.join(encoder)
        self._backward = ''.join(decoder)

    def encrypt(self, message):
        return self._transform(message, self._forward)

    def decrypt(self, secret):
        return self._transform(secret, self._backward)

    def _transform(self, original, code):
        msg = list(original)
        for k in range(len(msg)):
            if msg[k].isupper():
                j = ord(msg[k]) - ord('A')
                msg[k] = code[j]
        return ''.join(msg)

if __name__ == '__main__':
    cipher = CaesarCipher(3)
    msg = "THE EAGLE IS IN PLAY; MEET AT JOE'S"
    coded = cipher.encrypt(msg)
    print("Secret: %s" % coded)
    answer = cipher.decrypt(coded)
    print("Message: %s" % answer)