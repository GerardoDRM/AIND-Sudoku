assignments = []

# Get cross product between two elements
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]


rows = 'ABCDEFGHI'
cols = '123456789'
# Create boxes (string product)
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
# Define square units
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Define diagonal units
# Easiest way mix rows and cols on each position and then reverse cols string to get the other diagonal
diagonal_units = [[r+c for r,c in zip(rows, cols)], [r+c for r,c in zip(rows,cols[::-1])]]
# Define list units
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
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
    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return {boxes[idx]:data if data is not '.' else '123456789' for idx, data in enumerate(list(grid))}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    single_box = [i for i in values if len(values[i]) is 1 ]
    for s in single_box:
        d = values[s]
        for p in peers[s]:
            assign_value(values, p, values[p].replace(d, ''))
    return values

def only_choice(values):
    for unit in unitlist:
        for v in '123456789':
            d = [x for x in unit if v in values[x]]
            if len(d) is 1:
                assign_value(values, d[0], v)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Use naked twins Strategy
        values = naked_twins(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if not values:
        return False
    if all(len(values[x]) is 1 for x in values):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    node_k, node_v = min([(k,v) for k,v in values.items() if len(values[k]) > 1], key=lambda x:len(x[1]))
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for v in node_v:
        new_v = values.copy()
        new_v[node_k] = v

        tree = search(new_v)
        if tree:
            return tree

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
