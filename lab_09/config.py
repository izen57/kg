MAIN_COLOUR = "#99ff99"
ADD_COLOUR = "#000000"
CANVAS_COLOUR = "#ffffff"
DEFAULT_COLOUR = "#000000" 

WINDOW_WIDTH = 1520
WINDOW_HEIGHT = 780

# Frame sizes (relative).
BORDERS_PART = 0.03
BORDERS_WIDTH = int(WINDOW_WIDTH * BORDERS_PART)
BORDERS_HEIGHT = int(WINDOW_HEIGHT * BORDERS_PART)

# Number of rows (some kind of grid) for data.
ROWS = 26

DATA_PART_WIDTH = 0.28 - 2 * BORDERS_PART
DATA_PART_HEIGHT = 1 - 2 * BORDERS_PART
DATA_WIDTH = int(DATA_PART_WIDTH * WINDOW_WIDTH)
DATA_HEIGHT = int(DATA_PART_HEIGHT * WINDOW_HEIGHT)
SLOT_HEIGHT = DATA_HEIGHT // ROWS

FIELD_PART_WIDTH = (1 - DATA_PART_WIDTH) - 4 * BORDERS_PART
FIELD_PART_HEIGHT = 1 - 2 * BORDERS_PART
FIELD_WIDTH = int(FIELD_PART_WIDTH * WINDOW_WIDTH)
FIELD_HEIGHT = int(FIELD_PART_HEIGHT * WINDOW_HEIGHT)
CANVAS_CENTER = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2)

FIELD_BORDER_PART = 0.03

INFORMATION = '''\
Здесь должна быть информация.'''