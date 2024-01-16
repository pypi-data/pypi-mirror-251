
## Description

Simple use env settings with class type

# install
```
  pip install env-to-class
```

#### import

```python
from env_to_class import Settings
```

#### Description
```text
The library allows you to encrypt your settings stored in json format.
It is possible to convert from a simple storage option to an encrypted one. 
To work with the encrypted version of the settings, you need to pass the startup parameter - the password with which the encryption took place.
Try it, the library is very simple.
```


#### Usage
# Import lib
```python
  required_settings = 'Database.name, Database.user, Database.pwd, Database.host, Clickhouse.host, Clickhouse.user, Clickhouse.pwd'
  settings = Settings(required_settings)

  nameDB = settings.Database.name
  userDB = settings.Database.user
  pwdDb = settings.Database.pwd
  hostDB = settings.Database.host
  clickhouseHost = settings.Clickhouse.host
  clickhousePwd = settings.Clickhouse.pwd
  clickhouseUser = settings.Clickhouse.user
```
