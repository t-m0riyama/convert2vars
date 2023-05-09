convert2vars
=============

パラメータが埋め込まれた、JSON, YAMLを相互変換するための小さなツールです。
パラメータの処理は、Jinja2テンプレートエンジンの強力な機能が利用できます。

## インストール
```
$ pip install convert2vars
```

## 動作条件

* Python 3.7以降のバージョン

## 使い方

### 基本的な利用方法

以下のシンプルな例は、k8sのDeploymentファイルを変換する例です。
このファイルには、２つのパラメータ（REPLICASとCONTAINER_PORT）が含まれ、-eオプションを使うことで指定した値に変換されます。

``` k8s Deployment sample
$ cat k8s-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: {{ REPLICAS | default(2, True) }}
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: {{ CONTAINER_PORT | default(80, True) }}

$ convert2vars convert -e REPLICAS=4 -e CONTAINER_PORT=8080 -t k8s-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 4
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx:1.14.2
        name: nginx
        ports:
        - containerPort: 8080
```

### パラメータの指定

パラメータの値の指定は以下のような方法があり、複数の方法を組み合わせて利用することも可能です。
* -eオプション
  - 上述のようにコマンドラインオプションで指定します。複数のパラメータを指定することも可能です。
* 環境変数
  - 環境変数をセットした後に、-Eオプションと共に実行することで前述と同じ結果を得ることができます。
  ```
  $ export REPLICAS=4
  $ export CONTAINER_PORT=8080
  $ convert2vars convert -t k8s-deployment.yml -E
  ```
  - --dotenv-fileオプションを指定することで、dotenvファイルを組み合わせて利用することも可能です。
  ```
  $ cat dotenv-temp
  CONTAINER_PORT=8080
  REPLICAS=4
  
  $ convert2vars convert -t k8s-deployment.yml --dotenv-file dotenv-temp -E
  ```
* パラメータファイル
  - パラメータとその値を列挙したファイルを利用することで、多くのパラメータを一括して指定できます。
  - JSON, YAML、ini形式のファイルを利用可能です。以下の３つのパラメータファイルを利用すると、いずれも前述の-eオプションの例と同じ結果が得られます。

  ``` JSON parameter file example 
  ## JSON形式のパラメータファイルの例 (k8s-parameter.json)
  {
  "REPLICAS": 3,
  "CONTAINER_PORT": 8080
  }
  ```

  ``` YAML parameter file example
  ## YAML形式のパラメータファイルの例 (k8s-parameter.yml)
  REPLICAS: 3
  CONTAINER_PORT: 8080
  ```

  ``` ini parameter file example
  ## ini形式のパラメータファイルの例 (k8s-parameter.ini)
  [default]
  REPLICAS=3
  CONTAINER_PORT=8080
  ```
  - パラメータファイルを利用する場合は、-iオプションと-tオプションを合わせて利用します。
  ```
  $ convert2vars convert -t k8s-deployment.yml -i k8s-parameter.json
  ```

### テンプレートエンジンのサポート
Jinja2の提供するフィルタや条件分岐・繰り返しといった機能がそのまま利用できます。以下の例では、明示的にパラメータ値を指定していないため、Jinja2のdefaultフィルタにより、デフォルト値である2と80に変換されます。

```
$ convert2vars convert -t samples/templates/k8s-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx:1.14.2
        name: nginx
        ports:
        - containerPort: 80
```

### フォーマットの変換
JSONとYAMLについては、相互にフォーマットを変換することが可能です。
以下の例では、-fオプションを指定することで、JSONフォーマットに変換しています。
フォーマットの変換を行う場合は-tオプションを利用せず、変換元のファイルをパラメータファイルとして、-iオプションで指定します。

```
$ convert2vars convert -e REPLICAS=4 -e CONTAINER_PORT=8080 -i k8s-deployment.yml -f json | jq .
{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "nginx-deployment"
  },
  "spec": {
    "replicas": 4,
    "template": {
      "metadata": {
        "labels": {
          "app": "nginx"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "nginx",
            "image": "nginx:1.14.2",
            "ports": [
              {
                "containerPort": 8080
              }
            ]
          }
        ]
      }
    }
  }
}
```

## ライセンス
convert2varsは、t-m0riyama(Takeyuki Moriyama)が開発しています。
convert2varsは、MIT licenseでリリースされます。

詳細は、LICENSEファイルをご覧ください。
