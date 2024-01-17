<h1 align="center">
Herbal TEA

[![Gitlab](https://img.shields.io/badge/gitlab-%23181717.svg?logo=gitlab)](https://gitlab.com/lunardev/herbal)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://gitlab.com/lunardev/herbal/-/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/cpython-3.9%20|%203.10%20|%203.11%20|%203.12-blue.svg)](https://python.org)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://gothub.no-logs.com/psf/black)
[![Pipeline](https://gitlab.com/lunardev/herbal/badges/main/pipeline.svg)](https://gitlab.com/lunardev/herbal/-/pipelines)
[![Code Coverage](https://gitlab.com/lunardev/herbal/badges/main/coverage.svg)](https://gitlab.com/lunardev/herbal/-/commits/main)
</h1>

### Python package for the Tiny Encryption Algorithm (TEA).
> The Tiny Encryption Algorithm (TEA) is a simple and efficient block cipher algorithm.

## Features
- Supports Python 3.9+.
- Simple typed Python API.
- No third-party dependencies.
- Uses [scrypt](https://wikipedia.org/wiki/Scrypt) to derive encryption keys.
- Pads plaintext to allow for input text of any length.

## Installation
```shell
# Latest stable release.
pip install herbal
# Most recent (unstable) release.
pip install git+https://gitlab.com/lunardev/herbal.git
```

## Usage
```python
import herbal

password = "secret"
cipher = herbal.encrypt("example message!", password=password)
plain = herbal.decrypt(cipher, password=password)
print(plain)  # example message!
```

## To-Do
- [x] Implement the Tiny Encryption Algorithm.
- [x] Add plaintext padding.
- [ ] Implement extended algorithms.
  - [ ] XTEA
  - [ ] XXTEA
- [ ] Add error handling for bad data.
- [ ] Add unit tests.
  - [x] Local pytest cases
  - [x] GitLab CI pipeline
  - [x] Code coverage
- [ ] Write documentation.
- [x] Publish project to the [Python Package Index](https://pypi.org/project/herbal).

## References

1. Wheeler, David J.; Needham, Roger M. *TEA, a Tiny Encryption Algorithm*. 16 Dec. 1994 https://link.springer.com/content/pdf/10.1007/3-540-60590-8_29.pdf.
2. Shepherd, Simon. *The Tiny Encryption Algorithm (TEA)*. https://www.tayloredge.com/reference/Mathematics/TEA-XTEA.pdf.
3. Andem, Vikram Reddy. *A Cryptanalysis of the Tiny Encryption Algorithm*, 2003, https://tayloredge.com/reference/Mathematics/VRAndem.pdf.
4. Wikipedia. *Tiny Encryption Algorithm*, 6 Nov. 2023, https://wikipedia.org/wiki/Tiny_Encryption_Algorithm.
5. Fandom. *Tiny Encryption Algorithm*, 24 Sept. 2010, https://antifandom.com/cryptography/wiki/Tiny_Encryption_Algorithm.

## License

This project is licensed under the [MIT License](https://gitlab.com/lunardev/herbal/-/blob/main/LICENSE). Copyright (c) 2024.
