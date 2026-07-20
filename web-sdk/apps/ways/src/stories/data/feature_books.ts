// Real math-engine books for the new bet modes, extracted from the smoke run:
// [0] ante (guaranteed reel-1 scatter, triggers the bonus)
// [1] feature1 MIRROR SPIN (1 guaranteed mirror)
// [2] feature2 TWIN MIRRORS (2 guaranteed mirrors)
// [3] feature3 TRIPLE MIRRORS (3 guaranteed mirrors)
export default [
 {
  "id": 1877,
  "payoutMultiplier": 1700,
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
       "name": "H1"
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
       "name": "H5"
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
       "name": "L4"
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
       "name": "H3"
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
     ]
    ],
    "paddingPositions": [
     115,
     245,
     38,
     244,
     51
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
    "totalWin": 40,
    "wins": [
     {
      "symbol": "L3",
      "kind": 3,
      "win": 40,
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
        "row": 1
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
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 40,
       "symbolMult": 0
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
    "type": "freeSpinTrigger",
    "totalFs": 8,
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
      "reel": 4,
      "row": 3
     }
    ]
   },
   {
    "index": 5,
    "type": "bonusLevel",
    "level": 1,
    "name": "THE_SEANCE",
    "startHaunted": []
   },
   {
    "index": 6,
    "type": "updateFreeSpin",
    "amount": 0,
    "total": 8
   },
   {
    "index": 7,
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
       "name": "H4"
      },
      {
       "name": "H4"
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
       "name": "W",
       "wild": true
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
       "name": "H4"
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
       "name": "H4"
      },
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
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     72,
     184,
     6,
     7,
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
    "index": 8,
    "type": "setTotalWin",
    "amount": 40
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
       "name": "L1"
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
       "name": "L1"
      },
      {
       "name": "L4"
      },
      {
       "name": "W",
       "wild": true
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
       "name": "L4"
      },
      {
       "name": "H4"
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
     80,
     158,
     181,
     0,
     184
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
    "type": "winInfo",
    "totalWin": 300,
    "wins": [
     {
      "symbol": "H4",
      "kind": 5,
      "win": 300,
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
        "row": 3
       }
      ],
      "meta": {
       "ways": 1,
       "globalMult": 1,
       "winWithoutMult": 300,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 12,
    "type": "setWin",
    "amount": 300,
    "winLevel": 4
   },
   {
    "index": 13,
    "type": "setTotalWin",
    "amount": 340
   },
   {
    "index": 14,
    "type": "freeSpinRetrigger",
    "totalFs": 11,
    "positions": [
     {
      "reel": 0,
      "row": 4
     },
     {
      "reel": 1,
      "row": 1
     }
    ]
   },
   {
    "index": 15,
    "type": "updateFreeSpin",
    "amount": 2,
    "total": 11
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
       "name": "L2"
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
       "name": "L3"
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
       "name": "L1"
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
       "name": "L5"
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
       "name": "H1"
      },
      {
       "name": "L4"
      }
     ]
    ],
    "paddingPositions": [
     191,
     30,
     190,
     203,
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
    "index": 17,
    "type": "winInfo",
    "totalWin": 320,
    "wins": [
     {
      "symbol": "L4",
      "kind": 5,
      "win": 320,
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
        "row": 1
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
        "row": 1
       },
       {
        "reel": 4,
        "row": 3
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
    "index": 18,
    "type": "setWin",
    "amount": 320,
    "winLevel": 4
   },
   {
    "index": 19,
    "type": "setTotalWin",
    "amount": 660
   },
   {
    "index": 20,
    "type": "updateFreeSpin",
    "amount": 3,
    "total": 11
   },
   {
    "index": 21,
    "type": "reveal",
    "board": [
     [
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
       "name": "L2"
      }
     ]
    ],
    "paddingPositions": [
     27,
     193,
     38,
     31,
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
    "index": 22,
    "type": "setTotalWin",
    "amount": 660
   },
   {
    "index": 23,
    "type": "updateFreeSpin",
    "amount": 4,
    "total": 11
   },
   {
    "index": 24,
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
       "name": "L1"
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
       "name": "L4"
      },
      {
       "name": "H5"
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
       "name": "L2"
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
       "name": "L5"
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
     ]
    ],
    "paddingPositions": [
     223,
     176,
     50,
     0,
     170
    ],
    "gameType": "freegame",
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
    "amount": 660
   },
   {
    "index": 26,
    "type": "updateFreeSpin",
    "amount": 5,
    "total": 11
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
       "name": "H4"
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
       "name": "H5"
      },
      {
       "name": "H1"
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
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     170,
     161,
     228,
     210,
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
    "index": 28,
    "type": "setTotalWin",
    "amount": 660
   },
   {
    "index": 29,
    "type": "updateFreeSpin",
    "amount": 6,
    "total": 11
   },
   {
    "index": 30,
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
       "name": "H2"
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
       "name": "W",
       "wild": true
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
       "name": "L5"
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
       "name": "H5"
      },
      {
       "name": "L1"
      },
      {
       "name": "H5"
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
     78,
     79,
     126,
     6,
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
    "index": 31,
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
        "reel": 4,
        "row": 1,
        "apparitions": 2,
        "ttl": 1
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 4,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "H2"
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
        "apparitions": 2,
        "ttl": 1
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 2,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "L1"
      }
     }
    ],
    "totalWays": 5000
   },
   {
    "index": 32,
    "type": "setTotalWin",
    "amount": 660
   },
   {
    "index": 33,
    "type": "updateFreeSpin",
    "amount": 7,
    "total": 11
   },
   {
    "index": 34,
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
       "name": "L2"
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
       "name": "H5"
      },
      {
       "name": "H2"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H4"
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
       "name": "H1"
      },
      {
       "name": "H4"
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
     ]
    ],
    "paddingPositions": [
     156,
     66,
     211,
     196,
     229
    ],
    "gameType": "freegame",
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
       "row": 2
      },
      "reflected": [
       {
        "reel": 0,
        "row": 3,
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
        "reel": 0,
        "row": 2,
        "apparitions": 3,
        "ttl": 1
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 4,
        "ttl": 1
       }
      ],
      "mirrorBecomes": {
       "name": "H1"
      }
     }
    ],
    "totalWays": 6048
   },
   {
    "index": 36,
    "type": "winInfo",
    "totalWin": 960,
    "wins": [
     {
      "symbol": "H1",
      "kind": 3,
      "win": 800,
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
        "row": 4
       },
       {
        "reel": 2,
        "row": 3
       }
      ],
      "meta": {
       "ways": 8,
       "globalMult": 1,
       "winWithoutMult": 800,
       "symbolMult": 0
      }
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 160,
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
        "reel": 3,
        "row": 3
       }
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 160,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 37,
    "type": "setWin",
    "amount": 960,
    "winLevel": 5
   },
   {
    "index": 38,
    "type": "setTotalWin",
    "amount": 1620
   },
   {
    "index": 39,
    "type": "updateFreeSpin",
    "amount": 8,
    "total": 11
   },
   {
    "index": 40,
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
       "name": "L1"
      },
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
       "name": "L1"
      },
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
       "name": "H5"
      }
     ]
    ],
    "paddingPositions": [
     162,
     41,
     169,
     74,
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
    "index": 41,
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
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 80,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 42,
    "type": "setWin",
    "amount": 80,
    "winLevel": 2
   },
   {
    "index": 43,
    "type": "setTotalWin",
    "amount": 1700
   },
   {
    "index": 44,
    "type": "updateFreeSpin",
    "amount": 9,
    "total": 11
   },
   {
    "index": 45,
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
       "name": "L2"
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
       "name": "W",
       "wild": true
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
       "name": "H5"
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
       "name": "H5"
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
       "name": "H4"
      },
      {
       "name": "H2"
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
     29,
     184,
     85,
     14,
     25
    ],
    "gameType": "freegame",
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
    "type": "setTotalWin",
    "amount": 1700
   },
   {
    "index": 47,
    "type": "updateFreeSpin",
    "amount": 10,
    "total": 11
   },
   {
    "index": 48,
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
       "name": "H2"
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
       "name": "H2"
      },
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
       "name": "L3"
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
       "name": "L4"
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
     ]
    ],
    "paddingPositions": [
     154,
     59,
     178,
     138,
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
    "index": 49,
    "type": "setTotalWin",
    "amount": 1700
   },
   {
    "index": 50,
    "type": "freeSpinEnd",
    "amount": 1660,
    "winLevel": 4
   },
   {
    "index": 51,
    "type": "finalWin",
    "amount": 1700
   }
  ],
  "criteria": "freegame",
  "baseGameWins": 0.4,
  "freeGameWins": 16.6
 },
 {
  "id": 89,
  "payoutMultiplier": 1440,
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
       "name": "S",
       "scatter": true
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
       "name": "H3"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "ME",
       "eye": true
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
       "name": "L3"
      },
      {
       "name": "L3"
      },
      {
       "name": "H5"
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
     }
    ]
   },
   {
    "index": 3,
    "type": "winInfo",
    "totalWin": 1440,
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
        "reel": 1,
        "row": 4
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
        "row": 2
       }
      ],
      "meta": {
       "ways": 12,
       "globalMult": 1,
       "winWithoutMult": 960,
       "symbolMult": 2
      }
     },
     {
      "symbol": "L5",
      "kind": 5,
      "win": 480,
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
        "reel": 3,
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
       "ways": 6,
       "globalMult": 1,
       "winWithoutMult": 480,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 4,
    "type": "setWin",
    "amount": 1440,
    "winLevel": 5
   },
   {
    "index": 5,
    "type": "setTotalWin",
    "amount": 1440
   },
   {
    "index": 6,
    "type": "finalWin",
    "amount": 1440
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 14.4,
  "freeGameWins": 0.0
 },
 {
  "id": 526,
  "payoutMultiplier": 3100,
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
       "name": "W",
       "wild": true
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
     238,
     111,
     201,
     86,
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
        "row": 2,
        "apparitions": 4
       },
       {
        "reel": 3,
        "row": 3,
        "apparitions": 2
       },
       {
        "reel": 3,
        "row": 4,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "W"
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
        "apparitions": 4
       },
       {
        "reel": 2,
        "row": 2,
        "apparitions": 4
       },
       {
        "reel": 4,
        "row": 2,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "L1"
      }
     }
    ],
    "totalWays": 6720
   },
   {
    "index": 2,
    "type": "winInfo",
    "totalWin": 3100,
    "wins": [
     {
      "symbol": "L5",
      "kind": 5,
      "win": 2400,
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
        "reel": 3,
        "row": 3
       },
       {
        "reel": 4,
        "row": 2
       }
      ],
      "meta": {
       "ways": 30,
       "globalMult": 1,
       "winWithoutMult": 2400,
       "symbolMult": 2
      }
     },
     {
      "symbol": "L3",
      "kind": 4,
      "win": 540,
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
        "row": 4
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
     },
     {
      "symbol": "L2",
      "kind": 4,
      "win": 160,
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
      ],
      "meta": {
       "ways": 4,
       "globalMult": 1,
       "winWithoutMult": 160,
       "symbolMult": 2
      }
     }
    ]
   },
   {
    "index": 3,
    "type": "setWin",
    "amount": 3100,
    "winLevel": 7
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 3100
   },
   {
    "index": 5,
    "type": "finalWin",
    "amount": 3100
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 31.0,
  "freeGameWins": 0.0
 },
 {
  "id": 37,
  "payoutMultiplier": 4320,
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
       "name": "L4"
      },
      {
       "name": "L1"
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
       "name": "L4"
      },
      {
       "name": "HM",
       "mirror": true
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
       "name": "L2"
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
       "name": "H3"
      },
      {
       "name": "HM",
       "mirror": true
      },
      {
       "name": "H1"
      },
      {
       "name": "H5"
      },
      {
       "name": "W",
       "wild": true
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
    "type": "mirrorBurst",
    "mirrors": [
     {
      "mirror": {
       "reel": 3,
       "row": 1
      },
      "reflected": [
       {
        "reel": 4,
        "row": 2,
        "apparitions": 4
       },
       {
        "reel": 4,
        "row": 1,
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
     },
     {
      "mirror": {
       "reel": 1,
       "row": 2
      },
      "reflected": [
       {
        "reel": 1,
        "row": 1,
        "apparitions": 2
       },
       {
        "reel": 0,
        "row": 1,
        "apparitions": 2
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 3
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
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 0,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 2,
        "row": 3,
        "apparitions": 3
       },
       {
        "reel": 0,
        "row": 4,
        "apparitions": 2
       },
       {
        "reel": 1,
        "row": 3,
        "apparitions": 3
       }
      ],
      "mirrorBecomes": {
       "name": "L1"
      }
     }
    ],
    "totalWays": 14336
   },
   {
    "index": 2,
    "type": "winInfo",
    "totalWin": 4320,
    "wins": [
     {
      "symbol": "L1",
      "kind": 5,
      "win": 4320,
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
        "row": 2
       }
      ],
      "meta": {
       "ways": 36,
       "globalMult": 1,
       "winWithoutMult": 4320,
       "symbolMult": 0
      }
     }
    ]
   },
   {
    "index": 3,
    "type": "setWin",
    "amount": 4320,
    "winLevel": 7
   },
   {
    "index": 4,
    "type": "setTotalWin",
    "amount": 4320
   },
   {
    "index": 5,
    "type": "finalWin",
    "amount": 4320
   }
  ],
  "criteria": "basegame",
  "baseGameWins": 43.2,
  "freeGameWins": 0.0
 }
];
