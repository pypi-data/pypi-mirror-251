def example(extract='m', estimate=False):
    import numpy as np
    from pytest import approx

    import larch as lx

    import larch as lx

    varnames = [
        "price",
        "time",
        "conven",
        "comfort",
        "meals",
        "petfr",
        "emipp",
        "nonsig1",
        "nonsig2",
        "nonsig3",
    ]
    d = lx.examples.ARTIFICIAL()
    m = lx.Model(d)
    m.utility_ca = sum(lx.PX(i) for i in varnames)
    m.choice_ca_var = "choice"
    randvars_normal = ["meals", "petfr", "emipp"]

    m.mixtures = [lx.mixtures.Normal(k, f"sd.{k}") for k in randvars_normal]

    m.n_draws = 300
    m.seed = 42
    m.prerolled = True
    m.common_draws = True

    # TEST
    assert m.d_loglike() == approx(
        [
            2.085461e03,
            -1.130608e03,
            -5.535062e03,
            1.998748e02,
            -3.927801e03,
            3.330141e03,
            -4.460615e03,
            -1.380896e03,
            -1.267620e03,
            -3.135025e00,
            -3.900630e00,
            -1.376858e00,
            -2.561676e03,
        ],
        rel=1e-4,
    )

    # TEST
    se, hess, ihess = m.jax_param_cov(m.pvals)
    assert hess == approx(
        np.array(
            [
                [
                    5.214861e03,
                    -8.737501e03,
                    -1.207186e04,
                    4.689243e03,
                    -4.701574e03,
                    2.698417e03,
                    -2.037047e03,
                    -6.022355e03,
                    -8.715623e03,
                    4.149471e00,
                    -1.291960e01,
                    -1.636162e-01,
                    2.693130e03,
                ],
                [
                    -8.737502e03,
                    1.918251e04,
                    2.199170e04,
                    -1.065871e04,
                    6.688360e03,
                    -2.722472e03,
                    4.219213e01,
                    1.198888e04,
                    1.867886e04,
                    5.044937e00,
                    2.636754e01,
                    8.628845e-01,
                    -8.679251e03,
                ],
                [
                    -1.207186e04,
                    2.199169e04,
                    3.128377e04,
                    -1.174997e04,
                    1.223288e04,
                    -7.146222e03,
                    5.618984e03,
                    1.528325e04,
                    2.193285e04,
                    -1.277624e01,
                    3.275142e01,
                    6.413689e-01,
                    -6.471689e03,
                ],
                [
                    4.689244e03,
                    -1.065871e04,
                    -1.174997e04,
                    6.683431e03,
                    -3.098420e03,
                    9.166903e02,
                    8.549390e02,
                    -6.647478e03,
                    -1.064853e04,
                    -4.171021e00,
                    -1.501747e01,
                    -1.888428e-01,
                    5.545634e03,
                ],
                [
                    -4.701574e03,
                    6.688361e03,
                    1.223288e04,
                    -3.098420e03,
                    6.745899e03,
                    -4.474388e03,
                    4.947241e03,
                    5.334855e03,
                    6.653889e03,
                    -1.206940e01,
                    1.123395e01,
                    3.519630e-01,
                    2.137472e02,
                ],
                [
                    2.698417e03,
                    -2.722472e03,
                    -7.146222e03,
                    9.166902e02,
                    -4.474388e03,
                    4.030793e03,
                    -4.448886e03,
                    -2.682003e03,
                    -2.698321e03,
                    1.166885e01,
                    -5.420895e00,
                    -1.787338e-01,
                    -1.729178e03,
                ],
                [
                    -2.037046e03,
                    4.219213e01,
                    5.618985e03,
                    8.549389e02,
                    4.947241e03,
                    -4.448886e03,
                    6.745437e03,
                    1.371551e03,
                    3.171216e01,
                    -1.749387e01,
                    2.293404e00,
                    8.043671e-02,
                    4.169263e03,
                ],
                [
                    -6.022355e03,
                    1.198888e04,
                    1.528325e04,
                    -6.647478e03,
                    5.334855e03,
                    -2.682003e03,
                    1.371551e03,
                    8.437011e03,
                    1.195731e04,
                    1.625114e00,
                    1.781580e01,
                    7.714996e-01,
                    -4.662336e03,
                ],
                [
                    -8.715623e03,
                    1.867886e04,
                    2.193285e04,
                    -1.064853e04,
                    6.653889e03,
                    -2.698321e03,
                    3.171217e01,
                    1.195731e04,
                    1.910547e04,
                    4.064438e00,
                    2.614574e01,
                    5.830841e-01,
                    -8.672464e03,
                ],
                [
                    4.149475e00,
                    5.044861e00,
                    -1.277600e01,
                    -4.171112e00,
                    -1.206927e01,
                    1.166878e01,
                    -1.749390e01,
                    1.624878e00,
                    4.064697e00,
                    -2.158142e03,
                    1.105316e02,
                    -2.832360e01,
                    -1.466002e01,
                ],
                [
                    -1.291957e01,
                    2.636751e01,
                    3.275133e01,
                    -1.501750e01,
                    1.123393e01,
                    -5.420914e00,
                    2.293438e00,
                    1.781590e01,
                    2.614552e01,
                    1.105317e02,
                    3.290158e03,
                    1.039862e02,
                    -1.082738e01,
                ],
                [
                    -1.636047e-01,
                    8.629456e-01,
                    6.414795e-01,
                    -1.887054e-01,
                    3.519135e-01,
                    -1.787491e-01,
                    8.040237e-02,
                    7.715759e-01,
                    5.830688e-01,
                    -2.832359e01,
                    1.039862e02,
                    1.726320e03,
                    -4.051666e-01,
                ],
                [
                    2.693130e03,
                    -8.679251e03,
                    -6.471688e03,
                    5.545634e03,
                    2.137472e02,
                    -1.729178e03,
                    4.169263e03,
                    -4.662337e03,
                    -8.672464e03,
                    -1.466016e01,
                    -1.082734e01,
                    -4.051819e-01,
                    7.339009e03,
                ],
            ],
            dtype=np.float32,
        ),
        rel=1e-3,
    )
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True)

    m2 = m.copy()
    m2.pvals = "init"
    m2.common_draws = False

    result2 = m2.maximize_loglike(stderr=True)

    m2.parameter_summary()

    from xlogit import MixedLogit

    df = d.to_dataframe().reset_index()
    varnames = [
        "price",
        "time",
        "conven",
        "comfort",
        "meals",
        "petfr",
        "emipp",
        "nonsig1",
        "nonsig2",
        "nonsig3",
    ]
    X = df[varnames].values
    y = df["choice"].values
    randvars = {"meals": "n", "petfr": "n", "emipp": "n"}
    alts = df["alt"]
    ids = df["id"]
    panels = None
    batch_size = 5000
    n_draws = 300

    np.random.seed(0)
    model = MixedLogit()
    model.fit(
        X,
        y,
        varnames,
        alts=alts,
        ids=ids,
        n_draws=n_draws,
        panels=panels,
        verbose=0,
        randvars=randvars,
        batch_size=batch_size,
    )

    model.summary()
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
