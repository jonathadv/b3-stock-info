import json


class JsonSerializer:
    def to_json(self):
        result = {k: v for (k, v) in self.__dict__.items() if not k.startswith("_")}
        return json.dumps(result, sort_keys=False, indent=4, cls=_ComplexEncoder)


class _ComplexEncoder(json.JSONEncoder):
    """ Complex Encoder """

    def default(self, o):  # pylint: disable=method-hidden
        """ Default """

        if hasattr(o, "__dict__"):
            return o.__dict__
        return json.JSONEncoder.default(self, o)
