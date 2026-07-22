export default [
 {
  "id": 1,
  "payoutMultiplier": 1600,
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
       "name": "H5"
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
       "name": "L5"
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
       "name": "H5"
      },
      {
       "name": "L2"
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
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H4"
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
       "name": "L1"
      },
      {
       "name": "H4"
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     242,
     217,
     14,
     23,
     21
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
       "reel": 2,
       "row": 2
      },
      "reflected": [
       {
        "reel": 3,
        "row": 1,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 4
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 2880
   },
   {
    "index": 2,
    "type": "winInfo",
    "totalWin": 1600,
    "wins": [
     {
      "symbol": "H5",
      "kind": 5,
      "win": 1000,
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
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 1000,
       "symbolMult": 2
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 600,
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
        "row": 2
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "ways": 15,
       "globalMult": 1,
       "winWithoutMult": 600,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 3,
    "type": "setWin",
    "amount": 1600,
    "winLevel": 6
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 1600
   },
   {
    "index": 5,
    "type": "finalWin",
    "amount": 1600
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 16.0,
  "freeGameWins": 0.0
 },
 {
  "id": 1,
  "payoutMultiplier": 5260,
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
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "HM",
       "mirror": true
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
     100,
     148,
     124,
     174,
     149
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 4
      },
      "reflected": [
       {
        "reel": 2,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 0,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "L1"
      }
     }
    ],
    "totalWays": 2400
   },
   {
    "index": 2,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 3,
    "type": "freeSpinTrigger",
    "totalFs": 8,
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
      "reel": 4,
      "row": 1
     }
    ]
   },
   {
    "index": 4,
    "type": "bonusLevel",
    "level": 1,
    "name": "THE_SEANCE",
    "startHaunted": []
   },
   {
    "index": 5,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 6,
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "HM",
       "mirror": true
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
     131,
     172,
     143,
     46,
     228
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
    "index": 7,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 1
      },
      "reflected": [
       {
        "reel": 1,
        "row": 2,
        "apparitions": 4,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 1792
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
      }
     ],
     [
      {
       "name": "H2"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L3"
      },
      {
       "name": "HM",
       "mirror": true
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
     212,
     203,
     90,
     169,
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
    "index": 11,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 1
      },
      "reflected": [
       {
        "reel": 3,
        "row": 1,
        "apparitions": 4,
        "ttl": 1
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 3,
        "ttl": 1
       },
       {
        "reel": 1,
        "row": 2,
        "apparitions": 2,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     },
     {
      "mirror": {
       "reel": 2,
       "row": 4
      },
      "reflected": [
       {
        "reel": 3,
        "row": 4,
        "apparitions": 3,
        "ttl": 1
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 2,
        "ttl": 1
       },
       {
        "reel": 1,
        "row": 4,
        "apparitions": 2,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 5760
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "HM",
       "mirror": true
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
     225,
     19,
     200,
     210,
     87
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 2
      },
      "reflected": [
       {
        "reel": 4,
        "row": 3,
        "apparitions": 3,
        "ttl": 1
       },
       {
        "reel": 4,
        "row": 1,
        "apparitions": 4,
        "ttl": 1
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2,
        "ttl": 1
       },
       {
        "reel": 3,
        "row": 1,
        "apparitions": 3,
        "ttl": 1
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 3,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     },
     {
      "mirror": {
       "reel": 2,
       "row": 4
      },
      "reflected": [
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2,
        "ttl": 1
       },
       {
        "reel": 1,
        "row": 4,
        "apparitions": 2,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 7560
   },
   {
    "index": 16,
    "type": "winInfo",
    "totalWin": 1920,
    "wins": [
     {
      "symbol": "L1",
      "kind": 5,
      "win": 1920,
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
        "reel": 3,
        "row": 3
       },
       {
        "reel": 4,
        "row": 1
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
    "index": 17,
    "type": "setWin",
    "amount": 1920,
    "winLevel": 6
   },
   {
    "index": 18,
    "type": "setTotalWin",
    "amount": 1920
   },
   {
    "index": 19,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 8
   },
   {
    "index": 20,
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
       "name": "ME",
       "eye": true
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
       "name": "HM",
       "mirror": true
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
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     17,
     6,
     10,
     186,
     235
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 4
      },
      "reflected": [
       {
        "reel": 3,
        "row": 3,
        "apparitions": 2,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 1280
   },
   {
    "index": 22,
    "type": "madamsEye",
    "eye": {
     "reel": 0,
     "row": 4
    },
    "converted": [
     {
      "reel": 3,
      "row": 3,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 23,
    "type": "winInfo",
    "totalWin": 2300,
    "wins": [
     {
      "symbol": "H1",
      "kind": 4,
      "win": 1200,
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
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 1200,
       "symbolMult": 2
      }
     },
     {
      "symbol": "H4",
      "kind": 4,
      "win": 400,
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
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 400,
       "symbolMult": 2
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 160,
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
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 160,
       "symbolMult": 2
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 540,
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
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 18,
       "globalMult": 1,
       "winWithoutMult": 540,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 24,
    "type": "setWin",
    "amount": 2300,
    "winLevel": 6
   },
   {
    "index": 25,
    "type": "setTotalWin",
    "amount": 4220
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
       "name": "L1"
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
     196,
     154,
     189,
     11,
     230
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
    "index": 28,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 1
      },
      "reflected": [
       {
        "reel": 3,
        "row": 2,
        "apparitions": 2,
        "ttl": 1
       },
       {
        "reel": 3,
        "row": 1,
        "apparitions": 4,
        "ttl": 1
       },
       {
        "reel": 1,
        "row": 2,
        "apparitions": 2,
        "ttl": 1
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 3,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 3840
   },
   {
    "index": 29,
    "type": "setTotalWin",
    "amount": 4220
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
       "name": "L2"
      },
      {
       "name": "H5"
      },
      {
       "name": "H3"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H5"
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
       "name": "L4"
      },
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
     4,
     179,
     142,
     245,
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
    "index": 32,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 3
      },
      "reflected": [
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2,
        "ttl": 1
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
    "index": 33,
    "type": "winInfo",
    "totalWin": 400,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 400,
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
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 400,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 34,
    "type": "setWin",
    "amount": 400,
    "winLevel": 4
   },
   {
    "index": 35,
    "type": "setTotalWin",
    "amount": 4620
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
       "name": "H1"
      },
      {
       "name": "L1"
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
       "name": "HM",
       "mirror": true
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
     204,
     159,
     181,
     92,
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
    "index": 38,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 2
      },
      "reflected": [
       {
        "reel": 2,
        "row": 1,
        "apparitions": 2,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 1280
   },
   {
    "index": 39,
    "type": "winInfo",
    "totalWin": 640,
    "wins": [
     {
      "symbol": "L3",
      "kind": 5,
      "win": 640,
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
        "row": 4
       },
       {
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 640,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 40,
    "type": "setWin",
    "amount": 640,
    "winLevel": 5
   },
   {
    "index": 41,
    "type": "setTotalWin",
    "amount": 5260
   },
   {
    "index": 42,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 43,
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
       "name": "S",
       "scatter": true
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
       "name": "H5"
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
     171,
     118,
     116,
     79,
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
    "index": 44,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 2
      },
      "reflected": [
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2,
        "ttl": 1
       },
       {
        "reel": 0,
        "row": 3,
        "apparitions": 4,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 2240
   },
   {
    "index": 45,
    "type": "setTotalWin",
    "amount": 5260
   },
   {
    "index": 46,
    "type": "freeSpinEnd",
    "amount": 5260,
    "winLevel": 6
   },
   {
    "index": 47,
    "type": "finalWin",
    "amount": 5260
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 52.6
 },
 {
  "id": 4,
  "payoutMultiplier": 23760,
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
       "name": "H2"
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
    "type": "winInfo",
    "totalWin": 18000,
    "wins": [
     {
      "symbol": "H2",
      "kind": 5,
      "win": 18000,
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
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 36,
       "globalMult": 1,
       "winWithoutMult": 18000,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 10,
    "type": "setWin",
    "amount": 18000,
    "winLevel": 9
   },
   {
    "index": 11,
    "type": "setTotalWin",
    "amount": 18000
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
    "index": 14,
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
    "index": 15,
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
    "index": 16,
    "type": "setWin",
    "amount": 4800,
    "winLevel": 7
   },
   {
    "index": 17,
    "type": "setTotalWin",
    "amount": 22800
   },
   {
    "index": 18,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 10
   },
   {
    "index": 19,
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
    "index": 20,
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
    "index": 21,
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
    "index": 22,
    "type": "setWin",
    "amount": 800,
    "winLevel": 5
   },
   {
    "index": 23,
    "type": "setTotalWin",
    "amount": 23600
   },
   {
    "index": 24,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 10
   },
   {
    "index": 25,
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
    "index": 26,
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
    "index": 27,
    "type": "setTotalWin",
    "amount": 23600
   },
   {
    "index": 28,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 10
   },
   {
    "index": 29,
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
       "name": "L2"
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
    "index": 30,
    "type": "winInfo",
    "totalWin": 160,
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
        "row": 1
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
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 160,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 31,
    "type": "setWin",
    "amount": 160,
    "winLevel": 3
   },
   {
    "index": 32,
    "type": "setTotalWin",
    "amount": 23760
   },
   {
    "index": 33,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 10
   },
   {
    "index": 34,
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
     229,
     201,
     105,
     27,
     43
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 1
      },
      "reflected": [
       {
        "reel": 2,
        "row": 1,
        "apparitions": 4,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H5"
      }
     }
    ],
    "totalWays": 1792
   },
   {
    "index": 36,
    "type": "setTotalWin",
    "amount": 23760
   },
   {
    "index": 37,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 10
   },
   {
    "index": 38,
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
       "name": "L3",
       "multiplier": 4,
       "ttl": 1
      },
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
       "name": "L2"
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
     210,
     136,
     245,
     45,
     160
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
    "type": "setTotalWin",
    "amount": 23760
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
       "name": "H2"
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
       "name": "S",
       "scatter": true
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
     125,
     69,
     131,
     200,
     140
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
    "type": "setTotalWin",
    "amount": 23760
   },
   {
    "index": 43,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 10
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
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H5"
      },
      {
       "name": "HM",
       "mirror": true
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
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     201,
     203,
     198,
     91,
     177
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
    "index": 45,
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
        "row": 2,
        "apparitions": 3,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 46,
    "type": "setTotalWin",
    "amount": 23760
   },
   {
    "index": 47,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 10
   },
   {
    "index": 48,
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
      },
      {
       "name": "S",
       "scatter": true
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
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H5"
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
       "name": "H1"
      },
      {
       "name": "L1",
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
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     70,
     118,
     73,
     209,
     128
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 2
      },
      "reflected": [
       {
        "reel": 4,
        "row": 1,
        "apparitions": 4,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 2304
   },
   {
    "index": 50,
    "type": "setTotalWin",
    "amount": 23760
   },
   {
    "index": 51,
    "type": "freeSpinEnd",
    "amount": 23760,
    "winLevel": 7
   },
   {
    "index": 52,
    "type": "finalWin",
    "amount": 23760
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 237.6
 },
 {
  "id": 11,
  "payoutMultiplier": 170040,
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
       "name": "L2"
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
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "S",
       "scatter": true
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
       "name": "HM",
       "mirror": true
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
     115,
     79,
     247,
     151,
     120
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
       "reel": 3,
       "row": 4
      },
      "reflected": [
       {
        "reel": 4,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 4,
        "row": 3,
        "apparitions": 4
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     },
     {
      "mirror": {
       "reel": 1,
       "row": 4
      },
      "reflected": [
       {
        "reel": 2,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 0,
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "H5"
      }
     }
    ],
    "totalWays": 4480
   },
   {
    "index": 2,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 3,
    "type": "freeSpinTrigger",
    "totalFs": 12,
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
      "row": 2
     }
    ]
   },
   {
    "index": 4,
    "type": "bonusLevel",
    "level": 3,
    "name": "BLOOD_MOON",
    "startHaunted": []
   },
   {
    "index": 5,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 12
   },
   {
    "index": 6,
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
      },
      {
       "name": "HM",
       "mirror": true
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
     98,
     138,
     7,
     164,
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
    "index": 7,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 4
      },
      "reflected": [
       {
        "reel": 2,
        "row": 4,
        "apparitions": 2,
        "ttl": -1
       },
       {
        "reel": 0,
        "row": 4,
        "apparitions": 3,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "L5"
      }
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 8,
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 60,
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
        "row": 4
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
    "total": 12
   },
   {
    "index": 12,
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
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H5",
       "multiplier": 3,
       "ttl": -1
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
      },
      {
       "name": "H5",
       "multiplier": 2,
       "ttl": -1
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
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H5"
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
     132,
     6,
     56,
     172,
     109
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
        "row": 1,
        "apparitions": 2,
        "ttl": -1
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 2,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 2880
   },
   {
    "index": 14,
    "type": "setTotalWin",
    "amount": 60
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
       "name": "H4",
       "multiplier": 3,
       "ttl": -1
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
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L2"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L3",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H4",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "W",
       "wild": true
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
       "name": "L1",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "HM",
       "mirror": true
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
     121,
     178,
     245,
     219,
     123
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 4
      },
      "reflected": [
       {
        "reel": 2,
        "row": 4,
        "apparitions": 6,
        "ttl": -1
       },
       {
        "reel": 0,
        "row": 3,
        "apparitions": 2,
        "ttl": -1
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2,
        "ttl": -1
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2,
        "ttl": -1
       },
       {
        "reel": 0,
        "row": 4,
        "apparitions": 6,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H4"
      }
     },
     {
      "mirror": {
       "reel": 2,
       "row": 2
      },
      "reflected": [
       {
        "reel": 1,
        "row": 2,
        "apparitions": 2,
        "ttl": -1
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 4,
        "ttl": -1
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 5,
        "ttl": -1
       },
       {
        "reel": 3,
        "row": 1,
        "apparitions": 2,
        "ttl": -1
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 5,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     },
     {
      "mirror": {
       "reel": 3,
       "row": 4
      },
      "reflected": [
       {
        "reel": 4,
        "row": 4,
        "apparitions": 4,
        "ttl": -1
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 7,
        "ttl": -1
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 9,
        "ttl": -1
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 7,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H4"
      }
     }
    ],
    "totalWays": 101640
   },
   {
    "index": 18,
    "type": "winInfo",
    "totalWin": 9600,
    "wins": [
     {
      "symbol": "H4",
      "kind": 4,
      "win": 9600,
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
       "ways": 96,
       "globalMult": 1,
       "winWithoutMult": 9600,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 19,
    "type": "setWin",
    "amount": 9600,
    "winLevel": 8
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 9660
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 12
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
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L4",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L3",
       "multiplier": 6,
       "ttl": -1
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
       "name": "L1"
      },
      {
       "name": "L4",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "H4",
       "multiplier": 2,
       "ttl": -1
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
       "name": "L3",
       "multiplier": 5,
       "ttl": -1
      },
      {
       "name": "L5"
      },
      {
       "name": "L3",
       "multiplier": 7,
       "ttl": -1
      },
      {
       "name": "H3",
       "multiplier": 9,
       "ttl": -1
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
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H4",
       "multiplier": 7,
       "ttl": -1
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
       "name": "L1",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     72,
     133,
     65,
     7,
     174
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
        "row": 1,
        "apparitions": 7,
        "ttl": -1
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 10,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 141120
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 9660
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
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "H4",
       "multiplier": 6,
       "ttl": -1
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
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H1",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L5",
       "multiplier": 2,
       "ttl": -1
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
       "name": "L5",
       "multiplier": 7,
       "ttl": -1
      },
      {
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 7,
       "ttl": -1
      },
      {
       "name": "L4",
       "multiplier": 9,
       "ttl": -1
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
       "name": "H3",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L3",
       "multiplier": 10,
       "ttl": -1
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
       "name": "L3",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     66,
     194,
     10,
     106,
     110
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
       "reel": 1,
       "row": 1
      },
      "reflected": [
       {
        "reel": 0,
        "row": 2,
        "apparitions": 3,
        "ttl": -1
       },
       {
        "reel": 0,
        "row": 1,
        "apparitions": 3,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     },
     {
      "mirror": {
       "reel": 3,
       "row": 2
      },
      "reflected": [
       {
        "reel": 3,
        "row": 1,
        "apparitions": 4,
        "ttl": -1
       },
       {
        "reel": 4,
        "row": 2,
        "apparitions": 2,
        "ttl": -1
       },
       {
        "reel": 4,
        "row": 3,
        "apparitions": 3,
        "ttl": -1
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 10,
        "ttl": -1
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 9,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 389760
   },
   {
    "index": 28,
    "type": "winInfo",
    "totalWin": 72000,
    "wins": [
     {
      "symbol": "H3",
      "kind": 5,
      "win": 72000,
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
        "row": 2
       }
      ],
      "meta": {
       "ways": 180,
       "globalMult": 1,
       "winWithoutMult": 72000,
       "symbolMult": 9
      }
     }
    ]
   },
   {
    "index": 29,
    "type": "setWin",
    "amount": 72000,
    "winLevel": 9
   },
   {
    "index": 30,
    "type": "setTotalWin",
    "amount": 81660
   },
   {
    "index": 31,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 12
   },
   {
    "index": 32,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H4"
      },
      {
       "name": "L3",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L4",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "H5",
       "multiplier": 6,
       "ttl": -1
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
       "name": "L5"
      },
      {
       "name": "H3",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
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
       "name": "L3"
      },
      {
       "name": "L4",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "H1"
      },
      {
       "name": "L4",
       "multiplier": 9,
       "ttl": -1
      },
      {
       "name": "H4",
       "multiplier": 9,
       "ttl": -1
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
       "name": "L1",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L3"
      },
      {
       "name": "H3",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H5"
      },
      {
       "name": "H5",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L2",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "H3",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     54,
     136,
     153,
     179,
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
    "index": 33,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 4
      },
      "reflected": [
       {
        "reel": 2,
        "row": 3,
        "apparitions": 12,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 430080
   },
   {
    "index": 34,
    "type": "setTotalWin",
    "amount": 81660
   },
   {
    "index": 35,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 12
   },
   {
    "index": 36,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L3"
      },
      {
       "name": "L2",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "H1",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L4",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L5",
       "multiplier": 6,
       "ttl": -1
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
       "name": "H2"
      },
      {
       "name": "H1",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L5",
       "multiplier": 2,
       "ttl": -1
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
       "name": "L5"
      },
      {
       "name": "L3",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "L5"
      },
      {
       "name": "L1",
       "multiplier": 12,
       "ttl": -1
      },
      {
       "name": "H4",
       "multiplier": 9,
       "ttl": -1
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
       "name": "L5",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "H1"
      },
      {
       "name": "L4",
       "multiplier": 10,
       "ttl": -1
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
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L5",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "H3",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     46,
     194,
     173,
     168,
     163
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
    "type": "winInfo",
    "totalWin": 11520,
    "wins": [
     {
      "symbol": "L5",
      "kind": 5,
      "win": 11520,
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
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "ways": 144,
       "globalMult": 1,
       "winWithoutMult": 11520,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 38,
    "type": "setWin",
    "amount": 11520,
    "winLevel": 9
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 93180
   },
   {
    "index": 40,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 12
   },
   {
    "index": 41,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
      },
      {
       "name": "H4",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L2",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L1",
       "multiplier": 6,
       "ttl": -1
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
       "name": "L4",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L3",
       "multiplier": 2,
       "ttl": -1
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
       "name": "H5",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L2",
       "multiplier": 12,
       "ttl": -1
      },
      {
       "name": "L5",
       "multiplier": 9,
       "ttl": -1
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
       "name": "L5",
       "multiplier": 4,
       "ttl": -1
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
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "H3",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L3",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     124,
     159,
     113,
     124,
     45
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
    "index": 42,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 2
      },
      "reflected": [
       {
        "reel": 1,
        "row": 3,
        "apparitions": 4,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H5"
      }
     }
    ],
    "totalWays": 250880
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 93180
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
       "name": "H4"
      },
      {
       "name": "H3",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L1",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "H3",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "H1",
       "multiplier": 6,
       "ttl": -1
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
       "name": "W",
       "wild": true
      },
      {
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L1",
       "multiplier": 4,
       "ttl": -1
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
       "name": "L5",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "L3"
      },
      {
       "name": "H2",
       "multiplier": 12,
       "ttl": -1
      },
      {
       "name": "L3",
       "multiplier": 9,
       "ttl": -1
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L5"
      },
      {
       "name": "L5",
       "multiplier": 10,
       "ttl": -1
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
       "name": "L3"
      },
      {
       "name": "L5",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L4",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "H5",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     176,
     110,
     75,
     56,
     132
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
    "index": 46,
    "type": "setTotalWin",
    "amount": 93180
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
       "name": "H5"
      },
      {
       "name": "L4",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L2",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "H5",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L2",
       "multiplier": 6,
       "ttl": -1
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
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L2",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L4",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "L2"
      },
      {
       "name": "H1",
       "multiplier": 12,
       "ttl": -1
      },
      {
       "name": "H3",
       "multiplier": 9,
       "ttl": -1
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
       "name": "L5",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10,
       "ttl": -1
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
       "name": "H2"
      },
      {
       "name": "L4",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "H1",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "H4",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     41,
     128,
     118,
     99,
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
    "index": 49,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 4
      },
      "reflected": [
       {
        "reel": 2,
        "row": 3,
        "apparitions": 14,
        "ttl": -1
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 11,
        "ttl": -1
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 6,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 806400
   },
   {
    "index": 50,
    "type": "winInfo",
    "totalWin": 76800,
    "wins": [
     {
      "symbol": "L4",
      "kind": 5,
      "win": 48000,
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
        "row": 3
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 600,
       "globalMult": 1,
       "winWithoutMult": 48000,
       "symbolMult": 10
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 28800,
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
       }
      ],
      "meta": {
       "ways": 720,
       "globalMult": 1,
       "winWithoutMult": 28800,
       "symbolMult": 10
      }
     }
    ]
   },
   {
    "index": 51,
    "type": "setWin",
    "amount": 76800,
    "winLevel": 9
   },
   {
    "index": 52,
    "type": "setTotalWin",
    "amount": 169980
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
       "name": "L3"
      },
      {
       "name": "L3",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L5",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L2",
       "multiplier": 6,
       "ttl": -1
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
       "name": "L3",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L1",
       "multiplier": 6,
       "ttl": -1
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
       "name": "L4",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "L3"
      },
      {
       "name": "H1",
       "multiplier": 14,
       "ttl": -1
      },
      {
       "name": "L4",
       "multiplier": 11,
       "ttl": -1
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
       "name": "H2",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "H2"
      },
      {
       "name": "H5",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H4"
      },
      {
       "name": "L2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "H1",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L4",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     195,
     187,
     4,
     82,
     198
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
    "index": 55,
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
        "apparitions": 12,
        "ttl": -1
       },
       {
        "reel": 4,
        "row": 3,
        "apparitions": 6,
        "ttl": -1
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 1095120
   },
   {
    "index": 56,
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 60,
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
       "ways": 6,
       "globalMult": 1,
       "winWithoutMult": 60,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 57,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 58,
    "type": "setTotalWin",
    "amount": 170040
   },
   {
    "index": 59,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 12
   },
   {
    "index": 60,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L4"
      },
      {
       "name": "L3",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "L3",
       "multiplier": 3,
       "ttl": -1
      },
      {
       "name": "H2",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L3",
       "multiplier": 6,
       "ttl": -1
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
       "name": "L4"
      },
      {
       "name": "L3",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "H5",
       "multiplier": 6,
       "ttl": -1
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
       "name": "L4",
       "multiplier": 10,
       "ttl": -1
      },
      {
       "name": "H1"
      },
      {
       "name": "L4",
       "multiplier": 14,
       "ttl": -1
      },
      {
       "name": "H4",
       "multiplier": 11,
       "ttl": -1
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
       "name": "L2",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L1",
       "multiplier": 12,
       "ttl": -1
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
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4",
       "multiplier": 2,
       "ttl": -1
      },
      {
       "name": "L3",
       "multiplier": 6,
       "ttl": -1
      },
      {
       "name": "H3",
       "multiplier": 4,
       "ttl": -1
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     239,
     160,
     153,
     72,
     99
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
    "type": "setTotalWin",
    "amount": 170040
   },
   {
    "index": 62,
    "type": "freeSpinEnd",
    "amount": 170040,
    "winLevel": 8
   },
   {
    "index": 63,
    "type": "finalWin",
    "amount": 170040
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 1700.4
 }
];
