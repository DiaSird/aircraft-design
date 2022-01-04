# aircraft-design

English | [日本語](./docs/i18n/jp/readme.md)

Conceptual aircraft design

- [aircraft-design](#aircraft-design)
  - [Requirements](#requirements)
    - [local PC](#local-pc)
    - [Docker](#docker)
  - [development](#development)
  - [Make usage](#make-usage)
  - [License](#license)

## Requirements

### local PC

- Python 3.7 ~ 3.8
- poetry (`pip install poetry`)

### Docker

- Docker(if use `.devcontainer`)
- WSLg(if you use Windows11) or X server.

## development

- when use local PC

```bash
make install-dev
```

---

- when use Docker(WSLg)

  1.The following commands are used to build the image.

```bash
git clone https://github.com/DiaSird/aircraft-design.git
code aircraft-design
```

2.press F1, select `Reopen in Container...`.
Please wait a moment.This is going to take some time.

- when use Docker(X server)

  1.The following commands are used to build the image.

```bash
git clone https://github.com/DiaSird/aircraft-design.git
cd aircraft-design
make compose-x
code .
```

2.press F1, select `Reopen in Container...`.
Please wait a moment.This is going to take some time.

3.Start the X server.

## Make usage

| Command            | Description                                               |
| :----------------- | :-------------------------------------------------------- |
| `make start`       | Run python file(default: `src/1st-sizing/sizeplt-gui.py`) |
| `make install-dev` | Install dependencies (For dev)                            |
| `make install`     | Install dependencies (For prod)                           |
| `make test`        | Test with pytest                                          |
| `make lint`        | Lint with pysen                                           |
| `make lint-fix`    | Lint fix with pysen                                       |
| `make clean`       | Remove `__pycache__` files                                |

If you are using windows, you can install the `make` command
[here](http://gnuwin32.sourceforge.net/packages/make.htm). (Click the `Setup`
button at the top.)

## License

MIT
