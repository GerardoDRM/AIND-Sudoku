# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We use constraint propagation on naked twins as follows:

* First we get all possible twins candidates it means all units with length equals to 2
* Then we must guarantee that the candidates have a twin
* Then we get all twins regions to remove the twins values from units
* At the end we get the regions without naked twins

The  naked twins constraint ensures that units on a region can have only two options if a twin on the same region is presented

This function is complemented by iterating with "eliminate" and "only choice" strategies

```python
# Get all posible candidates
candidates = {k:v for k, v in values.items() if len(v) == 2}
for c,v in candidates.items():
    # Check if candidate has a twin
    same_values = [k for k,vs in candidates.items() if vs == v]
    # Get possible twins cells keys
    twins = list(set([k for k in same_values for k2 in same_values if k in peers[k2]]))
    # Remove value from units if it is a twin
    if len(twins) > 1:
        # Get all regions where twins are located
        boxes = []
        for t in twins:
            # Get region
            unit = [u for u in units[t] for i in twins if i in u and i!= t]
            if unit[0]:
                boxes.append(unit[0])
        # Remove twins value for each unit on region
        for box in boxes:
            for b in box:
                if values[b] != v:
                    assign_value(values, b, values[b].strip(v))
```


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We use constraint propagation on diagonal sudoku as follows:
* Getting the two diagonals presented on a matrix
* We get the first diagonal merging columns and rows with its related position
* The second diagonal is the same but with an inverse column

This is an additional unit in the sudoku.

```python
diagonal_units = [[r+c for r,c in zip(rows, cols)], [r+c for r,c in zip(rows,cols[::-1])]]
```

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

In order to run the solution
```bash
 $ python solution.py
```

In order to run the unittest
```bash
 $ python solution_test.py
```
