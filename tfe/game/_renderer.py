def render_tile(value):
    if value == 0:
        return "   -"
    return f"{value:4d}"


def render_row(row):
    return " ".join((render_tile(value) for value in row))


def render_tiles(tiles):
    return "\n".join((render_row(row) for row in tiles))
