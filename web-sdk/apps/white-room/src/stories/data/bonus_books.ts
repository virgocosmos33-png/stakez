export default [
 {
  "id": 715,
  "payoutMultiplier": 56620,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     219,
     84,
     139,
     151,
     198
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 10,
    "positions": [
     {
      "reel": 0,
      "row": 2
     },
     {
      "reel": 2,
      "row": 1
     },
     {
      "reel": 3,
      "row": 3
     },
     {
      "reel": 4,
      "row": 4
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 2,
    "name": "HER_SIDE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 10
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     86,
     208,
     78,
     62,
     3
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 7,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "W",
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 8,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 3
    },
    "symbol": "H5",
    "mult": 6,
    "cells": [
     {
      "reel": 0,
      "row": 2,
      "multiplier": 6
     },
     {
      "reel": 2,
      "row": 2,
      "multiplier": 6
     }
    ],
    "totalWays": 13608
   },
   {
    "index": 9,
    "type": "winInfo",
    "totalWin": 3240,
    "wins": [
     {
      "symbol": "H5",
      "kind": 3,
      "win": 3240,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 108,
       "globalMult": 1,
       "winWithoutMult": 3240,
       "symbolMult": 3
      }
     }
    ]
   },
   {
    "index": 10,
    "type": "setWin",
    "amount": 3240,
    "winLevel": 7
   },
   {
    "index": 11,
    "type": "setTotalWin",
    "amount": 3240
   },
   {
    "index": 12,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 10
   },
   {
    "index": 13,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     90,
     161,
     231,
     72,
     245
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 14,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 15,
    "type": "setTotalWin",
    "amount": 3240
   },
   {
    "index": 16,
    "type": "freeSpinRetrigger",
    "totalFs": 13,
    "positions": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 4,
      "row": 1
     }
    ]
   },
   {
    "index": 17,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 13
   },
   {
    "index": 18,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     197,
     48,
     229,
     203,
     43
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 19,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H2"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 3240
   },
   {
    "index": 21,
    "type": "freeSpinRetrigger",
    "totalFs": 16,
    "positions": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 2,
      "row": 1
     }
    ]
   },
   {
    "index": 22,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 16
   },
   {
    "index": 23,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     232,
     162,
     26,
     41,
     236
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 24,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 25,
    "type": "winInfo",
    "totalWin": 110,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 100,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 100,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 10,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 10,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 26,
    "type": "setWin",
    "amount": 110,
    "winLevel": 3
   },
   {
    "index": 27,
    "type": "setTotalWin",
    "amount": 3350
   },
   {
    "index": 28,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 16
   },
   {
    "index": 29,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     177,
     218,
     248,
     8,
     0
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 30,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 31,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 1024
   },
   {
    "index": 32,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 2
    },
    "symbol": "L1",
    "mult": 2,
    "cells": [
     {
      "reel": 0,
      "row": 1,
      "multiplier": 2
     }
    ],
    "totalWays": 1280
   },
   {
    "index": 33,
    "type": "winInfo",
    "totalWin": 220,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 100,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 100,
       "symbolMult": 0
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 50,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 50,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 34,
    "type": "setWin",
    "amount": 220,
    "winLevel": 4
   },
   {
    "index": 35,
    "type": "setTotalWin",
    "amount": 3570
   },
   {
    "index": 36,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 16
   },
   {
    "index": 37,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     66,
     118,
     237,
     167,
     6
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 38,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 3570
   },
   {
    "index": 40,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 16
   },
   {
    "index": 41,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     70,
     7,
     5,
     68,
     152
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 42,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 43,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 44,
    "type": "setTotalWin",
    "amount": 3570
   },
   {
    "index": 45,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 16
   },
   {
    "index": 46,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     199,
     64,
     98,
     49,
     67
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 47,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H3"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 512
   },
   {
    "index": 48,
    "type": "setTotalWin",
    "amount": 3570
   },
   {
    "index": 49,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 16
   },
   {
    "index": 50,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     114,
     197,
     202,
     125,
     28
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     1
    ]
   },
   {
    "index": 51,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     },
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 52,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 6912
   },
   {
    "index": 53,
    "type": "winInfo",
    "totalWin": 50850,
    "wins": [
     {
      "symbol": "H5",
      "kind": 6,
      "win": 36000,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 4,
        "row": 4
       },
       {
        "reel": 5,
        "row": 1
       }
      ],
      "meta": {
       "ways": 48,
       "globalMult": 1,
       "winWithoutMult": 36000,
       "symbolMult": 8
      }
     },
     {
      "symbol": "L2",
      "kind": 6,
      "win": 14400,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 4,
        "row": 2
       },
       {
        "reel": 5,
        "row": 1
       }
      ],
      "meta": {
       "ways": 48,
       "globalMult": 1,
       "winWithoutMult": 14400,
       "symbolMult": 8
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 450,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "ways": 15,
       "globalMult": 1,
       "winWithoutMult": 450,
       "symbolMult": 6
      }
     }
    ]
   },
   {
    "index": 54,
    "type": "setWin",
    "amount": 50850,
    "winLevel": 9
   },
   {
    "index": 55,
    "type": "setTotalWin",
    "amount": 54420
   },
   {
    "index": 56,
    "type": "freeSpinRetrigger",
    "totalFs": 19,
    "positions": [
     {
      "reel": 3,
      "row": 2
     },
     {
      "reel": 4,
      "row": 1
     }
    ]
   },
   {
    "index": 57,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 19
   },
   {
    "index": 58,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     181,
     166,
     7,
     18,
     5
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 59,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 60,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 1
    },
    "from": "H4",
    "to": "H5",
    "cells": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 5,
      "row": 1
     }
    ],
    "totalWays": 384
   },
   {
    "index": 61,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L4",
      "kind": 4,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 62,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 63,
    "type": "setTotalWin",
    "amount": 54450
   },
   {
    "index": 64,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 19
   },
   {
    "index": 65,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     238,
     51,
     220,
     13,
     93
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 66,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 67,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 3
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 68,
    "type": "setTotalWin",
    "amount": 54450
   },
   {
    "index": 69,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 19
   },
   {
    "index": 70,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     226,
     102,
     64,
     190,
     234
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 71,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 72,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 73,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 7,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 4
       }
      ]
     },
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 4,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 3584
   },
   {
    "index": 74,
    "type": "setTotalWin",
    "amount": 54450
   },
   {
    "index": 75,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 19
   },
   {
    "index": 76,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     228,
     166,
     199,
     59,
     104
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 77,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 78,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 79,
    "type": "setTotalWin",
    "amount": 54450
   },
   {
    "index": 80,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 19
   },
   {
    "index": 81,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     69,
     162,
     229,
     132,
     169
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 82,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 432
   },
   {
    "index": 83,
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "H4",
      "kind": 3,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 84,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 85,
    "type": "setTotalWin",
    "amount": 54490
   },
   {
    "index": 86,
    "type": "updateFreeSpin",
    "amount": 14,
    "total": 19
   },
   {
    "index": 87,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     68,
     112,
     235,
     206,
     75
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 88,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     }
    ],
    "totalWays": 432
   },
   {
    "index": 89,
    "type": "winInfo",
    "totalWin": 90,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 50,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 50,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 90,
    "type": "setWin",
    "amount": 90,
    "winLevel": 2
   },
   {
    "index": 91,
    "type": "setTotalWin",
    "amount": 54580
   },
   {
    "index": 92,
    "type": "updateFreeSpin",
    "amount": 15,
    "total": 19
   },
   {
    "index": 93,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     20,
     17,
     178,
     141,
     67
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 94,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 95,
    "type": "setTotalWin",
    "amount": 54580
   },
   {
    "index": 96,
    "type": "updateFreeSpin",
    "amount": 16,
    "total": 19
   },
   {
    "index": 97,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     0,
     41,
     180,
     243,
     207
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 98,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 99,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 4
       },
       {
        "row": 2,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 100,
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 101,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 102,
    "type": "setTotalWin",
    "amount": 54620
   },
   {
    "index": 103,
    "type": "updateFreeSpin",
    "amount": 17,
    "total": 19
   },
   {
    "index": 104,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     27,
     209,
     127,
     29,
     218
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 105,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 106,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 14,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 2
       },
       {
        "row": 3,
        "multiplier": 10
       }
      ]
     },
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 3,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 4032
   },
   {
    "index": 107,
    "type": "winInfo",
    "totalWin": 2000,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 2000,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "ways": 20,
       "globalMult": 1,
       "winWithoutMult": 2000,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 108,
    "type": "setWin",
    "amount": 2000,
    "winLevel": 6
   },
   {
    "index": 109,
    "type": "setTotalWin",
    "amount": 56620
   },
   {
    "index": 110,
    "type": "updateFreeSpin",
    "amount": 18,
    "total": 19
   },
   {
    "index": 111,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     82,
     43,
     20,
     92,
     87
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 112,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 113,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 1
    },
    "from": "L3",
    "to": "H4",
    "cells": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 4,
      "row": 3
     }
    ],
    "totalWays": 288
   },
   {
    "index": 114,
    "type": "setTotalWin",
    "amount": 56620
   },
   {
    "index": 115,
    "type": "freeSpinEnd",
    "amount": 56620,
    "winLevel": 8
   },
   {
    "index": 116,
    "type": "finalWin",
    "amount": 56620
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 566.2
 },
 {
  "id": 370,
  "payoutMultiplier": 1480,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     150,
     18,
     54,
     1,
     178
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 8,
    "positions": [
     {
      "reel": 1,
      "row": 1
     },
     {
      "reel": 2,
      "row": 1
     },
     {
      "reel": 4,
      "row": 4
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 1,
    "name": "THE_INTAKE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     207,
     12,
     149,
     129,
     210
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 5
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 7,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 768
   },
   {
    "index": 8,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 5,
      "cells": [
       {
        "row": 1,
        "multiplier": 3
       },
       {
        "row": 2,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 9,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 10,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 8
   },
   {
    "index": 11,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     93,
     25,
     34,
     177,
     92
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 12,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     }
    ],
    "sides": [],
    "totalWays": 432
   },
   {
    "index": 13,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 1
    },
    "from": "L4",
    "to": "H5",
    "cells": [
     {
      "reel": 3,
      "row": 2
     }
    ],
    "totalWays": 432
   },
   {
    "index": 14,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 15,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 8
   },
   {
    "index": 16,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     241,
     84,
     151,
     82,
     10
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 17,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     }
    ],
    "sides": [],
    "totalWays": 432
   },
   {
    "index": 18,
    "type": "winInfo",
    "totalWin": 260,
    "wins": [
     {
      "symbol": "H5",
      "kind": 5,
      "win": 250,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 3
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 250,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 10,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 10,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 19,
    "type": "setWin",
    "amount": 260,
    "winLevel": 4
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 260
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 8
   },
   {
    "index": 22,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     195,
     214,
     59,
     50,
     60
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 23,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     },
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 640
   },
   {
    "index": 24,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 640
   },
   {
    "index": 25,
    "type": "setTotalWin",
    "amount": 260
   },
   {
    "index": 26,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
   },
   {
    "index": 27,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     18,
     228,
     221,
     53,
     19
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 28,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 29,
    "type": "setTotalWin",
    "amount": 260
   },
   {
    "index": 30,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 8
   },
   {
    "index": 31,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     122,
     19,
     19,
     72,
     34
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 32,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 33,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [],
    "totalWays": 768
   },
   {
    "index": 34,
    "type": "winInfo",
    "totalWin": 900,
    "wins": [
     {
      "symbol": "H4",
      "kind": 5,
      "win": 900,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "ways": 3,
       "globalMult": 1,
       "winWithoutMult": 900,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 35,
    "type": "setWin",
    "amount": 900,
    "winLevel": 5
   },
   {
    "index": 36,
    "type": "setTotalWin",
    "amount": 1160
   },
   {
    "index": 37,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 38,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     110,
     26,
     12,
     200,
     139
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 39,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 720
   },
   {
    "index": 40,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [],
    "totalWays": 960
   },
   {
    "index": 41,
    "type": "winInfo",
    "totalWin": 320,
    "wins": [
     {
      "symbol": "H2",
      "kind": 3,
      "win": 240,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 240,
       "symbolMult": 2
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 80,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 42,
    "type": "setWin",
    "amount": 320,
    "winLevel": 4
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 1480
   },
   {
    "index": 44,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 45,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     26,
     193,
     25,
     5,
     60
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 46,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 512
   },
   {
    "index": 47,
    "type": "setTotalWin",
    "amount": 1480
   },
   {
    "index": 48,
    "type": "freeSpinEnd",
    "amount": 1480,
    "winLevel": 4
   },
   {
    "index": 49,
    "type": "finalWin",
    "amount": 1480
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 14.8
 },
 {
  "id": 506,
  "payoutMultiplier": 1530,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     99,
     18,
     248,
     153,
     240
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 1,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "H5",
      "kind": 3,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 30
   },
   {
    "index": 4,
    "type": "freeSpinTrigger",
    "totalFs": 12,
    "positions": [
     {
      "reel": 0,
      "row": 4
     },
     {
      "reel": 1,
      "row": 1
     },
     {
      "reel": 2,
      "row": 1
     },
     {
      "reel": 3,
      "row": 1
     },
     {
      "reel": 4,
      "row": 2
     }
    ]
   },
   {
    "index": 5,
    "type": "bonusLevel",
    "level": 3,
    "name": "WHITEOUT",
    "startHaunted": []
   },
   {
    "index": 6,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 12
   },
   {
    "index": 7,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     124,
     83,
     164,
     92,
     216
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 8,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 9,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 3
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 10,
    "type": "winInfo",
    "totalWin": 80,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 80,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 11,
    "type": "setWin",
    "amount": 80,
    "winLevel": 2
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 110
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 12
   },
   {
    "index": 14,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     97,
     162,
     103,
     37,
     137
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 15,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 16,
    "type": "setTotalWin",
    "amount": 110
   },
   {
    "index": 17,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 12
   },
   {
    "index": 18,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     223,
     43,
     106,
     78,
     46
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 19,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 20,
    "type": "winInfo",
    "totalWin": 320,
    "wins": [
     {
      "symbol": "H2",
      "kind": 3,
      "win": 120,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 120,
       "symbolMult": 0
      }
     },
     {
      "symbol": "H4",
      "kind": 4,
      "win": 200,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 200,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 21,
    "type": "setWin",
    "amount": 320,
    "winLevel": 4
   },
   {
    "index": 22,
    "type": "setTotalWin",
    "amount": 430
   },
   {
    "index": 23,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 12
   },
   {
    "index": 24,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     89,
     200,
     179,
     95,
     123
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 25,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H1"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 26,
    "type": "setTotalWin",
    "amount": 430
   },
   {
    "index": 27,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 12
   },
   {
    "index": 28,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     193,
     217,
     42,
     4,
     57
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 29,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 30,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 4
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 31,
    "type": "setTotalWin",
    "amount": 430
   },
   {
    "index": 32,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 12
   },
   {
    "index": 33,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     31,
     60,
     94,
     227,
     14
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 34,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 480
   },
   {
    "index": 35,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 36,
    "type": "setTotalWin",
    "amount": 430
   },
   {
    "index": 37,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 12
   },
   {
    "index": 38,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     235,
     108,
     79,
     139,
     18
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 39,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H2"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 5184
   },
   {
    "index": 40,
    "type": "winInfo",
    "totalWin": 370,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 50,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 50,
       "symbolMult": 0
      }
     },
     {
      "symbol": "H5",
      "kind": 4,
      "win": 320,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 3,
        "row": 1
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 320,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 41,
    "type": "setWin",
    "amount": 370,
    "winLevel": 4
   },
   {
    "index": 42,
    "type": "setTotalWin",
    "amount": 800
   },
   {
    "index": 43,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 12
   },
   {
    "index": 44,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     204,
     108,
     217,
     201,
     16
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 45,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 3
       },
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 46,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 6144
   },
   {
    "index": 47,
    "type": "winInfo",
    "totalWin": 660,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 300,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 6,
       "globalMult": 1,
       "winWithoutMult": 300,
       "symbolMult": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 240,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 6,
       "globalMult": 1,
       "winWithoutMult": 240,
       "symbolMult": 6
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 120,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 120,
       "symbolMult": 6
      }
     }
    ]
   },
   {
    "index": 48,
    "type": "setWin",
    "amount": 660,
    "winLevel": 5
   },
   {
    "index": 49,
    "type": "setTotalWin",
    "amount": 1460
   },
   {
    "index": 50,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 12
   },
   {
    "index": 51,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     248,
     130,
     65,
     216,
     101
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 52,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "left",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 53,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 4,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 54,
    "type": "winInfo",
    "totalWin": 10,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 10,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 10,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 55,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 56,
    "type": "setTotalWin",
    "amount": 1470
   },
   {
    "index": 57,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 12
   },
   {
    "index": 58,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     117,
     40,
     14,
     181,
     143
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 59,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 1024
   },
   {
    "index": 60,
    "type": "setTotalWin",
    "amount": 1470
   },
   {
    "index": 61,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 12
   },
   {
    "index": 62,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     232,
     103,
     39,
     174,
     226
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 63,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 64,
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 50,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 50,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 10,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 10,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 65,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 66,
    "type": "setTotalWin",
    "amount": 1530
   },
   {
    "index": 67,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 12
   },
   {
    "index": 68,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     82,
     175,
     80,
     225,
     120
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 69,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 5
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "W",
        "multiplier": 5
       }
      ]
     }
    ],
    "totalWays": 8640
   },
   {
    "index": 70,
    "type": "setTotalWin",
    "amount": 1530
   },
   {
    "index": 71,
    "type": "freeSpinEnd",
    "amount": 1500,
    "winLevel": 4
   },
   {
    "index": 72,
    "type": "finalWin",
    "amount": 1530
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.3,
  "freeGameWins": 15.0
 },
 {
  "id": 813,
  "payoutMultiplier": 420,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     47,
     189,
     124,
     68,
     238
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 8,
    "positions": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 4,
      "row": 4
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 1,
    "name": "THE_INTAKE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     238,
     247,
     115,
     99,
     202
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 7,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 2,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 8,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 9,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 8
   },
   {
    "index": 10,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     123,
     146,
     25,
     151,
     185
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 11,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 576
   },
   {
    "index": 12,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 3,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 13,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 14,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 8
   },
   {
    "index": 15,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     79,
     152,
     58,
     112,
     127
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 16,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 17,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 18,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 8
   },
   {
    "index": 19,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     153,
     32,
     180,
     219,
     148
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 20,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 21,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 22,
    "type": "winInfo",
    "totalWin": 120,
    "wins": [
     {
      "symbol": "L2",
      "kind": 4,
      "win": 120,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 3,
       "globalMult": 1,
       "winWithoutMult": 120,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 23,
    "type": "setWin",
    "amount": 120,
    "winLevel": 3
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 120
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
   },
   {
    "index": 26,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     223,
     109,
     223,
     241,
     45
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 27,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 28,
    "type": "setTotalWin",
    "amount": 120
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 8
   },
   {
    "index": 30,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     169,
     66,
     185,
     107,
     15
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 31,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 432
   },
   {
    "index": 32,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 9,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 6
       }
      ]
     }
    ],
    "totalWays": 1296
   },
   {
    "index": 33,
    "type": "winInfo",
    "totalWin": 180,
    "wins": [
     {
      "symbol": "H5",
      "kind": 3,
      "win": 180,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 6,
       "globalMult": 1,
       "winWithoutMult": 180,
       "symbolMult": 6
      }
     }
    ]
   },
   {
    "index": 34,
    "type": "setWin",
    "amount": 180,
    "winLevel": 3
   },
   {
    "index": 35,
    "type": "setTotalWin",
    "amount": 300
   },
   {
    "index": 36,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 37,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     197,
     23,
     167,
     45,
     157
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 38,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 300
   },
   {
    "index": 40,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 41,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     241,
     130,
     23,
     4,
     85
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 42,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 2
       },
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     },
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 43,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 1152
   },
   {
    "index": 44,
    "type": "winInfo",
    "totalWin": 120,
    "wins": [
     {
      "symbol": "L3",
      "kind": 4,
      "win": 120,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 120,
       "symbolMult": 4
      }
     }
    ]
   },
   {
    "index": 45,
    "type": "setWin",
    "amount": 120,
    "winLevel": 3
   },
   {
    "index": 46,
    "type": "setTotalWin",
    "amount": 420
   },
   {
    "index": 47,
    "type": "freeSpinEnd",
    "amount": 420,
    "winLevel": 2
   },
   {
    "index": 48,
    "type": "finalWin",
    "amount": 420
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 4.2
 },
 {
  "id": 896,
  "payoutMultiplier": 2270,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     173,
     17,
     54,
     197,
     201
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 12,
    "positions": [
     {
      "reel": 0,
      "row": 4
     },
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 2,
      "row": 1
     },
     {
      "reel": 3,
      "row": 1
     },
     {
      "reel": 4,
      "row": 1
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 3,
    "name": "WHITEOUT",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 12
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     3,
     240,
     35,
     228,
     144
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 1024
   },
   {
    "index": 7,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 8,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 12
   },
   {
    "index": 9,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     126,
     121,
     174,
     4,
     212
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 10,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 720
   },
   {
    "index": 11,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 14400
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 12
   },
   {
    "index": 14,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     92,
     218,
     139,
     65,
     81
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 15,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 16,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 2
    },
    "from": "L4",
    "to": "H5",
    "cells": [
     {
      "reel": 3,
      "row": 2
     },
     {
      "reel": 4,
      "row": 2
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 17,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L5",
      "kind": 4,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 18,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 19,
    "type": "setTotalWin",
    "amount": 30
   },
   {
    "index": 20,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 12
   },
   {
    "index": 21,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     239,
     15,
     91,
     128,
     23
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 22,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 23,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 5,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 1280
   },
   {
    "index": 24,
    "type": "winInfo",
    "totalWin": 960,
    "wins": [
     {
      "symbol": "L3",
      "kind": 5,
      "win": 960,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 3
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 960,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 25,
    "type": "setWin",
    "amount": 960,
    "winLevel": 5
   },
   {
    "index": 26,
    "type": "setTotalWin",
    "amount": 990
   },
   {
    "index": 27,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 12
   },
   {
    "index": 28,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     142,
     82,
     233,
     227,
     44
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 29,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 30,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 3
       },
       {
        "row": 2,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 31,
    "type": "setTotalWin",
    "amount": 990
   },
   {
    "index": 32,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 12
   },
   {
    "index": 33,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     36,
     219,
     134,
     247,
     167
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 34,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 35,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 5
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 4032
   },
   {
    "index": 36,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 8,
      "cells": [
       {
        "row": 1,
        "multiplier": 4
       },
       {
        "row": 2,
        "multiplier": 2
       },
       {
        "row": 3,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 10752
   },
   {
    "index": 37,
    "type": "setTotalWin",
    "amount": 990
   },
   {
    "index": 38,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 12
   },
   {
    "index": 39,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     245,
     209,
     41,
     61,
     224
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 40,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 2592
   },
   {
    "index": 41,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 15,
      "cells": [
       {
        "row": 1,
        "multiplier": 6
       },
       {
        "row": 2,
        "multiplier": 3
       },
       {
        "row": 3,
        "multiplier": 6
       }
      ]
     },
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 3,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 19440
   },
   {
    "index": 42,
    "type": "setTotalWin",
    "amount": 990
   },
   {
    "index": 43,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 12
   },
   {
    "index": 44,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     109,
     185,
     11,
     227,
     139
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 45,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 46,
    "type": "setTotalWin",
    "amount": 990
   },
   {
    "index": 47,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 12
   },
   {
    "index": 48,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     53,
     239,
     30,
     199,
     164
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 49,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 50,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 1
    },
    "symbol": "L3",
    "mult": 4,
    "cells": [
     {
      "reel": 0,
      "row": 2,
      "multiplier": 4
     },
     {
      "reel": 1,
      "row": 2,
      "multiplier": 4
     },
     {
      "reel": 2,
      "row": 1,
      "multiplier": 4
     },
     {
      "reel": 2,
      "row": 2,
      "multiplier": 4
     }
    ],
    "totalWays": 6048
   },
   {
    "index": 51,
    "type": "winInfo",
    "totalWin": 1280,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 1280,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 128,
       "globalMult": 1,
       "winWithoutMult": 1280,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 52,
    "type": "setWin",
    "amount": 1280,
    "winLevel": 5
   },
   {
    "index": 53,
    "type": "setTotalWin",
    "amount": 2270
   },
   {
    "index": 54,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 12
   },
   {
    "index": 55,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     196,
     246,
     102,
     106,
     26
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 56,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 2592
   },
   {
    "index": 57,
    "type": "setTotalWin",
    "amount": 2270
   },
   {
    "index": 58,
    "type": "freeSpinRetrigger",
    "totalFs": 15,
    "positions": [
     {
      "reel": 0,
      "row": 2
     },
     {
      "reel": 1,
      "row": 3
     },
     {
      "reel": 4,
      "row": 3
     }
    ]
   },
   {
    "index": 59,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 15
   },
   {
    "index": 60,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     215,
     63,
     56,
     204,
     206
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 61,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 62,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 3,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 432
   },
   {
    "index": 63,
    "type": "setTotalWin",
    "amount": 2270
   },
   {
    "index": 64,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 15
   },
   {
    "index": 65,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     196,
     200,
     222,
     192,
     92
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 66,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 2592
   },
   {
    "index": 67,
    "type": "setTotalWin",
    "amount": 2270
   },
   {
    "index": 68,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 15
   },
   {
    "index": 69,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     162,
     42,
     11,
     99,
     200
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 70,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 71,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 4,
      "cells": [
       {
        "row": 1,
        "multiplier": 3
       },
       {
        "row": 2,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 72,
    "type": "setTotalWin",
    "amount": 2270
   },
   {
    "index": 73,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 15
   },
   {
    "index": 74,
    "type": "reveal",
    "board": [
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     198,
     15,
     50,
     38,
     82
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 75,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H1"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 5184
   },
   {
    "index": 76,
    "type": "setTotalWin",
    "amount": 2270
   },
   {
    "index": 77,
    "type": "updateFreeSpin",
    "amount": 14,
    "total": 15
   },
   {
    "index": 78,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     217,
     106,
     232,
     181,
     45
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 79,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 80,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 5,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 2
       },
       {
        "row": 3,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 81,
    "type": "setTotalWin",
    "amount": 2270
   },
   {
    "index": 82,
    "type": "freeSpinEnd",
    "amount": 2270,
    "winLevel": 5
   },
   {
    "index": 83,
    "type": "finalWin",
    "amount": 2270
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 22.7
 },
 {
  "id": 254,
  "payoutMultiplier": 4380,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     149,
     113,
     124,
     196,
     13
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     1
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 8,
    "positions": [
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 3,
      "row": 2
     },
     {
      "reel": 4,
      "row": 3
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 1,
    "name": "THE_INTAKE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     17,
     136,
     37,
     90,
     204
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 7,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 3
       }
      ]
     },
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 2,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 8,
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L5",
      "kind": 4,
      "win": 60,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 60,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 9,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 10,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 11,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 8
   },
   {
    "index": 12,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     94,
     143,
     55,
     156,
     244
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 13,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 14,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 15,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 4,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 16,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 3
    },
    "symbol": "L3",
    "mult": 4,
    "cells": [
     {
      "reel": 0,
      "row": 2,
      "multiplier": 4
     },
     {
      "reel": 2,
      "row": 1,
      "multiplier": 8
     },
     {
      "reel": 2,
      "row": 2,
      "multiplier": 8
     }
    ],
    "totalWays": 5376
   },
   {
    "index": 17,
    "type": "winInfo",
    "totalWin": 640,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 640,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 64,
       "globalMult": 1,
       "winWithoutMult": 640,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 18,
    "type": "setWin",
    "amount": 640,
    "winLevel": 5
   },
   {
    "index": 19,
    "type": "setTotalWin",
    "amount": 700
   },
   {
    "index": 20,
    "type": "freeSpinRetrigger",
    "totalFs": 11,
    "positions": [
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 3,
      "row": 2
     },
     {
      "reel": 4,
      "row": 2
     }
    ]
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 11
   },
   {
    "index": 22,
    "type": "reveal",
    "board": [
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     121,
     100,
     140,
     51,
     47
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 23,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 24,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 1
    },
    "symbol": "L2",
    "mult": 2,
    "cells": [
     {
      "reel": 0,
      "row": 1,
      "multiplier": 2
     },
     {
      "reel": 1,
      "row": 3,
      "multiplier": 2
     },
     {
      "reel": 2,
      "row": 2,
      "multiplier": 2
     },
     {
      "reel": 3,
      "row": 2,
      "multiplier": 2
     }
    ],
    "totalWays": 1200
   },
   {
    "index": 25,
    "type": "winInfo",
    "totalWin": 640,
    "wins": [
     {
      "symbol": "L2",
      "kind": 4,
      "win": 640,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 16,
       "globalMult": 1,
       "winWithoutMult": 640,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 26,
    "type": "setWin",
    "amount": 640,
    "winLevel": 5
   },
   {
    "index": 27,
    "type": "setTotalWin",
    "amount": 1340
   },
   {
    "index": 28,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 11
   },
   {
    "index": 29,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     183,
     145,
     107,
     178,
     202
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 30,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 480
   },
   {
    "index": 31,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 480
   },
   {
    "index": 32,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 1
    },
    "from": "L1",
    "to": "H4",
    "cells": [
     {
      "reel": 3,
      "row": 2
     }
    ],
    "totalWays": 480
   },
   {
    "index": 33,
    "type": "setTotalWin",
    "amount": 1340
   },
   {
    "index": 34,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 11
   },
   {
    "index": 35,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     210,
     70,
     142,
     196,
     249
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 36,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [],
    "totalWays": 512
   },
   {
    "index": 37,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 9,
      "cells": [
       {
        "row": 1,
        "multiplier": 3
       },
       {
        "row": 2,
        "multiplier": 6
       }
      ]
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 38,
    "type": "winInfo",
    "totalWin": 1500,
    "wins": [
     {
      "symbol": "H5",
      "kind": 5,
      "win": 1500,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 1
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "ways": 6,
       "globalMult": 1,
       "winWithoutMult": 1500,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 39,
    "type": "setWin",
    "amount": 1500,
    "winLevel": 6
   },
   {
    "index": 40,
    "type": "setTotalWin",
    "amount": 2840
   },
   {
    "index": 41,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 11
   },
   {
    "index": 42,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     196,
     101,
     212,
     99,
     116
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 43,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 44,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 864
   },
   {
    "index": 45,
    "type": "setTotalWin",
    "amount": 2840
   },
   {
    "index": 46,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 11
   },
   {
    "index": 47,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     5,
     170,
     202,
     154,
     189
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 48,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H1"
     }
    ],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 49,
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 50,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 51,
    "type": "setTotalWin",
    "amount": 2880
   },
   {
    "index": 52,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 11
   },
   {
    "index": 53,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     111,
     47,
     3,
     169,
     138
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 54,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 768
   },
   {
    "index": 55,
    "type": "setTotalWin",
    "amount": 2880
   },
   {
    "index": 56,
    "type": "freeSpinRetrigger",
    "totalFs": 14,
    "positions": [
     {
      "reel": 1,
      "row": 3
     },
     {
      "reel": 4,
      "row": 1
     }
    ]
   },
   {
    "index": 57,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 14
   },
   {
    "index": 58,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     62,
     35,
     63,
     129,
     173
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 59,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 60,
    "type": "setTotalWin",
    "amount": 2880
   },
   {
    "index": 61,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 14
   },
   {
    "index": 62,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     210,
     153,
     202,
     242,
     205
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 63,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 64,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 576
   },
   {
    "index": 65,
    "type": "winInfo",
    "totalWin": 240,
    "wins": [
     {
      "symbol": "L2",
      "kind": 5,
      "win": 240,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 240,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 66,
    "type": "setWin",
    "amount": 240,
    "winLevel": 4
   },
   {
    "index": 67,
    "type": "setTotalWin",
    "amount": 3120
   },
   {
    "index": 68,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 14
   },
   {
    "index": 69,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     201,
     16,
     138,
     182,
     155
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 70,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H3"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 512
   },
   {
    "index": 71,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 2,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 512
   },
   {
    "index": 72,
    "type": "setTotalWin",
    "amount": 3120
   },
   {
    "index": 73,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 14
   },
   {
    "index": 74,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     33,
     190,
     85,
     134,
     145
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 75,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 76,
    "type": "setTotalWin",
    "amount": 3120
   },
   {
    "index": 77,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 14
   },
   {
    "index": 78,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     190,
     216,
     106,
     101,
     144
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 79,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [],
    "totalWays": 768
   },
   {
    "index": 80,
    "type": "winInfo",
    "totalWin": 1260,
    "wins": [
     {
      "symbol": "H4",
      "kind": 5,
      "win": 300,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 1
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 300,
       "symbolMult": 0
      }
     },
     {
      "symbol": "H5",
      "kind": 4,
      "win": 960,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 3,
        "row": 1
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 960,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 81,
    "type": "setWin",
    "amount": 1260,
    "winLevel": 5
   },
   {
    "index": 82,
    "type": "setTotalWin",
    "amount": 4380
   },
   {
    "index": 83,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 14
   },
   {
    "index": 84,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     188,
     58,
     221,
     205,
     181
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 85,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [],
    "totalWays": 512
   },
   {
    "index": 86,
    "type": "setTotalWin",
    "amount": 4380
   },
   {
    "index": 87,
    "type": "freeSpinEnd",
    "amount": 4380,
    "winLevel": 5
   },
   {
    "index": 88,
    "type": "finalWin",
    "amount": 4380
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 43.8
 },
 {
  "id": 351,
  "payoutMultiplier": 1280,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     175,
     17,
     138,
     151,
     121
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 12,
    "positions": [
     {
      "reel": 0,
      "row": 2
     },
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 3,
      "row": 3
     },
     {
      "reel": 4,
      "row": 1
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 3,
    "name": "WHITEOUT",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 12
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     229,
     14,
     112,
     111,
     41
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 7,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 2
    },
    "symbol": "L1",
    "mult": 2,
    "cells": [
     {
      "reel": 0,
      "row": 2,
      "multiplier": 2
     },
     {
      "reel": 0,
      "row": 4,
      "multiplier": 2
     },
     {
      "reel": 1,
      "row": 3,
      "multiplier": 2
     },
     {
      "reel": 2,
      "row": 1,
      "multiplier": 2
     },
     {
      "reel": 3,
      "row": 1,
      "multiplier": 2
     }
    ],
    "totalWays": 5760
   },
   {
    "index": 8,
    "type": "winInfo",
    "totalWin": 1280,
    "wins": [
     {
      "symbol": "L1",
      "kind": 4,
      "win": 1280,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 32,
       "globalMult": 1,
       "winWithoutMult": 1280,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 9,
    "type": "setWin",
    "amount": 1280,
    "winLevel": 5
   },
   {
    "index": 10,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 11,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 12
   },
   {
    "index": 12,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     17,
     210,
     207,
     191,
     91
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 13,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H1"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 14,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 15,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 12
   },
   {
    "index": 16,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     222,
     5,
     244,
     7,
     165
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 17,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 18,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 3,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 19,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 20,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 12
   },
   {
    "index": 21,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     113,
     184,
     148,
     150,
     231
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 22,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 23,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 3
    },
    "from": "L5",
    "to": "H3",
    "cells": [
     {
      "reel": 1,
      "row": 2
     }
    ],
    "totalWays": 576
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 12
   },
   {
    "index": 26,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     10,
     12,
     161,
     140,
     191
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 27,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 28,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 12
   },
   {
    "index": 30,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     115,
     192,
     40,
     19,
     169
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 31,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "left",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 32,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 33,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 12
   },
   {
    "index": 34,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     75,
     61,
     214,
     80,
     182
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 35,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 36,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 4,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     },
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 11,
      "cells": [
       {
        "row": 1,
        "multiplier": 4
       },
       {
        "row": 2,
        "multiplier": 5
       },
       {
        "row": 3,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 4224
   },
   {
    "index": 37,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 38,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 12
   },
   {
    "index": 39,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     77,
     233,
     137,
     12,
     107
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 40,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 41,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H1"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 42,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 43,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 12
   },
   {
    "index": 44,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     215,
     136,
     55,
     25,
     153
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 45,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 46,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 47,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 12
   },
   {
    "index": 48,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     240,
     75,
     138,
     201,
     145
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 49,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H1"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 50,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 51,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 12
   },
   {
    "index": 52,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     85,
     146,
     173,
     91,
     182
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 53,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 54,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 55,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 12
   },
   {
    "index": 56,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     185,
     190,
     57,
     180,
     159
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 57,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "left",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 58,
    "type": "setTotalWin",
    "amount": 1280
   },
   {
    "index": 59,
    "type": "freeSpinEnd",
    "amount": 1280,
    "winLevel": 4
   },
   {
    "index": 60,
    "type": "finalWin",
    "amount": 1280
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 12.8
 },
 {
  "id": 798,
  "payoutMultiplier": 4160,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     45,
     35,
     18,
     151,
     199
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 10,
    "positions": [
     {
      "reel": 0,
      "row": 3
     },
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 3,
      "row": 3
     },
     {
      "reel": 4,
      "row": 3
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 2,
    "name": "HER_SIDE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 10
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     104,
     206,
     137,
     3,
     0
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 7,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 8,
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 9,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 10,
    "type": "setTotalWin",
    "amount": 40
   },
   {
    "index": 11,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 10
   },
   {
    "index": 12,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     6,
     55,
     174,
     162,
     194
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 13,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 5
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 14,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 3456
   },
   {
    "index": 15,
    "type": "setTotalWin",
    "amount": 40
   },
   {
    "index": 16,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 10
   },
   {
    "index": 17,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     221,
     197,
     10,
     144,
     240
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 18,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "W",
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 19,
    "type": "setTotalWin",
    "amount": 40
   },
   {
    "index": 20,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 10
   },
   {
    "index": 21,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     118,
     242,
     38,
     22,
     105
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 22,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H2"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 23,
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 20,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 20,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 24,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 25,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 26,
    "type": "freeSpinRetrigger",
    "totalFs": 13,
    "positions": [
     {
      "reel": 0,
      "row": 3
     },
     {
      "reel": 3,
      "row": 3
     }
    ]
   },
   {
    "index": 27,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 13
   },
   {
    "index": 28,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     233,
     47,
     165,
     29,
     220
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 29,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 30,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 11,
      "cells": [
       {
        "row": 1,
        "multiplier": 6
       },
       {
        "row": 2,
        "multiplier": 5
       }
      ]
     }
    ],
    "totalWays": 1584
   },
   {
    "index": 31,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 32,
    "type": "freeSpinRetrigger",
    "totalFs": 16,
    "positions": [
     {
      "reel": 1,
      "row": 3
     },
     {
      "reel": 4,
      "row": 2
     }
    ]
   },
   {
    "index": 33,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 16
   },
   {
    "index": 34,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     45,
     22,
     216,
     196,
     176
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 35,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 36,
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L2",
      "kind": 4,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 37,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 38,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 39,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 16
   },
   {
    "index": 40,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     186,
     239,
     108,
     162,
     243
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 41,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 480
   },
   {
    "index": 42,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H1"
       }
      ]
     }
    ],
    "totalWays": 960
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 44,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 16
   },
   {
    "index": 45,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     53,
     192,
     107,
     81,
     97
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 46,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 47,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 48,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 49,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 16
   },
   {
    "index": 50,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     30,
     173,
     189,
     102,
     11
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 51,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 52,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 1024
   },
   {
    "index": 53,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 54,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 16
   },
   {
    "index": 55,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     210,
     94,
     121,
     124,
     3
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     1
    ]
   },
   {
    "index": 56,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H1"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 57,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 5
       },
       {
        "row": 2,
        "multiplier": 1
       }
      ]
     },
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 7,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 2
       },
       {
        "row": 3,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 4032
   },
   {
    "index": 58,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 59,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 16
   },
   {
    "index": 60,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     79,
     157,
     32,
     117,
     107
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 61,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     }
    ],
    "sides": [],
    "totalWays": 576
   },
   {
    "index": 62,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 63,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 16
   },
   {
    "index": 64,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     190,
     175,
     98,
     160,
     112
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 65,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 66,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 67,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 16
   },
   {
    "index": 68,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     22,
     22,
     136,
     151,
     113
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 69,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 70,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 1
    },
    "from": "H1",
    "to": "H5",
    "cells": [
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 4,
      "row": 3
     }
    ],
    "totalWays": 864
   },
   {
    "index": 71,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 72,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 16
   },
   {
    "index": 73,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     71,
     21,
     113,
     129,
     191
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 74,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H3"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 75,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 2
    },
    "symbol": "L4",
    "mult": 4,
    "cells": [
     {
      "reel": 0,
      "row": 1,
      "multiplier": 4
     },
     {
      "reel": 0,
      "row": 4,
      "multiplier": 4
     },
     {
      "reel": 1,
      "row": 2,
      "multiplier": 4
     },
     {
      "reel": 2,
      "row": 2,
      "multiplier": 4
     }
    ],
    "totalWays": 16800
   },
   {
    "index": 76,
    "type": "winInfo",
    "totalWin": 1280,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1280,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 128,
       "globalMult": 1,
       "winWithoutMult": 1280,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 77,
    "type": "setWin",
    "amount": 1280,
    "winLevel": 5
   },
   {
    "index": 78,
    "type": "setTotalWin",
    "amount": 1380
   },
   {
    "index": 79,
    "type": "updateFreeSpin",
    "amount": 14,
    "total": 16
   },
   {
    "index": 80,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     24,
     47,
     98,
     119,
     100
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 81,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 82,
    "type": "setTotalWin",
    "amount": 1380
   },
   {
    "index": 83,
    "type": "updateFreeSpin",
    "amount": 15,
    "total": 16
   },
   {
    "index": 84,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     64,
     144,
     42,
     96,
     242
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 85,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     },
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 86,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 87,
    "type": "winInfo",
    "totalWin": 2700,
    "wins": [
     {
      "symbol": "H4",
      "kind": 6,
      "win": 2700,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 4,
        "row": 1
       },
       {
        "reel": 5,
        "row": 1
       }
      ],
      "meta": {
       "ways": 3,
       "globalMult": 1,
       "winWithoutMult": 2700,
       "symbolMult": 3
      }
     }
    ]
   },
   {
    "index": 88,
    "type": "setWin",
    "amount": 2700,
    "winLevel": 6
   },
   {
    "index": 89,
    "type": "setTotalWin",
    "amount": 4080
   },
   {
    "index": 90,
    "type": "freeSpinRetrigger",
    "totalFs": 19,
    "positions": [
     {
      "reel": 1,
      "row": 1
     },
     {
      "reel": 4,
      "row": 4
     }
    ]
   },
   {
    "index": 91,
    "type": "updateFreeSpin",
    "amount": 16,
    "total": 19
   },
   {
    "index": 92,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     155,
     239,
     213,
     116,
     198
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 93,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 94,
    "type": "setTotalWin",
    "amount": 4080
   },
   {
    "index": 95,
    "type": "updateFreeSpin",
    "amount": 17,
    "total": 19
   },
   {
    "index": 96,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     51,
     115,
     132,
     171,
     151
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 97,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 98,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H1"
       }
      ]
     }
    ],
    "totalWays": 2048
   },
   {
    "index": 99,
    "type": "winInfo",
    "totalWin": 80,
    "wins": [
     {
      "symbol": "H5",
      "kind": 3,
      "win": 60,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 60,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 20,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 20,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 100,
    "type": "setWin",
    "amount": 80,
    "winLevel": 2
   },
   {
    "index": 101,
    "type": "setTotalWin",
    "amount": 4160
   },
   {
    "index": 102,
    "type": "updateFreeSpin",
    "amount": 18,
    "total": 19
   },
   {
    "index": 103,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     106,
     10,
     198,
     74,
     240
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 104,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 105,
    "type": "setTotalWin",
    "amount": 4160
   },
   {
    "index": 106,
    "type": "freeSpinEnd",
    "amount": 4160,
    "winLevel": 5
   },
   {
    "index": 107,
    "type": "finalWin",
    "amount": 4160
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 41.6
 },
 {
  "id": 83,
  "payoutMultiplier": 2110,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     46,
     102,
     184,
     195,
     238
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 10,
    "positions": [
     {
      "reel": 0,
      "row": 2
     },
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 3,
      "row": 3
     },
     {
      "reel": 4,
      "row": 4
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 2,
    "name": "HER_SIDE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 10
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     240,
     121,
     11,
     131,
     207
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 7,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 8,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 10
   },
   {
    "index": 9,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     69,
     30,
     232,
     187,
     26
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 10,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 10
       }
      ]
     }
    ],
    "totalWays": 1248
   },
   {
    "index": 11,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 3328
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 10
   },
   {
    "index": 14,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     157,
     236,
     48,
     40,
     67
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 15,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 10
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 4224
   },
   {
    "index": 16,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 4
       }
      ]
     }
    ],
    "totalWays": 12672
   },
   {
    "index": 17,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 18,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 10
   },
   {
    "index": 19,
    "type": "reveal",
    "board": [
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     121,
     218,
     56,
     152,
     65
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 20,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H2"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 21,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 1
    },
    "symbol": "L2",
    "mult": 2,
    "cells": [
     {
      "reel": 0,
      "row": 1,
      "multiplier": 2
     },
     {
      "reel": 1,
      "row": 2,
      "multiplier": 2
     },
     {
      "reel": 3,
      "row": 2,
      "multiplier": 2
     },
     {
      "reel": 4,
      "row": 2,
      "multiplier": 2
     }
    ],
    "totalWays": 3000
   },
   {
    "index": 22,
    "type": "winInfo",
    "totalWin": 1920,
    "wins": [
     {
      "symbol": "L2",
      "kind": 5,
      "win": 1920,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 16,
       "globalMult": 1,
       "winWithoutMult": 1920,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 23,
    "type": "setWin",
    "amount": 1920,
    "winLevel": 6
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 1920
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 10
   },
   {
    "index": 26,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     73,
     155,
     90,
     228,
     231
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 27,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 28,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 3
    },
    "from": "L3",
    "to": "H3",
    "cells": [
     {
      "reel": 0,
      "row": 3
     },
     {
      "reel": 1,
      "row": 1
     }
    ],
    "totalWays": 768
   },
   {
    "index": 29,
    "type": "winInfo",
    "totalWin": 140,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 100,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 100,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 30,
    "type": "setWin",
    "amount": 140,
    "winLevel": 3
   },
   {
    "index": 31,
    "type": "setTotalWin",
    "amount": 2060
   },
   {
    "index": 32,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 10
   },
   {
    "index": 33,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     127,
     0,
     103,
     2,
     221
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 34,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 35,
    "type": "setTotalWin",
    "amount": 2060
   },
   {
    "index": 36,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 10
   },
   {
    "index": 37,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     232,
     140,
     45,
     33,
     211
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 38,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 2060
   },
   {
    "index": 40,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 10
   },
   {
    "index": 41,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     48,
     91,
     88,
     4,
     237
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 42,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 2060
   },
   {
    "index": 44,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 10
   },
   {
    "index": 45,
    "type": "reveal",
    "board": [
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     198,
     238,
     142,
     30,
     152
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 46,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 47,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 2,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 48,
    "type": "winInfo",
    "totalWin": 50,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 50,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 50,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 49,
    "type": "setWin",
    "amount": 50,
    "winLevel": 2
   },
   {
    "index": 50,
    "type": "setTotalWin",
    "amount": 2110
   },
   {
    "index": 51,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 10
   },
   {
    "index": 52,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     40,
     98,
     120,
     30,
     119
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 53,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 54,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 9,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 6
       }
      ]
     }
    ],
    "totalWays": 2592
   },
   {
    "index": 55,
    "type": "setTotalWin",
    "amount": 2110
   },
   {
    "index": 56,
    "type": "freeSpinEnd",
    "amount": 2110,
    "winLevel": 5
   },
   {
    "index": 57,
    "type": "finalWin",
    "amount": 2110
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 21.1
 },
 {
  "id": 307,
  "payoutMultiplier": 42050,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     176,
     81,
     125,
     197,
     198
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 12,
    "positions": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 1,
      "row": 1
     },
     {
      "reel": 2,
      "row": 1
     },
     {
      "reel": 3,
      "row": 1
     },
     {
      "reel": 4,
      "row": 4
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 3,
    "name": "WHITEOUT",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 12
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     156,
     101,
     106,
     137,
     233
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 7,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 8,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 9,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 12
   },
   {
    "index": 10,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     89,
     186,
     21,
     233,
     147
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 11,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 12
   },
   {
    "index": 14,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     234,
     97,
     79,
     212,
     237
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 15,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 16,
    "type": "winInfo",
    "totalWin": 3000,
    "wins": [
     {
      "symbol": "H5",
      "kind": 6,
      "win": 3000,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 1
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 4,
        "row": 3
       },
       {
        "reel": 5,
        "row": 1
       },
       {
        "reel": 5,
        "row": 2
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 3000,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 17,
    "type": "setWin",
    "amount": 3000,
    "winLevel": 7
   },
   {
    "index": 18,
    "type": "setTotalWin",
    "amount": 3000
   },
   {
    "index": 19,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 12
   },
   {
    "index": 20,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     166,
     83,
     66,
     180,
     63
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 21,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H1"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 22,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L3",
      "kind": 4,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 23,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 3030
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 12
   },
   {
    "index": 26,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     181,
     191,
     213,
     109,
     46
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 27,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 480
   },
   {
    "index": 28,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 29,
    "type": "setTotalWin",
    "amount": 3030
   },
   {
    "index": 30,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 12
   },
   {
    "index": 31,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     118,
     80,
     23,
     172,
     228
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 32,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "left",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 33,
    "type": "setTotalWin",
    "amount": 3030
   },
   {
    "index": 34,
    "type": "freeSpinRetrigger",
    "totalFs": 15,
    "positions": [
     {
      "reel": 0,
      "row": 3
     },
     {
      "reel": 2,
      "row": 2
     }
    ]
   },
   {
    "index": 35,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 15
   },
   {
    "index": 36,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     155,
     82,
     133,
     144,
     215
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 37,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 38,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 5,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 2
       },
       {
        "row": 3,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 480
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 3030
   },
   {
    "index": 40,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 15
   },
   {
    "index": 41,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     27,
     4,
     216,
     73,
     242
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 42,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 3030
   },
   {
    "index": 44,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 15
   },
   {
    "index": 45,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     185,
     153,
     172,
     193,
     72
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 46,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 47,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 2
    },
    "symbol": "L3",
    "mult": 2,
    "cells": [
     {
      "reel": 0,
      "row": 4,
      "multiplier": 2
     },
     {
      "reel": 1,
      "row": 3,
      "multiplier": 2
     },
     {
      "reel": 2,
      "row": 2,
      "multiplier": 2
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 48,
    "type": "winInfo",
    "totalWin": 80,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 80,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 49,
    "type": "setWin",
    "amount": 80,
    "winLevel": 2
   },
   {
    "index": 50,
    "type": "setTotalWin",
    "amount": 3110
   },
   {
    "index": 51,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 15
   },
   {
    "index": 52,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     86,
     229,
     55,
     60,
     32
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 53,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H3"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 2
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 54,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 4
       }
      ]
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 55,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "H5",
      "kind": 3,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 56,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 57,
    "type": "setTotalWin",
    "amount": 3140
   },
   {
    "index": 58,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 15
   },
   {
    "index": 59,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     93,
     82,
     61,
     212,
     100
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 60,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 10
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 2
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 10368
   },
   {
    "index": 61,
    "type": "setTotalWin",
    "amount": 3140
   },
   {
    "index": 62,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 15
   },
   {
    "index": 63,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     158,
     238,
     110,
     207,
     59
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 64,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 65,
    "type": "setTotalWin",
    "amount": 3140
   },
   {
    "index": 66,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 15
   },
   {
    "index": 67,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     112,
     71,
     53,
     112,
     11
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 68,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 69,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 70,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 11,
      "cells": [
       {
        "row": 1,
        "multiplier": 6
       },
       {
        "row": 2,
        "multiplier": 4
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     },
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 5,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 2
       },
       {
        "row": 3,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 7040
   },
   {
    "index": 71,
    "type": "winInfo",
    "totalWin": 360,
    "wins": [
     {
      "symbol": "H5",
      "kind": 3,
      "win": 360,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 360,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 72,
    "type": "setWin",
    "amount": 360,
    "winLevel": 4
   },
   {
    "index": 73,
    "type": "setTotalWin",
    "amount": 3500
   },
   {
    "index": 74,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 15
   },
   {
    "index": 75,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     33,
     29,
     66,
     194,
     18
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 76,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 2048
   },
   {
    "index": 77,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L3",
      "kind": 4,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 78,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 79,
    "type": "setTotalWin",
    "amount": 3530
   },
   {
    "index": 80,
    "type": "updateFreeSpin",
    "amount": 14,
    "total": 15
   },
   {
    "index": 81,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     90,
     164,
     134,
     124,
     224
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 82,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 83,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 5,
      "cells": [
       {
        "row": 1,
        "multiplier": 3
       },
       {
        "row": 2,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 2880
   },
   {
    "index": 84,
    "type": "setTotalWin",
    "amount": 3530
   },
   {
    "index": 85,
    "type": "freeSpinRetrigger",
    "totalFs": 18,
    "positions": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 2,
      "row": 1
     },
     {
      "reel": 3,
      "row": 3
     }
    ]
   },
   {
    "index": 86,
    "type": "updateFreeSpin",
    "amount": 15,
    "total": 18
   },
   {
    "index": 87,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     154,
     58,
     84,
     244,
     107
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 88,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 10
       }
      ]
     },
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 2496
   },
   {
    "index": 89,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H2"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 7488
   },
   {
    "index": 90,
    "type": "winInfo",
    "totalWin": 36000,
    "wins": [
     {
      "symbol": "H1",
      "kind": 5,
      "win": 36000,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "ways": 36,
       "globalMult": 1,
       "winWithoutMult": 36000,
       "symbolMult": 13
      }
     }
    ]
   },
   {
    "index": 91,
    "type": "setWin",
    "amount": 36000,
    "winLevel": 9
   },
   {
    "index": 92,
    "type": "setTotalWin",
    "amount": 39530
   },
   {
    "index": 93,
    "type": "updateFreeSpin",
    "amount": 16,
    "total": 18
   },
   {
    "index": 94,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     110,
     213,
     64,
     30,
     156
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 95,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "left",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 96,
    "type": "setTotalWin",
    "amount": 39530
   },
   {
    "index": 97,
    "type": "updateFreeSpin",
    "amount": 17,
    "total": 18
   },
   {
    "index": 98,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     17,
     195,
     51,
     231,
     98
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 99,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 100,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "left",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 101,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 1
    },
    "symbol": "H3",
    "mult": 5,
    "cells": [
     {
      "reel": 0,
      "row": 4,
      "multiplier": 5
     },
     {
      "reel": 1,
      "row": 3,
      "multiplier": 5
     }
    ],
    "totalWays": 8064
   },
   {
    "index": 102,
    "type": "winInfo",
    "totalWin": 2520,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 2500,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 50,
       "globalMult": 1,
       "winWithoutMult": 2500,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 20,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 20,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 103,
    "type": "setWin",
    "amount": 2520,
    "winLevel": 6
   },
   {
    "index": 104,
    "type": "setTotalWin",
    "amount": 42050
   },
   {
    "index": 105,
    "type": "freeSpinEnd",
    "amount": 42050,
    "winLevel": 7
   },
   {
    "index": 106,
    "type": "finalWin",
    "amount": 42050
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 420.5
 },
 {
  "id": 306,
  "payoutMultiplier": 280,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     172,
     192,
     18,
     197,
     120
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     1
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 8,
    "positions": [
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 3,
      "row": 1
     },
     {
      "reel": 4,
      "row": 2
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 1,
    "name": "THE_INTAKE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     173,
     222,
     214,
     11,
     32
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 7,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 8,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 8
   },
   {
    "index": 9,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     130,
     16,
     215,
     40,
     80
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 10,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 720
   },
   {
    "index": 11,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 720
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 8
   },
   {
    "index": 14,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     64,
     194,
     36,
     152,
     112
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 15,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 720
   },
   {
    "index": 16,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 720
   },
   {
    "index": 17,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 3
    },
    "from": "L4",
    "to": "H2",
    "cells": [
     {
      "reel": 4,
      "row": 1
     }
    ],
    "totalWays": 720
   },
   {
    "index": 18,
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 19,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 40
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 8
   },
   {
    "index": 22,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     73,
     153,
     234,
     202,
     189
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 23,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 40
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
   },
   {
    "index": 26,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     189,
     65,
     18,
     164,
     150
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 27,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 28,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 2
    },
    "from": "L2",
    "to": "H4",
    "cells": [
     {
      "reel": 0,
      "row": 2
     }
    ],
    "totalWays": 384
   },
   {
    "index": 29,
    "type": "setTotalWin",
    "amount": 40
   },
   {
    "index": 30,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 8
   },
   {
    "index": 31,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     231,
     80,
     25,
     35,
     67
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 32,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 33,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 576
   },
   {
    "index": 34,
    "type": "winInfo",
    "totalWin": 90,
    "wins": [
     {
      "symbol": "L4",
      "kind": 4,
      "win": 90,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 3,
       "globalMult": 1,
       "winWithoutMult": 90,
       "symbolMult": 3
      }
     }
    ]
   },
   {
    "index": 35,
    "type": "setWin",
    "amount": 90,
    "winLevel": 2
   },
   {
    "index": 36,
    "type": "setTotalWin",
    "amount": 130
   },
   {
    "index": 37,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 38,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     98,
     177,
     240,
     71,
     15
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 39,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H2"
     }
    ],
    "sides": [],
    "totalWays": 432
   },
   {
    "index": 40,
    "type": "winInfo",
    "totalWin": 150,
    "wins": [
     {
      "symbol": "H2",
      "kind": 4,
      "win": 150,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 150,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 41,
    "type": "setWin",
    "amount": 150,
    "winLevel": 3
   },
   {
    "index": 42,
    "type": "setTotalWin",
    "amount": 280
   },
   {
    "index": 43,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 44,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     236,
     232,
     221,
     119,
     49
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 45,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 46,
    "type": "setTotalWin",
    "amount": 280
   },
   {
    "index": 47,
    "type": "freeSpinEnd",
    "amount": 280,
    "winLevel": 2
   },
   {
    "index": 48,
    "type": "finalWin",
    "amount": 280
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 2.8
 },
 {
  "id": 588,
  "payoutMultiplier": 6120,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     233,
     80,
     184,
     27,
     64
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 10,
    "positions": [
     {
      "reel": 0,
      "row": 2
     },
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 4,
      "row": 2
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 2,
    "name": "HER_SIDE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 10
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     170,
     130,
     35,
     44,
     69
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "W",
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 1296
   },
   {
    "index": 7,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 14,
      "cells": [
       {
        "row": 1,
        "multiplier": 3
       },
       {
        "row": 2,
        "multiplier": 6
       },
       {
        "row": 3,
        "multiplier": 5
       }
      ]
     }
    ],
    "totalWays": 6048
   },
   {
    "index": 8,
    "type": "winInfo",
    "totalWin": 1200,
    "wins": [
     {
      "symbol": "H4",
      "kind": 4,
      "win": 1200,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 1200,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 9,
    "type": "setWin",
    "amount": 1200,
    "winLevel": 5
   },
   {
    "index": 10,
    "type": "setTotalWin",
    "amount": 1200
   },
   {
    "index": 11,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 10
   },
   {
    "index": 12,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     219,
     102,
     205,
     125,
     125
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 13,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 864
   },
   {
    "index": 14,
    "type": "setTotalWin",
    "amount": 1200
   },
   {
    "index": 15,
    "type": "freeSpinRetrigger",
    "totalFs": 13,
    "positions": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 3,
      "row": 2
     }
    ]
   },
   {
    "index": 16,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 13
   },
   {
    "index": 17,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     50,
     114,
     20,
     72,
     58
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 18,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 432
   },
   {
    "index": 19,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 3
    },
    "from": "L4",
    "to": "H4",
    "cells": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 0,
      "row": 2
     },
     {
      "reel": 4,
      "row": 1
     },
     {
      "reel": 4,
      "row": 4
     }
    ],
    "totalWays": 432
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 1200
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 13
   },
   {
    "index": 22,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     141,
     62,
     94,
     58,
     63
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 23,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 1200
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 13
   },
   {
    "index": 26,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     110,
     96,
     179,
     5,
     24
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 27,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 28,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 13,
      "cells": [
       {
        "row": 1,
        "multiplier": 5
       },
       {
        "row": 2,
        "multiplier": 4
       },
       {
        "row": 3,
        "multiplier": 4
       }
      ]
     }
    ],
    "totalWays": 1248
   },
   {
    "index": 29,
    "type": "winInfo",
    "totalWin": 640,
    "wins": [
     {
      "symbol": "L2",
      "kind": 4,
      "win": 640,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 16,
       "globalMult": 1,
       "winWithoutMult": 640,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 30,
    "type": "setWin",
    "amount": 640,
    "winLevel": 5
   },
   {
    "index": 31,
    "type": "setTotalWin",
    "amount": 1840
   },
   {
    "index": 32,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 13
   },
   {
    "index": 33,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     90,
     108,
     30,
     64,
     109
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 34,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 35,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 36,
    "type": "setTotalWin",
    "amount": 1840
   },
   {
    "index": 37,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 13
   },
   {
    "index": 38,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     89,
     181,
     211,
     198,
     163
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 39,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 40,
    "type": "setTotalWin",
    "amount": 1840
   },
   {
    "index": 41,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 13
   },
   {
    "index": 42,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     145,
     181,
     240,
     84,
     72
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 43,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 44,
    "type": "setTotalWin",
    "amount": 1840
   },
   {
    "index": 45,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 13
   },
   {
    "index": 46,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     225,
     60,
     186,
     176,
     198
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 47,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 48,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 1
    },
    "from": "L4",
    "to": "H4",
    "cells": [
     {
      "reel": 1,
      "row": 1
     },
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 1,
      "row": 3
     },
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 3,
      "row": 1
     },
     {
      "reel": 3,
      "row": 3
     },
     {
      "reel": 4,
      "row": 4
     }
    ],
    "totalWays": 768
   },
   {
    "index": 49,
    "type": "setTotalWin",
    "amount": 1840
   },
   {
    "index": 50,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 13
   },
   {
    "index": 51,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     87,
     60,
     75,
     197,
     110
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 52,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 53,
    "type": "setTotalWin",
    "amount": 1840
   },
   {
    "index": 54,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 13
   },
   {
    "index": 55,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     89,
     175,
     146,
     192,
     107
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 56,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 57,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 4,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 2
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 58,
    "type": "winInfo",
    "totalWin": 3200,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 200,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 200,
       "symbolMult": 2
      }
     },
     {
      "symbol": "H5",
      "kind": 6,
      "win": 3000,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 4,
        "row": 3
       },
       {
        "reel": 5,
        "row": 1
       },
       {
        "reel": 5,
        "row": 2
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 3000,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 59,
    "type": "setWin",
    "amount": 3200,
    "winLevel": 7
   },
   {
    "index": 60,
    "type": "setTotalWin",
    "amount": 5040
   },
   {
    "index": 61,
    "type": "freeSpinRetrigger",
    "totalFs": 16,
    "positions": [
     {
      "reel": 0,
      "row": 2
     },
     {
      "reel": 2,
      "row": 1
     }
    ]
   },
   {
    "index": 62,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 16
   },
   {
    "index": 63,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     71,
     129,
     130,
     180,
     185
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 64,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 65,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 3,
      "cells": [
       {
        "row": 1,
        "multiplier": 1
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 66,
    "type": "winInfo",
    "totalWin": 80,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 80,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 67,
    "type": "setWin",
    "amount": 80,
    "winLevel": 2
   },
   {
    "index": 68,
    "type": "setTotalWin",
    "amount": 5120
   },
   {
    "index": 69,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 16
   },
   {
    "index": 70,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     80,
     156,
     101,
     32,
     132
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 71,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 72,
    "type": "setTotalWin",
    "amount": 5120
   },
   {
    "index": 73,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 16
   },
   {
    "index": 74,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     60,
     45,
     6,
     98,
     44
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 75,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H3"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 3
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 76,
    "type": "setTotalWin",
    "amount": 5120
   },
   {
    "index": 77,
    "type": "updateFreeSpin",
    "amount": 14,
    "total": 16
   },
   {
    "index": 78,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     161,
     114,
     143,
     158,
     121
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 79,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 80,
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L2",
      "kind": 4,
      "win": 40,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 81,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 82,
    "type": "setTotalWin",
    "amount": 5160
   },
   {
    "index": 83,
    "type": "updateFreeSpin",
    "amount": 15,
    "total": 16
   },
   {
    "index": 84,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     147,
     83,
     167,
     124,
     71
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     1
    ]
   },
   {
    "index": 85,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 2
       },
       {
        "row": 4,
        "multiplier": 10
       }
      ]
     }
    ],
    "totalWays": 2016
   },
   {
    "index": 86,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 8064
   },
   {
    "index": 87,
    "type": "winInfo",
    "totalWin": 960,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 120,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 120,
       "symbolMult": 12
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 120,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 120,
       "symbolMult": 12
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 720,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 24,
       "globalMult": 1,
       "winWithoutMult": 720,
       "symbolMult": 12
      }
     }
    ]
   },
   {
    "index": 88,
    "type": "setWin",
    "amount": 960,
    "winLevel": 5
   },
   {
    "index": 89,
    "type": "setTotalWin",
    "amount": 6120
   },
   {
    "index": 90,
    "type": "freeSpinEnd",
    "amount": 6120,
    "winLevel": 6
   },
   {
    "index": 91,
    "type": "finalWin",
    "amount": 6120
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 61.2
 },
 {
  "id": 184,
  "payoutMultiplier": 140,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     175,
     216,
     197,
     181,
     240
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 8,
    "positions": [
     {
      "reel": 0,
      "row": 2
     },
     {
      "reel": 2,
      "row": 1
     },
     {
      "reel": 4,
      "row": 2
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 1,
    "name": "THE_INTAKE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     53,
     192,
     220,
     97,
     66
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H3"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [],
    "totalWays": 576
   },
   {
    "index": 7,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 8,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 8
   },
   {
    "index": 9,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     33,
     31,
     228,
     47,
     47
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 10,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 11,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H1"
     }
    ],
    "sides": [],
    "totalWays": 512
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 8
   },
   {
    "index": 14,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     166,
     59,
     23,
     219,
     207
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 15,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 16,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 17,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 8
   },
   {
    "index": 18,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     42,
     144,
     182,
     107,
     85
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 19,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [],
    "totalWays": 432
   },
   {
    "index": 20,
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L3",
      "kind": 4,
      "win": 60,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 1
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 60,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 21,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 22,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 23,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
   },
   {
    "index": 24,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     79,
     249,
     15,
     24,
     70
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     1
    ]
   },
   {
    "index": 25,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 26,
    "type": "winInfo",
    "totalWin": 80,
    "wins": [
     {
      "symbol": "L3",
      "kind": 5,
      "win": 80,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 3
       },
       {
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 27,
    "type": "setWin",
    "amount": 80,
    "winLevel": 2
   },
   {
    "index": 28,
    "type": "setTotalWin",
    "amount": 140
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 8
   },
   {
    "index": 30,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     182,
     47,
     67,
     180,
     198
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 31,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 32,
    "type": "setTotalWin",
    "amount": 140
   },
   {
    "index": 33,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 34,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     150,
     15,
     37,
     144,
     84
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 35,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 288
   },
   {
    "index": 36,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 1
    },
    "from": "L1",
    "to": "H2",
    "cells": [
     {
      "reel": 0,
      "row": 3
     },
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 4,
      "row": 2
     },
     {
      "reel": 4,
      "row": 4
     }
    ],
    "totalWays": 288
   },
   {
    "index": 37,
    "type": "setTotalWin",
    "amount": 140
   },
   {
    "index": 38,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 39,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     238,
     215,
     97,
     234,
     17
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 40,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 41,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 1,
    "unlocked": [
     "bottom"
    ],
    "bottom": [],
    "sides": [],
    "totalWays": 384
   },
   {
    "index": 42,
    "type": "setTotalWin",
    "amount": 140
   },
   {
    "index": 43,
    "type": "freeSpinEnd",
    "amount": 140,
    "winLevel": 2
   },
   {
    "index": 44,
    "type": "finalWin",
    "amount": 140
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 1.4
 },
 {
  "id": 249,
  "payoutMultiplier": 3980,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     164,
     80,
     53,
     195,
     119
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 10,
    "positions": [
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 3,
      "row": 3
     },
     {
      "reel": 4,
      "row": 3
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 2,
    "name": "HER_SIDE",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 10
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     108,
     173,
     48,
     237,
     120
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 3
       },
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 1008
   },
   {
    "index": 7,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 3024
   },
   {
    "index": 8,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 3
    },
    "from": "L1",
    "to": "H5",
    "cells": [
     {
      "reel": 0,
      "row": 4
     },
     {
      "reel": 4,
      "row": 1
     },
     {
      "reel": 4,
      "row": 2
     }
    ],
    "totalWays": 3024
   },
   {
    "index": 9,
    "type": "winInfo",
    "totalWin": 600,
    "wins": [
     {
      "symbol": "H3",
      "kind": 4,
      "win": 600,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 5,
       "globalMult": 1,
       "winWithoutMult": 600,
       "symbolMult": 5
      }
     }
    ]
   },
   {
    "index": 10,
    "type": "setWin",
    "amount": 600,
    "winLevel": 5
   },
   {
    "index": 11,
    "type": "setTotalWin",
    "amount": 600
   },
   {
    "index": 12,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 10
   },
   {
    "index": 13,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     248,
     91,
     209,
     198,
     54
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 14,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 15,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 2,
      "mode": "normal",
      "baseRows": 2,
      "reelWays": 4,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 2
       }
      ]
     },
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 6,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 3
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 16,
    "type": "setTotalWin",
    "amount": 600
   },
   {
    "index": 17,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 10
   },
   {
    "index": 18,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     49,
     188,
     235,
     239,
     145
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 19,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 2,
      "baseRows": 2,
      "added": 2,
      "cells": [
       {
        "row": 3,
        "multiplier": 1
       },
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 720
   },
   {
    "index": 20,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 21,
    "type": "setTotalWin",
    "amount": 600
   },
   {
    "index": 22,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 10
   },
   {
    "index": 23,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     163,
     178,
     23,
     48,
     170
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 24,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 25,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 2
    },
    "from": "H5",
    "to": "H2",
    "cells": [
     {
      "reel": 4,
      "row": 4
     }
    ],
    "totalWays": 576
   },
   {
    "index": 26,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 1
    },
    "symbol": "H1",
    "mult": 3,
    "cells": [
     {
      "reel": 0,
      "row": 1,
      "multiplier": 3
     },
     {
      "reel": 1,
      "row": 2,
      "multiplier": 3
     },
     {
      "reel": 2,
      "row": 1,
      "multiplier": 3
     }
    ],
    "totalWays": 2880
   },
   {
    "index": 27,
    "type": "winInfo",
    "totalWin": 2700,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 2700,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "ways": 27,
       "globalMult": 1,
       "winWithoutMult": 2700,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 28,
    "type": "setWin",
    "amount": 2700,
    "winLevel": 6
   },
   {
    "index": 29,
    "type": "setTotalWin",
    "amount": 3300
   },
   {
    "index": 30,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 10
   },
   {
    "index": 31,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     202,
     34,
     10,
     38,
     92
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 32,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 33,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 2
    },
    "from": "H2",
    "to": "H5",
    "cells": [
     {
      "reel": 2,
      "row": 2
     }
    ],
    "totalWays": 576
   },
   {
    "index": 34,
    "type": "setTotalWin",
    "amount": 3300
   },
   {
    "index": 35,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 10
   },
   {
    "index": 36,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     214,
     66,
     142,
     103,
     191
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 37,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 38,
    "type": "splitSymbols",
    "label": "Split",
    "cell": {
     "reel": 3
    },
    "symbol": "H3",
    "mult": 2,
    "cells": [
     {
      "reel": 0,
      "row": 4,
      "multiplier": 2
     },
     {
      "reel": 2,
      "row": 2,
      "multiplier": 2
     }
    ],
    "totalWays": 1080
   },
   {
    "index": 39,
    "type": "winInfo",
    "totalWin": 200,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 200,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 200,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 40,
    "type": "setWin",
    "amount": 200,
    "winLevel": 4
   },
   {
    "index": 41,
    "type": "setTotalWin",
    "amount": 3500
   },
   {
    "index": 42,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 10
   },
   {
    "index": 43,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     39,
     223,
     237,
     46,
     88
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 44,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 45,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 46,
    "type": "setTotalWin",
    "amount": 3500
   },
   {
    "index": 47,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 10
   },
   {
    "index": 48,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     20,
     64,
     111,
     159,
     188
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 49,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 50,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 7,
      "cells": [
       {
        "row": 1,
        "multiplier": 2
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 4
       }
      ]
     }
    ],
    "totalWays": 672
   },
   {
    "index": 51,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 2
    },
    "from": "H4",
    "to": "H5",
    "cells": [
     {
      "reel": 3,
      "row": 2
     }
    ],
    "totalWays": 672
   },
   {
    "index": 52,
    "type": "winInfo",
    "totalWin": 240,
    "wins": [
     {
      "symbol": "L2",
      "kind": 5,
      "win": 240,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 1
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 240,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 53,
    "type": "setWin",
    "amount": 240,
    "winLevel": 4
   },
   {
    "index": 54,
    "type": "setTotalWin",
    "amount": 3740
   },
   {
    "index": 55,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 10
   },
   {
    "index": 56,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     38,
     220,
     83,
     8,
     28
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 57,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 58,
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L4",
      "kind": 4,
      "win": 60,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 0,
        "row": 4
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 60,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 59,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 60,
    "type": "setTotalWin",
    "amount": 3800
   },
   {
    "index": 61,
    "type": "freeSpinRetrigger",
    "totalFs": 13,
    "positions": [
     {
      "reel": 1,
      "row": 3
     },
     {
      "reel": 4,
      "row": 1
     }
    ]
   },
   {
    "index": 62,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 13
   },
   {
    "index": 63,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     99,
     137,
     186,
     4,
     4
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 64,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H2"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 512
   },
   {
    "index": 65,
    "type": "setTotalWin",
    "amount": 3800
   },
   {
    "index": 66,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 13
   },
   {
    "index": 67,
    "type": "reveal",
    "board": [
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     121,
     64,
     108,
     237,
     243
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 68,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 69,
    "type": "winInfo",
    "totalWin": 120,
    "wins": [
     {
      "symbol": "H5",
      "kind": 3,
      "win": 120,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 120,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 70,
    "type": "setWin",
    "amount": 120,
    "winLevel": 3
   },
   {
    "index": 71,
    "type": "setTotalWin",
    "amount": 3920
   },
   {
    "index": 72,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 13
   },
   {
    "index": 73,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     120,
     53,
     207,
     144,
     112
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 74,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 75,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H1"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H3"
       }
      ]
     }
    ],
    "totalWays": 1152
   },
   {
    "index": 76,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 3,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 7,
      "cells": [
       {
        "row": 1,
        "multiplier": 5
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 2688
   },
   {
    "index": 77,
    "type": "setTotalWin",
    "amount": 3920
   },
   {
    "index": 78,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 13
   },
   {
    "index": 79,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     187,
     6,
     66,
     117,
     54
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 80,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 384
   },
   {
    "index": 81,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 2,
    "unlocked": [
     "bottom",
     "right"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H2"
     },
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 82,
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L5",
      "kind": 4,
      "win": 60,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 1
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 60,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 83,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 84,
    "type": "setTotalWin",
    "amount": 3980
   },
   {
    "index": 85,
    "type": "freeSpinEnd",
    "amount": 3980,
    "winLevel": 5
   },
   {
    "index": 86,
    "type": "finalWin",
    "amount": 3980
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 39.8
 },
 {
  "id": 537,
  "payoutMultiplier": 60,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     99,
     18,
     124,
     196,
     81
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     1,
     2,
     3
    ]
   },
   {
    "index": 1,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "freeSpinTrigger",
    "totalFs": 12,
    "positions": [
     {
      "reel": 0,
      "row": 4
     },
     {
      "reel": 1,
      "row": 1
     },
     {
      "reel": 2,
      "row": 2
     },
     {
      "reel": 3,
      "row": 2
     },
     {
      "reel": 4,
      "row": 3
     }
    ]
   },
   {
    "index": 3,
    "type": "bonusLevel",
    "level": 3,
    "name": "WHITEOUT",
    "startHaunted": []
   },
   {
    "index": 4,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 12
   },
   {
    "index": 5,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     40,
     75,
     177,
     221,
     238
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 6,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 7,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 8,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 12
   },
   {
    "index": 9,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     17,
     187,
     52,
     84,
     70
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 10,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 480
   },
   {
    "index": 11,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H2"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 2160
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 12
   },
   {
    "index": 14,
    "type": "reveal",
    "board": [
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     220,
     124,
     194,
     109,
     157
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 15,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 16,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 17,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 12
   },
   {
    "index": 18,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     240,
     214,
     247,
     106,
     197
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 19,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "left",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 12
   },
   {
    "index": 22,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     159,
     51,
     172,
     157,
     118
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     1
    ]
   },
   {
    "index": 23,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 480
   },
   {
    "index": 24,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 480
   },
   {
    "index": 25,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 26,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 12
   },
   {
    "index": 27,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     103,
     63,
     28,
     23,
     13
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     1
    ]
   },
   {
    "index": 28,
    "type": "wildReel",
    "label": "Wild Reel",
    "reels": [
     {
      "reel": 1,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 1
       }
      ]
     },
     {
      "reel": 3,
      "baseRows": 3,
      "added": 1,
      "cells": [
       {
        "row": 4,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 640
   },
   {
    "index": 29,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H4"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H4"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 2880
   },
   {
    "index": 30,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 31,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 12
   },
   {
    "index": 32,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     139,
     133,
     23,
     10,
     172
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     1,
     2
    ]
   },
   {
    "index": 33,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 2,
      "row": 3,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H3"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 2
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H4"
       }
      ]
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 34,
    "type": "cloneSymbol",
    "label": "Clone",
    "cell": {
     "reel": 1
    },
    "from": "L1",
    "to": "H5",
    "cells": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 1,
      "row": 1
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 35,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "H5",
      "kind": 3,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 36,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 37,
    "type": "setTotalWin",
    "amount": 30
   },
   {
    "index": 38,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 12
   },
   {
    "index": 39,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     30,
     176,
     150,
     132,
     5
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     1,
     2,
     3,
     4
    ]
   },
   {
    "index": 40,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H4"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 768
   },
   {
    "index": 41,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L5",
      "kind": 4,
      "win": 30,
      "positions": [
       {
        "reel": 0,
        "row": 1
       },
       {
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 1
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 30,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 42,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 44,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 12
   },
   {
    "index": 45,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     4,
     84,
     70,
     50,
     49
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 46,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "H2"
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H2"
       }
      ]
     }
    ],
    "totalWays": 576
   },
   {
    "index": 47,
    "type": "stretchReel",
    "label": "Stretch",
    "reels": [
     {
      "reel": 1,
      "mode": "normal",
      "baseRows": 3,
      "reelWays": 9,
      "cells": [
       {
        "row": 1,
        "multiplier": 6
       },
       {
        "row": 2,
        "multiplier": 1
       },
       {
        "row": 3,
        "multiplier": 2
       }
      ]
     }
    ],
    "totalWays": 1728
   },
   {
    "index": 48,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 49,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 12
   },
   {
    "index": 50,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     76,
     210,
     49,
     6,
     50
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 51,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     },
     {
      "reel": 3,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "W",
        "multiplier": 1
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 512
   },
   {
    "index": 52,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 53,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 12
   },
   {
    "index": 54,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L5"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     97,
     217,
     215,
     188,
     35
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 55,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "H1"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 2,
        "name": "W",
        "multiplier": 1
       }
      ]
     }
    ],
    "totalWays": 288
   },
   {
    "index": 56,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 57,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 12
   },
   {
    "index": 58,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     127,
     56,
     16,
     160,
     140
    ],
    "gameType": "freegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 59,
    "type": "unlockedSlots",
    "label": "Unlocked Slots",
    "level": 3,
    "unlocked": [
     "bottom",
     "right",
     "left"
    ],
    "bottom": [
     {
      "reel": 1,
      "row": 4,
      "name": "H5"
     }
    ],
    "sides": [
     {
      "side": "right",
      "reel": 5,
      "cells": [
       {
        "row": 1,
        "slotRow": 0,
        "name": "W",
        "multiplier": 1
       },
       {
        "row": 2,
        "slotRow": 1,
        "name": "H5"
       },
       {
        "row": 3,
        "slotRow": 2,
        "name": "H4"
       }
      ]
     },
     {
      "side": "left",
      "reel": 6,
      "cells": [
       {
        "row": 1,
        "slotRow": 1,
        "name": "H3"
       },
       {
        "row": 2,
        "slotRow": 2,
        "name": "H5"
       }
      ]
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 60,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 61,
    "type": "freeSpinEnd",
    "amount": 60,
    "winLevel": 1
   },
   {
    "index": 62,
    "type": "finalWin",
    "amount": 60
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 0.6
 }
];
