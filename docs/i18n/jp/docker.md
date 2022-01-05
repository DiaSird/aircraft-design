# Docker

[English](../en/docker.md) | 日本語

![WSLg](../../images/wslg.png)

- [Docker](#docker)
  - [必要なもの](#必要なもの)
  - [開発](#開発)
    - [Docker(WSLg)を使用する場合](#dockerwslgを使用する場合)
    - [Docker(X サーバー)を使用する場合](#dockerx-サーバーを使用する場合)
  - [Make の使い方](#make-の使い方)

## 必要なもの

- Docker(`.devcontainer`を使用する場合)
- WSLg(Windows11 をお使いの場合)または X サーバー。

## 開発

### Docker(WSLg)を使用する場合

1 以下のコマンドでイメージを構築します。

```bash
git clone https://github.com/DiaSird/aircraft-design.git
code aircraft-design
```

2 F1 キーを押し、「`Reopen in Container...」を選択。
少し時間がかかりますので、しばらくお待ちください。

### Docker(X サーバー)を使用する場合

1 以下のコマンドでイメージを構築します。

```bash
git clone https://github.com/DiaSird/aircraft-design.git
cd aircraft-design
make compose-x # create docker-compose.yml for X server
make compose # build
code .
```

2 F1 を押し、「`Reopen in Container...`」を選択します。
少し時間がかかりますので、しばらくお待ちください。

3 X サーバーを起動しておきます。

## Make の使い方

| コマンド           | 説明                                                                    |
| :----------------- | :---------------------------------------------------------------------- |
| `make start`       | python ファイル(デフォルト: `src/1st-sizing/sizeplt-gui.py`) を実行する |
| `make install-dev` | 依存関係のインストール(dev 用)                                          |
| `make install`     | 依存関係のインストール (prod の場合)                                    |
| `make test`        | pytest でテストする。                                                   |
| `make lint`        | pysen を使った Lint                                                     |
| `make lint-fix`    | pysen を使った Lint の修正プログラム                                    |
| `make clean`       | `__pycache__` ファイルを削除                                            |

Windows をお使いの場合、[こちら](http://gnuwin32.sourceforge.net/packages/make.htm)から`make`コマンドをインストールできます。(`setup`ボタンをクリックします)
