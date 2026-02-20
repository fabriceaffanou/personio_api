from dataclasses import dataclass, field
from typing import Dict

import marshmallow


class LinksField(marshmallow.fields.Field):
    def _deserialize(self, value, attr, data, **kwargs) -> Dict[str, str]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise marshmallow.ValidationError("links must be an object/dict")
        out: Dict[str, str] = {}
        for k, v in value.items():
            if isinstance(v, dict) and "href" in v:
                href = v["href"]
                if not isinstance(href, str):
                    raise marshmallow.ValidationError(
                        f"links['{k}'].href must be a string"
                    )
                out[k] = href
            elif isinstance(v, str):
                # allow already-flattened input
                out[k] = v
            else:
                raise marshmallow.ValidationError(
                    f"links['{k}'] must be an object with 'href' or a string"
                )
        return out

    def _serialize(self, value: Dict[str, str], attr, obj, **kwargs):
        if value is None:
            return None
        if not isinstance(value, dict):
            raise marshmallow.ValidationError("internal links must be a dict[str,str]")
        return {k: {"href": v} for k, v in value.items()}


@dataclass
class Meta:
    links: Dict[str, str] = field(metadata={"marshmallow_field": LinksField()})
