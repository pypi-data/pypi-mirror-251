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

## token

pypi-AgEIcHlwaS5vcmcCJDc1YWMxMmEwLTkyMzUtNGQyNy1hOTNiLTFiMzkyMDg3NDUyZAACDVsxLFsicHlsd3IiXV0AAixbMixbImU3Zjg5ZGUwLTliYjYtNDE1OS1iYTc3LTExMmQyM2RjNGNlYyJdXQAABiDcvtCmr4Gzde2LY_pNdu5GdSVre2a3ObxQv0KBpZeOoA

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
