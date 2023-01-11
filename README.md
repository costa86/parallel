# Benchmarking joblib Python lib

Compares performance of reading a dataset using regular Python sync code vs using the `joblib` library (using parallelism).

Results:

    Regular execution using 5 rows
    (141, 144, 140)
    (140, 170, 194)
    (209, 201, 187)
    (208, 206, 206)
    (213, 215, 214)
    Took: 5.323754787445068

    Parallel execution using 5 rows
    (209, 201, 187)
    (208, 206, 206)
    (140, 170, 194)
    (213, 215, 214)
    (141, 144, 140)
    Took: 1.7356815338134766