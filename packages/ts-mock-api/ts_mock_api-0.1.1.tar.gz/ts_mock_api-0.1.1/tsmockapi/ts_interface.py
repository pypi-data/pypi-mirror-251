import json
import os
import random

from tsmockapi import settings
from tsmockapi.dto.io import Output, OutputBuilder, Input


class TsInterface:
    """This is the API that wraps the software"""

    @staticmethod
    def load() -> None:
        pass

    @staticmethod
    def predict(input: Input) -> Output:
        output = OutputBuilder().with_detections(random.randint(0, 10)).build()
        return output

    @staticmethod
    def validate() -> bool:
        with open(os.path.join(settings.RESOURCE_DIR, 'test.json')) as json_file:
            data = json.load(json_file)
        return data['value'] == 1337


if __name__ == '__main__':
    ts = TsInterface()
    ts.load()
    ts.validate()
    input = Input(product_path='test')
    output = ts.predict(input)
    print(output)
