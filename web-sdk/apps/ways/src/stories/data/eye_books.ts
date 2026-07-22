export default [
 {
  "id": 0,
  "payoutMultiplier": 2400,
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
       "name": "H2"
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
       "name": "S",
       "scatter": true
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
       "name": "L4"
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
       "name": "L4"
      },
      {
       "name": "ME",
       "eye": true
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
       "name": "L2"
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
       "name": "L1"
      },
      {
       "name": "HM",
       "mirror": true
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
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     216,
     205,
     195,
     16,
     65
    ],
    "gameType": "basegame",
    "anticipation": [
     0,
     0,
     0,
     0,
     0
    ]
   },
   {
    "index": 1,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 4
      },
      "reflected": [
       {
        "reel": 3,
        "row": 3,
        "apparitions": 4
       },
       {
        "reel": 4,
        "row": 3,
        "apparitions": 4
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 3136
   },
   {
    "index": 2,
    "type": "madamsEye",
    "eye": {
     "reel": 2,
     "row": 1
    },
    "converted": [
     {
      "reel": 3,
      "row": 3,
      "apparitions": 4
     },
     {
      "reel": 4,
      "row": 3,
      "apparitions": 4
     }
    ]
   },
   {
    "index": 3,
    "type": "winInfo",
    "totalWin": 2400,
    "wins": [
     {
      "symbol": "L2",
      "kind": 5,
      "win": 2400,
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
       "ways": 20,
       "globalMult": 1,
       "winWithoutMult": 2400,
       "symbolMult": 8
      }
     }
    ]
   },
   {
    "index": 4,
    "type": "setWin",
    "amount": 2400,
    "winLevel": 6
   },
   {
    "index": 5,
    "type": "setTotalWin",
    "amount": 2400
   },
   {
    "index": 6,
    "type": "finalWin",
    "amount": 2400
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 24.0,
  "freeGameWins": 0.0
 },
 {
  "id": 4,
  "payoutMultiplier": 368820,
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
       "name": "S",
       "scatter": true
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
       "name": "H2"
      },
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
       "name": "HM",
       "mirror": true
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
       "name": "L4"
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "ME",
       "eye": true
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
     117,
     78,
     139,
     3,
     14
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 3
      },
      "reflected": [
       {
        "reel": 3,
        "row": 4,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 1280
   },
   {
    "index": 2,
    "type": "madamsEye",
    "eye": {
     "reel": 4,
     "row": 3
    },
    "converted": [
     {
      "reel": 3,
      "row": 4,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 4,
    "type": "freeSpinTrigger",
    "totalFs": 10,
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
      "reel": 4,
      "row": 2
     }
    ]
   },
   {
    "index": 5,
    "type": "bonusLevel",
    "level": 2,
    "name": "THE_OTHER_SIDE",
    "startHaunted": []
   },
   {
    "index": 6,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 10
   },
   {
    "index": 7,
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
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L2"
      },
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
       "name": "ME",
       "eye": true
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
       "name": "HM",
       "mirror": true
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
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     223,
     42,
     74,
     80,
     246
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 2
      },
      "reflected": [
       {
        "reel": 0,
        "row": 1,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     },
     {
      "mirror": {
       "reel": 3,
       "row": 1
      },
      "reflected": [
       {
        "reel": 3,
        "row": 2,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 4,
        "row": 1,
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 3600
   },
   {
    "index": 9,
    "type": "madamsEye",
    "eye": {
     "reel": 2,
     "row": 4
    },
    "converted": [
     {
      "reel": 0,
      "row": 1,
      "apparitions": 3
     },
     {
      "reel": 1,
      "row": 3,
      "apparitions": 2
     },
     {
      "reel": 3,
      "row": 2,
      "apparitions": 3
     },
     {
      "reel": 4,
      "row": 1,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 10,
    "type": "winInfo",
    "totalWin": 206280,
    "wins": [
     {
      "symbol": "H1",
      "kind": 5,
      "win": 36000,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 36,
       "globalMult": 1,
       "winWithoutMult": 36000,
       "symbolMult": 10
      }
     },
     {
      "symbol": "H2",
      "kind": 5,
      "win": 90000,
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
        "reel": 0,
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
        "row": 4
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
        "reel": 3,
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 180,
       "globalMult": 1,
       "winWithoutMult": 90000,
       "symbolMult": 10
      }
     },
     {
      "symbol": "H3",
      "kind": 5,
      "win": 14400,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 36,
       "globalMult": 1,
       "winWithoutMult": 14400,
       "symbolMult": 10
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 10800,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 36,
       "globalMult": 1,
       "winWithoutMult": 10800,
       "symbolMult": 10
      }
     },
     {
      "symbol": "H5",
      "kind": 5,
      "win": 9000,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 36,
       "globalMult": 1,
       "winWithoutMult": 9000,
       "symbolMult": 10
      }
     },
     {
      "symbol": "L1",
      "kind": 5,
      "win": 19440,
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
        "reel": 1,
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
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
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 162,
       "globalMult": 1,
       "winWithoutMult": 19440,
       "symbolMult": 10
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 6480,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 3
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 54,
       "globalMult": 1,
       "winWithoutMult": 6480,
       "symbolMult": 10
      }
     },
     {
      "symbol": "L3",
      "kind": 5,
      "win": 8640,
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
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 108,
       "globalMult": 1,
       "winWithoutMult": 8640,
       "symbolMult": 10
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 5760,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 72,
       "globalMult": 1,
       "winWithoutMult": 5760,
       "symbolMult": 10
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 5760,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 72,
       "globalMult": 1,
       "winWithoutMult": 5760,
       "symbolMult": 10
      }
     }
    ]
   },
   {
    "index": 11,
    "type": "setWin",
    "amount": 206280,
    "winLevel": 9
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 206280
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 10
   },
   {
    "index": 14,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "L3",
       "multiplier": 3,
       "ttl": 1
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
       "name": "H5"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1",
       "multiplier": 2,
       "ttl": 1
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
       "name": "H3"
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
       "name": "HM",
       "mirror": true
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3,
       "ttl": 1
      },
      {
       "name": "L5"
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
       "name": "H5"
      },
      {
       "name": "L1",
       "multiplier": 2,
       "ttl": 1
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
     45,
     14,
     65,
     249,
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
    "index": 15,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 1
      },
      "reflected": [
       {
        "reel": 2,
        "row": 2,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 4,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 8100
   },
   {
    "index": 16,
    "type": "winInfo",
    "totalWin": 4800,
    "wins": [
     {
      "symbol": "L3",
      "kind": 5,
      "win": 4800,
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
        "row": 2
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "ways": 60,
       "globalMult": 1,
       "winWithoutMult": 4800,
       "symbolMult": 3
      }
     }
    ]
   },
   {
    "index": 17,
    "type": "setWin",
    "amount": 4800,
    "winLevel": 7
   },
   {
    "index": 18,
    "type": "setTotalWin",
    "amount": 211080
   },
   {
    "index": 19,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 10
   },
   {
    "index": 20,
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
       "name": "L1"
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
       "name": "H2"
      },
      {
       "name": "H2",
       "multiplier": 4,
       "ttl": 1
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3,
       "ttl": 1
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
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L4"
      },
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
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     88,
     131,
     90,
     228,
     134
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
    "index": 21,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 2
      },
      "reflected": [
       {
        "reel": 2,
        "row": 2,
        "apparitions": 5,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 2816
   },
   {
    "index": 22,
    "type": "winInfo",
    "totalWin": 800,
    "wins": [
     {
      "symbol": "L4",
      "kind": 5,
      "win": 800,
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
        "reel": 3,
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 10,
       "globalMult": 1,
       "winWithoutMult": 800,
       "symbolMult": 5
      }
     }
    ]
   },
   {
    "index": 23,
    "type": "setWin",
    "amount": 800,
    "winLevel": 5
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 211880
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 3,
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
       "name": "H4"
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
       "name": "H3"
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
       "name": "H4"
      },
      {
       "name": "L2",
       "multiplier": 5,
       "ttl": 1
      },
      {
       "name": "L2"
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
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H1"
      },
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
       "name": "H3"
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     45,
     204,
     20,
     160,
     38
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 3
      },
      "reflected": [
       {
        "reel": 4,
        "row": 3,
        "apparitions": 2,
        "ttl": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 4,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 3520
   },
   {
    "index": 28,
    "type": "setTotalWin",
    "amount": 211880
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 10
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
       "name": "W",
       "wild": true
      },
      {
       "name": "ME",
       "eye": true
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
       "name": "L4"
      },
      {
       "name": "L2",
       "multiplier": 4,
       "ttl": 1
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
       "name": "H1"
      },
      {
       "name": "L2",
       "multiplier": 2,
       "ttl": 1
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
     126,
     85,
     214,
     53,
     33
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
    "index": 31,
    "type": "madamsEye",
    "eye": {
     "reel": 1,
     "row": 1
    },
    "converted": [
     {
      "reel": 2,
      "row": 3,
      "apparitions": 4
     },
     {
      "reel": 4,
      "row": 3,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 32,
    "type": "winInfo",
    "totalWin": 640,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 160,
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
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 160,
       "symbolMult": 4
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
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 4
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 80,
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
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 4
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 320,
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
        "reel": 1,
        "row": 1
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 320,
       "symbolMult": 4
      }
     }
    ]
   },
   {
    "index": 33,
    "type": "setWin",
    "amount": 640,
    "winLevel": 5
   },
   {
    "index": 34,
    "type": "setTotalWin",
    "amount": 212520
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
       "name": "L5"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H3"
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
       "name": "L4"
      },
      {
       "name": "ME",
       "eye": true
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
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     201,
     105,
     27,
     43,
     111
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 1
      },
      "reflected": [
       {
        "reel": 0,
        "row": 1,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 2,
        "ttl": 2
       },
       {
        "reel": 1,
        "row": 2,
        "apparitions": 2,
        "ttl": 2
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 2880
   },
   {
    "index": 38,
    "type": "madamsEye",
    "eye": {
     "reel": 3,
     "row": 2
    },
    "converted": [
     {
      "reel": 0,
      "row": 1,
      "apparitions": 3
     },
     {
      "reel": 1,
      "row": 2,
      "apparitions": 2
     },
     {
      "reel": 2,
      "row": 1,
      "apparitions": 2
     },
     {
      "reel": 2,
      "row": 2,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 39,
    "type": "winInfo",
    "totalWin": 66870,
    "wins": [
     {
      "symbol": "H1",
      "kind": 4,
      "win": 14400,
      "positions": [
       {
        "reel": 0,
        "row": 2
       },
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
        "reel": 2,
        "row": 1
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
       "ways": 48,
       "globalMult": 1,
       "winWithoutMult": 14400,
       "symbolMult": 9
      }
     },
     {
      "symbol": "H2",
      "kind": 4,
      "win": 3600,
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
       "ways": 24,
       "globalMult": 1,
       "winWithoutMult": 3600,
       "symbolMult": 9
      }
     },
     {
      "symbol": "H3",
      "kind": 5,
      "win": 28800,
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
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 72,
       "globalMult": 1,
       "winWithoutMult": 28800,
       "symbolMult": 9
      }
     },
     {
      "symbol": "H4",
      "kind": 4,
      "win": 6400,
      "positions": [
       {
        "reel": 0,
        "row": 3
       },
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
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "ways": 64,
       "globalMult": 1,
       "winWithoutMult": 6400,
       "symbolMult": 9
      }
     },
     {
      "symbol": "H5",
      "kind": 4,
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
        "row": 1
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
       "ways": 24,
       "globalMult": 1,
       "winWithoutMult": 1920,
       "symbolMult": 9
      }
     },
     {
      "symbol": "L1",
      "kind": 5,
      "win": 2880,
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
        "row": 4
       }
      ],
      "meta": {
       "ways": 24,
       "globalMult": 1,
       "winWithoutMult": 2880,
       "symbolMult": 9
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 1280,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
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
       "ways": 32,
       "globalMult": 1,
       "winWithoutMult": 1280,
       "symbolMult": 9
      }
     },
     {
      "symbol": "L3",
      "kind": 5,
      "win": 2400,
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
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "ways": 30,
       "globalMult": 1,
       "winWithoutMult": 2400,
       "symbolMult": 9
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 3840,
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
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 48,
       "globalMult": 1,
       "winWithoutMult": 3840,
       "symbolMult": 9
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 1350,
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
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 3
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
        "row": 2
       }
      ],
      "meta": {
       "ways": 45,
       "globalMult": 1,
       "winWithoutMult": 1350,
       "symbolMult": 9
      }
     }
    ]
   },
   {
    "index": 40,
    "type": "setWin",
    "amount": 66870,
    "winLevel": 9
   },
   {
    "index": 41,
    "type": "setTotalWin",
    "amount": 279390
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
       "name": "L4"
      },
      {
       "name": "H3",
       "multiplier": 3,
       "ttl": 1
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
       "name": "H2",
       "multiplier": 2,
       "ttl": 1
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
       "name": "H1"
      },
      {
       "name": "H3",
       "multiplier": 2,
       "ttl": 1
      },
      {
       "name": "H3",
       "multiplier": 2,
       "ttl": 1
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
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "HM",
       "mirror": true
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
     200,
     140,
     222,
     128,
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
    "index": 44,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 3
      },
      "reflected": [
       {
        "reel": 3,
        "row": 4,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 5040
   },
   {
    "index": 45,
    "type": "setTotalWin",
    "amount": 279390
   },
   {
    "index": 46,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 10
   },
   {
    "index": 47,
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
       "name": "L2"
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
       "name": "L1"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L3",
       "multiplier": 2,
       "ttl": 1
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
       "name": "H2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4",
       "multiplier": 3,
       "ttl": 1
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
      }
     ]
    ],
    "paddingPositions": [
     140,
     198,
     64,
     83,
     171
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 2
      },
      "reflected": [
       {
        "reel": 3,
        "row": 1,
        "apparitions": 2,
        "ttl": 2
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 2800
   },
   {
    "index": 49,
    "type": "winInfo",
    "totalWin": 190,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 10,
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
       "winWithoutMult": 10,
       "symbolMult": 0
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 100,
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
       "winWithoutMult": 100,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 20,
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
       "winWithoutMult": 20,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 60,
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
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 6,
       "globalMult": 1,
       "winWithoutMult": 60,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 50,
    "type": "setWin",
    "amount": 190,
    "winLevel": 3
   },
   {
    "index": 51,
    "type": "setTotalWin",
    "amount": 279580
   },
   {
    "index": 52,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 10
   },
   {
    "index": 53,
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
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L5",
       "multiplier": 2,
       "ttl": 1
      },
      {
       "name": "H3"
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
       "name": "L5"
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
       "name": "H4"
      },
      {
       "name": "H4",
       "multiplier": 2,
       "ttl": 1
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
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "ME",
       "eye": true
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
     ]
    ],
    "paddingPositions": [
     214,
     92,
     239,
     218,
     122
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
    "index": 54,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 2
      },
      "reflected": [
       {
        "reel": 0,
        "row": 3,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 0,
        "row": 2,
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 2800
   },
   {
    "index": 55,
    "type": "madamsEye",
    "eye": {
     "reel": 4,
     "row": 2
    },
    "converted": [
     {
      "reel": 0,
      "row": 2,
      "apparitions": 2
     },
     {
      "reel": 0,
      "row": 3,
      "apparitions": 3
     },
     {
      "reel": 1,
      "row": 3,
      "apparitions": 2
     },
     {
      "reel": 3,
      "row": 1,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 56,
    "type": "winInfo",
    "totalWin": 38800,
    "wins": [
     {
      "symbol": "H2",
      "kind": 5,
      "win": 30000,
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
       },
       {
        "reel": 3,
        "row": 1
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
      "meta": {
       "ways": 60,
       "globalMult": 1,
       "winWithoutMult": 30000,
       "symbolMult": 9
      }
     },
     {
      "symbol": "L1",
      "kind": 5,
      "win": 7200,
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
        "reel": 3,
        "row": 1
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 60,
       "globalMult": 1,
       "winWithoutMult": 7200,
       "symbolMult": 9
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 1600,
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
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 20,
       "globalMult": 1,
       "winWithoutMult": 1600,
       "symbolMult": 9
      }
     }
    ]
   },
   {
    "index": 57,
    "type": "setWin",
    "amount": 38800,
    "winLevel": 9
   },
   {
    "index": 58,
    "type": "setTotalWin",
    "amount": 318380
   },
   {
    "index": 59,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 10
   },
   {
    "index": 60,
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
       "name": "L2",
       "multiplier": 2,
       "ttl": 1
      },
      {
       "name": "H5",
       "multiplier": 3,
       "ttl": 1
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
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "HM",
       "mirror": true
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
      },
      {
       "name": "ME",
       "eye": true
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
       "name": "H5"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     120,
     57,
     42,
     13,
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
    "index": 61,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 2
      },
      "reflected": [
       {
        "reel": 1,
        "row": 1,
        "apparitions": 2,
        "ttl": 2
       },
       {
        "reel": 0,
        "row": 2,
        "apparitions": 4,
        "ttl": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 3600
   },
   {
    "index": 62,
    "type": "madamsEye",
    "eye": {
     "reel": 2,
     "row": 4
    },
    "converted": [
     {
      "reel": 0,
      "row": 2,
      "apparitions": 4
     },
     {
      "reel": 0,
      "row": 3,
      "apparitions": 3
     },
     {
      "reel": 1,
      "row": 1,
      "apparitions": 2
     },
     {
      "reel": 2,
      "row": 3,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 63,
    "type": "winInfo",
    "totalWin": 50440,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 8400,
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
       "ways": 84,
       "globalMult": 1,
       "winWithoutMult": 8400,
       "symbolMult": 11
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 2520,
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
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 42,
       "globalMult": 1,
       "winWithoutMult": 2520,
       "symbolMult": 11
      }
     },
     {
      "symbol": "H3",
      "kind": 5,
      "win": 22400,
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
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 56,
       "globalMult": 1,
       "winWithoutMult": 22400,
       "symbolMult": 11
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 2240,
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
       "ways": 56,
       "globalMult": 1,
       "winWithoutMult": 2240,
       "symbolMult": 11
      }
     },
     {
      "symbol": "H5",
      "kind": 3,
      "win": 1440,
      "positions": [
       {
        "reel": 0,
        "row": 4
       },
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
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 48,
       "globalMult": 1,
       "winWithoutMult": 1440,
       "symbolMult": 11
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 840,
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
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 42,
       "globalMult": 1,
       "winWithoutMult": 840,
       "symbolMult": 11
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 840,
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
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 42,
       "globalMult": 1,
       "winWithoutMult": 840,
       "symbolMult": 11
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 1260,
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
       }
      ],
      "meta": {
       "ways": 42,
       "globalMult": 1,
       "winWithoutMult": 1260,
       "symbolMult": 11
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 10080,
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
       "ways": 126,
       "globalMult": 1,
       "winWithoutMult": 10080,
       "symbolMult": 11
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 420,
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
        "reel": 2,
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 42,
       "globalMult": 1,
       "winWithoutMult": 420,
       "symbolMult": 11
      }
     }
    ]
   },
   {
    "index": 64,
    "type": "setWin",
    "amount": 50440,
    "winLevel": 9
   },
   {
    "index": 65,
    "type": "setTotalWin",
    "amount": 368820
   },
   {
    "index": 66,
    "type": "freeSpinEnd",
    "amount": 368820,
    "winLevel": 9
   },
   {
    "index": 67,
    "type": "finalWin",
    "amount": 368820
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 3688.2
 }
];
