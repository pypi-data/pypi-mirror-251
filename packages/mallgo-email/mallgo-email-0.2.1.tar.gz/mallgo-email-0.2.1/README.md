# MallGo Email Service

This is a library developed by the [Inkremental team](https://inkremental.co) in order
to use integrate the mallgo-email-service on django projects.

## Usage

### Install the library

```bash
pip install mallgo-email
```

### Add the library settings to your django project

```python
# settings.py
EMAIL_BACKEND = 'MallGoEmail.backends.MallGoEmailBackend'
MALLGO_PUBLIC_KEY = "YOUR_PUBLIC_KEY"
```

### Django compatibility

| Django version   | Library version   |
|------------------|-------------------|
| 2.0 - <3.0.0     | 0.2.x             |
| 3.0 <=           | 0.3.x             |
