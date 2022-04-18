from math import exp


def predict_turn(point):
    minmax = [
        [54.0, 784.0],
        [58.0, 1060.0],
        [298.0, 1361.0],
        [0.0, 21.2132034355964],
        [0, 1]
    ]

    network = [
        [
            {
                'weights': [
                    10.787467301389258,
                    -19.069534838411133,
                    -2.1616970686987877,
                    6.610362368882941,
                    0.022057666209446304
                ],
                'output': 0.08901430794962625,
                'delta': -0.0900064850167518
            },
            {
                'weights': [
                    -52.45606084078775,
                    69.89549698059389,
                    5.4949248493009355,
                    0.8218819992441782,
                    -3.536192196700494
                ],
                'output': 0.26184916625658633,
                'delta': 0.636840367621383
            },
            {
                'weights': [
                    72.2898866327055,
                    -97.00477281903295,
                    6.483413804260495,
                    -4.319407834555138,
                    -3.501469063744765
                ],
                'output': 0.5427443337900569,
                'delta': -0.9231380636379565
            },
            {
                'weights': [
                    -11.694009621310363,
                    3.5730064726602264,
                    5.637204850545952,
                    -5.6192157372095,
                    -2.965242334563364
                ],
                'output': 0.0011144659387273036,
                'delta': 0.0015058662659967448
            },
            {
                'weights': [
                    -36.003516329588706,
                    48.47180741983483,
                    -2.126870362914438,
                    -8.673875664265584,
                    2.759629686039794
                ],
                'output': 0.5280417828650562,
                'delta': 0.5500914693403068
            }
        ],
        [
            {
                'weights': [
                    -4.16283164927734,
                    12.432285188016873,
                    -14.103097711823388,
                    5.116802388267798,
                    8.334361200524993,
                    0.3774294946326948
                ],
                'output': 0.5308461540227336,
                'delta': 0.1322064462371017
            },
            {
                'weights': [
                    4.2468498257158585,
                    -12.461961555152643,
                    14.112273802325683,
                    -5.1176723745766175,
                    -8.296395334493134,
                    -0.4008640270318837
                ],
                'output': 0.46949280493819256,
                'delta': -0.1321330615808263
            }
        ]
    ]
    point = normalize_data([point], minmax)[0]
    outputs = forward_propagate(network, point)
    return outputs.index(max(outputs))


def normalize_data(data, minmax):
    for point in data:
        for i in range(len(point) - 1):
            point[i] = (point[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])

    return data


def forward_propagate(network, point):
    inp = point
    for layer in network:
        next_layer_inp = []

        for neuron in layer:
            activation = activate(neuron['weights'], inp)
            neuron['output'] = calculate_sigmoid(activation)
            next_layer_inp.append(neuron['output'])

        inp = next_layer_inp

    return inp


def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation


def calculate_sigmoid(activation):
    try:
        return 1.0 / (1.0 + exp(- activation))
    except Exception:
        return 0
