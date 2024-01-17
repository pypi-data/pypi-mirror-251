# Python第三方包二次封装

应该会用到一些其他依赖

## 注意

由于oracledb的原因，python版本需要大于3.7

## 封装依赖

```shell
pip install build
pip install twine
pip install pymysql
pip install oracledb
```

## 安装

```shell
pip install pylwr
```

打包与上传

```shell
python -m build
python setup.py sdist bdist_wheel
python -m twine upload dist\*
```
