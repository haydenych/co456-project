# CO456 Project

## Instructions

```
cd antichess
python3 main.py {white / black}
```

## Techniques

- Minimax with alpha-beta pruning.

- Decrease search depth as it gets near the time allowance.

- Increase search depth on specific branches with limited moves (<= 2), this is because feasible moves are usually restricted to captures in anti-chess.

## Using Docker

```
docker build -t co456 .
docker run -it --name co456 co456
python3 main.py {white / black}
```

## Results

Ranked 2/36 in an in-class Swiss Tournament.
Please check out this [link](https://djao.math.uwaterloo.ca/co456/standing.html) for more information.
