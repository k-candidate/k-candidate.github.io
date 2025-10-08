---
layout: post
title: "TIL - OpenSSH - PQC"
date: 2025-10-08 00:00:00-0000
categories: 
---

From [https://www.openssh.com/pq.html](https://www.openssh.com/pq.html):
> OpenSSH has offered post-quantum key agreement (KexAlgorithms) by default since release 9.0 (April 2022), initially via the sntrup761x25519-sha512 algorithm. More recently, in OpenSSH 9.9, we have added a second post-quantum key agreement mlkem768x25519-sha256 and it was made the new default scheme in OpenSSH 10.0 (April 2025).  
To encourage migration to these stronger algorithms, OpenSSH 10.1 will warn the user when a non post-quantum key agreement scheme is selected, with the following message:  
    
    ** WARNING: connection is not using a post-quantum key exchange algorithm.
    ** This session may be vulnerable to "store now, decrypt later" attacks.
    ** The server may need to be upgraded. See https://openssh.com/pq.html

> ...  
Fortunately, quantum computers of sufficient power to break cryptography have not been invented yet. Estimates for when a cryptographically-relevant quantum computer will arrive, based on the rate of progress in the field, range from 5-20 years, with many observers expecting them to arrive in the mid-2030s.  
...  
 OpenSSH has supported post-quantum key agreement to prevent "store now, decrypt later" attacks for several years and it has been the default since OpenSSH-9.0, released in 2022. 

And they proceed to address the 2 important questions:
> I don't believe we'll ever get quantum computers. This is a waste of time  
Some people consider the task of scaling existing quantum computers up to the point where they can tackle cryptographic problems to be practically insurmountable. This is a possibility. However, it appears that most of the barriers to a cryptographically-relevant quantum computer are engineering challenges rather than underlying physics.  
If we're right about quantum computers being practical, then we will have protected vast quantities of user data. If we're wrong about it, then all we'll have done is moved to cryptographic algorithms with stronger mathematical underpinnings. 

> These post-quantum algorithms are new. Are we sure they aren't broken?  
We're wary of this too. Though post-quantum key agreement algorithms have received a lot of concerted cryptographic attention over the last few years, it's possible that new attacks might be found.  
To defend against this happening we have selected post-quantum algorithms with good safety margins. This means that even if they turn out to be weaker than expected they are still likely to be strong enough to be considered fit for purpose.  
Additionally, all the post-quantum algorithms implemented by OpenSSH are "hybrids" that combine a post-quantum algorithm with a classical algorithm. For example mlkem768x25519-sha256 combines ML-KEM, a post-quantum key agreement scheme, with ECDH/x25519, a classical key agreement algorithm that was formerly OpenSSH's preferred default. This ensures that the combined, hybrid algorithm is no worse than the previous best classical algorithm, even if the post-quantum algorithm turns out to be completely broken by future cryptanalysis.

## How did this play out in the past? 
SIKE was a late-stage candidate in the NIST PQC standardization process. It was cracked using a normal CPU on a classical computer. See [https://thequantuminsider.com/2022/08/05/nist-approved-post-quantum-safe-algorithm-cracked-in-an-hour-on-a-pc/](https://thequantuminsider.com/2022/08/05/nist-approved-post-quantum-safe-algorithm-cracked-in-an-hour-on-a-pc/).

I mentioned in a previous post ([https://k-candidate.github.io/2024/11/23/real-world-cryptography-book-takeaways.html](https://k-candidate.github.io/2024/11/23/real-world-cryptography-book-takeaways.html)):  
"_Follow the updated best practices. Be conservative, and use tried and tested cryptography._"

So it might be time to give the company's encryption policy another read, and act accordingly.