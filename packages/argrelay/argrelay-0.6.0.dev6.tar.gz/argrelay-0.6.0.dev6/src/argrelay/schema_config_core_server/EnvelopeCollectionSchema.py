from __future__ import annotations

from typing import Callable

from marshmallow import Schema, RAISE, fields, post_load

from argrelay.misc_helper_common.TypeDesc import TypeDesc
from argrelay.runtime_data.EnvelopeCollection import EnvelopeCollection
from argrelay.runtime_data.ServerConfig import ServerConfig
from argrelay.schema_config_interp.DataEnvelopeSchema import data_envelope_desc, mongo_id_
from argrelay.schema_response.FilteredDict import FilteredDict

index_fields_ = "index_fields"
data_envelopes_ = "data_envelopes"


class EnvelopeCollectionSchema(Schema):
    class Meta:
        unknown = RAISE
        strict = True

    index_fields = fields.List(
        fields.String(),
        required = False,
        load_default = [],
    )

    # TODO_00_79_72_55: do not store `data_envelopes`
    data_envelopes = fields.List(
        FilteredDict(
            filtered_keys = [mongo_id_]
        ),
        required = False,
        load_default = [],
    )

    @post_load
    def make_object(
        self,
        input_dict,
        **kwargs,
    ):
        return EnvelopeCollection(
            index_fields = input_dict[index_fields_],
            data_envelopes = input_dict[data_envelopes_],
        )


envelope_collection_desc = TypeDesc(
    dict_schema = EnvelopeCollectionSchema(),
    ref_name = EnvelopeCollectionSchema.__name__,
    dict_example = {
        index_fields_: [
            "SomeTypeA",
            "SomeTypeB",
        ],
        data_envelopes_: [
            data_envelope_desc.dict_example,
        ],
    },
    default_file_path = "",
)


def init_envelop_collections(
    server_config: ServerConfig,
    class_names: list[str],
    get_index_fields: Callable[[str, str], list[str]],
):
    class_to_collection_map: dict = server_config.class_to_collection_map

    for class_name in class_names:
        class_to_collection_map.setdefault(
            class_name,
            class_name,
        )
        collection_name = class_to_collection_map[class_name]
        envelope_collection = server_config.static_data.envelope_collections.setdefault(
            collection_name,
            EnvelopeCollection(
                index_fields = [],
                data_envelopes = [],
            ),
        )

        index_fields = envelope_collection.index_fields
        for index_field in get_index_fields(collection_name, class_name):
            if index_field not in index_fields:
                index_fields.append(index_field)
