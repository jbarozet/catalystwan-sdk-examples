from typing import Literal

from catalystwan.api.configuration_groups.parcel import Global, as_global
from pydantic import BaseModel

Mode = Literal["on", "off"]


class My(BaseModel):
    mode: Global[Mode]


# Wrong =>  m = My(mode="off")
m = My(mode=as_global("off", Mode))
print(m)
