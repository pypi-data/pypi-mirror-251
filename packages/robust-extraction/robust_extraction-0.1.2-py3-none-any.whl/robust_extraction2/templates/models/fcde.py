import numpy as np
import ramda as R
from .. import SheetModel, SheetModel2, Template1d, Template1d2

NUM_W = 0.035
BOX_W = 0.139
SPACE_W = 0.027

FCDE2 = SheetModel2(
    cols=Template1d2(
        points=np.cumsum([0, NUM_W, BOX_W, BOX_W, SPACE_W, NUM_W, BOX_W, BOX_W, SPACE_W, NUM_W, BOX_W, BOX_W]),
        a=1, b=12
    ),
    rows=Template1d2(
        points=np.cumsum([0, 1] + R.repeat(1, 25) + [1.8, 0.8]),
        a=1, b=27
    ),
    block_cols=[0, 4, 8]
)

FCDE = SheetModel(
    cols=[
        Template1d(
            offsets=[NUM_W, BOX_W, BOX_W, SPACE_W, NUM_W, BOX_W, BOX_W, SPACE_W, NUM_W, BOX_W, BOX_W],
            importants=[1, 2, 3, 5, 6, 7, 9, 10, 11]
        )
    ],
    min_cols=12,
    rows=[
        Template1d(
            offsets=(27, 1/26),
            importants=(1, 27)
        ),
        Template1d(
            offsets=(26, 1/25),
            importants=(0, 26)
        ),
    ],
    min_rows=26,
    block_cols=[0, 3, 6]
)