# Hello CLI

This is a Python CLI app designed to facilitate learning how to configure Python CLI applications.

## 세팅하기

먼저 Poetry로 프로젝트를 시작한다.

```sh
poetry add paikwiki-hello-cli
```

`paikwiki_hello_cli/main.py` 파일을 생성하고, 아래처럼 입력한다.

```py
# main.py
def run():
    print("Hello, World!")

if __name__ == "__main__":
    run()
```

`pyproject.toml`에 아래의 설정을 추가한다.

```toml
[tool.poetry.scripts]
hello = "paikwiki_hello_cli.main:run"
```

터미널에서 가상환경을 시작한다.

```sh
$ poetry shell
Spawning shell within /Users/{USER_NAME}/Library/Caches/pypoetry/virtualenvs/paikwiki-hello-cli-{HASH}-py3.123.12
$ emulate bash -c '. /Users/{USER_NAME}/Library/Caches/pypoetry/virtualenvs/paikwiki-hello-cli-{HASH}-py3.12
3.12/bin/activate'
(hello-cli-py3.12) $
```

아래 명령어로 `paikwiki-hello-cli`를 설치한다.

```sh
poetry install
```

실행이 잘 되는지 테스트한다.

```sh
(paikwiki-hello-cli-py3.12) $ hello
Hello, World!
```

## Deploy

PyPi API 토큰을 설정한다.

```sh
poetry config pypi-token.pypi {API_TOKEN}
```

패키지를 빌드한다.

```sh
$ poetry build
Building paikwiki-hello-cli (0.0.1)
  - Building sdist
  - Built paikwiki_hello_cli-0.0.1.tar.gz
  - Building wheel
  - Built paikwiki_hello_cli-0.0.1-py3-none-any.whl
```

패키지를 배포한다.

```sh
$ poetry publish
```
