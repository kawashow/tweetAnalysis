# 公式からpython3.7 on alpine linuxイメージをpull
FROM python:3.7-alpine

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

# psycopg2のインストール
RUN apk update \
    && apk add --virtual build-deps python3-dev musl-dev \
    && apk add gcc g++ libstdc++ \
    # && apk add --update libstdc++.so.6 \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    #&& pip install numpy \
    #&& pip install cython \
    #&& pip --no-cache-dir install pandas --no-build-isolation \
    # && pip install pandas \
    && apk del build-deps \
    && apk add git \
    && apk add nodejs npm \
    && apk add vim \
    && apk add --update-cache freetype-dev

#RUN pip install numpy

# Pipenvをインストール
RUN pip install --upgrade pip \
&& pip install pipenv

# ホストのpipfileをコンテナの作業ディレクトリにコピー
COPY ./Pipfile /usr/src/app/Pipfile

# pipfileからパッケージをインストールしてDjango環境を構築
RUN pipenv install --skip-lock --system --dev

# entrypoint.shをコピー
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# ホストのカレントディレクトリ（現在はappディレクトリ）を作業ディレクトリにコピー
COPY . /usr/src/app/

# entrypoint.shを実行
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

