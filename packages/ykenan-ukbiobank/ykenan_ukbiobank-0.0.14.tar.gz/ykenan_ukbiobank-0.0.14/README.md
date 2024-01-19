# ykenan_ukbiobank

> upload

```shell
py -m build
twine check dist/*
twine upload dist/*
```

```shell
pip3 install ykenan_ukbiobank
```

```python
from ykenan_ukbiobank import Download

download = Download(
    ukbfetch_file="/mnt/f/software/ukbiobank/ukbfetch",
    bulk_file="/mnt/f/software/ukbiobank/ukb676745.bulk",
    key_file="/mnt/f/software/ukbiobank/k152703r676745.key",
    output_path="/mnt/f/software/ukbiobank/download"
)
download.run()
```

