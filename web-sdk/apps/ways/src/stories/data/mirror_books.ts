export default [
 {
  "id": 5,
  "payoutMultiplier": 380,
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
       "name": "L3"
      },
      {
       "name": "L3"
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
       "name": "L4"
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
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H4"
      },
      {
       "name": "L2"
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
       "name": "L1"
      },
      {
       "name": "L5"
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
     210,
     20,
     124,
     195,
     66
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
        "reel": 1,
        "row": 2,
        "apparitions": 3
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 3,
        "row": 1,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 4608
   },
   {
    "index": 2,
    "type": "winInfo",
    "totalWin": 380,
    "wins": [
     {
      "symbol": "L2",
      "kind": 4,
      "win": 80,
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
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 200,
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
        "reel": 1,
        "row": 3
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
       "ways": 20,
       "globalMult": 1,
       "winWithoutMult": 200,
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
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 100,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 3,
    "type": "setWin",
    "amount": 380,
    "winLevel": 4
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 380
   },
   {
    "index": 5,
    "type": "finalWin",
    "amount": 380
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 3.8,
  "freeGameWins": 0.0
 },
 {
  "id": 2,
  "payoutMultiplier": 8440,
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
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
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
       "name": "L4"
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
       "name": "S",
       "scatter": true
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
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
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
     246,
     183,
     245,
     120,
     21
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
       "row": 2
      },
      "reflected": [
       {
        "reel": 2,
        "row": 1,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 1280
   },
   {
    "index": 2,
    "type": "winInfo",
    "totalWin": 250,
    "wins": [
     {
      "symbol": "L3",
      "kind": 5,
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
        "row": 4
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
        "reel": 3,
        "row": 4
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "ways": 3,
       "globalMult": 1,
       "winWithoutMult": 240,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 10,
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
    "index": 3,
    "type": "setWin",
    "amount": 250,
    "winLevel": 4
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 250
   },
   {
    "index": 5,
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
      "row": 2
     }
    ]
   },
   {
    "index": 6,
    "type": "bonusLevel",
    "level": 1,
    "name": "THE_SEANCE",
    "startHaunted": []
   },
   {
    "index": 7,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 8,
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
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "L1"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H4"
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
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L3"
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
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     210,
     221,
     68,
     121,
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
    "index": 9,
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
        "apparitions": 3
       },
       {
        "reel": 4,
        "row": 3,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
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
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 4
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 4480
   },
   {
    "index": 10,
    "type": "setTotalWin",
    "amount": 250
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
       "name": "L1"
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
       "name": "L2"
      },
      {
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
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
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L1"
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
     ]
    ],
    "paddingPositions": [
     237,
     7,
     219,
     71,
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
    "index": 13,
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
        "row": 4,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 1280
   },
   {
    "index": 14,
    "type": "setTotalWin",
    "amount": 250
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
       "name": "L2"
      },
      {
       "name": "L1"
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
       "name": "H4"
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
       "name": "L4"
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
       "name": "L2"
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
       "name": "L1"
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
     105,
     229,
     38,
     5,
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
    "index": 17,
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
        "reel": 2,
        "row": 3,
        "apparitions": 4
       },
       {
        "reel": 4,
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 4,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "L1"
      }
     }
    ],
    "totalWays": 6048
   },
   {
    "index": 18,
    "type": "winInfo",
    "totalWin": 130,
    "wins": [
     {
      "symbol": "H4",
      "kind": 4,
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
       "winWithoutMult": 100,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 30,
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
    "index": 19,
    "type": "setWin",
    "amount": 130,
    "winLevel": 3
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 380
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
       "name": "L1"
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
       "name": "L4"
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
       "name": "L4"
      },
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
       "name": "L3"
      },
      {
       "name": "L4"
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
     86,
     80,
     92,
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
    "index": 23,
    "type": "setTotalWin",
    "amount": 380
   },
   {
    "index": 24,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
   },
   {
    "index": 25,
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
       "name": "H3"
      },
      {
       "name": "L5"
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
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "L3"
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
       "name": "L2"
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
     117,
     222,
     133,
     98,
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
    "index": 26,
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 20,
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
        "row": 4
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
    "index": 27,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 28,
    "type": "setTotalWin",
    "amount": 400
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
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H1"
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
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
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
       "name": "L1"
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
       "name": "H4"
      },
      {
       "name": "H1"
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
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
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
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L1"
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
     ]
    ],
    "paddingPositions": [
     26,
     158,
     249,
     240,
     207
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
    "index": 31,
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
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2
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
       },
       {
        "reel": 4,
        "row": 4,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 5184
   },
   {
    "index": 32,
    "type": "winInfo",
    "totalWin": 6400,
    "wins": [
     {
      "symbol": "L3",
      "kind": 5,
      "win": 6400,
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
       "ways": 80,
       "globalMult": 1,
       "winWithoutMult": 6400,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 33,
    "type": "setWin",
    "amount": 6400,
    "winLevel": 8
   },
   {
    "index": 34,
    "type": "setTotalWin",
    "amount": 6800
   },
   {
    "index": 35,
    "type": "freeSpinRetrigger",
    "totalFs": 11,
    "positions": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 1,
      "row": 1
     }
    ]
   },
   {
    "index": 36,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 11
   },
   {
    "index": 37,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
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
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
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
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
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
       "name": "H4"
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
       "name": "L2"
      },
      {
       "name": "H4"
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
     ]
    ],
    "paddingPositions": [
     125,
     5,
     150,
     15,
     244
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
        "row": 2,
        "apparitions": 3
       },
       {
        "reel": 0,
        "row": 2,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "L3"
      }
     },
     {
      "mirror": {
       "reel": 1,
       "row": 4
      },
      "reflected": [
       {
        "reel": 0,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 4032
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 6800
   },
   {
    "index": 40,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 11
   },
   {
    "index": 41,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L2"
      },
      {
       "name": "H2"
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
       "name": "L1"
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "L3"
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
       "name": "H4"
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
       "name": "L3"
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
       "name": "L5"
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
       "name": "L3"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     111,
     166,
     178,
     24,
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
    "index": 42,
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
        "row": 2,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 3
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 1,
        "row": 4,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     },
     {
      "mirror": {
       "reel": 1,
       "row": 1
      },
      "reflected": [
       {
        "reel": 0,
        "row": 1,
        "apparitions": 2
       },
       {
        "reel": 1,
        "row": 2,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 5760
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 6800
   },
   {
    "index": 44,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 11
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
       "name": "H4"
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
       "name": "L2"
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
       "name": "L5"
      },
      {
       "name": "S",
       "scatter": true
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
       "name": "H3"
      },
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     74,
     107,
     145,
     104,
     9
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
    "index": 46,
    "type": "winInfo",
    "totalWin": 160,
    "wins": [
     {
      "symbol": "H4",
      "kind": 3,
      "win": 80,
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
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 80,
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
        "row": 2
       },
       {
        "reel": 4,
        "row": 4
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
    "index": 47,
    "type": "setWin",
    "amount": 160,
    "winLevel": 3
   },
   {
    "index": 48,
    "type": "setTotalWin",
    "amount": 6960
   },
   {
    "index": 49,
    "type": "freeSpinRetrigger",
    "totalFs": 14,
    "positions": [
     {
      "reel": 1,
      "row": 2
     },
     {
      "reel": 3,
      "row": 3
     }
    ]
   },
   {
    "index": 50,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 14
   },
   {
    "index": 51,
    "type": "reveal",
    "board": [
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
       "name": "H3"
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
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1"
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
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "H2"
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
     1,
     122,
     241,
     213,
     225
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
        "apparitions": 3
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 4,
        "row": 4,
        "apparitions": 4
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 3360
   },
   {
    "index": 53,
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 20,
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
    "index": 54,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 55,
    "type": "setTotalWin",
    "amount": 6980
   },
   {
    "index": 56,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 14
   },
   {
    "index": 57,
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "L2"
      },
      {
       "name": "L1"
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
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
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
       "name": "L2"
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
       "name": "H1"
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
       "name": "L4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     236,
     50,
     229,
     226,
     230
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
    "index": 58,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 2,
       "row": 3
      },
      "reflected": [
       {
        "reel": 2,
        "row": 4,
        "apparitions": 4
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 1792
   },
   {
    "index": 59,
    "type": "winInfo",
    "totalWin": 1200,
    "wins": [
     {
      "symbol": "L1",
      "kind": 5,
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
        "row": 1
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 10,
       "globalMult": 1,
       "winWithoutMult": 1200,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 60,
    "type": "setWin",
    "amount": 1200,
    "winLevel": 5
   },
   {
    "index": 61,
    "type": "setTotalWin",
    "amount": 8180
   },
   {
    "index": 62,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 14
   },
   {
    "index": 63,
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
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
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
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true
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
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L1"
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
     ]
    ],
    "paddingPositions": [
     207,
     200,
     15,
     90,
     56
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 1
      },
      "reflected": [
       {
        "reel": 3,
        "row": 2,
        "apparitions": 2
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
    "index": 65,
    "type": "winInfo",
    "totalWin": 240,
    "wins": [
     {
      "symbol": "H3",
      "kind": 4,
      "win": 240,
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
    "amount": 8420
   },
   {
    "index": 68,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 14
   },
   {
    "index": 69,
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
       "name": "L4"
      },
      {
       "name": "L4"
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
       "name": "H4"
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
       "name": "H4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
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
       "name": "H1"
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
     133,
     108,
     13,
     121,
     82
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
    "index": 70,
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 20,
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
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 20,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 71,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 72,
    "type": "setTotalWin",
    "amount": 8440
   },
   {
    "index": 73,
    "type": "updateFreeSpin",
    "amount": 13,
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
       "name": "H3"
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
       "name": "H2"
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
       "name": "L4"
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
       "name": "L3"
      },
      {
       "name": "L4"
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
       "name": "L4"
      },
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
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     14,
     198,
     32,
     11,
     31
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
        "reel": 1,
        "row": 3,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 1600
   },
   {
    "index": 76,
    "type": "setTotalWin",
    "amount": 8440
   },
   {
    "index": 77,
    "type": "freeSpinEnd",
    "amount": 8190,
    "winLevel": 6
   },
   {
    "index": 78,
    "type": "finalWin",
    "amount": 8440
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 2.5,
  "freeGameWins": 81.9
 },
 {
  "id": 0,
  "payoutMultiplier": 13890,
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
       "name": "L4"
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
       "name": "L2"
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
       "name": "S",
       "scatter": true
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
       "name": "L3"
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
        "reel": 0,
        "row": 3,
        "apparitions": 4
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
    "index": 2,
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
        "row": 2
       },
       {
        "reel": 1,
        "row": 2
       },
       {
        "reel": 2,
        "row": 4
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
    "index": 3,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 10
   },
   {
    "index": 5,
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
    "index": 6,
    "type": "bonusLevel",
    "level": 2,
    "name": "THE_OTHER_SIDE",
    "startHaunted": []
   },
   {
    "index": 7,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 10
   },
   {
    "index": 8,
    "type": "reveal",
    "board": [
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
       "name": "H4"
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
       "name": "L4"
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
       "name": "L2"
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
       "name": "HM",
       "mirror": true
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
       "name": "L3"
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
       "name": "L1"
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
       "name": "L3"
      },
      {
       "name": "H2"
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
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     55,
     248,
     108,
     185,
     7
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
    "index": 9,
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
        "apparitions": 3
       },
       {
        "reel": 1,
        "row": 1,
        "apparitions": 3
       },
       {
        "reel": 3,
        "row": 1,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 2688
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
        "reel": 1,
        "row": 1
       },
       {
        "reel": 1,
        "row": 4
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
    "amount": 90
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
       "name": "L2"
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
       "name": "H3"
      },
      {
       "name": "H3",
       "multiplier": 3
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
       "name": "W",
       "wild": true
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
       "name": "H4"
      },
      {
       "name": "H1"
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
       "name": "H2",
       "multiplier": 2
      },
      {
       "name": "H4",
       "multiplier": 3
      },
      {
       "name": "H4"
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
       "name": "L3"
      },
      {
       "name": "H3"
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
     229,
     184,
     249,
     182,
     128
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
    "index": 15,
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
        "row": 4
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
    "index": 16,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 17,
    "type": "setTotalWin",
    "amount": 130
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
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1"
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
       "name": "L3"
      },
      {
       "name": "L5"
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
       "name": "L3"
      },
      {
       "name": "L4"
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
       "name": "H3"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H4"
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
       "name": "L1"
      },
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     212,
     233,
     171,
     48,
     77
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
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 2
       },
       {
        "reel": 3,
        "row": 1,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     },
     {
      "mirror": {
       "reel": 1,
       "row": 3
      },
      "reflected": [
       {
        "reel": 2,
        "row": 2,
        "apparitions": 2
       },
       {
        "reel": 1,
        "row": 2,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 4
       },
       {
        "reel": 0,
        "row": 2,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 2
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
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 6
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 5
       }
      ],
      "mirrorBecomes": {
       "name": "H4"
      }
     }
    ],
    "totalWays": 18000
   },
   {
    "index": 21,
    "type": "setTotalWin",
    "amount": 130
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
       "name": "H4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5",
       "multiplier": 2
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
     ],
     [
      {
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2",
       "multiplier": 3
      },
      {
       "name": "H3"
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
       "name": "L3",
       "multiplier": 2
      },
      {
       "name": "L2",
       "multiplier": 2
      },
      {
       "name": "H3",
       "multiplier": 5
      },
      {
       "name": "L3",
       "multiplier": 6
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
       "name": "H3",
       "multiplier": 2
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H2"
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
       "name": "L2",
       "multiplier": 3
      },
      {
       "name": "L2"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1",
       "multiplier": 3
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     131,
     88,
     243,
     216,
     147
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
    "index": 24,
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
        "apparitions": 10
       },
       {
        "reel": 0,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 7
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     },
     {
      "mirror": {
       "reel": 3,
       "row": 2
      },
      "reflected": [
       {
        "reel": 4,
        "row": 2,
        "apparitions": 2
       },
       {
        "reel": 3,
        "row": 1,
        "apparitions": 4
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 9
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 52164
   },
   {
    "index": 25,
    "type": "winInfo",
    "totalWin": 12960,
    "wins": [
     {
      "symbol": "H3",
      "kind": 4,
      "win": 12960,
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
       }
      ],
      "meta": {
       "ways": 108,
       "globalMult": 1,
       "winWithoutMult": 12960,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 26,
    "type": "setWin",
    "amount": 12960,
    "winLevel": 9
   },
   {
    "index": 27,
    "type": "setTotalWin",
    "amount": 13090
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H4",
       "multiplier": 2
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
       "name": "H1"
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
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L4",
       "multiplier": 9
      },
      {
       "name": "H3",
       "multiplier": 10
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
       "name": "L1",
       "multiplier": 4
      },
      {
       "name": "L5"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L5"
      },
      {
       "name": "L4",
       "multiplier": 2
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
     ]
    ],
    "paddingPositions": [
     84,
     117,
     153,
     7,
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
    "index": 30,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 3
      },
      "reflected": [
       {
        "reel": 2,
        "row": 2,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 15400
   },
   {
    "index": 31,
    "type": "setTotalWin",
    "amount": 13090
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
       "name": "L3"
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
       "name": "H2"
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
       "name": "L3",
       "multiplier": 2
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
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true
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
       "name": "L1"
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
    "index": 34,
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
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 1,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 35,
    "type": "setTotalWin",
    "amount": 13090
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
       "name": "H4"
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
       "name": "H2"
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
       "name": "L5",
       "multiplier": 2
      },
      {
       "name": "H2"
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L1",
       "multiplier": 2
      },
      {
       "name": "L2"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L4"
      },
      {
       "name": "H3"
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
     ],
     [
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
       "name": "L3"
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
     107,
     203,
     48,
     66,
     27
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
       "row": 3
      },
      "reflected": [
       {
        "reel": 3,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 4
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
      }
     }
    ],
    "totalWays": 3840
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 13090
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
       "name": "L2"
      },
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
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
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
       "name": "L4"
      },
      {
       "name": "L2",
       "multiplier": 4
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
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1",
       "multiplier": 3
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
       "name": "H4"
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
       "name": "H4"
      },
      {
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     177,
     132,
     115,
     57,
     134
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 4
      },
      "reflected": [
       {
        "reel": 0,
        "row": 3,
        "apparitions": 2
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
    "index": 43,
    "type": "setTotalWin",
    "amount": 13090
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "H1",
       "multiplier": 2
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
       "name": "L1"
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
       "name": "L5"
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
       "name": "H4"
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
       "name": "L5"
      }
     ],
     [
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L1"
      },
      {
       "name": "H2"
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
     190,
     40,
     106,
     144,
     64
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
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 1600
   },
   {
    "index": 47,
    "type": "setTotalWin",
    "amount": 13090
   },
   {
    "index": 48,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 10
   },
   {
    "index": 49,
    "type": "reveal",
    "board": [
     [
      {
       "name": "S",
       "scatter": true
      },
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
       "name": "H4"
      },
      {
       "name": "H2"
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
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L1"
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
       "name": "L1",
       "multiplier": 2
      },
      {
       "name": "L1"
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
       "name": "L3"
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
       "name": "W",
       "wild": true
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
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     151,
     49,
     126,
     26,
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
    "index": 50,
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
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 1,
        "row": 1,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 3360
   },
   {
    "index": 51,
    "type": "winInfo",
    "totalWin": 800,
    "wins": [
     {
      "symbol": "L1",
      "kind": 4,
      "win": 800,
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
        "row": 1
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "ways": 20,
       "globalMult": 1,
       "winWithoutMult": 800,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 52,
    "type": "setWin",
    "amount": 800,
    "winLevel": 5
   },
   {
    "index": 53,
    "type": "setTotalWin",
    "amount": 13890
   },
   {
    "index": 54,
    "type": "freeSpinEnd",
    "amount": 13880,
    "winLevel": 7
   },
   {
    "index": 55,
    "type": "finalWin",
    "amount": 13890
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.1,
  "freeGameWins": 138.8
 },
 {
  "id": 0,
  "payoutMultiplier": 50580,
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
       "name": "L4"
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
       "name": "L4"
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
       "name": "L3"
      },
      {
       "name": "H3"
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
       "name": "L1"
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
       "name": "S",
       "scatter": true
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
       "name": "S",
       "scatter": true
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
     ]
    ],
    "paddingPositions": [
     245,
     246,
     214,
     61,
     93
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
       "reel": 1,
       "row": 4
      },
      "reflected": [
       {
        "reel": 2,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 0,
        "row": 3,
        "apparitions": 4
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2
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
    "index": 2,
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
    "index": 3,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 10
   },
   {
    "index": 5,
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
      "row": 4
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
    "index": 6,
    "type": "bonusLevel",
    "level": 3,
    "name": "BLOOD_MOON",
    "startHaunted": []
   },
   {
    "index": 7,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 12
   },
   {
    "index": 8,
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
       "name": "L1"
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
       "name": "H3"
      },
      {
       "name": "H2"
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
       "name": "H3"
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
       "name": "L1"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L2"
      },
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
       "name": "L5"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     173,
     56,
     194,
     117,
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
    "index": 9,
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
        "row": 4,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 1536
   },
   {
    "index": 10,
    "type": "winInfo",
    "totalWin": 440,
    "wins": [
     {
      "symbol": "L5",
      "kind": 5,
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
        "row": 4
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
        "row": 4
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 320,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
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
        "row": 4
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
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 120,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 11,
    "type": "setWin",
    "amount": 440,
    "winLevel": 4
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 450
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
       "name": "L3"
      },
      {
       "name": "S",
       "scatter": true
      },
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
       "name": "L3"
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
       "name": "L2"
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L1",
       "multiplier": 3
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
    "index": 15,
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
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H4"
      }
     }
    ],
    "totalWays": 1920
   },
   {
    "index": 16,
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
        "row": 2
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
    "index": 17,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 18,
    "type": "setTotalWin",
    "amount": 490
   },
   {
    "index": 19,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 12
   },
   {
    "index": 20,
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
       "name": "H1"
      },
      {
       "name": "H4"
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
       "name": "H3"
      },
      {
       "name": "S",
       "scatter": true
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
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1",
       "multiplier": 2
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
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5",
       "multiplier": 3
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     217,
     157,
     151,
     148,
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
    "index": 21,
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
        "apparitions": 2
       },
       {
        "reel": 3,
        "row": 2,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 4,
        "apparitions": 4
       },
       {
        "reel": 3,
        "row": 4,
        "apparitions": 4
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 9072
   },
   {
    "index": 22,
    "type": "winInfo",
    "totalWin": 80,
    "wins": [
     {
      "symbol": "H4",
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
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "ways": 2,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 23,
    "type": "setWin",
    "amount": 80,
    "winLevel": 2
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 570
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 12
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
       "name": "H2"
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
       "name": "L4"
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
       "name": "L2"
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
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3",
       "multiplier": 2
      },
      {
       "name": "L4",
       "multiplier": 2
      },
      {
       "name": "L4",
       "multiplier": 4
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
       "name": "H4",
       "multiplier": 3
      },
      {
       "name": "L2"
      },
      {
       "name": "H1",
       "multiplier": 4
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
       "name": "L2",
       "multiplier": 2
      },
      {
       "name": "H4"
      },
      {
       "name": "L5",
       "multiplier": 3
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     199,
     143,
     52,
     109,
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
        "reel": 0,
        "row": 2,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "W"
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
        "apparitions": 7
       },
       {
        "reel": 0,
        "row": 3,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "L2"
      }
     }
    ],
    "totalWays": 32760
   },
   {
    "index": 28,
    "type": "winInfo",
    "totalWin": 180,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "ways": 18,
       "globalMult": 1,
       "winWithoutMult": 180,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 29,
    "type": "setWin",
    "amount": 180,
    "winLevel": 3
   },
   {
    "index": 30,
    "type": "setTotalWin",
    "amount": 750
   },
   {
    "index": 31,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 12
   },
   {
    "index": 32,
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
       "name": "H3",
       "multiplier": 3
      },
      {
       "name": "H1",
       "multiplier": 3
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
       "name": "L3"
      },
      {
       "name": "L1"
      },
      {
       "name": "L1",
       "multiplier": 2
      },
      {
       "name": "L3"
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
       "name": "L4",
       "multiplier": 2
      },
      {
       "name": "L5",
       "multiplier": 2
      },
      {
       "name": "L2",
       "multiplier": 2
      },
      {
       "name": "L5",
       "multiplier": 7
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
       "name": "L3",
       "multiplier": 3
      },
      {
       "name": "L4"
      },
      {
       "name": "H3",
       "multiplier": 4
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
       "name": "L4",
       "multiplier": 2
      },
      {
       "name": "H1"
      },
      {
       "name": "L5",
       "multiplier": 3
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     46,
     220,
     23,
     204,
     141
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
    "type": "setTotalWin",
    "amount": 750
   },
   {
    "index": 34,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 12
   },
   {
    "index": 35,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5",
       "multiplier": 3
      },
      {
       "name": "L4",
       "multiplier": 3
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
       "name": "L5"
      },
      {
       "name": "H2",
       "multiplier": 2
      },
      {
       "name": "H1"
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
       "name": "L4",
       "multiplier": 2
      },
      {
       "name": "H3",
       "multiplier": 2
      },
      {
       "name": "L5",
       "multiplier": 2
      },
      {
       "name": "L5",
       "multiplier": 7
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
       "name": "L3",
       "multiplier": 3
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "L5",
       "multiplier": 4
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
       "name": "L4",
       "multiplier": 2
      },
      {
       "name": "L5"
      },
      {
       "name": "L3",
       "multiplier": 3
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     65,
     8,
     215,
     241,
     172
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
        "apparitions": 9
       },
       {
        "reel": 0,
        "row": 4,
        "apparitions": 2
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     },
     {
      "mirror": {
       "reel": 3,
       "row": 3
      },
      "reflected": [
       {
        "reel": 2,
        "row": 4,
        "apparitions": 11
       },
       {
        "reel": 4,
        "row": 2,
        "apparitions": 5
       }
      ],
      "mirrorBecomes": {
       "name": "H3"
      }
     }
    ],
    "totalWays": 68850
   },
   {
    "index": 37,
    "type": "winInfo",
    "totalWin": 15600,
    "wins": [
     {
      "symbol": "L5",
      "kind": 5,
      "win": 15600,
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
        "row": 1
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
       "ways": 195,
       "globalMult": 1,
       "winWithoutMult": 15600,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 38,
    "type": "setWin",
    "amount": 15600,
    "winLevel": 9
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 16350
   },
   {
    "index": 40,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 12
   },
   {
    "index": 41,
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L3",
       "multiplier": 3
      },
      {
       "name": "L3",
       "multiplier": 2
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
       "name": "L1",
       "multiplier": 2
      },
      {
       "name": "L1"
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
       "name": "L1"
      },
      {
       "name": "L3",
       "multiplier": 2
      },
      {
       "name": "L5",
       "multiplier": 2
      },
      {
       "name": "L3",
       "multiplier": 2
      },
      {
       "name": "L4",
       "multiplier": 11
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
       "name": "W",
       "wild": true
      },
      {
       "name": "H3",
       "multiplier": 3
      },
      {
       "name": "L1"
      },
      {
       "name": "L1",
       "multiplier": 4
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
       "name": "H2",
       "multiplier": 5
      },
      {
       "name": "L4"
      },
      {
       "name": "H3",
       "multiplier": 3
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     82,
     127,
     121,
     29,
     6
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
    "index": 42,
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
        "apparitions": 15
       }
      ],
      "mirrorBecomes": {
       "name": "L1"
      }
     }
    ],
    "totalWays": 66150
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 16350
   },
   {
    "index": 44,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 12
   },
   {
    "index": 45,
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
       "name": "H2",
       "multiplier": 3
      },
      {
       "name": "H3",
       "multiplier": 3
      },
      {
       "name": "L2",
       "multiplier": 2
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
       "name": "L5",
       "multiplier": 2
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "H3",
       "multiplier": 2
      },
      {
       "name": "H4",
       "multiplier": 2
      },
      {
       "name": "H1",
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 15
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
       "name": "H4",
       "multiplier": 3
      },
      {
       "name": "L1"
      },
      {
       "name": "L5",
       "multiplier": 4
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
       "name": "L1",
       "multiplier": 5
      },
      {
       "name": "L1"
      },
      {
       "name": "L5",
       "multiplier": 3
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     110,
     209,
     249,
     5,
     57
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
    "index": 46,
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 1,
       "row": 3
      },
      "reflected": [
       {
        "reel": 1,
        "row": 2,
        "apparitions": 5
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 4
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 149040
   },
   {
    "index": 47,
    "type": "winInfo",
    "totalWin": 6150,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 900,
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
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "ways": 45,
       "globalMult": 1,
       "winWithoutMult": 900,
       "symbolMult": 15
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 2700,
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
        "row": 4
       }
      ],
      "meta": {
       "ways": 45,
       "globalMult": 1,
       "winWithoutMult": 2700,
       "symbolMult": 15
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 2550,
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
        "row": 4
       }
      ],
      "meta": {
       "ways": 51,
       "globalMult": 1,
       "winWithoutMult": 2550,
       "symbolMult": 15
      }
     }
    ]
   },
   {
    "index": 48,
    "type": "setWin",
    "amount": 6150,
    "winLevel": 8
   },
   {
    "index": 49,
    "type": "setTotalWin",
    "amount": 22500
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
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4",
       "multiplier": 3
      },
      {
       "name": "L1",
       "multiplier": 3
      },
      {
       "name": "L1",
       "multiplier": 2
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
       "name": "L5",
       "multiplier": 5
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
       "name": "L2"
      },
      {
       "name": "L3",
       "multiplier": 2
      },
      {
       "name": "L4",
       "multiplier": 4
      },
      {
       "name": "H1",
       "multiplier": 2
      },
      {
       "name": "L3",
       "multiplier": 15
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
       "name": "H1"
      },
      {
       "name": "L2",
       "multiplier": 3
      },
      {
       "name": "L4"
      },
      {
       "name": "H4",
       "multiplier": 4
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
       "name": "L2"
      },
      {
       "name": "L2",
       "multiplier": 5
      },
      {
       "name": "L2"
      },
      {
       "name": "L1",
       "multiplier": 3
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
    "index": 52,
    "type": "setTotalWin",
    "amount": 22500
   },
   {
    "index": 53,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 12
   },
   {
    "index": 54,
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
       "name": "L2",
       "multiplier": 3
      },
      {
       "name": "H2",
       "multiplier": 3
      },
      {
       "name": "H3",
       "multiplier": 2
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
       "name": "L2",
       "multiplier": 5
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
       "name": "H2"
      },
      {
       "name": "L3",
       "multiplier": 2
      },
      {
       "name": "L3",
       "multiplier": 4
      },
      {
       "name": "H2",
       "multiplier": 2
      },
      {
       "name": "H3",
       "multiplier": 15
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
       "name": "L1",
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true
      },
      {
       "name": "L2",
       "multiplier": 4
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
       "name": "L1",
       "multiplier": 5
      },
      {
       "name": "L3"
      },
      {
       "name": "L3",
       "multiplier": 3
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     109,
     15,
     188,
     76,
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
    "index": 55,
    "type": "setTotalWin",
    "amount": 22500
   },
   {
    "index": 56,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 12
   },
   {
    "index": 57,
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
       "name": "L5",
       "multiplier": 3
      },
      {
       "name": "H3",
       "multiplier": 3
      },
      {
       "name": "L2",
       "multiplier": 2
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
       "name": "H1"
      },
      {
       "name": "L2",
       "multiplier": 5
      },
      {
       "name": "L1"
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
       "name": "L1",
       "multiplier": 2
      },
      {
       "name": "L1",
       "multiplier": 4
      },
      {
       "name": "L4",
       "multiplier": 2
      },
      {
       "name": "H3",
       "multiplier": 15
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
       "name": "L5",
       "multiplier": 3
      },
      {
       "name": "L4"
      },
      {
       "name": "H2",
       "multiplier": 4
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
       "name": "L1",
       "multiplier": 5
      },
      {
       "name": "H3"
      },
      {
       "name": "H2",
       "multiplier": 3
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     78,
     18,
     219,
     19,
     79
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
    "index": 58,
    "type": "setTotalWin",
    "amount": 22500
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
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1",
       "multiplier": 3
      },
      {
       "name": "L2",
       "multiplier": 3
      },
      {
       "name": "L2",
       "multiplier": 2
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
       "name": "H3",
       "multiplier": 5
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
       "name": "L5"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "H2",
       "multiplier": 2
      },
      {
       "name": "L2",
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "L2",
       "multiplier": 15
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
       "name": "L4"
      },
      {
       "name": "L5",
       "multiplier": 3
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H3",
       "multiplier": 4
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
       "name": "L3",
       "multiplier": 5
      },
      {
       "name": "L3"
      },
      {
       "name": "L3",
       "multiplier": 3
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     40,
     106,
     144,
     64,
     33
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
    "index": 61,
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
        "apparitions": 17
       },
       {
        "reel": 0,
        "row": 3,
        "apparitions": 5
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 4
       },
       {
        "reel": 0,
        "row": 4,
        "apparitions": 5
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     },
     {
      "mirror": {
       "reel": 3,
       "row": 3
      },
      "reflected": [
       {
        "reel": 4,
        "row": 4,
        "apparitions": 5
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 6
       },
       {
        "reel": 4,
        "row": 2,
        "apparitions": 7
       }
      ],
      "mirrorBecomes": {
       "name": "W"
      }
     }
    ],
    "totalWays": 409248
   },
   {
    "index": 62,
    "type": "winInfo",
    "totalWin": 28080,
    "wins": [
     {
      "symbol": "H3",
      "kind": 4,
      "win": 14400,
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
        "row": 3
       },
       {
        "reel": 3,
        "row": 4
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 120,
       "globalMult": 1,
       "winWithoutMult": 14400,
       "symbolMult": 4
      }
     },
     {
      "symbol": "L1",
      "kind": 5,
      "win": 2880,
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
        "reel": 1,
        "row": 4
       },
       {
        "reel": 2,
        "row": 3
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
       "ways": 24,
       "globalMult": 1,
       "winWithoutMult": 2880,
       "symbolMult": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 10800,
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
        "row": 4
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
        "reel": 2,
        "row": 3
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 270,
       "globalMult": 1,
       "winWithoutMult": 10800,
       "symbolMult": 4
      }
     }
    ]
   },
   {
    "index": 63,
    "type": "setWin",
    "amount": 28080,
    "winLevel": 9
   },
   {
    "index": 64,
    "type": "setTotalWin",
    "amount": 50580
   },
   {
    "index": 65,
    "type": "freeSpinEnd",
    "amount": 50570,
    "winLevel": 8
   },
   {
    "index": 66,
    "type": "finalWin",
    "amount": 50580
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.1,
  "freeGameWins": 505.7
 }
];
