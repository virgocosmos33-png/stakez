export default [
 {
  "id": 1,
  "payoutMultiplier": 74040,
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
       "name": "L2"
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
       "name": "L5"
      },
      {
       "name": "L4"
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
       "name": "S",
       "scatter": true
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
       "name": "L3"
      },
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
       "name": "H1"
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "ME",
       "eye": true
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
        "apparitions": 4
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 3
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 4
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 5376
   },
   {
    "index": 2,
    "type": "madamsEye",
    "eye": {
     "reel": 4,
     "row": 4
    },
    "converted": [
     {
      "reel": 1,
      "row": 3,
      "apparitions": 4
     },
     {
      "reel": 2,
      "row": 1,
      "apparitions": 3
     },
     {
      "reel": 3,
      "row": 1,
      "apparitions": 4
     },
     {
      "reel": 3,
      "row": 3,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 3,
    "type": "winInfo",
    "totalWin": 74040,
    "wins": [
     {
      "symbol": "L2",
      "kind": 5,
      "win": 12600,
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
        "row": 1
       },
       {
        "reel": 3,
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
      "meta": {
       "ways": 105,
       "globalMult": 1,
       "winWithoutMult": 12600,
       "symbolMult": 13
      }
     },
     {
      "symbol": "H3",
      "kind": 5,
      "win": 38400,
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
        "reel": 3,
        "row": 3
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "ways": 96,
       "globalMult": 1,
       "winWithoutMult": 38400,
       "symbolMult": 13
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 5760,
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
       "ways": 72,
       "globalMult": 1,
       "winWithoutMult": 5760,
       "symbolMult": 13
      }
     },
     {
      "symbol": "L3",
      "kind": 5,
      "win": 17280,
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
        "row": 3
       },
       {
        "reel": 4,
        "row": 1
       },
       {
        "reel": 4,
        "row": 3
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "ways": 216,
       "globalMult": 1,
       "winWithoutMult": 17280,
       "symbolMult": 13
      }
     }
    ]
   },
   {
    "index": 4,
    "type": "setWin",
    "amount": 74040,
    "winLevel": 9
   },
   {
    "index": 5,
    "type": "setTotalWin",
    "amount": 74040
   },
   {
    "index": 6,
    "type": "finalWin",
    "amount": 74040
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 740.4,
  "freeGameWins": 0.0
 },
 {
  "id": 0,
  "payoutMultiplier": 54040,
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
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
       "name": "L3"
      },
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
       "name": "HM",
       "mirror": true
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
       "name": "H4"
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
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "ME",
       "eye": true
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
       "name": "L4"
      },
      {
       "name": "H1"
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
     245,
     155,
     217,
     60,
     91
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
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 2,
    "type": "madamsEye",
    "eye": {
     "reel": 3,
     "row": 3
    },
    "converted": [
     {
      "reel": 2,
      "row": 3,
      "apparitions": 2
     },
     {
      "reel": 2,
      "row": 4,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 3,
    "type": "winInfo",
    "totalWin": 1200,
    "wins": [
     {
      "symbol": "L3",
      "kind": 4,
      "win": 240,
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
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 240,
       "symbolMult": 4
      }
     },
     {
      "symbol": "H3",
      "kind": 4,
      "win": 960,
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
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 960,
       "symbolMult": 4
      }
     }
    ]
   },
   {
    "index": 4,
    "type": "setWin",
    "amount": 1200,
    "winLevel": 5
   },
   {
    "index": 5,
    "type": "setTotalWin",
    "amount": 1200
   },
   {
    "index": 6,
    "type": "freeSpinTrigger",
    "totalFs": 10,
    "positions": [
     {
      "reel": 0,
      "row": 4
     },
     {
      "reel": 2,
      "row": 1
     },
     {
      "reel": 3,
      "row": 4
     },
     {
      "reel": 4,
      "row": 4
     }
    ]
   },
   {
    "index": 7,
    "type": "bonusLevel",
    "level": 2,
    "name": "THE_OTHER_SIDE",
    "startHaunted": []
   },
   {
    "index": 8,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 10
   },
   {
    "index": 9,
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
       "name": "H4"
      },
      {
       "name": "L4"
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
       "name": "L1"
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
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
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
       "name": "L3"
      },
      {
       "name": "ME",
       "eye": true
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
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
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     56,
     195,
     112,
     240,
     126
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 3
      },
      "reflected": [
       {
        "reel": 2,
        "row": 2,
        "apparitions": 2,
        "ttl": 2
       },
       {
        "reel": 1,
        "row": 4,
        "apparitions": 2,
        "ttl": 2
       },
       {
        "reel": 1,
        "row": 2,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 0,
        "row": 3,
        "apparitions": 3,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 3360
   },
   {
    "index": 11,
    "type": "madamsEye",
    "eye": {
     "reel": 3,
     "row": 1
    },
    "converted": [
     {
      "reel": 0,
      "row": 3,
      "apparitions": 3
     },
     {
      "reel": 1,
      "row": 2,
      "apparitions": 3
     },
     {
      "reel": 1,
      "row": 4,
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
    "index": 12,
    "type": "winInfo",
    "totalWin": 22800,
    "wins": [
     {
      "symbol": "L2",
      "kind": 4,
      "win": 1600,
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
        "row": 1
       }
      ],
      "meta": {
       "ways": 40,
       "globalMult": 1,
       "winWithoutMult": 1600,
       "symbolMult": 10
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 18000,
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
        "row": 4
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
       "ways": 60,
       "globalMult": 1,
       "winWithoutMult": 18000,
       "symbolMult": 10
      }
     },
     {
      "symbol": "H5",
      "kind": 4,
      "win": 3200,
      "positions": [
       {
        "reel": 0,
        "row": 4
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
       "ways": 40,
       "globalMult": 1,
       "winWithoutMult": 3200,
       "symbolMult": 10
      }
     }
    ]
   },
   {
    "index": 13,
    "type": "setWin",
    "amount": 22800,
    "winLevel": 9
   },
   {
    "index": 14,
    "type": "setTotalWin",
    "amount": 24000
   },
   {
    "index": 15,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 10
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "H5"
      },
      {
       "name": "H2",
       "multiplier": 3,
       "ttl": 1
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
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L3",
       "multiplier": 3,
       "ttl": 1
      },
      {
       "name": "H5"
      },
      {
       "name": "L1",
       "multiplier": 2,
       "ttl": 1
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
       "name": "H5",
       "multiplier": 2,
       "ttl": 1
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
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
       "name": "L2"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L4"
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
       "name": "H5"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     150,
     218,
     8,
     122,
     62
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
    "index": 17,
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
        "row": 2,
        "apparitions": 2,
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
       "name": "H5"
      }
     }
    ],
    "totalWays": 5040
   },
   {
    "index": 18,
    "type": "winInfo",
    "totalWin": 500,
    "wins": [
     {
      "symbol": "H5",
      "kind": 5,
      "win": 500,
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
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 500,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 19,
    "type": "setWin",
    "amount": 500,
    "winLevel": 5
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 24500
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 10
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
       "name": "H3"
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
       "name": "L2"
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
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
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
       "name": "H3"
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
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H4"
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
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1",
       "multiplier": 2,
       "ttl": 1
      },
      {
       "name": "L1"
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
     180,
     217,
     157,
     151,
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
        "reel": 4,
        "row": 3,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 5,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 3584
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 24500
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
       "name": "H5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
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
       "name": "H5"
      },
      {
       "name": "H5"
      },
      {
       "name": "L4",
       "multiplier": 5,
       "ttl": 1
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
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
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5",
       "multiplier": 3,
       "ttl": 1
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
     98,
     200,
     219,
     210,
     244
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
    "type": "setTotalWin",
    "amount": 24500
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
       "name": "H5"
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
       "name": "L2"
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
       "name": "H3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H2"
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
       "name": "H4"
      },
      {
       "name": "L5"
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
       "name": "W",
       "wild": true
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
       "name": "H3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     132,
     199,
     143,
     52,
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
    "index": 30,
    "type": "setTotalWin",
    "amount": 24500
   },
   {
    "index": 31,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 10
   },
   {
    "index": 32,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
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
       "name": "L2"
      },
      {
       "name": "ME",
       "eye": true
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
       "name": "H3"
      },
      {
       "name": "H5"
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
       "name": "H4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H2"
      },
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
       "name": "L5"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     93,
     145,
     141,
     51,
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
    "index": 33,
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
        "apparitions": 2,
        "ttl": 2
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 4,
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
    "totalWays": 2400
   },
   {
    "index": 34,
    "type": "madamsEye",
    "eye": {
     "reel": 1,
     "row": 2
    },
    "converted": [
     {
      "reel": 2,
      "row": 2,
      "apparitions": 3
     },
     {
      "reel": 3,
      "row": 4,
      "apparitions": 2
     },
     {
      "reel": 4,
      "row": 2,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 35,
    "type": "winInfo",
    "totalWin": 12600,
    "wins": [
     {
      "symbol": "L5",
      "kind": 5,
      "win": 4320,
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
       },
       {
        "reel": 3,
        "row": 2
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
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 54,
       "globalMult": 1,
       "winWithoutMult": 4320,
       "symbolMult": 7
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 5400,
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
       "ways": 18,
       "globalMult": 1,
       "winWithoutMult": 5400,
       "symbolMult": 7
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 2880,
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
        "reel": 2,
        "row": 2
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
       "ways": 24,
       "globalMult": 1,
       "winWithoutMult": 2880,
       "symbolMult": 7
      }
     }
    ]
   },
   {
    "index": 36,
    "type": "setWin",
    "amount": 12600,
    "winLevel": 9
   },
   {
    "index": 37,
    "type": "setTotalWin",
    "amount": 37100
   },
   {
    "index": 38,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 10
   },
   {
    "index": 39,
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
       "name": "H1"
      },
      {
       "name": "H4"
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
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H4"
      },
      {
       "name": "H5"
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
       "name": "L3"
      },
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
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "H3"
      },
      {
       "name": "H5",
       "multiplier": 2,
       "ttl": 1
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
       "name": "H5"
      },
      {
       "name": "L5",
       "multiplier": 2,
       "ttl": 1
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
     71,
     63,
     68,
     28,
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
    "index": 40,
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
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 3000
   },
   {
    "index": 41,
    "type": "setTotalWin",
    "amount": 37100
   },
   {
    "index": 42,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 10
   },
   {
    "index": 43,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H5"
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
       "name": "H3"
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
       "name": "H1"
      },
      {
       "name": "L5",
       "multiplier": 2,
       "ttl": 1
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
       "name": "L3"
      },
      {
       "name": "H5"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L1"
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
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
       "name": "ME",
       "eye": true
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
     79,
     98,
     87,
     107,
     203
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
       "reel": 2,
       "row": 2
      },
      "reflected": [
       {
        "reel": 2,
        "row": 1,
        "apparitions": 3,
        "ttl": 2
       },
       {
        "reel": 3,
        "row": 1,
        "apparitions": 2,
        "ttl": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 2400
   },
   {
    "index": 45,
    "type": "madamsEye",
    "eye": {
     "reel": 4,
     "row": 3
    },
    "converted": [
     {
      "reel": 1,
      "row": 2,
      "apparitions": 2
     },
     {
      "reel": 2,
      "row": 1,
      "apparitions": 3
     },
     {
      "reel": 3,
      "row": 1,
      "apparitions": 2
     }
    ]
   },
   {
    "index": 46,
    "type": "winInfo",
    "totalWin": 16900,
    "wins": [
     {
      "symbol": "L5",
      "kind": 5,
      "win": 2560,
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
        "reel": 3,
        "row": 1
       },
       {
        "reel": 4,
        "row": 1
       },
       {
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "ways": 32,
       "globalMult": 1,
       "winWithoutMult": 2560,
       "symbolMult": 7
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 8100,
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
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 1
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
        "row": 3
       }
      ],
      "meta": {
       "ways": 27,
       "globalMult": 1,
       "winWithoutMult": 8100,
       "symbolMult": 7
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 1440,
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
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 1440,
       "symbolMult": 7
      }
     },
     {
      "symbol": "H3",
      "kind": 5,
      "win": 4800,
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
        "row": 3
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 4800,
       "symbolMult": 7
      }
     }
    ]
   },
   {
    "index": 47,
    "type": "setWin",
    "amount": 16900,
    "winLevel": 9
   },
   {
    "index": 48,
    "type": "setTotalWin",
    "amount": 54000
   },
   {
    "index": 49,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 10
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
       "name": "H4"
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
       "name": "L5"
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
       "name": "L1"
      },
      {
       "name": "L3",
       "multiplier": 3,
       "ttl": 1
      },
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
       "name": "H5"
      }
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H1",
       "multiplier": 2,
       "ttl": 1
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
       "name": "H5"
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
       "name": "L2"
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
     166,
     7,
     101,
     172,
     147
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
    "type": "setTotalWin",
    "amount": 54000
   },
   {
    "index": 52,
    "type": "updateFreeSpin",
    "amount": 9,
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
       "name": "H4"
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
       "name": "H5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
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
       "name": "H2"
      },
      {
       "name": "H3"
      },
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
       "name": "H3"
      },
      {
       "name": "L1"
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
     188,
     76,
     32,
     247,
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
    "index": 54,
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
        "row": 4
       },
       {
        "reel": 2,
        "row": 3
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
    "index": 55,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 56,
    "type": "setTotalWin",
    "amount": 54040
   },
   {
    "index": 57,
    "type": "freeSpinEnd",
    "amount": 52840,
    "winLevel": 8
   },
   {
    "index": 58,
    "type": "finalWin",
    "amount": 54040
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 12.0,
  "freeGameWins": 528.4
 }
];
