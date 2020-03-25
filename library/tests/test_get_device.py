def test_get_device_matrix(config_file):
    from plasma import get_device

    device, args = get_device(config_file)
