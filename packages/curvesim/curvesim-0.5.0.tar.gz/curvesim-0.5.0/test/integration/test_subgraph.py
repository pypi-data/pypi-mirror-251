import pytest

from curvesim.exceptions import SubgraphError
from curvesim.network.subgraph import pool_snapshot
from curvesim.network.utils import sync

ZERO_ADDRESS = "0x" + "00" * 20


def test_convex_subgraph_stableswap_snapshot_query():
    """Test the pool snapshot query for stableswap."""

    chain = "mainnet"
    address = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
    end_ts = 1687305600
    _snapshot_sync = sync(pool_snapshot)
    snapshot = _snapshot_sync(address, chain, end_ts=end_ts)
    assert snapshot["address"] == address
    assert snapshot["chain"] == chain

    assert snapshot["timestamp"] <= end_ts

    assert snapshot["version"] == 1

    params = snapshot["params"]
    assert params["A"] > 0

    with pytest.raises(SubgraphError):
        _snapshot_sync(ZERO_ADDRESS, chain)


def test_convex_subgraph_cryptoswap_snapshot_query():
    """Test the pool snapshot query for cryptoswap."""

    chain = "mainnet"
    address = "0x3211C6cBeF1429da3D0d58494938299C92Ad5860"
    end_ts = 1687305600
    _snapshot_sync = sync(pool_snapshot)
    snapshot = _snapshot_sync(address, chain, end_ts=end_ts)
    assert snapshot["address"] == address
    assert snapshot["chain"] == chain

    assert snapshot["timestamp"] <= end_ts

    assert snapshot["version"] == 2

    params = snapshot["params"]
    assert params["A"] > 0
    assert params["gamma"] > 0
