


******

Bravo!  You have received a Medical Diploma in Earring from   
the Orbital Convergence University International Air and Water Embassy of the Tangerine Planet.  

You are now officially certified to include "earring" in your practice.

******



# earring


## install
`[ZSH] pip install earring`

## generate keys
```
import earring.modules.ED448.private.creator as ED448_private_key_creator
import earring.modules.ED448.public.creator as ED448_public_key_creator

import pathlib
from os.path import dirname, join, normpath
import os

seed = "4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8"
format = "PEM"

private_key_path = normpath (join (pathlib.Path (__file__).parent.resolve (), "ED448_private_key")) + "." + format
public_key_path = normpath (join (pathlib.Path (__file__).parent.resolve (), "ED448_public_key")) + "." + format

private_key = ED448_private_key_creator.create (seed, format, private_key_path)
private_key_instance = private_key ["instance"]
private_key_string = private_key ["string"]

public_key = ED448_public_key_creator.create (
	private_key_path = private_key_path,
	public_key_path = public_key_path,
	public_key_format = format
)
public_key_instance = public_key ["instance"]
public_key_string = public_key ["string"]
```


## signing and verifying
```
import earring.modules.ED448.sign as sign

unsigned_bytes = b"{}"
signed = sign.start (
	private_key_path = "",
	unsigned_bytes = unsigned_bytes
)

signed_bytes = signed.bytes
```

```
import earring.modules.ED448.verify as verify

unsigned_bytes = b"{}"
signed_bytes = signed.bytes	
	
vouched = vouch.start (
	public_key_path = "",
	
	signed_bytes = signed_bytes,
	unsigned_bytes = unsigned_bytes
)
```