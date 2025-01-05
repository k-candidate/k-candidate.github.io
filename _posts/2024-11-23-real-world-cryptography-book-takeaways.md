---
layout: post
title: "Real-World Cryptography Book Takeaways"
date: 2024-11-23 00:00:00-0000
categories: 
---
> If you’re looking for a practical book that teaches you the cryptography that companies and products implement and use, and if you’re curious about how real-world cryptography works underneath the surface but aren’t looking for a reference book with all the implementation details, then this book is for you.

![Book cover for Real-World Cryptography]({{ site.baseurl }}/assets/images/real-world-cryptography-book-cover.png)

I recently finished reading David Wong’s book Real-World Cryptography, and it brought back a distant memory.

One summer during my childhood, I decided to figure out what writing code is about. I stumbled upon a university’s pdf about Pascal. They say that our early experiences leave indelible marks. I learned a lot, and I loved it.

I wrote 2 small programs that summer: “cryptor” and “decryptor”. The former asks for user input, shifts every character by 13, and outputs an “encrypted” text. The latter does the opposite.
That’s the Caesar cipher, but I did not know that at the time.

My main takeaways from this book:
- Do not roll your own crypto.
- Follow the updated best practices. Be conservative, and use tried and tested cryptography.
- Think of cryptographic primitives as puzzle pieces for a protocol. Find a respected implementation and use it. If it does not exist, then you’ll have to assemble the pieces yourself.
- Broadly speaking, encryption is based on two general principles: substitution and transposition.
- In the real world, software runs on hardware. Both have supply chains. At some point, you have no other choice but to trust or assume security. Hence the importance of risk management, and defense in depth.

The details that caught my attention:

### Hash functions
- The most widely adopted hash function is SHA-2, while the recommended hash function is SHA3 due to SHA-2’s lack of resistance to length-extension attacks.
- For hashing passwords, Argon2 is state-of-the-art.

### Message Authentication Codes
- Use standardized functions like HMAC

### Authenticated Encryption
- To avoid misuse, best practice is to use AEAD (Authenticated Encryption with Associated Data) algorithms instead of constructing one from a symmetric encryption algorithm and a MAC.
- The most widely adopted ones are AES-GCM and ChaCha20-Poly1305.
- When it comes to disk encryption, Microsoft (Bitlocker) and Apple (FileVault) use AES-XTS, which is a non-ideal solution as it is unauthenticated and is not a wide-block cipher.

### Asymmetric encryption
- RSA PKCS#1 v1.5 is broken. Prefer v2.2.

### Signatures
- Using elliptic curves is the way to go.

### End-to-end encryption
- An alternative to PGP is saltpack.
- The Signal protocol is what’s used by most messaging applications (WhatsApp, Facebook Messenger, Skype).

### Cryptocurrency:
- Bitcoin accounts are simply ECDSA key pairs, and a transaction is a signed message. It uses Merkle trees for block size compression and for transaction verification inclusion.
- Zero-knowledge proofs (ZKPs) are used by many blockchain applications (Zcash, Coda)

### Hardware cryptography
- HSMs (in AWS for example), TPMs (in all modern laptops), and TEE (extension of a CPU’s instruction set).

### Post-Quantum Cryptography
- What to worry about:
  - Shor’s algorithm, which can efficiently solve the discrete logarithm problem and the factorization problem. It breaks most of today’s asymmetric cryptography.
  - Frovers’s algorithm, which can efficiently search for a key or value in a space of 1128 values, impacts most symmetric algorithms with 128-bit security. Boosting a symmetric algorithm’s parameters to provide 256-bit security is enough to thwart quantum attacks.
- Consider upgrading all usage of symmetric cryptographic algorithms to use parameters that provide 256-bit security. For example, move from AES-128-GCM to AES-256-GCM, and from SHA-3-256 to SHA-3-512.
- For hash based signatures, use XMSS and SPHINCS+.

### Next generation crypto
- Fully homomorphic encryption (FHE) for the cloud or a data processor.

## Conclusion
It is worth reading for anyone in the DevSecOps field.