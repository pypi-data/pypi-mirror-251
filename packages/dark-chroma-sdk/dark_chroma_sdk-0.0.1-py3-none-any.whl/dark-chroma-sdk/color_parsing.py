class DeviceError(Exception):
    pass


def parse_rgb(color):
    if isinstance(color, (list, tuple)) and len(color) == 3:
        if min(color) >= 0 and max(color) <= 255:
            return (int(color[2]) << 16) | (int(color[1]) << 8) | int(color[0])
        else:
            raise DeviceError('Can not parse inserted color')
    else:
        raise DeviceError('Can not parse inserted color')


def parse_hex(color):
    if isinstance(color, str) and 5 < len(color) < 8:
        try:
            return (int(color[-2:], base=16) << 16) | (int(color[-4:-2], base=16) << 8) | int(color[-6:-4], base=16)
        except ValueError:
            raise DeviceError('Can not parse inserted color')
    else:
        raise DeviceError('Can not parse inserted color')
