### 使用说明

安装打包:
```sh
pip install -U setuptools wheel twine
```

使用打包命令
```sh
python setup.py sdist bdist_wheel
```

上传到PyPI:
```sh
twine upload --repository-url https://upload.pypi.org/legacy/  dist/*
```
注:
去pypi申请账号
注册获取api key 配置好~/.pypirc文件
```sh
twine upload --repository-url https://upload.pypi.org/legacy/ --config-file $HOME/.pypirc dist/*
```
