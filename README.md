# NEST

nest is a collection of tools. In particular, is a series of small command line tool.

now, it supported tools as:

- [x] `nest w`: Current location weather
- [x] `nest t`: Language translation
- [x] `nest b`: Bytes convert

### install
for install, just use pip:
```
pip install nestall
```
Then, execute on the command line:
```
nest --help
```

### tools
- `nest t`
    **nest t** provide translation service between diffrent languages, you just need to type `nest t <query>` at the command line, like this:


    ```
    > nest t hello
    ---------------------
    你好
    ---------------------
    ```

    type `nest t --help` for more feature！

- `nest w`
    provide weather report, just type `nest w <location>`：
    ```
    > nest w beijing
    beijing: ☀️ +9°C
    ```
- `nest b`
    provide betes and MB and GB covert to each other:
    ```
    > nest b 1024
    bytes: 1024, MB: 1.00, GB: 0.00
    > nest b -m 1024
    bytes: 1048576, MB: 1024.00, GB: 1.00
    > nest b -g 1
    bytes: 1048576, MB: 1024.00, GB: 1.00
    ```
