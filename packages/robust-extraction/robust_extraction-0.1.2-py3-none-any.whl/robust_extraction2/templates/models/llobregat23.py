import numpy as np
from .. import SheetModel, SheetModel2, Template1d, Template1d2

BOX_W = 0.23 / 1.05
NUM_W = 0.065 / 1.05

LLOBREGAT2 = SheetModel2(
    cols=Template1d2(
        points=np.cumsum([0, NUM_W, BOX_W, BOX_W, NUM_W, BOX_W, BOX_W]),
        a=1, b=7
    ),
    rows=Template1d2(
        points=np.cumsum([0, 0.8, 1.25, 0.8] + [1 for _ in range(31)] + [2]),
        a=4, b=35
    ),
    block_cols=[0, 3]
)

LLOBREGAT23 = SheetModel(
    cols=[Template1d(
        offsets=[NUM_W, BOX_W, BOX_W, NUM_W, BOX_W, BOX_W],
        importants=(1, 7)
    )],
    min_cols=7,
    rows=[
        Template1d(
            offsets=(34, 1/33),
            importants=(2, 33)
        ),
        Template1d(
            offsets=(33, 1/32),
            importants=(2, 33)
        ),
        Template1d(
            offsets=(32, 1/31),
            importants=(1, 32)
        ),
        Template1d(
            offsets=(31, 1/30),
            importants=(0, 31)
        )
    ],
    min_rows=32, # include top extra line: gets basically always detected
    block_cols=[0, 3]
)
