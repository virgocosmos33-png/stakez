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
     64,
     155,
     54,
     155,
     9
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
    "totalWin": 1600,
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
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 4
      }
     },
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
        "row": 1
       },
       {
        "reel": 2,
        "row": 1
       }
      ],
      "meta": {
       "lineIndex": 48,
       "multiplier": 4,
       "winWithoutMult": 200,
       "globalMult": 1,
       "lineMultiplier": 4
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
 }
];
