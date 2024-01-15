# Armored

[![test](https://github.com/korawica/armored/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/korawica/armored/actions/workflows/tests.yml)

Armored that implements Model objects for Data Pipeline. The Model objects was
implemented from the Pydantic's `BaseModel` V2.

## Models

### DataTypes Model

```python
from armored.dtypes import StringType

dtype = StringType()
assert dtype.type == "string"
assert dtype.max_length == -1
```

### Constraints Model

```python
from armored.constraints import PrimaryKey

const = PrimaryKey(columns=["foo", "bar"])
assert const.name == "foo_bar_pk"
assert const.columns == ["foo", "bar"]
```

### Catalogs Model

```python
from armored.catalogs import Column

col = Column(name="foo", dtype="varchar( 100 )")
assert "foo", col.name
assert "varchar", col.dtype.type
assert 100, col.dtype.max_length
```

## License

This project was licensed under the terms of the [MIT license](LICENSE).
