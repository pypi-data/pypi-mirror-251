from typing import Any
from typing import Union

from pydantic import BaseModel
from pydantic import Field

from amsdal_utils.models.data_models.address import Address


class TableSchema(BaseModel):
    address: Address
    columns: list['TableColumnSchema']
    indexed: list['TableIndexSchema'] = Field(default_factory=list)
    unique_columns: list[list[str]] = Field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.address.to_string())


class JsonSchemaModel(BaseModel):
    ...


class NestedSchemaModel(BaseModel):
    properties: dict[
        str, Union['NestedSchemaModel', 'ArraySchemaModel', 'DictSchemaModel', type[JsonSchemaModel], type]
    ]


class ArraySchemaModel(BaseModel):
    item_type: Union['ArraySchemaModel', 'NestedSchemaModel', 'DictSchemaModel', type[JsonSchemaModel], type]


class DictSchemaModel(BaseModel):
    key_type: type
    value_type: Union['DictSchemaModel', 'NestedSchemaModel', 'ArraySchemaModel', type[JsonSchemaModel], type]


class TableColumnSchema(BaseModel):
    name: str
    type: type | NestedSchemaModel | ArraySchemaModel | DictSchemaModel | type[JsonSchemaModel]
    default: Any
    nullable: bool = True


class TableIndexSchema(BaseModel):
    column_name: str
    index_type: str = ''
