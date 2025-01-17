from decimal import Decimal

import pytest
from dataclass_settings import Env, load_settings
from pydantic import BaseModel, ValidationError
from typing_extensions import Annotated

from tests.utils import env_setup


def test_missing_required():
    class Config(BaseModel):
        foo: Annotated[str, Env("FOO")]

    with env_setup({}), pytest.raises(ValidationError):
        load_settings(Config)


def test_has_required_required():
    class Config(BaseModel):
        foo: Annotated[str, Env("FOO")]
        ignoreme: str = "asdf"

    with env_setup({"FOO": "1", "VALUE": "two"}):
        config = load_settings(Config)

    assert config == Config(foo="1", ignoreme="asdf")


def test_nested():
    class Sub(BaseModel):
        foo: Annotated[str, Env("FOO")]

    class Config(BaseModel):
        sub: Sub

    with env_setup({"FOO": "3"}):
        config = load_settings(Config)

    assert config == Config(sub=Sub(foo="3"))


def test_map_int():
    class Config(BaseModel):
        foo: Annotated[int, Env("FOO")]

    with env_setup({"FOO": "3"}):
        config = load_settings(Config)

    assert config == Config(foo=3)


def test_map_decimal():
    class Config(BaseModel):
        foo: Annotated[Decimal, Env("FOO")]

    with env_setup({"FOO": "3"}):
        config = load_settings(Config)

    assert config == Config(foo=Decimal("3"))
