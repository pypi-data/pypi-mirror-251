from typing import Literal, TypedDict
from azure.cosmos.aio import CosmosClient
import haskellian as hk
from ..errors import CosmosHttpResponseError
from .. import KEY, ENDPOINT
from ..util import with_client

ValueOp = TypedDict('ValueOp', {
    'op': Literal['add', 'replace', 'set', 'incr', 'remove'],
    'value': str,
    'path': str
})

def value_op(
    op: Literal['add', 'replace', 'set', 'incr', 'remove'],
    value: str, path: str
) -> ValueOp:
    assert path.startswith('/'), '`path` must start with "/"'
    return dict(op=op, value=value, path=path)

MoveOp = TypedDict('MoveOp', {
    'op': Literal['move'],
    'from': str,
    'path': str
})

def move_op(from_: str, path: str) -> MoveOp:
    assert from_.startswith('/'), '`from` must start with "/"'
    assert path.startswith('/'), '`path` must start with "/"'
    return {"op": "move", "from": from_, "path": path}

Op = ValueOp | MoveOp

def validate(op: Op) -> bool:
    return op.path.startswith('/') and op.get('from', '/').startswith('/')

@with_client
async def item(
    database: str, container: str, id: str, ops: list[Op], partition_key: str | None = None,
    *, client: CosmosClient | None = None, url: str | None = ENDPOINT, key: str | None = KEY,
) -> CosmosHttpResponseError | dict[str]:
    """Partial update (PATCH) a given item. See [Azure's docs](https://learn.microsoft.com/en-us/azure/cosmos-db/partial-document-update) and [python SDK docs](https://learn.microsoft.com/en-us/azure/cosmos-db/partial-document-update-getting-started?tabs=python) for details
    - Returns the patched object"""
    cc = client.get_database_client(database).get_container_client(container)
    try:
        return await cc.patch_item(item=id, partition_key=partition_key or id, patch_operations=ops)
    except (CosmosHttpResponseError) as e:
        return e