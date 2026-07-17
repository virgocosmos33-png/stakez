export default [
 {
  "id": 0,
  "payoutMultiplier": 0,
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
       "name": "L1"
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
       "name": "H1"
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
       "name": "H4"
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
       "name": "L1"
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
       "name": "H1"
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 1,
  "payoutMultiplier": 88080,
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
       "name": "L1"
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
       "name": "H2"
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     6,
     6,
     36,
     6,
     70
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
      "symbol": "L2",
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 2,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "totalFs": 15,
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
      "reel": 3,
      "row": 4
     },
     {
      "reel": 4,
      "row": 3
     }
    ]
   },
   {
    "index": 5,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 15
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
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "L3"
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
       "name": "H3"
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
       "name": "L3"
      },
      {
       "name": "L2"
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
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "L1"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     93,
     119,
     81,
     97,
     108
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
    "type": "setTotalWin",
    "amount": 30
   },
   {
    "index": 8,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 15
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
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H3"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "L4"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     60,
     59,
     6,
     45,
     83
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
    "type": "setTotalWin",
    "amount": 30
   },
   {
    "index": 11,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 15
   },
   {
    "index": 12,
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
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H4"
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
       "name": "L3"
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
       "name": "H1"
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
       "name": "H4"
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
       "name": "L2"
      },
      {
       "name": "L4"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     195,
     93,
     202,
     151,
     90
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
    "type": "winInfo",
    "totalWin": 600,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 600,
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
       "lineIndex": 19,
       "multiplier": 3,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 14,
    "type": "setWin",
    "amount": 600,
    "winLevel": 5
   },
   {
    "index": 15,
    "type": "setTotalWin",
    "amount": 630
   },
   {
    "index": 16,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 15
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
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L3"
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
       "name": "H4"
      },
      {
       "name": "H2"
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
       "name": "H1"
      },
      {
       "name": "H2"
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
       "name": "L1"
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
       "name": "L5"
      },
      {
       "name": "H3"
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
     193,
     102,
     183,
     189,
     118
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
    "type": "winInfo",
    "totalWin": 400,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 200,
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
       "lineIndex": 10,
       "multiplier": 4,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 200,
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
       "lineIndex": 28,
       "multiplier": 4,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     }
    ]
   },
   {
    "index": 19,
    "type": "setWin",
    "amount": 400,
    "winLevel": 4
   },
   {
    "index": 20,
    "type": "setTotalWin",
    "amount": 1030
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 15
   },
   {
    "index": 22,
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
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L3"
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
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "H3"
      },
      {
       "name": "H1"
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
     127,
     128,
     131,
     90,
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
    "index": 23,
    "type": "winInfo",
    "totalWin": 76530,
    "wins": [
     {
      "symbol": "W",
      "kind": 3,
      "win": 23000,
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
       "lineIndex": 6,
       "multiplier": 23,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 23
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 20000,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 20,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 1300,
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
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 13,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 13
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 400,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 20,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "W",
      "kind": 3,
      "win": 23000,
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
       "lineIndex": 26,
       "multiplier": 23,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 23
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 130,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 13,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 13
      }
     },
     {
      "symbol": "H4",
      "kind": 4,
      "win": 2600,
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
       }
      ],
      "meta": {
       "lineIndex": 35,
       "multiplier": 13,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 13
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 3900,
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
       "lineIndex": 37,
       "multiplier": 13,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 13
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 200,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 10,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 2000,
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
       "lineIndex": 46,
       "multiplier": 20,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     }
    ]
   },
   {
    "index": 24,
    "type": "setWin",
    "amount": 76530,
    "winLevel": 9
   },
   {
    "index": 25,
    "type": "setTotalWin",
    "amount": 77560
   },
   {
    "index": 26,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 15
   },
   {
    "index": 27,
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
       "name": "H4"
      },
      {
       "name": "H3"
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
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
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
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "W",
       "wild": true,
       "multiplier": 4
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
     56,
     83,
     179,
     42,
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
    "index": 28,
    "type": "setTotalWin",
    "amount": 77560
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 15
   },
   {
    "index": 30,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
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
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L3"
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
       "name": "H1"
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
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "L2"
      },
      {
       "name": "H3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     166,
     157,
     150,
     104,
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
    "index": 31,
    "type": "setTotalWin",
    "amount": 77560
   },
   {
    "index": 32,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 15
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
       "name": "L4"
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
       "name": "L5"
      },
      {
       "name": "L3"
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
       "name": "L1"
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
       "name": "H4"
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
       "name": "H2"
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
       "name": "H2"
      },
      {
       "name": "L4"
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
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     200,
     87,
     185,
     2,
     48
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
    "type": "setTotalWin",
    "amount": 77560
   },
   {
    "index": 35,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 15
   },
   {
    "index": 36,
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
       "name": "L2"
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
     ],
     [
      {
       "name": "H1"
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
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H1"
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
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     147,
     167,
     12,
     69,
     151
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
    "index": 37,
    "type": "setTotalWin",
    "amount": 77560
   },
   {
    "index": 38,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 15
   },
   {
    "index": 39,
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
       "name": "L1"
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
       "name": "H1"
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
       "name": "L2"
      },
      {
       "name": "L2"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
     133,
     34,
     68,
     62,
     53
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
    "type": "setTotalWin",
    "amount": 77560
   },
   {
    "index": 41,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 15
   },
   {
    "index": 42,
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
       "name": "H2"
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
       "name": "L4"
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
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
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
       "name": "H2"
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
       "name": "L5"
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
     ]
    ],
    "paddingPositions": [
     92,
     44,
     63,
     172,
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
    "index": 43,
    "type": "wildNudge",
    "reel": 3,
    "nudges": 3,
    "multiplier": 4,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     }
    ]
   },
   {
    "index": 44,
    "type": "winInfo",
    "totalWin": 2400,
    "wins": [
     {
      "symbol": "L1",
      "kind": 4,
      "win": 2400,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     }
    ]
   },
   {
    "index": 45,
    "type": "setWin",
    "amount": 2400,
    "winLevel": 6
   },
   {
    "index": 46,
    "type": "setTotalWin",
    "amount": 79960
   },
   {
    "index": 47,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 15
   },
   {
    "index": 48,
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
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "H3"
      },
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
       "name": "H4"
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
       "name": "L2"
      },
      {
       "name": "L4"
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
     63,
     38,
     9,
     1,
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
    "index": 49,
    "type": "setTotalWin",
    "amount": 79960
   },
   {
    "index": 50,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 15
   },
   {
    "index": 51,
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
       "name": "L5"
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
       "name": "L3"
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
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H2"
      },
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
       "name": "L1"
      },
      {
       "name": "H4"
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
     ]
    ],
    "paddingPositions": [
     191,
     28,
     73,
     86,
     125
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
    "type": "wildNudge",
    "reel": 2,
    "nudges": 2,
    "multiplier": 3,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     }
    ]
   },
   {
    "index": 53,
    "type": "winInfo",
    "totalWin": 8100,
    "wins": [
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       "lineIndex": 8,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       "lineIndex": 13,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       "lineIndex": 17,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       "lineIndex": 23,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       "lineIndex": 44,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 54,
    "type": "setWin",
    "amount": 8100,
    "winLevel": 8
   },
   {
    "index": 55,
    "type": "setTotalWin",
    "amount": 88060
   },
   {
    "index": 56,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 15
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
       "name": "H2"
      },
      {
       "name": "L3"
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
       "name": "L3"
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
       "name": "L2"
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
       "name": "L1"
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
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     175,
     80,
     26,
     6,
     114
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 59,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 60,
    "type": "setTotalWin",
    "amount": 88080
   },
   {
    "index": 61,
    "type": "updateFreeSpin",
    "amount": 14,
    "total": 15
   },
   {
    "index": 62,
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
       "name": "H4"
      },
      {
       "name": "L1"
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
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
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
       "name": "L3"
      },
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
       "name": "H3"
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
       "name": "H4"
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
     132,
     149,
     199,
     100,
     124
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
    "type": "setTotalWin",
    "amount": 88080
   },
   {
    "index": 64,
    "type": "freeSpinEnd",
    "amount": 88050,
    "winLevel": 8
   },
   {
    "index": 65,
    "type": "finalWin",
    "amount": 88080
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.3,
  "freeGameWins": 880.5
 },
 {
  "id": 2,
  "payoutMultiplier": 0,
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
       "name": "H3"
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
       "name": "H4"
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
       "name": "L2"
      },
      {
       "name": "L2"
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
     139,
     33,
     94,
     154,
     121
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 3,
  "payoutMultiplier": 20,
  "events": [
   {
    "index": 0,
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
       "name": "L5"
      },
      {
       "name": "L4"
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
       "name": "L5"
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
       "name": "L1"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
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
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     140,
     74,
     204,
     195,
     15
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L5",
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 11,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
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
       "lineIndex": 19,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 20
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.2,
  "freeGameWins": 0.0
 },
 {
  "id": 4,
  "payoutMultiplier": 0,
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
       "name": "L1"
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
       "name": "L2"
      },
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
       "name": "H2"
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
       "name": "L5"
      },
      {
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "L5"
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
     189,
     91,
     203,
     176,
     215
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 5,
  "payoutMultiplier": 0,
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
       "name": "L2"
      },
      {
       "name": "L1"
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
       "name": "L1"
      },
      {
       "name": "H2"
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
       "name": "H3"
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
       "name": "H1"
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
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 6,
  "payoutMultiplier": 3880,
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
       "name": "L3"
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
       "name": "H3"
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
       "name": "H3"
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
       "name": "S",
       "scatter": true
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
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     8,
     111,
     107,
     9,
     9
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
      "reel": 0,
      "row": 2
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
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 4,
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
       "name": "L5"
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
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L3"
      },
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
       "name": "H3"
      },
      {
       "name": "H3"
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
       "name": "L3"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     108,
     15,
     144,
     31,
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
    "index": 5,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 6,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 8
   },
   {
    "index": 7,
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
       "name": "L1"
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
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L4"
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
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     149,
     101,
     12,
     56,
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
    "index": 8,
    "type": "winInfo",
    "totalWin": 300,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 150,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 150,
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
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 39,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 9,
    "type": "setWin",
    "amount": 300,
    "winLevel": 4
   },
   {
    "index": 10,
    "type": "setTotalWin",
    "amount": 300
   },
   {
    "index": 11,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 8
   },
   {
    "index": 12,
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
       "name": "L2"
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
       "name": "H2"
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
       "name": "L1"
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
       "name": "H3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H2"
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
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
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
     146,
     78,
     143,
     174,
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
    "index": 13,
    "type": "wildNudge",
    "reel": 3,
    "nudges": 2,
    "multiplier": 3,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     }
    ]
   },
   {
    "index": 14,
    "type": "setTotalWin",
    "amount": 300
   },
   {
    "index": 15,
    "type": "updateFreeSpin",
    "amount": 3,
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
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
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
       "name": "L1"
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
       "name": "H2"
      },
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
       "name": "H3"
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
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      }
     ]
    ],
    "paddingPositions": [
     149,
     116,
     92,
     76,
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
    "index": 17,
    "type": "winInfo",
    "totalWin": 50,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       "lineIndex": 19,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 18,
    "type": "setWin",
    "amount": 50,
    "winLevel": 2
   },
   {
    "index": 19,
    "type": "setTotalWin",
    "amount": 350
   },
   {
    "index": 20,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
   },
   {
    "index": 21,
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
       "name": "H4"
      },
      {
       "name": "L4"
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
       "name": "S",
       "scatter": true
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
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      }
     ],
     [
      {
       "name": "H1"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     134,
     126,
     87,
     186,
     114
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
    "type": "winInfo",
    "totalWin": 1200,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 60,
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
       "lineIndex": 3,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 60,
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
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 40,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 40,
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
       "lineIndex": 40,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1000,
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
       "lineIndex": 50,
       "multiplier": 50,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 50
      }
     }
    ]
   },
   {
    "index": 23,
    "type": "setWin",
    "amount": 1200,
    "winLevel": 5
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 1550
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 5,
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
       "name": "H3"
      },
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
       "name": "L1"
      },
      {
       "name": "L5"
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
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L1"
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
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     125,
     107,
     10,
     171,
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
    "index": 27,
    "type": "setTotalWin",
    "amount": 1550
   },
   {
    "index": 28,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 29,
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
       "name": "L4"
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
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H3"
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
       "name": "H1"
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
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
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
       "name": "L4"
      },
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
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     177,
     89,
     152,
     127,
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
    "index": 30,
    "type": "wildNudge",
    "reel": 1,
    "nudges": 3,
    "multiplier": 4,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     }
    ]
   },
   {
    "index": 31,
    "type": "winInfo",
    "totalWin": 1230,
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
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 17,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
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
        "row": 1
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
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
        "row": 3
       },
       {
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 37,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 630,
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
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 9,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 9
      }
     }
    ]
   },
   {
    "index": 32,
    "type": "setWin",
    "amount": 1230,
    "winLevel": 5
   },
   {
    "index": 33,
    "type": "setTotalWin",
    "amount": 2780
   },
   {
    "index": 34,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
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
       "name": "H3"
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
       "name": "L3"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L1"
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
       "name": "L5"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     72,
     183,
     98,
     171,
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
    "index": 36,
    "type": "winInfo",
    "totalWin": 1100,
    "wins": [
     {
      "symbol": "H3",
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
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 2,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 100,
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
       }
      ],
      "meta": {
       "lineIndex": 11,
       "multiplier": 2,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 200,
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
       "lineIndex": 17,
       "multiplier": 1,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H3",
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
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 2,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 37,
    "type": "setWin",
    "amount": 1100,
    "winLevel": 5
   },
   {
    "index": 38,
    "type": "setTotalWin",
    "amount": 3880
   },
   {
    "index": 39,
    "type": "freeSpinEnd",
    "amount": 3880,
    "winLevel": 5
   },
   {
    "index": 40,
    "type": "finalWin",
    "amount": 3880
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 38.8
 },
 {
  "id": 7,
  "payoutMultiplier": 470,
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
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L3"
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
       "name": "L3"
      },
      {
       "name": "L5"
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
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L5"
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
       "name": "H2"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     158,
     212,
     96,
     27,
     169
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
    "type": "winInfo",
    "totalWin": 470,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       "lineIndex": 6,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 8,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
       }
      ],
      "meta": {
       "lineIndex": 23,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
       }
      ],
      "meta": {
       "lineIndex": 26,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 44,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       "lineIndex": 46,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
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
       }
      ],
      "meta": {
       "lineIndex": 50,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 470,
    "winLevel": 4
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 470
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 470
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 4.7,
  "freeGameWins": 0.0
 },
 {
  "id": 8,
  "payoutMultiplier": 400,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
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
       "name": "H4"
      },
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
       "name": "L2"
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
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H2"
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
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     95,
     68,
     35,
     47,
     173
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
    "type": "wildNudge",
    "reel": 3,
    "nudges": 3,
    "multiplier": 4,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     }
    ]
   },
   {
    "index": 2,
    "type": "winInfo",
    "totalWin": 400,
    "wins": [
     {
      "symbol": "L5",
      "kind": 5,
      "win": 400,
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
        "row": 3
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 37,
       "multiplier": 4,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     }
    ]
   },
   {
    "index": 3,
    "type": "setWin",
    "amount": 400,
    "winLevel": 4
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 400
   },
   {
    "index": 5,
    "type": "finalWin",
    "amount": 400
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 4.0,
  "freeGameWins": 0.0
 },
 {
  "id": 9,
  "payoutMultiplier": 30,
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
       "name": "L2"
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
       "name": "H1"
      },
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
       "name": "L3"
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
       "name": "H1"
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
     ]
    ],
    "paddingPositions": [
     63,
     190,
     92,
     11,
     107
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
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 30,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "type": "finalWin",
    "amount": 30
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.3,
  "freeGameWins": 0.0
 },
 {
  "id": 10,
  "payoutMultiplier": 0,
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
       "name": "L2"
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
       "name": "L4"
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
       "name": "L4"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
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
       "name": "L2"
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
       "name": "L2"
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
       "name": "H3"
      },
      {
       "name": "H3"
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
     143,
     199,
     119,
     115,
     130
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 11,
  "payoutMultiplier": 600,
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
       "name": "H3"
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
       "name": "H2"
      },
      {
       "name": "H3"
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
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
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
       "name": "L4"
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
     ]
    ],
    "paddingPositions": [
     113,
     28,
     169,
     108,
     34
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
    "type": "winInfo",
    "totalWin": 600,
    "wins": [
     {
      "symbol": "H2",
      "kind": 3,
      "win": 300,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 1,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 300,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 1,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 600,
    "winLevel": 5
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 600
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 600
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 6.0,
  "freeGameWins": 0.0
 },
 {
  "id": 12,
  "payoutMultiplier": 1040,
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
       "name": "H1"
      },
      {
       "name": "H2"
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
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L5"
      },
      {
       "name": "L4"
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
       "name": "L5"
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
       "name": "L2"
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
       "name": "L2"
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     175,
     175,
     205,
     217,
     47
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
    "type": "winInfo",
    "totalWin": 1040,
    "wins": [
     {
      "symbol": "L5",
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
       "lineIndex": 10,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
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
       "lineIndex": 28,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       "lineIndex": 40,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 1040,
    "winLevel": 5
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 1040
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 1040
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 10.4,
  "freeGameWins": 0.0
 },
 {
  "id": 13,
  "payoutMultiplier": 0,
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
       "name": "H1"
      },
      {
       "name": "H1"
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
       "name": "H2"
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
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
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "L3"
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
     ]
    ],
    "paddingPositions": [
     179,
     193,
     166,
     134,
     63
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 14,
  "payoutMultiplier": 40,
  "events": [
   {
    "index": 0,
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
       "name": "L1"
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
       "name": "L4"
      },
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
       "name": "H4"
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
       "name": "L4"
      },
      {
       "name": "H1"
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
     2,
     133,
     188,
     9,
     40
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
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L4",
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 6,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 26,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 40
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 40
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.4,
  "freeGameWins": 0.0
 },
 {
  "id": 15,
  "payoutMultiplier": 240,
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
       "name": "H3"
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
       "name": "L3"
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
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "L1"
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
     72,
     208,
     165,
     7,
     85
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
      "row": 3
     },
     {
      "reel": 3,
      "row": 3
     }
    ]
   },
   {
    "index": 3,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 4,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "W",
       "wild": true,
       "multiplier": 20
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
       "name": "L5"
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
       "name": "L4"
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
       "name": "L4"
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
       "name": "L3"
      },
      {
       "name": "H3"
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
     154,
     79,
     5,
     202,
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
    "index": 5,
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L4",
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 13,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 6,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 7,
    "type": "setTotalWin",
    "amount": 60
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
       "name": "L4"
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
       "name": "L2"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L5"
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
       "name": "H1"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     170,
     161,
     7,
     118,
     116
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
       "lineIndex": 19,
       "multiplier": 4,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     }
    ]
   },
   {
    "index": 11,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 100
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
       "name": "L2"
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
       "name": "L4"
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
       "name": "L1"
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
       "name": "L2"
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
       "name": "H1"
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
       "name": "L2"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     200,
     79,
     92,
     66,
     107
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
    "index": 15,
    "type": "winInfo",
    "totalWin": 80,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 7,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 17,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 24,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 16,
    "type": "setWin",
    "amount": 80,
    "winLevel": 2
   },
   {
    "index": 17,
    "type": "setTotalWin",
    "amount": 180
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
       "name": "H1"
      },
      {
       "name": "L2"
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
       "name": "H4"
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
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
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
       "name": "L2"
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
     144,
     75,
     148,
     11,
     72
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
    "index": 20,
    "type": "setTotalWin",
    "amount": 180
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
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
       "name": "H4"
      },
      {
       "name": "L1"
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
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
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
     ],
     [
      {
       "name": "H2"
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
       "name": "H4"
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
       "name": "L5"
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
     ]
    ],
    "paddingPositions": [
     133,
     95,
     60,
     125,
     39
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
    "amount": 180
   },
   {
    "index": 24,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 8
   },
   {
    "index": 25,
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
       "name": "L1"
      },
      {
       "name": "L3"
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
       "name": "H3"
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
       "name": "H2"
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
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "L4"
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
       "name": "H4"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     116,
     16,
     42,
     179,
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
    "index": 26,
    "type": "setTotalWin",
    "amount": 180
   },
   {
    "index": 27,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 28,
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
       "name": "H2"
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
       "name": "L4"
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
       "name": "H4"
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
       "name": "L3"
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
       "name": "L2"
      },
      {
       "name": "H2"
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
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     125,
     3,
     121,
     178,
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
    "index": 29,
    "type": "setTotalWin",
    "amount": 180
   },
   {
    "index": 30,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 31,
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
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "L5"
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
       "name": "L5"
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
       "name": "L4"
      },
      {
       "name": "L5"
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
       "name": "L4"
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
       "name": "H3"
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
     ]
    ],
    "paddingPositions": [
     127,
     167,
     5,
     36,
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
    "index": 32,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 33,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 34,
    "type": "setTotalWin",
    "amount": 240
   },
   {
    "index": 35,
    "type": "freeSpinEnd",
    "amount": 240,
    "winLevel": 2
   },
   {
    "index": 36,
    "type": "finalWin",
    "amount": 240
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 2.4
 },
 {
  "id": 16,
  "payoutMultiplier": 0,
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
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
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
       "name": "H3"
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
       "name": "H3"
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
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
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
       "name": "H3"
      },
      {
       "name": "H4"
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
       "name": "H4"
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
     180,
     138,
     169,
     71,
     28
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 17,
  "payoutMultiplier": 20,
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
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L4"
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
       "name": "H2"
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
       "name": "H3"
      },
      {
       "name": "L1"
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
       "name": "H2"
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
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     51,
     207,
     173,
     193,
     213
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L4",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 20
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.2,
  "freeGameWins": 0.0
 },
 {
  "id": 18,
  "payoutMultiplier": 600,
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
       "name": "H3"
      },
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
       "name": "H3"
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
       "name": "L4"
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
       "name": "H2"
      },
      {
       "name": "L1"
      },
      {
       "name": "H1"
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
       "name": "L5"
      },
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
       "name": "H3"
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
     200,
     133,
     30,
     130,
     51
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
    "type": "winInfo",
    "totalWin": 600,
    "wins": [
     {
      "symbol": "H2",
      "kind": 3,
      "win": 300,
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
       "lineIndex": 8,
       "multiplier": 1,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 300,
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
       "lineIndex": 23,
       "multiplier": 1,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 600,
    "winLevel": 5
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 600
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 600
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 6.0,
  "freeGameWins": 0.0
 },
 {
  "id": 19,
  "payoutMultiplier": 20,
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
       "name": "H1"
      },
      {
       "name": "H2"
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
       "name": "L3"
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
       "name": "H1"
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
       "name": "L5"
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
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
     175,
     201,
     196,
     38,
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 36,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 20
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.2,
  "freeGameWins": 0.0
 },
 {
  "id": 20,
  "payoutMultiplier": 0,
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
       "name": "L3"
      },
      {
       "name": "L3"
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
       "name": "H2"
      },
      {
       "name": "H1"
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
       "name": "L3"
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
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
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
       "name": "L5"
      },
      {
       "name": "L3"
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
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     109,
     17,
     37,
     203,
     192
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 21,
  "payoutMultiplier": 107380,
  "events": [
   {
    "index": 0,
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
       "name": "H2"
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
       "name": "L4"
      }
     ],
     [
      {
       "name": "H2"
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
       "name": "S",
       "scatter": true
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
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     165,
     8,
     6,
     9,
     72
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
    "totalFs": 15,
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
      "row": 4
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
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 15
   },
   {
    "index": 4,
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
       "name": "L5"
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
       "name": "H2"
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
       "name": "H4"
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
       "name": "H3"
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
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     48,
     46,
     28,
     149,
     135
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
    "index": 5,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 6,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 15
   },
   {
    "index": 7,
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
       "name": "H1"
      },
      {
       "name": "L2"
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
       "wild": true,
       "multiplier": 3
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
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
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
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
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
       "name": "L2"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
     144,
     15,
     178,
     83,
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
    "index": 8,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 9,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 15
   },
   {
    "index": 10,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L1"
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
       "name": "L2"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "H1"
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
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
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
     ]
    ],
    "paddingPositions": [
     166,
     131,
     36,
     71,
     69
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
    "index": 11,
    "type": "wildNudge",
    "reel": 3,
    "nudges": 2,
    "multiplier": 3,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     }
    ]
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 13,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 15
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
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L2"
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
       "name": "H2"
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
       "name": "H2"
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
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     152,
     143,
     139,
     134,
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
    "index": 15,
    "type": "winInfo",
    "totalWin": 1200,
    "wins": [
     {
      "symbol": "H2",
      "kind": 3,
      "win": 1200,
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
       "lineIndex": 40,
       "multiplier": 4,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     }
    ]
   },
   {
    "index": 16,
    "type": "setWin",
    "amount": 1200,
    "winLevel": 5
   },
   {
    "index": 17,
    "type": "setTotalWin",
    "amount": 1200
   },
   {
    "index": 18,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 15
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
       "name": "H4"
      },
      {
       "name": "L3"
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
       "name": "H2"
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
       "name": "L2"
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
       "name": "L2"
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
       "name": "H4"
      },
      {
       "name": "H3"
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
     23,
     113,
     91,
     25,
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
    "index": 20,
    "type": "setTotalWin",
    "amount": 1200
   },
   {
    "index": 21,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 15
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
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "H1"
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
       "name": "H2"
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
       "name": "H1"
      },
      {
       "name": "L3"
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
       "name": "L5"
      },
      {
       "name": "L3"
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
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     50,
     131,
     61,
     102,
     1
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
    "index": 23,
    "type": "setTotalWin",
    "amount": 1200
   },
   {
    "index": 24,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 15
   },
   {
    "index": 25,
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
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "H3"
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
       "name": "L3"
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
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
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
       "name": "H2"
      },
      {
       "name": "L5"
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
     89,
     45,
     84,
     91,
     161
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
    "totalWin": 450,
    "wins": [
     {
      "symbol": "L4",
      "kind": 4,
      "win": 250,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 5,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 2,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 27,
    "type": "setWin",
    "amount": 450,
    "winLevel": 4
   },
   {
    "index": 28,
    "type": "setTotalWin",
    "amount": 1650
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 15
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
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "H1"
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
       "name": "L1"
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
       "name": "H2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
     ]
    ],
    "paddingPositions": [
     51,
     167,
     177,
     25,
     13
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
    "type": "winInfo",
    "totalWin": 2020,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 2000,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 2,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
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
        "row": 1
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 2,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 32,
    "type": "setWin",
    "amount": 2020,
    "winLevel": 6
   },
   {
    "index": 33,
    "type": "setTotalWin",
    "amount": 3670
   },
   {
    "index": 34,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 15
   },
   {
    "index": 35,
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
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "L1"
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
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     11,
     30,
     127,
     181,
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
    "index": 36,
    "type": "winInfo",
    "totalWin": 42000,
    "wins": [
     {
      "symbol": "H1",
      "kind": 4,
      "win": 14000,
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
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 4,
       "multiplier": 7,
       "winWithoutMult": 2000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 7000,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 7,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 7000,
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
       "lineIndex": 22,
       "multiplier": 7,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 7000,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 7,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 7000,
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
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 7,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     }
    ]
   },
   {
    "index": 37,
    "type": "setWin",
    "amount": 42000,
    "winLevel": 9
   },
   {
    "index": 38,
    "type": "setTotalWin",
    "amount": 45670
   },
   {
    "index": 39,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 15
   },
   {
    "index": 40,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
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
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H1"
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
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L2"
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
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     16,
     164,
     182,
     90,
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
    "index": 41,
    "type": "wildNudge",
    "reel": 1,
    "nudges": 2,
    "multiplier": 3,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     }
    ]
   },
   {
    "index": 42,
    "type": "winInfo",
    "totalWin": 24900,
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
        "row": 1
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
       "lineIndex": 1,
       "multiplier": 8,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       "lineIndex": 3,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 8,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 800,
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
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 8,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 400,
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
       "lineIndex": 13,
       "multiplier": 8,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H4",
      "kind": 4,
      "win": 1600,
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
       "lineIndex": 17,
       "multiplier": 8,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H2",
      "kind": 4,
      "win": 3000,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 6,
       "winWithoutMult": 500,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L1",
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
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 21,
       "multiplier": 8,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H2",
      "kind": 4,
      "win": 5500,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 11,
       "winWithoutMult": 500,
       "globalMult": 1,
       "lineMultiplier": 11
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 800,
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
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 8,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       "lineIndex": 31,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 400,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 8,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 36,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
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
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 37,
       "multiplier": 8,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       "lineIndex": 39,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
      "kind": 4,
      "win": 1100,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 11,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 11
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 400,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 8,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "L1",
      "kind": 4,
      "win": 1100,
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
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 11,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 11
      }
     }
    ]
   },
   {
    "index": 43,
    "type": "setWin",
    "amount": 24900,
    "winLevel": 9
   },
   {
    "index": 44,
    "type": "setTotalWin",
    "amount": 70570
   },
   {
    "index": 45,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 15
   },
   {
    "index": 46,
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
       "name": "H3"
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
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
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
       "name": "L3"
      },
      {
       "name": "H1"
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
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "L1"
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
       "name": "L3"
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
       "name": "H4"
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
     90,
     173,
     30,
     55,
     136
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
    "type": "winInfo",
    "totalWin": 2000,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 48,
    "type": "setWin",
    "amount": 2000,
    "winLevel": 6
   },
   {
    "index": 49,
    "type": "setTotalWin",
    "amount": 72570
   },
   {
    "index": 50,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 15
   },
   {
    "index": 51,
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
       "name": "L5"
      },
      {
       "name": "H3"
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
       "name": "L3"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L2"
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
       "name": "H2"
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
      }
     ]
    ],
    "paddingPositions": [
     70,
     192,
     24,
     148,
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
    "index": 52,
    "type": "setTotalWin",
    "amount": 72570
   },
   {
    "index": 53,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 15
   },
   {
    "index": 54,
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
       "name": "H4"
      },
      {
       "name": "L4"
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
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "L1"
      },
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
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     134,
     46,
     9,
     60,
     96
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
    "amount": 72570
   },
   {
    "index": 56,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 15
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
       "name": "L3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L4"
      },
      {
       "name": "L1"
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
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "H2"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
      }
     ]
    ],
    "paddingPositions": [
     52,
     52,
     192,
     125,
     162
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
    "type": "winInfo",
    "totalWin": 34810,
    "wins": [
     {
      "symbol": "H1",
      "kind": 4,
      "win": 14000,
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
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 3,
       "multiplier": 7,
       "winWithoutMult": 2000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 3000,
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
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 3,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 210,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 7,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 4,
      "win": 14000,
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
        "row": 2
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 7,
       "winWithoutMult": 2000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 3000,
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
       "lineIndex": 40,
       "multiplier": 3,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 46,
       "multiplier": 4,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 50,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 1,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 350,
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
       "lineIndex": 50,
       "multiplier": 7,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     }
    ]
   },
   {
    "index": 59,
    "type": "setWin",
    "amount": 34810,
    "winLevel": 9
   },
   {
    "index": 60,
    "type": "setTotalWin",
    "amount": 107380
   },
   {
    "index": 61,
    "type": "updateFreeSpin",
    "amount": 14,
    "total": 15
   },
   {
    "index": 62,
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
       "name": "L1"
      },
      {
       "name": "L5"
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
       "name": "H3"
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
       "name": "H2"
      },
      {
       "name": "H3"
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
       "name": "L2"
      },
      {
       "name": "L5"
      },
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
     ]
    ],
    "paddingPositions": [
     68,
     16,
     170,
     144,
     40
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
    "type": "setTotalWin",
    "amount": 107380
   },
   {
    "index": 64,
    "type": "freeSpinEnd",
    "amount": 107380,
    "winLevel": 8
   },
   {
    "index": 65,
    "type": "finalWin",
    "amount": 107380
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 1073.8
 },
 {
  "id": 22,
  "payoutMultiplier": 0,
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
       "name": "H3"
      },
      {
       "name": "L4"
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
       "name": "L3"
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
       "name": "H3"
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
       "name": "H4"
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
       "name": "H2"
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
       "name": "H2"
      },
      {
       "name": "H4"
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
     74,
     212,
     21,
     4,
     151
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 23,
  "payoutMultiplier": 161310,
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
       "name": "H4"
      },
      {
       "name": "H1"
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
       "name": "L4"
      },
      {
       "name": "H2"
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
      },
      {
       "name": "H1"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     71,
     138,
     165,
     7,
     167
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
    "totalFs": 12,
    "positions": [
     {
      "reel": 0,
      "row": 2
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
    ]
   },
   {
    "index": 3,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 12
   },
   {
    "index": 4,
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
       "name": "L3"
      },
      {
       "name": "L1"
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
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H1"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
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
       "name": "H1"
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     8,
     54,
     80,
     86,
     190
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
    "index": 5,
    "type": "wildNudge",
    "reel": 3,
    "nudges": 2,
    "multiplier": 3,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     }
    ]
   },
   {
    "index": 6,
    "type": "winInfo",
    "totalWin": 2350,
    "wins": [
     {
      "symbol": "H4",
      "kind": 4,
      "win": 1000,
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
       }
      ],
      "meta": {
       "lineIndex": 1,
       "multiplier": 5,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 350,
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
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 19,
       "multiplier": 5,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H4",
      "kind": 4,
      "win": 1000,
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
       "lineIndex": 21,
       "multiplier": 5,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     }
    ]
   },
   {
    "index": 7,
    "type": "setWin",
    "amount": 2350,
    "winLevel": 6
   },
   {
    "index": 8,
    "type": "setTotalWin",
    "amount": 2350
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
       "name": "L2"
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
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "L5"
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
       "name": "H1"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     200,
     39,
     167,
     36,
     83
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L4",
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 17,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 12,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 13,
    "type": "setTotalWin",
    "amount": 2370
   },
   {
    "index": 14,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 12
   },
   {
    "index": 15,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L5"
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
       "name": "H4"
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
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L1"
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
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     33,
     121,
     129,
     66,
     130
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
    "index": 16,
    "type": "winInfo",
    "totalWin": 158030,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 150,
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
       "lineIndex": 2,
       "multiplier": 5,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 6,
       "multiplier": 3,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
       "lineIndex": 7,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 5,
      "win": 50000,
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
        "row": 1
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 10,
       "winWithoutMult": 5000,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 800,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 12,
       "multiplier": 8,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 4000,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 4,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 5000,
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
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 5,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       "lineIndex": 17,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 4,
      "win": 10000,
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
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 19,
       "multiplier": 5,
       "winWithoutMult": 2000,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 400,
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
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 4,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
       "lineIndex": 24,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 5,
      "win": 35000,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 26,
       "multiplier": 7,
       "winWithoutMult": 5000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 8000,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 8,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 7000,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 7,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 500,
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
       "lineIndex": 35,
       "multiplier": 5,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
       "lineIndex": 37,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 700,
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
       "lineIndex": 40,
       "multiplier": 7,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H1",
      "kind": 4,
      "win": 8000,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 4,
       "winWithoutMult": 2000,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 210,
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
       "lineIndex": 44,
       "multiplier": 7,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 210,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 7,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 700,
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
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 7,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       "lineIndex": 49,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     }
    ]
   },
   {
    "index": 17,
    "type": "setWin",
    "amount": 158030,
    "winLevel": 9
   },
   {
    "index": 18,
    "type": "setTotalWin",
    "amount": 160400
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
       "name": "L4"
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
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
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
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "L1"
      },
      {
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     103,
     17,
     120,
     92,
     83
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
    "type": "setTotalWin",
    "amount": 160400
   },
   {
    "index": 22,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 12
   },
   {
    "index": 23,
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
       "name": "H4"
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
       "name": "H3"
      },
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
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "H1"
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
     63,
     95,
     8,
     14,
     115
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
    "type": "setTotalWin",
    "amount": 160400
   },
   {
    "index": 25,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 12
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
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L3"
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
       "name": "H1"
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
       "name": "L4"
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
       "name": "L4"
      },
      {
       "name": "L2"
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
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
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
       "name": "H1"
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
       "name": "H2"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     22,
     9,
     20,
     83,
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
    "index": 27,
    "type": "setTotalWin",
    "amount": 160400
   },
   {
    "index": 28,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 12
   },
   {
    "index": 29,
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
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
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
       "name": "L5"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
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
       "name": "H1"
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
       "name": "H3"
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
       "name": "H1"
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
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      }
     ]
    ],
    "paddingPositions": [
     127,
     147,
     134,
     104,
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
    "index": 30,
    "type": "winInfo",
    "totalWin": 50,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 50,
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
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 5,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     }
    ]
   },
   {
    "index": 31,
    "type": "setWin",
    "amount": 50,
    "winLevel": 2
   },
   {
    "index": 32,
    "type": "setTotalWin",
    "amount": 160450
   },
   {
    "index": 33,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 12
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
       "name": "L2"
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
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
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
     148,
     164,
     4,
     67,
     139
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
    "index": 35,
    "type": "wildNudge",
    "reel": 2,
    "nudges": 1,
    "multiplier": 2,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     }
    ]
   },
   {
    "index": 36,
    "type": "winInfo",
    "totalWin": 200,
    "wins": [
     {
      "symbol": "L4",
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
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 8,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
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
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
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
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 23,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
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
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 36,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
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
        "reel": 2,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 44,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 37,
    "type": "setWin",
    "amount": 200,
    "winLevel": 4
   },
   {
    "index": 38,
    "type": "setTotalWin",
    "amount": 160650
   },
   {
    "index": 39,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 12
   },
   {
    "index": 40,
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
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "H2"
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
       "name": "L4"
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
       "name": "L4"
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
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
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
     202,
     17,
     43,
     200,
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
    "index": 41,
    "type": "setTotalWin",
    "amount": 160650
   },
   {
    "index": 42,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 12
   },
   {
    "index": 43,
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
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H1"
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
       "name": "L2"
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
       "name": "H3"
      },
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
       "name": "H1"
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
     150,
     54,
     114,
     34,
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
    "index": 44,
    "type": "wildNudge",
    "reel": 1,
    "nudges": 3,
    "multiplier": 4,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     }
    ]
   },
   {
    "index": 45,
    "type": "winInfo",
    "totalWin": 360,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 40,
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
       "lineIndex": 4,
       "multiplier": 4,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 120,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 120,
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
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 22,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 40,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 4,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 40,
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
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 4,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     }
    ]
   },
   {
    "index": 46,
    "type": "setWin",
    "amount": 360,
    "winLevel": 4
   },
   {
    "index": 47,
    "type": "setTotalWin",
    "amount": 161010
   },
   {
    "index": 48,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 12
   },
   {
    "index": 49,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "H1"
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
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     36,
     199,
     129,
     195,
     20
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
    "type": "winInfo",
    "totalWin": 300,
    "wins": [
     {
      "symbol": "L4",
      "kind": 4,
      "win": 300,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 6,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     }
    ]
   },
   {
    "index": 51,
    "type": "setWin",
    "amount": 300,
    "winLevel": 4
   },
   {
    "index": 52,
    "type": "setTotalWin",
    "amount": 161310
   },
   {
    "index": 53,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 12
   },
   {
    "index": 54,
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
       "name": "L3"
      },
      {
       "name": "L4"
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
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "L2"
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
       "name": "H3"
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
       "name": "H1"
      },
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
       "name": "L1"
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
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     117,
     165,
     96,
     105,
     168
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
    "amount": 161310
   },
   {
    "index": 56,
    "type": "freeSpinEnd",
    "amount": 161310,
    "winLevel": 8
   },
   {
    "index": 57,
    "type": "finalWin",
    "amount": 161310
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 1613.1
 },
 {
  "id": 24,
  "payoutMultiplier": 800,
  "events": [
   {
    "index": 0,
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
       "name": "L1"
      },
      {
       "name": "L4"
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
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
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
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "H2"
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
       "name": "L5"
      },
      {
       "name": "H4"
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
     ]
    ],
    "paddingPositions": [
     215,
     215,
     3,
     54,
     78
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
    "type": "winInfo",
    "totalWin": 800,
    "wins": [
     {
      "symbol": "H2",
      "kind": 4,
      "win": 500,
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
       }
      ],
      "meta": {
       "lineIndex": 6,
       "multiplier": 1,
       "winWithoutMult": 500,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 300,
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
       "lineIndex": 26,
       "multiplier": 1,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 800,
    "winLevel": 5
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 800
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 800
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 8.0,
  "freeGameWins": 0.0
 },
 {
  "id": 25,
  "payoutMultiplier": 0,
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
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H4"
      },
      {
       "name": "L5"
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
       "name": "H1"
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
       "name": "L2"
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
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     51,
     168,
     52,
     110,
     153
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 26,
  "payoutMultiplier": 0,
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
       "name": "L1"
      },
      {
       "name": "L2"
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
       "name": "L3"
      },
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
       "name": "H3"
      },
      {
       "name": "L3"
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
       "name": "L4"
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
     ]
    ],
    "paddingPositions": [
     211,
     138,
     85,
     64,
     95
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 27,
  "payoutMultiplier": 0,
  "events": [
   {
    "index": 0,
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
       "name": "L4"
      },
      {
       "name": "L4"
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
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
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
       "name": "L3"
      },
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "L1"
      },
      {
       "name": "H2"
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
     ]
    ],
    "paddingPositions": [
     33,
     139,
     152,
     182,
     45
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 28,
  "payoutMultiplier": 20,
  "events": [
   {
    "index": 0,
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
       "name": "H2"
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
       "name": "L5"
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
       "name": "H4"
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
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "H2"
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
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     165,
     120,
     101,
     210,
     158
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L4",
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 20
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.2,
  "freeGameWins": 0.0
 },
 {
  "id": 29,
  "payoutMultiplier": 0,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
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
       "name": "L3"
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
       "name": "H3"
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
       "name": "L1"
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
       "name": "H4"
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
       "name": "L1"
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
       "name": "H4"
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
      }
     ]
    ],
    "paddingPositions": [
     65,
     12,
     101,
     96,
     164
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 30,
  "payoutMultiplier": 4490,
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
       "name": "L3"
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
       "name": "L5"
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
       "name": "L4"
      },
      {
       "name": "L5"
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
       "name": "H2"
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
       "name": "L5"
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
     8,
     34,
     9,
     59,
     38
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
      "row": 1
     }
    ]
   },
   {
    "index": 3,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 4,
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
       "name": "L4"
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
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H4"
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
       "name": "L5"
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
     ]
    ],
    "paddingPositions": [
     105,
     52,
     151,
     23,
     30
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
    "index": 5,
    "type": "winInfo",
    "totalWin": 200,
    "wins": [
     {
      "symbol": "L1",
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
       "lineIndex": 6,
       "multiplier": 2,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L1",
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
       "lineIndex": 26,
       "multiplier": 2,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 6,
    "type": "setWin",
    "amount": 200,
    "winLevel": 4
   },
   {
    "index": 7,
    "type": "setTotalWin",
    "amount": 200
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
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "L3"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "H3"
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
     50,
     52,
     84,
     100,
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
    "index": 10,
    "type": "winInfo",
    "totalWin": 570,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 100,
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
       "lineIndex": 7,
       "multiplier": 5,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "L4",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 5,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 100,
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
       "lineIndex": 24,
       "multiplier": 5,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 150,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 5,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 60,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 60,
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
       "lineIndex": 49,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 11,
    "type": "setWin",
    "amount": 570,
    "winLevel": 5
   },
   {
    "index": 12,
    "type": "setTotalWin",
    "amount": 770
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
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L1"
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
       "name": "L2"
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
       "name": "L4"
      },
      {
       "name": "L5"
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
       "name": "L1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
     13,
     46,
     91,
     34,
     52
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
    "type": "winInfo",
    "totalWin": 2050,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 100,
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
       }
      ],
      "meta": {
       "lineIndex": 11,
       "multiplier": 2,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 1400,
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
        "row": 3
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
       "lineIndex": 16,
       "multiplier": 7,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L4",
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
        "row": 3
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 31,
       "multiplier": 2,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 150,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 150,
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
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 150,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 16,
    "type": "setWin",
    "amount": 2050,
    "winLevel": 6
   },
   {
    "index": 17,
    "type": "setTotalWin",
    "amount": 2820
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
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "H1"
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
       "name": "H2"
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
       "name": "L2"
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
       "name": "H1"
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
       "name": "H3"
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
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     55,
     53,
     110,
     186,
     94
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
    "type": "winInfo",
    "totalWin": 1450,
    "wins": [
     {
      "symbol": "H2",
      "kind": 3,
      "win": 1200,
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
       }
      ],
      "meta": {
       "lineIndex": 29,
       "multiplier": 4,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 200,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 4,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 50,
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
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 1,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 21,
    "type": "setWin",
    "amount": 1450,
    "winLevel": 5
   },
   {
    "index": 22,
    "type": "setTotalWin",
    "amount": 4270
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
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L2"
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
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H1"
      },
      {
       "name": "H2"
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
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      }
     ]
    ],
    "paddingPositions": [
     86,
     75,
     85,
     146,
     101
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
    "index": 25,
    "type": "setTotalWin",
    "amount": 4270
   },
   {
    "index": 26,
    "type": "updateFreeSpin",
    "amount": 5,
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
       "name": "L1"
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
       "name": "L2"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H2"
      },
      {
       "name": "H2"
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
       "name": "H1"
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
       "name": "H3"
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
       "name": "H2"
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
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     143,
     159,
     139,
     172,
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
    "index": 28,
    "type": "winInfo",
    "totalWin": 220,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 10,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 70,
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
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 28,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 60,
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
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 29,
    "type": "setWin",
    "amount": 220,
    "winLevel": 4
   },
   {
    "index": 30,
    "type": "setTotalWin",
    "amount": 4490
   },
   {
    "index": 31,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
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
       "name": "L4"
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
       "name": "L4"
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
       "name": "H3"
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
       "name": "H1"
      },
      {
       "name": "L3"
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
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     178,
     24,
     171,
     102,
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
    "index": 33,
    "type": "setTotalWin",
    "amount": 4490
   },
   {
    "index": 34,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 35,
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
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L2"
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
       "name": "L4"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     50,
     29,
     116,
     51,
     85
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
    "type": "setTotalWin",
    "amount": 4490
   },
   {
    "index": 37,
    "type": "freeSpinEnd",
    "amount": 4490,
    "winLevel": 5
   },
   {
    "index": 38,
    "type": "finalWin",
    "amount": 4490
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 44.9
 },
 {
  "id": 31,
  "payoutMultiplier": 20,
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
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L5"
      },
      {
       "name": "H2"
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
       "name": "L1"
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
       "name": "H2"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     54,
     37,
     77,
     178,
     60
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L5",
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 13,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 10,
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
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 20
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.2,
  "freeGameWins": 0.0
 },
 {
  "id": 32,
  "payoutMultiplier": 0,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H1"
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
       "name": "H2"
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
       "name": "H1"
      },
      {
       "name": "L4"
      },
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
       "name": "L5"
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
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     161,
     59,
     209,
     215,
     70
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 33,
  "payoutMultiplier": 0,
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
       "name": "L3"
      },
      {
       "name": "L2"
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
       "name": "H4"
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
       "name": "S",
       "scatter": true
      },
      {
       "name": "L4"
      },
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
       "name": "L5"
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
       "name": "H2"
      },
      {
       "name": "L3"
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
     ]
    ],
    "paddingPositions": [
     149,
     7,
     215,
     58,
     7
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 34,
  "payoutMultiplier": 50,
  "events": [
   {
    "index": 0,
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
       "name": "L1"
      },
      {
       "name": "H1"
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
       "name": "L2"
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
       "name": "L1"
      },
      {
       "name": "L4"
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
       "name": "L2"
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
       "name": "L3"
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
     ]
    ],
    "paddingPositions": [
     192,
     33,
     191,
     87,
     39
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
    "type": "winInfo",
    "totalWin": 50,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 50,
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
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 1,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 50,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 50
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 50
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.5,
  "freeGameWins": 0.0
 },
 {
  "id": 35,
  "payoutMultiplier": 0,
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
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H1"
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
       "name": "H2"
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
       "name": "L5"
      },
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
       "name": "H3"
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
     ]
    ],
    "paddingPositions": [
     160,
     45,
     63,
     68,
     186
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 36,
  "payoutMultiplier": 0,
  "events": [
   {
    "index": 0,
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
       "name": "L4"
      },
      {
       "name": "H4"
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
     ],
     [
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
       "name": "L1"
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
       "name": "L5"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     23,
     158,
     170,
     215,
     191
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 37,
  "payoutMultiplier": 240,
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
       "name": "L3"
      },
      {
       "name": "L3"
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
       "name": "H2"
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
       "name": "H3"
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
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H4"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     109,
     193,
     185,
     26,
     16
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
    "type": "winInfo",
    "totalWin": 240,
    "wins": [
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 7,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
        "row": 4
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 24,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 240,
    "winLevel": 4
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 240
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 240
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 2.4,
  "freeGameWins": 0.0
 },
 {
  "id": 38,
  "payoutMultiplier": 0,
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
       "name": "H4"
      },
      {
       "name": "L4"
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
       "name": "L4"
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
       "name": "S",
       "scatter": true
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
       "name": "L5"
      },
      {
       "name": "H2"
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
       "name": "H4"
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
     ]
    ],
    "paddingPositions": [
     98,
     6,
     49,
     56,
     101
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 39,
  "payoutMultiplier": 0,
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
       "name": "L2"
      },
      {
       "name": "L1"
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
       "name": "H4"
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
       "name": "H4"
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
       "name": "H1"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L5"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     134,
     8,
     62,
     72,
     170
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 40,
  "payoutMultiplier": 200,
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
       "name": "H1"
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
       "name": "L2"
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
       "name": "L3"
      },
      {
       "name": "L3"
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
       "name": "L3"
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
       "name": "H2"
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
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H3"
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
     ]
    ],
    "paddingPositions": [
     59,
     42,
     98,
     147,
     176
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
    "type": "winInfo",
    "totalWin": 200,
    "wins": [
     {
      "symbol": "H4",
      "kind": 3,
      "win": 100,
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
       "lineIndex": 10,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 100,
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
       "lineIndex": 28,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 200,
    "winLevel": 4
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 200
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 200
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 2.0,
  "freeGameWins": 0.0
 },
 {
  "id": 41,
  "payoutMultiplier": 1400,
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
       "name": "L1"
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
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L2"
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
       "name": "H4"
      }
     ],
     [
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "H1"
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
       "name": "H2"
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
       "name": "L1"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     189,
     139,
     22,
     151,
     108
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
    "type": "wildNudge",
    "reel": 1,
    "nudges": 1,
    "multiplier": 2,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     }
    ]
   },
   {
    "index": 2,
    "type": "winInfo",
    "totalWin": 1400,
    "wins": [
     {
      "symbol": "H4",
      "kind": 3,
      "win": 200,
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
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 2,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "H4",
      "kind": 4,
      "win": 400,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 2,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 200,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 2,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 46,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "H4",
      "kind": 4,
      "win": 400,
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
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 2,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 140,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 2,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 3,
    "type": "setWin",
    "amount": 1400,
    "winLevel": 5
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 1400
   },
   {
    "index": 5,
    "type": "finalWin",
    "amount": 1400
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 14.0,
  "freeGameWins": 0.0
 },
 {
  "id": 42,
  "payoutMultiplier": 1080,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H2"
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
       "name": "H4"
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
       "name": "L3"
      },
      {
       "name": "L4"
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
       "name": "L2"
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
     ]
    ],
    "paddingPositions": [
     167,
     159,
     6,
     218,
     165
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "freeSpinTrigger",
    "totalFs": 8,
    "positions": [
     {
      "reel": 0,
      "row": 1
     },
     {
      "reel": 2,
      "row": 4
     },
     {
      "reel": 4,
      "row": 3
     }
    ]
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
       "name": "H4"
      },
      {
       "name": "H2"
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
       "name": "L2"
      },
      {
       "name": "L4"
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
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
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
       "name": "H1"
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
       "name": "L5"
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
     ]
    ],
    "paddingPositions": [
     111,
     100,
     45,
     14,
     27
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
    "index": 7,
    "type": "setTotalWin",
    "amount": 20
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
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L1"
      },
      {
       "name": "H4"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H4"
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
       "name": "L4"
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
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      }
     ]
    ],
    "paddingPositions": [
     131,
     126,
     32,
     197,
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
    "index": 10,
    "type": "wildNudge",
    "reel": 1,
    "nudges": 1,
    "multiplier": 2,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     }
    ]
   },
   {
    "index": 11,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 12,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 8
   },
   {
    "index": 13,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H2"
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
       "name": "L4"
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
       "name": "L3"
      },
      {
       "name": "L4"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L2"
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
       "name": "H1"
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
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     15,
     24,
     159,
     117,
     201
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
    "type": "winInfo",
    "totalWin": 460,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 80,
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
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 4,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 60,
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
       "lineIndex": 19,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 200,
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
       "lineIndex": 27,
       "multiplier": 4,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
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
        "row": 4
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     }
    ]
   },
   {
    "index": 15,
    "type": "setWin",
    "amount": 460,
    "winLevel": 4
   },
   {
    "index": 16,
    "type": "setTotalWin",
    "amount": 480
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
       "name": "H1"
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
       "name": "H4"
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
       "name": "H3"
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
       "name": "L2"
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
       "name": "L5"
      },
      {
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H2"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     20,
     199,
     81,
     12,
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
    "index": 19,
    "type": "setTotalWin",
    "amount": 480
   },
   {
    "index": 20,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
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
       "name": "H2"
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
       "name": "L1"
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
       "name": "L2"
      },
      {
       "name": "L3"
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
       "name": "H2"
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
       "name": "H3"
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
       "name": "H2"
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
       "name": "L1"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     18,
     141,
     169,
     29,
     76
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
    "type": "setTotalWin",
    "amount": 480
   },
   {
    "index": 23,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 8
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
       "name": "H3"
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
       "name": "L4"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "L5"
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
       "name": "H2"
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
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L4"
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
     ]
    ],
    "paddingPositions": [
     92,
     183,
     111,
     10,
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
    "index": 25,
    "type": "wildNudge",
    "reel": 1,
    "nudges": 2,
    "multiplier": 3,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     }
    ]
   },
   {
    "index": 26,
    "type": "winInfo",
    "totalWin": 600,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 150,
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
       "lineIndex": 10,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 150,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 150,
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
       "lineIndex": 28,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 150,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 3,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 27,
    "type": "setWin",
    "amount": 600,
    "winLevel": 5
   },
   {
    "index": 28,
    "type": "setTotalWin",
    "amount": 1080
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
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
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "L4"
      },
      {
       "name": "L2"
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
       "name": "H1"
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
       "name": "H1"
      },
      {
       "name": "H3"
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
       "name": "H3"
      },
      {
       "name": "H1"
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
     27,
     202,
     31,
     32,
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
    "index": 31,
    "type": "setTotalWin",
    "amount": 1080
   },
   {
    "index": 32,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
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
       "name": "L4"
      },
      {
       "name": "L2"
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
       "name": "H3"
      },
      {
       "name": "H1"
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
       "name": "L3"
      },
      {
       "name": "H1"
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
       "name": "L1"
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
       "name": "H3"
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
       "name": "L3"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     199,
     86,
     30,
     183,
     136
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
    "type": "setTotalWin",
    "amount": 1080
   },
   {
    "index": 35,
    "type": "freeSpinEnd",
    "amount": 1060,
    "winLevel": 4
   },
   {
    "index": 36,
    "type": "finalWin",
    "amount": 1080
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.2,
  "freeGameWins": 10.6
 },
 {
  "id": 43,
  "payoutMultiplier": 0,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
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
       "name": "H3"
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
       "name": "L5"
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
       "name": "H2"
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
       "name": "L2"
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
       "name": "L1"
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
       "name": "H3"
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
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     198,
     131,
     176,
     77,
     177
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 44,
  "payoutMultiplier": 0,
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
       "name": "H2"
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
       "name": "H3"
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
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     124,
     65,
     20,
     77,
     86
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 45,
  "payoutMultiplier": 0,
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
       "name": "S",
       "scatter": true
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
       "name": "H4"
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
       "name": "L2"
      },
      {
       "name": "L2"
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
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "L1"
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
       "name": "H4"
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
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     38,
     149,
     137,
     205,
     8
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 46,
  "payoutMultiplier": 0,
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
       "name": "L1"
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
       "name": "L3"
      },
      {
       "name": "H4"
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
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "H1"
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
       "name": "L5"
      },
      {
       "name": "H3"
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
     ]
    ],
    "paddingPositions": [
     6,
     26,
     0,
     67,
     202
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 47,
  "payoutMultiplier": 4000,
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
       "name": "H1"
      },
      {
       "name": "H1"
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
       "name": "L1"
      },
      {
       "name": "H1"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      },
      {
       "name": "H2"
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
       "name": "L5"
      },
      {
       "name": "H2"
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
       "name": "H1"
      },
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
       "name": "H1"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     27,
     126,
     166,
     56,
     55
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
    "type": "winInfo",
    "totalWin": 4000,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
       "lineIndex": 8,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
       "lineIndex": 23,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
       }
      ],
      "meta": {
       "lineIndex": 29,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
       "lineIndex": 50,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 4000,
    "winLevel": 7
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 4000
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 4000
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 40.0,
  "freeGameWins": 0.0
 },
 {
  "id": 48,
  "payoutMultiplier": 60,
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
       "name": "L5"
      },
      {
       "name": "L1"
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
       "name": "L5"
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
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "H3"
      },
      {
       "name": "H4"
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
       "name": "L5"
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
     11,
     194,
     188,
     70,
     39
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
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       "lineIndex": 13,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 60
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.6,
  "freeGameWins": 0.0
 },
 {
  "id": 49,
  "payoutMultiplier": 30,
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
       "name": "L4"
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
       "name": "L3"
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
       "name": "L5"
      },
      {
       "name": "H2"
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
       "name": "L3"
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
     21,
     137,
     81,
     57,
     173
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
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "type": "finalWin",
    "amount": 30
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.3,
  "freeGameWins": 0.0
 },
 {
  "id": 50,
  "payoutMultiplier": 30,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
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
       "name": "H2"
      },
      {
       "name": "H1"
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
       "name": "L4"
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
       "name": "L3"
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
       "name": "H3"
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     65,
     101,
     140,
     118,
     187
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
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "type": "finalWin",
    "amount": 30
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.3,
  "freeGameWins": 0.0
 },
 {
  "id": 51,
  "payoutMultiplier": 0,
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
       "name": "L1"
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
       "name": "H4"
      },
      {
       "name": "H1"
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
       "name": "H3"
      },
      {
       "name": "L4"
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
       "name": "L3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H4"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     13,
     185,
     131,
     123,
     218
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 52,
  "payoutMultiplier": 50,
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
       "name": "L4"
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
       "name": "L5"
      },
      {
       "name": "H2"
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
       "name": "L3"
      },
      {
       "name": "L5"
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
       "name": "H3"
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
       "name": "H2"
      },
      {
       "name": "L3"
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
       "name": "L5"
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
       "name": "L4"
      },
      {
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     58,
     112,
     50,
     58,
     32
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
    "type": "winInfo",
    "totalWin": 50,
    "wins": [
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
       "lineIndex": 8,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
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
       "lineIndex": 23,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 50,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 50
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 50
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.5,
  "freeGameWins": 0.0
 },
 {
  "id": 53,
  "payoutMultiplier": 1120,
  "events": [
   {
    "index": 0,
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
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "H4"
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
       "name": "H4"
      },
      {
       "name": "H1"
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
       "name": "L3"
      },
      {
       "name": "H1"
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
       "name": "L3"
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
       "name": "L4"
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
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     53,
     185,
     51,
     14,
     126
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
    "type": "winInfo",
    "totalWin": 1120,
    "wins": [
     {
      "symbol": "L3",
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 1,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       }
      ],
      "meta": {
       "lineIndex": 11,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 21,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       "lineIndex": 39,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 1120,
    "winLevel": 5
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 1120
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 1120
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 11.2,
  "freeGameWins": 0.0
 },
 {
  "id": 54,
  "payoutMultiplier": 0,
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
       "name": "H2"
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
       "name": "L2"
      },
      {
       "name": "H4"
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
       "name": "L4"
      },
      {
       "name": "H4"
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
       "name": "L5"
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
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
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
     47,
     77,
     22,
     90,
     184
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 55,
  "payoutMultiplier": 1160,
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
       "name": "H4"
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
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L3"
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
       "name": "L3"
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
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     148,
     142,
     35,
     98,
     174
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
    "type": "wildNudge",
    "reel": 1,
    "nudges": 1,
    "multiplier": 2,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     }
    ]
   },
   {
    "index": 2,
    "type": "winInfo",
    "totalWin": 1160,
    "wins": [
     {
      "symbol": "L2",
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 60,
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
       "lineIndex": 8,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L2",
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
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 10,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 140,
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
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 2,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L3",
      "kind": 5,
      "win": 600,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 23,
       "multiplier": 2,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L2",
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L2",
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
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 28,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 60,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 60,
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
       "lineIndex": 50,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 3,
    "type": "setWin",
    "amount": 1160,
    "winLevel": 5
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 1160
   },
   {
    "index": 5,
    "type": "finalWin",
    "amount": 1160
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 11.6,
  "freeGameWins": 0.0
 },
 {
  "id": 56,
  "payoutMultiplier": 0,
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
       "name": "L3"
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
       "name": "H1"
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
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "H2"
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
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     150,
     154,
     4,
     57,
     131
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 57,
  "payoutMultiplier": 10,
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
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L2"
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
       "name": "L3"
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
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     52,
     189,
     164,
     51,
     10
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
    "type": "winInfo",
    "totalWin": 10,
    "wins": [
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
        "row": 3
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 50,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 10
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 10
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.1,
  "freeGameWins": 0.0
 },
 {
  "id": 58,
  "payoutMultiplier": 500000,
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
       "name": "S",
       "scatter": true
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
       "name": "H2"
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
       "name": "H1"
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     35,
     8,
     8,
     9,
     37
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
    "totalWin": 10,
    "wins": [
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
        "row": 3
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 10
   },
   {
    "index": 4,
    "type": "freeSpinTrigger",
    "totalFs": 15,
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
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 15
   },
   {
    "index": 6,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "H4"
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
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "H4"
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
       "name": "L1"
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
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      }
     ]
    ],
    "paddingPositions": [
     91,
     23,
     44,
     53,
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
    "index": 7,
    "type": "wildNudge",
    "reel": 2,
    "nudges": 3,
    "multiplier": 4,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 4
     }
    ]
   },
   {
    "index": 8,
    "type": "winInfo",
    "totalWin": 372800,
    "wins": [
     {
      "symbol": "L4",
      "kind": 4,
      "win": 2700,
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
       }
      ],
      "meta": {
       "lineIndex": 1,
       "multiplier": 54,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 480,
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
       "lineIndex": 2,
       "multiplier": 24,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 2400,
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
       "lineIndex": 3,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 14000,
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
       "lineIndex": 4,
       "multiplier": 14,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1080,
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
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 54,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 1400,
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
       "lineIndex": 6,
       "multiplier": 14,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 7,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 480,
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
       "lineIndex": 8,
       "multiplier": 24,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 2700,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 54,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 14000,
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
       "lineIndex": 10,
       "multiplier": 14,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 1200,
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
       }
      ],
      "meta": {
       "lineIndex": 11,
       "multiplier": 24,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 24000,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 12,
       "multiplier": 24,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1080,
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
       "lineIndex": 13,
       "multiplier": 54,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 1400,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 14,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 480,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 24,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1080,
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
       "lineIndex": 17,
       "multiplier": 54,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 1400,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 14,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 1200,
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
       },
       {
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 19,
       "multiplier": 24,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 24000,
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
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 24,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1080,
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
       }
      ],
      "meta": {
       "lineIndex": 21,
       "multiplier": 54,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 14000,
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
       "lineIndex": 22,
       "multiplier": 14,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 1200,
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
       }
      ],
      "meta": {
       "lineIndex": 23,
       "multiplier": 24,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 24,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 20800,
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
        "row": 4
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 104,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 104
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 1400,
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
       "lineIndex": 26,
       "multiplier": 14,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1080,
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
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 54,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 14000,
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
       "lineIndex": 28,
       "multiplier": 14,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 480,
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
       }
      ],
      "meta": {
       "lineIndex": 29,
       "multiplier": 24,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 2400,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 480,
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
       "lineIndex": 31,
       "multiplier": 24,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 2400,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 5400,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 54,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 280,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 14,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 24000,
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
       "lineIndex": 35,
       "multiplier": 24,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 8800,
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
        "row": 3
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
       "lineIndex": 36,
       "multiplier": 44,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 44
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 5400,
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
       "lineIndex": 37,
       "multiplier": 54,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 280,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 14,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 1200,
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
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 39,
       "multiplier": 24,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 24000,
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
       "lineIndex": 40,
       "multiplier": 24,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 54000,
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
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 54,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 12800,
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
        "row": 1
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 64,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 64
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 480,
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
       "lineIndex": 44,
       "multiplier": 24,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1080,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 54,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 1400,
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
       "lineIndex": 46,
       "multiplier": 14,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 54000,
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
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 54,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 54
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 12800,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 64,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 64
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 480,
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
       "lineIndex": 49,
       "multiplier": 24,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 2400,
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
       "lineIndex": 50,
       "multiplier": 24,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 24
      }
     }
    ]
   },
   {
    "index": 9,
    "type": "setWin",
    "amount": 372800,
    "winLevel": 9
   },
   {
    "index": 10,
    "type": "setTotalWin",
    "amount": 372810
   },
   {
    "index": 11,
    "type": "updateFreeSpin",
    "amount": 1,
    "total": 15
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
       "name": "L2"
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
       "name": "H2"
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
       "name": "L3"
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
       "name": "L5"
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
       "name": "L2"
      },
      {
       "name": "L4"
      },
      {
       "name": "H1"
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
       "name": "H1"
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
       "name": "H3"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     50,
     76,
     3,
     70,
     51
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
    "type": "setTotalWin",
    "amount": 372810
   },
   {
    "index": 14,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 15
   },
   {
    "index": 15,
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
       "name": "L1"
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
       "name": "L3"
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
       "name": "H1"
      },
      {
       "name": "L4"
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
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     60,
     20,
     2,
     33,
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
    "index": 16,
    "type": "winInfo",
    "totalWin": 90,
    "wins": [
     {
      "symbol": "L4",
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
       "lineIndex": 4,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
      "kind": 4,
      "win": 50,
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
       },
       {
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 22,
       "multiplier": 1,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 17,
    "type": "setWin",
    "amount": 90,
    "winLevel": 2
   },
   {
    "index": 18,
    "type": "setTotalWin",
    "amount": 372900
   },
   {
    "index": 19,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 15
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
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "H4"
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
       "name": "L4"
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
       "name": "H3"
      },
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
       "name": "L3"
      },
      {
       "name": "H3"
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
     31,
     8,
     77,
     33,
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
    "index": 21,
    "type": "winInfo",
    "totalWin": 8400,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 200,
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
       "lineIndex": 3,
       "multiplier": 20,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "L5",
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 20,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 2000,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 20,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 50,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 50
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 500,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 5,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 5000,
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
       "lineIndex": 49,
       "multiplier": 50,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 50
      }
     }
    ]
   },
   {
    "index": 22,
    "type": "setWin",
    "amount": 8400,
    "winLevel": 8
   },
   {
    "index": 23,
    "type": "setTotalWin",
    "amount": 381300
   },
   {
    "index": 24,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 15
   },
   {
    "index": 25,
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
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L4"
      },
      {
       "name": "L1"
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
       "name": "L4"
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
       "name": "H1"
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
       "name": "H1"
      },
      {
       "name": "H2"
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
       "name": "H3"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      }
     ]
    ],
    "paddingPositions": [
     30,
     71,
     48,
     84,
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
    "index": 26,
    "type": "winInfo",
    "totalWin": 1120,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 60,
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
       "lineIndex": 8,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 60,
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
       "lineIndex": 23,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1000,
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
       }
      ],
      "meta": {
       "lineIndex": 29,
       "multiplier": 50,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 50
      }
     }
    ]
   },
   {
    "index": 27,
    "type": "setWin",
    "amount": 1120,
    "winLevel": 5
   },
   {
    "index": 28,
    "type": "setTotalWin",
    "amount": 382420
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 15
   },
   {
    "index": 30,
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
       "name": "L2"
      },
      {
       "name": "H2"
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
       "name": "L3"
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
       "name": "H1"
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
       "name": "H1"
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
       "name": "H2"
      },
      {
       "name": "H1"
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
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     3,
     79,
     31,
     65,
     68
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
    "type": "setTotalWin",
    "amount": 382420
   },
   {
    "index": 32,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 15
   },
   {
    "index": 33,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "L5"
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
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
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
       "name": "H4"
      },
      {
       "name": "H1"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
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
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      }
     ]
    ],
    "paddingPositions": [
     95,
     92,
     54,
     43,
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
    "index": 34,
    "type": "winInfo",
    "totalWin": 500000,
    "wins": [
     {
      "symbol": "H4",
      "kind": 5,
      "win": 38400,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 1,
       "multiplier": 48,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 48
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 25600,
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
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 2,
       "multiplier": 32,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 32
      }
     },
     {
      "symbol": "H1",
      "kind": 5,
      "win": 260000,
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
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 52,
       "winWithoutMult": 5000,
       "globalMult": 1,
       "lineMultiplier": 52
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 8000,
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
       "lineIndex": 7,
       "multiplier": 80,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 80
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 38400,
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
        "row": 1
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 48,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 48
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 22400,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 11,
       "multiplier": 28,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 28
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 4200,
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
        "row": 4
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
       "lineIndex": 12,
       "multiplier": 42,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 42
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 41600,
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
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 13,
       "multiplier": 52,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 52
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 64000,
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
        "row": 3
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 80,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 80
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 41600,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 17,
       "multiplier": 52,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 52
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 22400,
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
       "lineIndex": 19,
       "multiplier": 28,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 28
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 23200,
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
       },
       {
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 21,
       "multiplier": 29,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 29
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 5000,
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
       "lineIndex": 24,
       "multiplier": 50,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 50
      }
     },
     {
      "symbol": "H1",
      "kind": 5,
      "win": 300000,
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
        "row": 4
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 60,
       "winWithoutMult": 5000,
       "globalMult": 1,
       "lineMultiplier": 60
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 68000,
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
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 85,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 85
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 25600,
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
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 29,
       "multiplier": 32,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 32
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 6200,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 62,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 62
      }
     },
     {
      "symbol": "H1",
      "kind": 5,
      "win": 160000,
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
       "lineIndex": 31,
       "multiplier": 32,
       "winWithoutMult": 5000,
       "globalMult": 1,
       "lineMultiplier": 32
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 80000,
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
       "lineIndex": 33,
       "multiplier": 100,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 100
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 48000,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 35,
       "multiplier": 60,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 60
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 80000,
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
        "row": 3
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 37,
       "multiplier": 100,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 100
      }
     },
     {
      "symbol": "H1",
      "kind": 5,
      "win": 140000,
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
        "reel": 3,
        "row": 1
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 39,
       "multiplier": 28,
       "winWithoutMult": 5000,
       "globalMult": 1,
       "lineMultiplier": 28
      }
     },
     {
      "symbol": "H4",
      "kind": 5,
      "win": 64000,
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
        "row": 4
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 80,
       "winWithoutMult": 800,
       "globalMult": 1,
       "lineMultiplier": 80
      }
     },
     {
      "symbol": "H1",
      "kind": 5,
      "win": 400000,
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
        "reel": 3,
        "row": 3
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 80,
       "winWithoutMult": 5000,
       "globalMult": 1,
       "lineMultiplier": 80
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 5200,
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
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 52,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 52
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 8000,
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
        "reel": 3,
        "row": 4
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 80,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 80
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 3200,
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
       "lineIndex": 49,
       "multiplier": 32,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 32
      }
     }
    ]
   },
   {
    "index": 35,
    "type": "wincap",
    "amount": 500000
   },
   {
    "index": 36,
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 37,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 15
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
       "name": "L1"
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
       "name": "H3"
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
       "name": "L5"
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
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L2"
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
       "name": "H4"
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
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
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
     84,
     16,
     68,
     4,
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
    "index": 39,
    "type": "winInfo",
    "totalWin": 1400,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 4,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 1200,
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
       "lineIndex": 50,
       "multiplier": 4,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     }
    ]
   },
   {
    "index": 40,
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 41,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 15
   },
   {
    "index": 42,
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
       "name": "L5"
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
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "L4"
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
       "name": "L4"
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
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     1,
     60,
     64,
     45,
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
    "index": 43,
    "type": "winInfo",
    "totalWin": 190800,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 6000,
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
       "lineIndex": 3,
       "multiplier": 30,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 30
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 1800,
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
       "lineIndex": 4,
       "multiplier": 60,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 60
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 13000,
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
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 65,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 65
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 700,
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
       "lineIndex": 7,
       "multiplier": 70,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 70
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 600,
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
       "lineIndex": 10,
       "multiplier": 20,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 12000,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 12,
       "multiplier": 60,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 60
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 11000,
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
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 13,
       "multiplier": 55,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 55
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 2100,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 70,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 70
      }
     },
     {
      "symbol": "H3",
      "kind": 4,
      "win": 19500,
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
        "row": 3
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 65,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 65
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 900,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 30,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 30
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 4000,
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
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 20,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 1800,
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
       "lineIndex": 22,
       "multiplier": 60,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 60
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 2100,
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
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 24,
       "multiplier": 70,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 70
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 300,
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
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 15,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 15
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 4900,
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
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 28,
       "multiplier": 70,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 70
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 14000,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 70,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 70
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 6500,
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
       "lineIndex": 31,
       "multiplier": 65,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 65
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 4000,
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
       "lineIndex": 33,
       "multiplier": 20,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 31500,
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
        "row": 2
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 105,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 105
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 19500,
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
        "row": 2
       },
       {
        "reel": 4,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 65,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 65
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 1400,
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
        "reel": 3,
        "row": 1
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 39,
       "multiplier": 14,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 14
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 10,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L5",
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
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 30,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 30
      }
     },
     {
      "symbol": "L4",
      "kind": 5,
      "win": 21000,
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
        "reel": 3,
        "row": 2
       },
       {
        "reel": 4,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 105,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 105
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 1200,
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
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 60,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 60
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 10500,
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
       "lineIndex": 49,
       "multiplier": 105,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 105
      }
     }
    ]
   },
   {
    "index": 44,
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 45,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 15
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
       "name": "L2"
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
       "name": "H2"
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
       "name": "L5"
      },
      {
       "name": "H4"
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
       "name": "L2"
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      }
     ]
    ],
    "paddingPositions": [
     54,
     3,
     2,
     21,
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
    "index": 47,
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 48,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 15
   },
   {
    "index": 49,
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
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "H3"
      },
      {
       "name": "L4"
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
       "name": "H1"
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
       "name": "H4"
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
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     28,
     68,
     32,
     72,
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
    "index": 50,
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 51,
    "type": "updateFreeSpin",
    "amount": 11,
    "total": 15
   },
   {
    "index": 52,
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
       "name": "H4"
      },
      {
       "name": "L4"
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
       "name": "L4"
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
       "name": "H4"
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
       "name": "H1"
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
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
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
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     63,
     70,
     76,
     65,
     71
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
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       }
      ],
      "meta": {
       "lineIndex": 1,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       }
      ],
      "meta": {
       "lineIndex": 21,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 54,
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 55,
    "type": "updateFreeSpin",
    "amount": 12,
    "total": 15
   },
   {
    "index": 56,
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
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L2"
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
       "name": "L3"
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
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
       "name": "H3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
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
     25,
     65,
     2,
     87,
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
    "index": 57,
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 58,
    "type": "updateFreeSpin",
    "amount": 13,
    "total": 15
   },
   {
    "index": 59,
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
       "name": "L2"
      },
      {
       "name": "H1"
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
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "L3"
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
       "name": "L3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
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
       "name": "H3"
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
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     179,
     51,
     160,
     13,
     124
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
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 61,
    "type": "updateFreeSpin",
    "amount": 14,
    "total": 15
   },
   {
    "index": 62,
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
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "W",
       "wild": true,
       "multiplier": 5
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
       "name": "H1"
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
       "name": "H3"
      },
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
       "name": "H1"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
     ]
    ],
    "paddingPositions": [
     13,
     28,
     0,
     33,
     95
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
    "type": "winInfo",
    "totalWin": 50100,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 10000,
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
       "lineIndex": 4,
       "multiplier": 10,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 5000,
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
       "lineIndex": 7,
       "multiplier": 5,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 5000,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 12,
       "multiplier": 5,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 10000,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 10,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 100,
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
       "lineIndex": 19,
       "multiplier": 5,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 10000,
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
       "lineIndex": 22,
       "multiplier": 10,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 5000,
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
       "lineIndex": 24,
       "multiplier": 5,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 5000,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 5,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     }
    ]
   },
   {
    "index": 64,
    "type": "setTotalWin",
    "amount": 500000
   },
   {
    "index": 65,
    "type": "freeSpinEnd",
    "amount": 500000,
    "winLevel": 10
   },
   {
    "index": 66,
    "type": "finalWin",
    "amount": 500000
   }
  ],
  "criteria": "wincap",
  "baseGameWins": 0.1,
  "freeGameWins": 5000
 },
 {
  "id": 59,
  "payoutMultiplier": 50,
  "events": [
   {
    "index": 0,
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
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L5"
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
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "L1"
      }
     ]
    ],
    "paddingPositions": [
     159,
     160,
     203,
     172,
     38
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
    "type": "winInfo",
    "totalWin": 50,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 10,
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
       "lineIndex": 35,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       "lineIndex": 49,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 50,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 50
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 50
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.5,
  "freeGameWins": 0.0
 },
 {
  "id": 60,
  "payoutMultiplier": 0,
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
       "name": "L2"
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
       "name": "L5"
      },
      {
       "name": "H3"
      },
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
       "name": "L4"
      },
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
     ]
    ],
    "paddingPositions": [
     142,
     55,
     207,
     82,
     75
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 61,
  "payoutMultiplier": 100,
  "events": [
   {
    "index": 0,
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
       "name": "L3"
      },
      {
       "name": "H4"
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
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L4"
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
       "name": "L3"
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
       "name": "H4"
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
       "name": "H1"
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
       "name": "L5"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     60,
     176,
     156,
     71,
     49
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
    "type": "winInfo",
    "totalWin": 100,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 7,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 24,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 10,
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
       "lineIndex": 37,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L3",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 49,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 100,
    "winLevel": 3
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 100
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 1.0,
  "freeGameWins": 0.0
 },
 {
  "id": 62,
  "payoutMultiplier": 40,
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
       "name": "L3"
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
       "name": "L5"
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
       "name": "H4"
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
       "name": "L4"
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
       "name": "H2"
      },
      {
       "name": "L3"
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
       "name": "L5"
      },
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
       "name": "H4"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     152,
     183,
     41,
     58,
     195
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
    "type": "winInfo",
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L4",
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 8,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 23,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 40,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 40
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 40
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.4,
  "freeGameWins": 0.0
 },
 {
  "id": 63,
  "payoutMultiplier": 57170,
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
       "name": "H3"
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
       "name": "H2"
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
       "name": "L5"
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
       "name": "H4"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     71,
     112,
     9,
     50,
     35
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
    "type": "winInfo",
    "totalWin": 10,
    "wins": [
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 10
   },
   {
    "index": 4,
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
      "row": 4
     }
    ]
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
       "name": "L4"
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
       "name": "H2"
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "L2"
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
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     173,
     1,
     16,
     44,
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
    "index": 7,
    "type": "wildNudge",
    "reel": 1,
    "nudges": 2,
    "multiplier": 3,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 3
     }
    ]
   },
   {
    "index": 8,
    "type": "winInfo",
    "totalWin": 2960,
    "wins": [
     {
      "symbol": "L2",
      "kind": 4,
      "win": 420,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 6,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 90,
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
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 3,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 420,
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
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 31,
       "multiplier": 6,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 1610,
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
        "reel": 3,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 39,
       "multiplier": 23,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 23
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 420,
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
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 6,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     }
    ]
   },
   {
    "index": 9,
    "type": "setWin",
    "amount": 2960,
    "winLevel": 6
   },
   {
    "index": 10,
    "type": "setTotalWin",
    "amount": 2970
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
       "name": "H4"
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
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H3"
      },
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
       "name": "H3"
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
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     45,
     12,
     0,
     59,
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
    "index": 13,
    "type": "winInfo",
    "totalWin": 500,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 40,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 400,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 2,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 60,
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
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 14,
    "type": "setWin",
    "amount": 500,
    "winLevel": 5
   },
   {
    "index": 15,
    "type": "setTotalWin",
    "amount": 3470
   },
   {
    "index": 16,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 8
   },
   {
    "index": 17,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
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
       "name": "H2"
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
       "name": "H2"
      },
      {
       "name": "H1"
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
       "name": "L3"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H2"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     55,
     172,
     62,
     7,
     184
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
    "type": "setTotalWin",
    "amount": 3470
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
       "name": "H2"
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
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "L1"
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
       "name": "H2"
      },
      {
       "name": "H2"
      },
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
       "name": "L4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     76,
     57,
     164,
     145,
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
    "index": 21,
    "type": "setTotalWin",
    "amount": 3470
   },
   {
    "index": 22,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 8
   },
   {
    "index": 23,
    "type": "reveal",
    "board": [
     [
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
       "name": "L1"
      },
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      }
     ],
     [
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     38,
     157,
     66,
     108,
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
    "index": 24,
    "type": "winInfo",
    "totalWin": 36780,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 160,
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
       "lineIndex": 2,
       "multiplier": 8,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 1800,
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
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 6,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
       "lineIndex": 8,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 1800,
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
       "lineIndex": 13,
       "multiplier": 6,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 17,
       "multiplier": 8,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
       "lineIndex": 23,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 1800,
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
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 6,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 120,
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
       }
      ],
      "meta": {
       "lineIndex": 29,
       "multiplier": 6,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 120,
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
       "lineIndex": 31,
       "multiplier": 6,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 900,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 3,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 1500,
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
       "lineIndex": 37,
       "multiplier": 5,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 8000,
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
       "lineIndex": 44,
       "multiplier": 8,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 8
      }
     }
    ]
   },
   {
    "index": 25,
    "type": "setWin",
    "amount": 36780,
    "winLevel": 9
   },
   {
    "index": 26,
    "type": "setTotalWin",
    "amount": 40250
   },
   {
    "index": 27,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 8
   },
   {
    "index": 28,
    "type": "reveal",
    "board": [
     [
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L1"
      }
     ],
     [
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H2"
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
       "name": "H1"
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
       "name": "H1"
      },
      {
       "name": "H2"
      },
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
       "name": "L4"
      },
      {
       "name": "H1"
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
     130,
     14,
     43,
     85,
     143
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
    "type": "winInfo",
    "totalWin": 16800,
    "wins": [
     {
      "symbol": "H2",
      "kind": 4,
      "win": 3000,
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
       }
      ],
      "meta": {
       "lineIndex": 1,
       "multiplier": 6,
       "winWithoutMult": 500,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 1800,
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
       }
      ],
      "meta": {
       "lineIndex": 21,
       "multiplier": 6,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H1",
      "kind": 3,
      "win": 6000,
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
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 6,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     }
    ]
   },
   {
    "index": 30,
    "type": "setWin",
    "amount": 16800,
    "winLevel": 9
   },
   {
    "index": 31,
    "type": "setTotalWin",
    "amount": 57050
   },
   {
    "index": 32,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 33,
    "type": "reveal",
    "board": [
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
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H1"
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
       "name": "H4"
      },
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
       "name": "L5"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L4"
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
       "name": "H1"
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
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     126,
     81,
     176,
     131,
     180
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
    "type": "setTotalWin",
    "amount": 57050
   },
   {
    "index": 35,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 36,
    "type": "reveal",
    "board": [
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H1"
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
       "name": "H1"
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
       "name": "H3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L4"
      },
      {
       "name": "L3"
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
       "name": "H1"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L5"
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
     ]
    ],
    "paddingPositions": [
     36,
     194,
     186,
     195,
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
    "index": 37,
    "type": "winInfo",
    "totalWin": 120,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 46,
       "multiplier": 3,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 38,
    "type": "setWin",
    "amount": 120,
    "winLevel": 3
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 57170
   },
   {
    "index": 40,
    "type": "freeSpinEnd",
    "amount": 57160,
    "winLevel": 8
   },
   {
    "index": 41,
    "type": "finalWin",
    "amount": 57170
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.1,
  "freeGameWins": 571.6
 },
 {
  "id": 64,
  "payoutMultiplier": 50,
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
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
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
       "name": "H4"
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
     ]
    ],
    "paddingPositions": [
     67,
     50,
     167,
     121,
     159
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
    "type": "winInfo",
    "totalWin": 50,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 50,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 1,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 50,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 50
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 50
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.5,
  "freeGameWins": 0.0
 },
 {
  "id": 65,
  "payoutMultiplier": 30,
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
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
       "name": "L2"
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
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L5"
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
       "name": "H2"
      },
      {
       "name": "H1"
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
       "name": "H2"
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
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     111,
     63,
     201,
     114,
     75
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
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "type": "finalWin",
    "amount": 30
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.3,
  "freeGameWins": 0.0
 },
 {
  "id": 66,
  "payoutMultiplier": 1000,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
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
       "name": "L4"
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
       "name": "H3"
      },
      {
       "name": "L5"
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
       "name": "H2"
      },
      {
       "name": "H3"
      },
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
     ]
    ],
    "paddingPositions": [
     196,
     104,
     119,
     106,
     68
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
    "type": "winInfo",
    "totalWin": 1000,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 1000,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 36,
       "multiplier": 1,
       "winWithoutMult": 1000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 1000,
    "winLevel": 5
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 1000
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 1000
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 10.0,
  "freeGameWins": 0.0
 },
 {
  "id": 67,
  "payoutMultiplier": 0,
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
       "name": "H4"
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
       "name": "L2"
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
       "name": "H3"
      },
      {
       "name": "L5"
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
       "name": "H1"
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
       "name": "L4"
      },
      {
       "name": "L5"
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
     62,
     110,
     120,
     67,
     184
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 68,
  "payoutMultiplier": 0,
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
       "name": "L3"
      },
      {
       "name": "L1"
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
       "name": "H1"
      },
      {
       "name": "L5"
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
       "name": "H3"
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
       "name": "L4"
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
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     24,
     205,
     42,
     17,
     154
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 69,
  "payoutMultiplier": 20,
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
       "name": "H3"
      },
      {
       "name": "L4"
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
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "L1"
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
       "name": "H4"
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
       "name": "H2"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
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
       "name": "H1"
      },
      {
       "name": "S",
       "scatter": true
      }
     ]
    ],
    "paddingPositions": [
     75,
     179,
     117,
     115,
     34
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L5",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 4,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 22,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 20
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.2,
  "freeGameWins": 0.0
 },
 {
  "id": 70,
  "payoutMultiplier": 130,
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
       "name": "H3"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H1"
      },
      {
       "name": "L5"
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
       "name": "H2"
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
       "name": "H4"
      },
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
       "name": "H4"
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
       "name": "L3"
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
     ]
    ],
    "paddingPositions": [
     158,
     204,
     2,
     67,
     39
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
    "type": "winInfo",
    "totalWin": 130,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 100,
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
       "lineIndex": 44,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 130,
    "winLevel": 3
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 130
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 130
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 1.3,
  "freeGameWins": 0.0
 },
 {
  "id": 71,
  "payoutMultiplier": 10,
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
       "name": "H3"
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
       "name": "L3"
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
       "name": "H4"
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
       "name": "L5"
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
       "name": "L3"
      },
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
       "name": "L3"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     106,
     65,
     68,
     88,
     94
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
    "type": "winInfo",
    "totalWin": 10,
    "wins": [
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
        "row": 3
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 3,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 10
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 10
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.1,
  "freeGameWins": 0.0
 },
 {
  "id": 72,
  "payoutMultiplier": 70,
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
       "name": "L3"
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
       "name": "L3"
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
       "name": "H2"
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
       "name": "L2"
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
       "name": "L3"
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
       "name": "L3"
      },
      {
       "name": "H4"
      },
      {
       "name": "H1"
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
     ]
    ],
    "paddingPositions": [
     103,
     132,
     128,
     51,
     115
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
    "type": "winInfo",
    "totalWin": 70,
    "wins": [
     {
      "symbol": "L3",
      "kind": 4,
      "win": 70,
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
       "lineIndex": 17,
       "multiplier": 1,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 70,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 70
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 70
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.7,
  "freeGameWins": 0.0
 },
 {
  "id": 73,
  "payoutMultiplier": 30,
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
       "name": "L2"
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
       "name": "H3"
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
       "name": "H4"
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
       "name": "L3"
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
     ]
    ],
    "paddingPositions": [
     131,
     29,
     81,
     30,
     204
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
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "type": "finalWin",
    "amount": 30
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.3,
  "freeGameWins": 0.0
 },
 {
  "id": 74,
  "payoutMultiplier": 0,
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
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
       "name": "H4"
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
       "name": "H4"
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
       "name": "L5"
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
       "name": "L3"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     111,
     116,
     10,
     186,
     196
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 75,
  "payoutMultiplier": 38160,
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
       "name": "H2"
      },
      {
       "name": "H2"
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
       "name": "L5"
      },
      {
       "name": "H4"
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
       "name": "L3"
      },
      {
       "name": "L4"
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
     69,
     8,
     167,
     85,
     216
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
    "totalFs": 8,
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
     }
    ]
   },
   {
    "index": 3,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 4,
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
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "H2"
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
       "name": "H1"
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
       "name": "H1"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
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
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
     136,
     15,
     1,
     168,
     105
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
    "index": 5,
    "type": "winInfo",
    "totalWin": 1000,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 800,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 4,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 200,
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
       "lineIndex": 49,
       "multiplier": 1,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 6,
    "type": "setWin",
    "amount": 1000,
    "winLevel": 5
   },
   {
    "index": 7,
    "type": "setTotalWin",
    "amount": 1000
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
       "name": "L3"
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
       "name": "L3"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 10
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
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L4"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "L1"
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
     25,
     62,
     162,
     195,
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
    "index": 10,
    "type": "wildNudge",
    "reel": 2,
    "nudges": 1,
    "multiplier": 2,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     }
    ]
   },
   {
    "index": 11,
    "type": "winInfo",
    "totalWin": 23600,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "lineIndex": 1,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 3600,
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
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 2,
       "multiplier": 12,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 12
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 40,
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
       "lineIndex": 3,
       "multiplier": 4,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 700,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 10,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 120,
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
       "lineIndex": 6,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 7,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 300,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 8,
       "multiplier": 10,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "lineIndex": 11,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 700,
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
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 13,
       "multiplier": 10,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 120,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 300,
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
        "row": 3
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 10,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 700,
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
       "lineIndex": 17,
       "multiplier": 10,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 120,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       "lineIndex": 19,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 700,
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
       "lineIndex": 21,
       "multiplier": 10,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 60,
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
       "lineIndex": 23,
       "multiplier": 6,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 24,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 120,
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
       "lineIndex": 26,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 3600,
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
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 29,
       "multiplier": 12,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 12
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 40,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 4,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 3600,
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
       "lineIndex": 31,
       "multiplier": 12,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 12
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 40,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 4,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 120,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 700,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 10,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L2",
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 35,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 36,
       "multiplier": 6,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 120,
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
       "lineIndex": 37,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 700,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 10,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 180,
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
       "lineIndex": 39,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 60,
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
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
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
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L5",
      "kind": 4,
      "win": 300,
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
       },
       {
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 44,
       "multiplier": 10,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 700,
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
        "reel": 3,
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 10,
       "winWithoutMult": 70,
       "globalMult": 1,
       "lineMultiplier": 10
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 120,
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
       "lineIndex": 46,
       "multiplier": 4,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 60,
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
       }
      ],
      "meta": {
       "lineIndex": 47,
       "multiplier": 2,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 180,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 6,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L2",
      "kind": 5,
      "win": 3600,
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
       "lineIndex": 49,
       "multiplier": 12,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 12
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 40,
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
       "lineIndex": 50,
       "multiplier": 4,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     }
    ]
   },
   {
    "index": 12,
    "type": "setWin",
    "amount": 23600,
    "winLevel": 9
   },
   {
    "index": 13,
    "type": "setTotalWin",
    "amount": 24600
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
       "name": "H2"
      },
      {
       "name": "L5"
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
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L5"
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
       "name": "H2"
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
       "name": "H3"
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
       "name": "L2"
      },
      {
       "name": "H4"
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
       "name": "L1"
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
       "name": "L4"
      },
      {
       "name": "L5"
      }
     ]
    ],
    "paddingPositions": [
     192,
     116,
     199,
     150,
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
    "index": 16,
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L5",
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 5,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 25,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 17,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 18,
    "type": "setTotalWin",
    "amount": 24620
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
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "L3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "H4"
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
     155,
     150,
     146,
     5,
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
    "index": 21,
    "type": "wildNudge",
    "reel": 1,
    "nudges": 1,
    "multiplier": 2,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     }
    ]
   },
   {
    "index": 22,
    "type": "winInfo",
    "totalWin": 9400,
    "wins": [
     {
      "symbol": "L1",
      "kind": 4,
      "win": 600,
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
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 4,
       "multiplier": 6,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 6,
       "multiplier": 6,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 100,
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
       "lineIndex": 7,
       "multiplier": 2,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 600,
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
       "lineIndex": 10,
       "multiplier": 6,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 300,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 6,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 6,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 300,
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
       "lineIndex": 22,
       "multiplier": 6,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L1",
      "kind": 4,
      "win": 200,
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
       },
       {
        "reel": 3,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 24,
       "multiplier": 2,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 26,
       "multiplier": 6,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 600,
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
       "lineIndex": 28,
       "multiplier": 6,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 300,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 6,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 600,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 6,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 6,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 46,
       "multiplier": 6,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 1200,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 6,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 6
      }
     },
     {
      "symbol": "L1",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 49,
       "multiplier": 2,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 23,
    "type": "setWin",
    "amount": 9400,
    "winLevel": 8
   },
   {
    "index": 24,
    "type": "setTotalWin",
    "amount": 34020
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
       "name": "H1"
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
       "name": "H4"
      },
      {
       "name": "L2"
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
     ],
     [
      {
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "L2"
      }
     ],
     [
      {
       "name": "L1"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H4"
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
       "name": "L3"
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
     182,
     201,
     169,
     158,
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
    "index": 27,
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 12,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 28,
    "type": "setWin",
    "amount": 30,
    "winLevel": 2
   },
   {
    "index": 29,
    "type": "setTotalWin",
    "amount": 34050
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
       "name": "H2"
      },
      {
       "name": "H4"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "H2"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
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
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H4"
      },
      {
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
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
       "name": "H1"
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
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     128,
     22,
     13,
     82,
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
    "index": 32,
    "type": "winInfo",
    "totalWin": 800,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 100,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 5,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 500,
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
       "lineIndex": 40,
       "multiplier": 5,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 100,
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
       }
      ],
      "meta": {
       "lineIndex": 41,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 100,
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
       "lineIndex": 44,
       "multiplier": 5,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 5
      }
     }
    ]
   },
   {
    "index": 33,
    "type": "setWin",
    "amount": 800,
    "winLevel": 5
   },
   {
    "index": 34,
    "type": "setTotalWin",
    "amount": 34850
   },
   {
    "index": 35,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 36,
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
       "name": "L4"
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
       "name": "L3"
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
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
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
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "L1"
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
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     169,
     31,
     17,
     91,
     108
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
    "type": "setTotalWin",
    "amount": 34850
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
       "name": "H2"
      },
      {
       "name": "L1"
      },
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
       "name": "L4"
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
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 5
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
       "name": "W",
       "wild": true,
       "multiplier": 5
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L2"
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
     95,
     12,
     73,
     99,
     161
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
    "type": "wildNudge",
    "reel": 2,
    "nudges": 1,
    "multiplier": 2,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     }
    ]
   },
   {
    "index": 41,
    "type": "winInfo",
    "totalWin": 3310,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 70,
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
       "lineIndex": 3,
       "multiplier": 7,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 210,
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
       "lineIndex": 6,
       "multiplier": 7,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 140,
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
       "lineIndex": 7,
       "multiplier": 7,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 40,
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
       }
      ],
      "meta": {
       "lineIndex": 11,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 200,
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
        "row": 4
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
       "lineIndex": 12,
       "multiplier": 2,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 210,
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 7,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 140,
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
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 7,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 210,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 7,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 40,
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
       "lineIndex": 19,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 200,
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
        "row": 4
       },
       {
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 2,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 140,
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
       "lineIndex": 24,
       "multiplier": 7,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 210,
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
       "lineIndex": 26,
       "multiplier": 7,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 70,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 7,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 70,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 7,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 350,
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
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 33,
       "multiplier": 7,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 350,
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
       "lineIndex": 37,
       "multiplier": 7,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 40,
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
       "lineIndex": 39,
       "multiplier": 2,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 200,
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
        "row": 4
       },
       {
        "reel": 4,
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 40,
       "multiplier": 2,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 140,
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
       }
      ],
      "meta": {
       "lineIndex": 43,
       "multiplier": 7,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L3",
      "kind": 3,
      "win": 210,
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
       "lineIndex": 46,
       "multiplier": 7,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 70,
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
       "lineIndex": 50,
       "multiplier": 7,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 7
      }
     }
    ]
   },
   {
    "index": 42,
    "type": "setWin",
    "amount": 3310,
    "winLevel": 7
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 38160
   },
   {
    "index": 44,
    "type": "freeSpinEnd",
    "amount": 38160,
    "winLevel": 7
   },
   {
    "index": 45,
    "type": "finalWin",
    "amount": 38160
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.0,
  "freeGameWins": 381.6
 },
 {
  "id": 76,
  "payoutMultiplier": 300,
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
       "name": "L2"
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
       "name": "H1"
      },
      {
       "name": "H4"
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
       "name": "L3"
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
       "name": "H4"
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
       "name": "L3"
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
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     142,
     156,
     60,
     37,
     142
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
    "type": "winInfo",
    "totalWin": 300,
    "wins": [
     {
      "symbol": "H4",
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
       "lineIndex": 6,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H4",
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
       "lineIndex": 26,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 100,
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 32,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 300,
    "winLevel": 4
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 300
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 300
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 3.0,
  "freeGameWins": 0.0
 },
 {
  "id": 77,
  "payoutMultiplier": 0,
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
       "name": "L3"
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
       "name": "L3"
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "H4"
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
     8,
     167,
     37,
     166,
     102
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
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 78,
  "payoutMultiplier": 0,
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
       "name": "H2"
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
       "name": "L5"
      },
      {
       "name": "L1"
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
       "name": "H2"
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
       "name": "H3"
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
       "name": "L4"
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
       "name": "H3"
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
     89,
     152,
     41,
     61,
     62
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 79,
  "payoutMultiplier": 10,
  "events": [
   {
    "index": 0,
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
       "name": "L5"
      },
      {
       "name": "L4"
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
       "name": "L5"
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
       "name": "L5"
      },
      {
       "name": "H1"
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
       "name": "L3"
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
       "name": "H2"
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
       "name": "H2"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     140,
     194,
     215,
     98,
     56
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
    "type": "winInfo",
    "totalWin": 10,
    "wins": [
     {
      "symbol": "L5",
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
       "lineIndex": 19,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 10
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 10
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.1,
  "freeGameWins": 0.0
 },
 {
  "id": 80,
  "payoutMultiplier": 30,
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
       "name": "S",
       "scatter": true
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
       "name": "H4"
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
       "name": "H4"
      },
      {
       "name": "L1"
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
       "name": "H3"
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
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     38,
     115,
     172,
     195,
     215
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
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L5",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 4,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
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
        "row": 4
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 12,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 22,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "type": "finalWin",
    "amount": 30
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.3,
  "freeGameWins": 0.0
 },
 {
  "id": 81,
  "payoutMultiplier": 0,
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
       "name": "H4"
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
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L4"
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
       "name": "L4"
      },
      {
       "name": "H3"
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
       "name": "H4"
      },
      {
       "name": "L3"
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
     ]
    ],
    "paddingPositions": [
     42,
     174,
     66,
     40,
     195
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 82,
  "payoutMultiplier": 30,
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
       "name": "L4"
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
       "name": "L3"
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
       "name": "H2"
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
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
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
       "name": "L5"
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
     21,
     209,
     13,
     105,
     39
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
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 30,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 1,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "type": "finalWin",
    "amount": 30
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.3,
  "freeGameWins": 0.0
 },
 {
  "id": 83,
  "payoutMultiplier": 0,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
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
       "name": "H3"
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
       "name": "L4"
      },
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
       "name": "L1"
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
       "name": "H3"
      },
      {
       "name": "H1"
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
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     198,
     9,
     125,
     1,
     133
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 84,
  "payoutMultiplier": 400,
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
       "name": "H3"
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
       "name": "L5"
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
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L5"
      },
      {
       "name": "L5"
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
       "name": "H1"
      },
      {
       "name": "L5"
      },
      {
       "name": "H1"
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
     ]
    ],
    "paddingPositions": [
     137,
     57,
     198,
     175,
     150
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
    "type": "winInfo",
    "totalWin": 400,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 200,
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
       }
      ],
      "meta": {
       "lineIndex": 30,
       "multiplier": 1,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H3",
      "kind": 3,
      "win": 200,
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
       }
      ],
      "meta": {
       "lineIndex": 45,
       "multiplier": 1,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 400,
    "winLevel": 4
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 400
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 400
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 4.0,
  "freeGameWins": 0.0
 },
 {
  "id": 85,
  "payoutMultiplier": 0,
  "events": [
   {
    "index": 0,
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
       "name": "L2"
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
       "name": "L4"
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
       "name": "L5"
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
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L3"
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
       "name": "H3"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     184,
     209,
     96,
     26,
     129
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 86,
  "payoutMultiplier": 0,
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
       "name": "H1"
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
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "L4"
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
       "name": "H1"
      },
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
       "name": "H1"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "H4"
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
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     48,
     214,
     208,
     138,
     26
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 87,
  "payoutMultiplier": 30,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
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
       "name": "L5"
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
       "name": "L1"
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
       "name": "L4"
      },
      {
       "name": "H3"
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
       "name": "H3"
      },
      {
       "name": "H1"
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
       "name": "L3"
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
     ]
    ],
    "paddingPositions": [
     176,
     35,
     154,
     44,
     113
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
    "type": "winInfo",
    "totalWin": 30,
    "wins": [
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
        "row": 4
       },
       {
        "reel": 2,
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 12,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       }
      ],
      "meta": {
       "lineIndex": 15,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
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
    "type": "finalWin",
    "amount": 30
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.3,
  "freeGameWins": 0.0
 },
 {
  "id": 88,
  "payoutMultiplier": 0,
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
       "name": "H1"
      },
      {
       "name": "L4"
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
       "name": "L1"
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
       "name": "H4"
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
       "name": "L3"
      },
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
       "name": "L5"
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
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     155,
     180,
     66,
     35,
     88
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 89,
  "payoutMultiplier": 100,
  "events": [
   {
    "index": 0,
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
       "name": "L5"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "L4"
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
       "name": "S",
       "scatter": true
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
       "name": "H3"
      },
      {
       "name": "H3"
      },
      {
       "name": "L5"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "H1"
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
     ]
    ],
    "paddingPositions": [
     23,
     123,
     168,
     147,
     150
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
    "type": "winInfo",
    "totalWin": 100,
    "wins": [
     {
      "symbol": "L1",
      "kind": 3,
      "win": 50,
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
       "lineIndex": 10,
       "multiplier": 1,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L1",
      "kind": 3,
      "win": 50,
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
       "lineIndex": 28,
       "multiplier": 1,
       "winWithoutMult": 50,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 100,
    "winLevel": 3
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 100
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 100
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 1.0,
  "freeGameWins": 0.0
 },
 {
  "id": 90,
  "payoutMultiplier": 0,
  "events": [
   {
    "index": 0,
    "type": "reveal",
    "board": [
     [
      {
       "name": "H3"
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
       "name": "L3"
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
       "name": "L4"
      },
      {
       "name": "H4"
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
       "name": "H2"
      },
      {
       "name": "H4"
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
      },
      {
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     196,
     212,
     22,
     204,
     174
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 91,
  "payoutMultiplier": 200,
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
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
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
       "name": "L5"
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
       "name": "H1"
      },
      {
       "name": "L4"
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
       "name": "H1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "L3"
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
     172,
     195,
     207,
     24,
     145
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
    "type": "winInfo",
    "totalWin": 200,
    "wins": [
     {
      "symbol": "L4",
      "kind": 5,
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
        "row": 4
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
       "lineIndex": 47,
       "multiplier": 1,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 200,
    "winLevel": 4
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 200
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 200
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 2.0,
  "freeGameWins": 0.0
 },
 {
  "id": 92,
  "payoutMultiplier": 0,
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
       "name": "H1"
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
       "name": "L2"
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
       "name": "L2"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
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
       "name": "L5"
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
       "name": "H4"
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
       "name": "H4"
      },
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
      }
     ]
    ],
    "paddingPositions": [
     126,
     144,
     185,
     90,
     29
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 93,
  "payoutMultiplier": 20,
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H3"
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
       "name": "H1"
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
       "name": "L2"
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
       "name": "L2"
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
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L3"
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
     111,
     3,
     190,
     111,
     91
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L4",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 14,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 20
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.2,
  "freeGameWins": 0.0
 },
 {
  "id": 94,
  "payoutMultiplier": 60,
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
       "name": "H4"
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
       "name": "L4"
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
       "name": "H4"
      },
      {
       "name": "L3"
      }
     ]
    ],
    "paddingPositions": [
     71,
     190,
     203,
     99,
     95
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
    "type": "winInfo",
    "totalWin": 60,
    "wins": [
     {
      "symbol": "L4",
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
       "lineIndex": 4,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
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
        "row": 3
       }
      ],
      "meta": {
       "lineIndex": 16,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L4",
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
       "lineIndex": 22,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
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
        "row": 2
       }
      ],
      "meta": {
       "lineIndex": 44,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 60,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 60
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 60
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.6,
  "freeGameWins": 0.0
 },
 {
  "id": 95,
  "payoutMultiplier": 2000,
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
       "name": "L4"
      },
      {
       "name": "L5"
      },
      {
       "name": "L5"
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
       "name": "H1"
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
       "name": "L1"
      },
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
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L5"
      },
      {
       "name": "H1"
      },
      {
       "name": "L4"
      },
      {
       "name": "H2"
      }
     ]
    ],
    "paddingPositions": [
     172,
     101,
     52,
     24,
     209
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
    "type": "winInfo",
    "totalWin": 2000,
    "wins": [
     {
      "symbol": "H1",
      "kind": 4,
      "win": 2000,
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
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 1,
       "winWithoutMult": 2000,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 2000,
    "winLevel": 6
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 2000
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 2000
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 20.0,
  "freeGameWins": 0.0
 },
 {
  "id": 96,
  "payoutMultiplier": 0,
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
       "name": "H2"
      },
      {
       "name": "L2"
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
       "name": "H4"
      },
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
       "name": "L5"
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
       "name": "H3"
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "L2"
      },
      {
       "name": "H4"
      },
      {
       "name": "H4"
      },
      {
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     208,
     69,
     94,
     6,
     18
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
    "type": "setTotalWin",
    "amount": 0
   },
   {
    "index": 2,
    "type": "finalWin",
    "amount": 0
   }
  ],
  "criteria": "0",
  "baseGameWins": 0.0,
  "freeGameWins": 0.0
 },
 {
  "id": 97,
  "payoutMultiplier": 2240,
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
       "name": "L1"
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
       "name": "H2"
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
     ]
    ],
    "paddingPositions": [
     7,
     49,
     72,
     212,
     69
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
     {
      "symbol": "L5",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 4,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
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
        "row": 4
       }
      ],
      "meta": {
       "lineIndex": 22,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 20
   },
   {
    "index": 4,
    "type": "freeSpinTrigger",
    "totalFs": 8,
    "positions": [
     {
      "reel": 0,
      "row": 3
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
       "name": "L5"
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
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "H4"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     45,
     145,
     128,
     48,
     68
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
    "type": "winInfo",
    "totalWin": 420,
    "wins": [
     {
      "symbol": "L4",
      "kind": 3,
      "win": 400,
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
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 20,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 20
      }
     },
     {
      "symbol": "L4",
      "kind": 3,
      "win": 20,
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
       "lineIndex": 40,
       "multiplier": 1,
       "winWithoutMult": 20,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 8,
    "type": "setWin",
    "amount": 420,
    "winLevel": 4
   },
   {
    "index": 9,
    "type": "setTotalWin",
    "amount": 440
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
       "name": "L4"
      },
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
       "name": "L5"
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
       "name": "L4"
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
       "name": "H2"
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
       "name": "H1"
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
       "name": "H2"
      },
      {
       "name": "H3"
      },
      {
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 50
      }
     ]
    ],
    "paddingPositions": [
     40,
     98,
     40,
     80,
     126
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
    "type": "winInfo",
    "totalWin": 20,
    "wins": [
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
       "lineIndex": 8,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
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
       "lineIndex": 23,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 13,
    "type": "setWin",
    "amount": 20,
    "winLevel": 2
   },
   {
    "index": 14,
    "type": "setTotalWin",
    "amount": 460
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
       "name": "L4"
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
       "name": "L4"
      },
      {
       "name": "H4"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L2"
      },
      {
       "name": "L2"
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
       "name": "H2"
      },
      {
       "name": "L1"
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
       "name": "L1"
      },
      {
       "name": "H4"
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
     ]
    ],
    "paddingPositions": [
     47,
     11,
     114,
     182,
     125
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
    "type": "winInfo",
    "totalWin": 360,
    "wins": [
     {
      "symbol": "L2",
      "kind": 3,
      "win": 90,
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
       "lineIndex": 10,
       "multiplier": 3,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 90,
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
       }
      ],
      "meta": {
       "lineIndex": 20,
       "multiplier": 3,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 90,
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
       "lineIndex": 28,
       "multiplier": 3,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     },
     {
      "symbol": "L2",
      "kind": 3,
      "win": 90,
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
       "lineIndex": 40,
       "multiplier": 3,
       "winWithoutMult": 30,
       "globalMult": 1,
       "lineMultiplier": 3
      }
     }
    ]
   },
   {
    "index": 18,
    "type": "setWin",
    "amount": 360,
    "winLevel": 4
   },
   {
    "index": 19,
    "type": "setTotalWin",
    "amount": 820
   },
   {
    "index": 20,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 8
   },
   {
    "index": 21,
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
       "name": "L2"
      },
      {
       "name": "H2"
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
       "name": "L2"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
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
       "name": "L1"
      },
      {
       "name": "L2"
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
       "name": "H3"
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
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     3,
     138,
     15,
     136,
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
    "index": 22,
    "type": "setTotalWin",
    "amount": 820
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
       "name": "L3"
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
       "name": "L2"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 20
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
       "name": "H1"
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
       "name": "H1"
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
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L2"
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
       "name": "L4"
      },
      {
       "name": "H3"
      }
     ]
    ],
    "paddingPositions": [
     10,
     31,
     155,
     8,
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
    "index": 25,
    "type": "setTotalWin",
    "amount": 820
   },
   {
    "index": 26,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 8
   },
   {
    "index": 27,
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
       "name": "L3"
      },
      {
       "name": "L1"
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
       "name": "H4"
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
       "name": "H4"
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
       "name": "L4"
      },
      {
       "name": "H2"
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
       "name": "H1"
      }
     ]
    ],
    "paddingPositions": [
     8,
     97,
     188,
     185,
     175
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
    "type": "winInfo",
    "totalWin": 220,
    "wins": [
     {
      "symbol": "H4",
      "kind": 3,
      "win": 100,
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
       }
      ],
      "meta": {
       "lineIndex": 9,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 10,
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
       }
      ],
      "meta": {
       "lineIndex": 18,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H4",
      "kind": 3,
      "win": 100,
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
       }
      ],
      "meta": {
       "lineIndex": 27,
       "multiplier": 1,
       "winWithoutMult": 100,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "L5",
      "kind": 3,
      "win": 10,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 29,
    "type": "setWin",
    "amount": 220,
    "winLevel": 4
   },
   {
    "index": 30,
    "type": "setTotalWin",
    "amount": 1040
   },
   {
    "index": 31,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 8
   },
   {
    "index": 32,
    "type": "reveal",
    "board": [
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
       "name": "L4"
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
       "name": "H3"
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
       "name": "H1"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
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
       "name": "H1"
      },
      {
       "name": "H2"
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
       "name": "H3"
      },
      {
       "name": "H4"
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
     ]
    ],
    "paddingPositions": [
     167,
     3,
     84,
     146,
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
    "index": 33,
    "type": "setTotalWin",
    "amount": 1040
   },
   {
    "index": 34,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 8
   },
   {
    "index": 35,
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
       "name": "L5"
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
       "name": "H4"
      },
      {
       "name": "H1"
      },
      {
       "name": "H2"
      },
      {
       "name": "H1"
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
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 3
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
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
       "name": "L1"
      },
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
       "name": "H2"
      },
      {
       "name": "H3"
      }
     ],
     [
      {
       "name": "W",
       "wild": true,
       "multiplier": 2
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 4
      },
      {
       "name": "L1"
      },
      {
       "name": "H3"
      },
      {
       "name": "H2"
      },
      {
       "name": "H4"
      }
     ]
    ],
    "paddingPositions": [
     108,
     169,
     54,
     173,
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
    "index": 36,
    "type": "wildNudge",
    "reel": 2,
    "nudges": 1,
    "multiplier": 2,
    "finalReel": [
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     },
     {
      "name": "W",
      "wild": true,
      "multiplier": 2
     }
    ]
   },
   {
    "index": 37,
    "type": "winInfo",
    "totalWin": 1200,
    "wins": [
     {
      "symbol": "H2",
      "kind": 3,
      "win": 600,
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
       }
      ],
      "meta": {
       "lineIndex": 34,
       "multiplier": 2,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 600,
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
       }
      ],
      "meta": {
       "lineIndex": 38,
       "multiplier": 2,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 2
      }
     }
    ]
   },
   {
    "index": 38,
    "type": "setWin",
    "amount": 1200,
    "winLevel": 5
   },
   {
    "index": 39,
    "type": "setTotalWin",
    "amount": 2240
   },
   {
    "index": 40,
    "type": "freeSpinEnd",
    "amount": 2220,
    "winLevel": 5
   },
   {
    "index": 41,
    "type": "finalWin",
    "amount": 2240
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.2,
  "freeGameWins": 22.2
 },
 {
  "id": 98,
  "payoutMultiplier": 10,
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
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
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
       "name": "L1"
      },
      {
       "name": "H1"
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
       "name": "L5"
      },
      {
       "name": "H2"
      },
      {
       "name": "H2"
      },
      {
       "name": "L3"
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
       "name": "L3"
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
     ]
    ],
    "paddingPositions": [
     51,
     153,
     45,
     58,
     63
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
    "type": "winInfo",
    "totalWin": 10,
    "wins": [
     {
      "symbol": "L5",
      "kind": 3,
      "win": 10,
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
       }
      ],
      "meta": {
       "lineIndex": 42,
       "multiplier": 1,
       "winWithoutMult": 10,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 10,
    "winLevel": 2
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 10
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 10
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 0.1,
  "freeGameWins": 0.0
 },
 {
  "id": 99,
  "payoutMultiplier": 500,
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
       "name": "H2"
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
       "name": "H2"
      },
      {
       "name": "H3"
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
       "name": "H1"
      },
      {
       "name": "L3"
      },
      {
       "name": "W",
       "wild": true,
       "multiplier": 1
      },
      {
       "name": "L1"
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
       "name": "L3"
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
       "name": "H1"
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
       "name": "H3"
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
     ]
    ],
    "paddingPositions": [
     204,
     28,
     136,
     31,
     20
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
    "type": "winInfo",
    "totalWin": 500,
    "wins": [
     {
      "symbol": "H3",
      "kind": 3,
      "win": 200,
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
       "lineIndex": 37,
       "multiplier": 1,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     },
     {
      "symbol": "H2",
      "kind": 3,
      "win": 300,
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
       "lineIndex": 44,
       "multiplier": 1,
       "winWithoutMult": 300,
       "globalMult": 1,
       "lineMultiplier": 1
      }
     }
    ]
   },
   {
    "index": 2,
    "type": "setWin",
    "amount": 500,
    "winLevel": 5
   },
   {
    "index": 3,
    "type": "setTotalWin",
    "amount": 500
   },
   {
    "index": 4,
    "type": "finalWin",
    "amount": 500
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 5.0,
  "freeGameWins": 0.0
 }
];
