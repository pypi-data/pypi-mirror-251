import typing

import momotor.bundles


class ElementMixinProtocol(typing.Protocol):
    bundle: "momotor.bundles.Bundle"
