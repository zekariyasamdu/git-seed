# test objects
REPO_OBJECTS = {
    "testrepo": [{"sha": "abc123", "data": "obj1"}, {"sha": "def456", "data": "obj2"}],
    "testtworepo": [{"sha": "xyz789", "data": "objA"}]
}


# test repo names
REPO_ALLOWLIST = {
    "testrepo": {"127.0.0.1", "192.168.1.100"},
    "testtworepo": {"192.168.1.101"}
}
