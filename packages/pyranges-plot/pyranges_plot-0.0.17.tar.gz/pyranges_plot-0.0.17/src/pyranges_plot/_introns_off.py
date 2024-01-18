

def _gby_apply_next_int_col(df, margin=1, threshold=None):
    """
    Sort the data, create next intron size column for each exon and where is the intron flexible.
    - ["where_flexible"]: -1(last exon), -2(small exon), ( , )(large shrinkable coordinates)
    """
    if threshold is None:
        threshold = 2 * margin
    # Sort rows
    df = df.sort_values(by=['transcript_id', 'Start'])

    # Create next_intron_size and where_flexible column
    introns = []
    where_flex = []
    for i in range(len(df)):
        # last exon has no next intron, fill and skip
        if i == len(df) - 1:
            introns.append('last')
            where_flex.append(-1)
            continue

        # calculate and evaluate next intron size
        nint_len = df.Start.iloc[i + 1] - df.End.iloc[i]
        introns.append(nint_len)
        if nint_len > threshold:
            where_flex.append((df.End.iloc[i] + margin, df.Start.iloc[i + 1] - margin))
        else:
            where_flex.append(-2)

    # Add data
    df["where_flexible"] = where_flex
    df["next_intron_size"] = introns

    return (df)


def _apply_is_flexible(df):
    """Evaluate where_flexible column."""

    if not isinstance(df.where_flexible, int):
        return True
    else:
        return False


def recurs_interval_comparison(df, flex_interval):
    """Compare and determine where i and j are really flexible considering all data"""

    # The interval has been splitted, evaluate both individually
    if isinstance(flex_interval, list):
        return [recurs_interval_comparison(df, flex_interval[0]), recurs_interval_comparison(df, flex_interval[1])]

    # Store FLEXIBLE coordinates to evaluate (1 interval)
    i, j = flex_interval

    # Iterate over NON-FLEXIBLE intervals and compare with flexible (all data intervals)
    for infl_i, infl_j in df["where_not_flexible"]:

        # non-flexible interval inside the flexible interval
        if i < infl_i and j > infl_j:
            # divide flexible interval to avoid non-flexible region
            i1 = i
            j1 = infl_i
            i2 = infl_j
            j2 = j
            # evaluate both subintervals separately
            flex_interval = [recurs_interval_comparison(df, (i1, j1)), recurs_interval_comparison(df, (i2, j2))]
            break

        # first flexible coordinate (i) inside non-flexible interval
        elif i > infl_i and i < infl_j:

            if j > infl_j:  # a) second coordinate is outside
                i = infl_j  # first one moves to non-flexible border
                flex_interval = (i, j)

            else:  # b) second coordinate also inside non-flexible interval
                flex_interval = -2  # becomes non-flexible

        # second flexible coordinate (j) inside non-flexible interval
        elif j > infl_i and j < infl_j:

            if i < infl_i:  # a) first coordinate is outside
                j = infl_i  # second one moves to non-flexible border
                flex_interval = (i, j)
            ##repeated
            else:  # b) first coordinate also inside non-flexible interval
                flex_interval = -2  # becomes non-flexible


        else:
            # ?? marcar de alguna manera los que no se cruzan para no compararlos de nuevo??
            # i>inlf_j / j<infl_i
            continue

    # If the result is a list of nested flexible intervals, flatten it
    def flatten_list(nested_list):
        flatl = []
        for item in nested_list:
            if isinstance(item, list):
                flatl.extend(flatten_list(item))
            else:
                flatl.append(item)
        return flatl

    if isinstance(flex_interval, list):
        flex_interval = flatten_list(flex_interval)

    return flex_interval


def _gby_get_shrinkable(df):
    """Include information in df for flexible/shrinkable regions."""

    eval_flex = df.loc[df["is_flexible"] == True, 'where_flexible']

    # por cada intervalo flexible
    for n in range(len(eval_flex)):
        eval_flex.iloc[n] = recurs_interval_comparison(df, eval_flex.iloc[n])

    df.loc[df["is_flexible"] == True, 'where_flexible'] = eval_flex
    return df


def _gby_apply_intron_shrink(df):
    """Update data coordinates according to calculated flexible regions."""

    # If there are flexible regions
    if df.is_flexible.any():  # some parts of the gene can be shrinked.
        # start accumulation
        acc = 0

        def get_accumulation(interv, acc):
            """Calculate shrink distance and accumulate it"""

            if isinstance(interv, tuple):
                shrink = interv[1] - interv[0]
                acc += shrink

            elif isinstance(interv, list):
                for subint in interv:
                    acc = get_accumulation(subint, acc)

            return acc

        # evaluate each exon
        for i in range(len(df) - 1):
            df.End.iloc[i] -= acc  # adjust exon's end
            acc = get_accumulation(df["where_flexible"].iloc[i], acc) # update accumulation
            df.Start.iloc[i + 1] -= acc  # adjust next exon's start

        df.End.iloc[-1] -= acc  # adjust last exon's end

        return (df)

    else:
        return (df)



def introns_off(df, margin = None, threshold = None):

    # Define margin and threshold
    if margin is None:
        margin = 1

    if threshold is None:
        threshold = 2 * margin

    # Start needed columns
    df["where_not_flexible"] = list(zip(df.Start - margin, df.End + margin))
    df["next_intron_size"] = [0] * len(df)
    df["where_flexible"] = [0] * len(df)
    df["is_flexible"] = [0] * len(df)

    # Calculate next intron for each exon and determine if it can be shrinked/flexible (> threshold)
    df = df.groupby('transcript_id').apply(lambda df: _gby_apply_next_int_col(df, margin, threshold))
    df = df.reset_index(level="transcript_id", drop=True)
    df["is_flexible"] = df.apply(_apply_is_flexible, axis=1)

    # Compare flexible and not flexible intervals and determine if they are truly flexible
    df = df.groupby("Chromosome").apply(_gby_get_shrinkable)
    df = df.reset_index(level="Chromosome", drop=True)
    df["is_flexible"] = df.apply(_apply_is_flexible, axis=1)

    # Update coordinates
    df = df.groupby("transcript_id").apply(_gby_apply_intron_shrink)
    df = df.reset_index(level="transcript_id", drop=True)

    return df



