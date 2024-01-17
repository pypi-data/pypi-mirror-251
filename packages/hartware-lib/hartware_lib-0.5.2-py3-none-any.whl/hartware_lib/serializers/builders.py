from __future__ import annotations

from functools import partial
from typing import Any, Set

from hartware_lib.serializers.main import deserialize, serialize
from hartware_lib.serializers.pandas import (
    pandas_extra_deserializer,
    pandas_extra_serializer,
)
from hartware_lib.types import (
    Deserializer,
    ExtraDeserializer,
    ExtraSerializer,
    Serializer,
)


class SerializerBuilder:
    def __init__(self) -> None:
        self.extra_serializers: Set[ExtraSerializer] = set()

    def with_pandas(self) -> SerializerBuilder:
        self.extra_serializers.add(pandas_extra_serializer)

        return self

    def get(self) -> Serializer:
        return partial(serialize, extra_serializers=list(self.extra_serializers))


class DeserializerBuilder:
    def __init__(self) -> None:
        self.extra_deserializers: Set[ExtraDeserializer] = set()

    def with_pandas(self, *args: Any, **kwargs: Any) -> DeserializerBuilder:
        self.extra_deserializers.add(pandas_extra_deserializer(*args, **kwargs))

        return self

    def get(self) -> Deserializer:
        return partial(deserialize, extra_deserializers=list(self.extra_deserializers))
