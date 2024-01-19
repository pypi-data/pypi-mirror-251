def example(extract='m', estimate=False):
    import numpy as np
    import pandas as pd

    import larch as lx
    from larch import P, X

    hh, pp, tour, skims, emp = lx.example(200, ["hh", "pp", "tour", "skims", "emp"])

    hh["INCOME_GRP"] = pd.qcut(hh.INCOME, 3)

    co = lx.Dataset.construct(
        tour.set_index("TOURID"),
        caseid="TOURID",
        alts=skims.TAZ_ID,
    )
    co

    emp.info()

    tree = lx.DataTree(
        base=co,
        hh=hh.set_index("HHID"),
        person=pp.set_index("PERSONID"),
        emp=emp,
        skims=lx.Dataset.construct.from_omx(skims),
        relationships=(
            "base.TAZ_ID @ emp.TAZ",
            "base.HHID @ hh.HHID",
            "base.PERSONID @ person.PERSONID",
            "hh.HOMETAZ @ skims.otaz",
            "base.TAZ_ID @ skims.dtaz",
        ),
    ).digitize_relationships()

    m = lx.Model(datatree=tree)
    m.title = "Exampville Tour Destination Choice v2"

    m.quantity_ca = (
        +P.EmpRetail_HighInc * X("RETAIL_EMP * (INCOME>50000)")
        + P.EmpNonRetail_HighInc * X("NONRETAIL_EMP") * X("INCOME>50000")
        + P.EmpRetail_LowInc * X("RETAIL_EMP") * X("INCOME<=50000")
        + P.EmpNonRetail_LowInc * X("NONRETAIL_EMP") * X("INCOME<=50000")
    )

    m.quantity_scale = P.Theta

    m.utility_ca = +P.distance * X.AUTO_DIST

    m.choice_co_code = "base.DTAZ"

    m.plock(EmpRetail_HighInc=0, EmpRetail_LowInc=0)

    # TEST
    assert m.availability_any

    mj = m.copy()

    m.compute_engine = "numba"

    # TEST
    assert m.d_loglike() == approx([-223.95036, -682.1102, 0.0, 0.0, -7406.393, -34762.906])
    assert mj.d_loglike() == approx(
        [-223.81805, -681.7803, 0.0, 0.0, -7406.3945, -34767.668], rel=1e-5
    )
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    result = m.maximize_loglike(stderr=True)

    resultj = mj.maximize_loglike(stderr=True)

    resultj

    # TEST
    mj.bhhh() == approx(
        np.asarray(
            [
                [
                    4.894633e01,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    1.824293e02,
                    2.349278e02,
                ],
                [
                    0.000000e00,
                    3.654184e02,
                    0.000000e00,
                    0.000000e00,
                    -2.068872e02,
                    5.649638e02,
                ],
                [
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                ],
                [
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                ],
                [
                    1.824293e02,
                    -2.068872e02,
                    0.000000e00,
                    0.000000e00,
                    1.450995e04,
                    1.208727e04,
                ],
                [
                    2.349278e02,
                    5.649638e02,
                    0.000000e00,
                    0.000000e00,
                    1.208727e04,
                    8.600401e04,
                ],
            ]
        )
    )

    # TEST
    assert m.bhhh() == approx(
        np.asarray(
            [
                [
                    4.842784e01,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    1.817289e02,
                    2.330331e02,
                ],
                [
                    0.000000e00,
                    3.653474e02,
                    0.000000e00,
                    0.000000e00,
                    -2.060223e02,
                    5.647817e02,
                ],
                [
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                ],
                [
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                ],
                [
                    1.817289e02,
                    -2.060223e02,
                    0.000000e00,
                    0.000000e00,
                    1.451344e04,
                    1.209207e04,
                ],
                [
                    2.330331e02,
                    5.647817e02,
                    0.000000e00,
                    0.000000e00,
                    1.209207e04,
                    8.600466e04,
                ],
            ]
        )
    )



    m.histogram_on_idca_variable("AUTO_DIST")

    m.histogram_on_idca_variable("RETAIL_EMP")

    m.histogram_on_idca_variable("AUTO_DIST", bins=40, span=(0, 10))

    m.histogram_on_idca_variable(
        "AUTO_DIST",
        x_label="Distance (miles)",
        bins=26,
        span=(0, 13),
        filter_co="INCOME<10000",
    )



    tour_plus = tour.join(hh.set_index("HHID")[["HOMETAZ", "INCOME"]], on="HHID")
    tour_plus["LOW_INCOME"] = tour_plus.INCOME < 50_000
    tour_agg = (
        tour_plus.groupby(["HOMETAZ", "DTAZ", "LOW_INCOME"])
        .size()
        .unstack("DTAZ")
        .fillna(0)
    )

    # j = tour_agg.reset_index(drop=True)
    # lx.DataArray(j.values, dims=("index", "DTAZ"), coords={"index": j.index, "DTAZ": j.columns})

    agg_dataset = lx.Dataset.construct.from_idco(
        tour_agg.index.to_frame().reset_index(drop=True)
    )
    j = tour_agg.reset_index(drop=True)
    agg_dataset = agg_dataset.assign(
        destinations=lx.DataArray(
            j.values,
            dims=("index", "DTAZ"),
            coords={"index": j.index, "DTAZ": j.columns},
        )
    )
    agg_dataset.dc.ALTID = "DTAZ"
    agg_dataset

    agg_tree = lx.DataTree(
        base=agg_dataset,
        emp=emp,
        skims=lx.Dataset.construct.from_omx(skims),
        relationships=(
            "base.DTAZ @ emp.TAZ",
            "base.HOMETAZ @ skims.otaz",
            "base.DTAZ @ skims.dtaz",
        ),
    )

    mg = lx.Model(datatree=agg_tree, compute_engine="numba")
    mg.title = "Exampville Semi-Aggregate Destination Choice"

    mg.quantity_ca = (
        +P.EmpRetail_HighInc * X("RETAIL_EMP * (1-LOW_INCOME)")
        + P.EmpNonRetail_HighInc * X("NONRETAIL_EMP") * X("(1-LOW_INCOME)")
        + P.EmpRetail_LowInc * X("RETAIL_EMP") * X("LOW_INCOME")
        + P.EmpNonRetail_LowInc * X("NONRETAIL_EMP") * X("LOW_INCOME")
    )

    mg.quantity_scale = P.Theta

    mg.utility_ca = +P.distance * X.AUTO_DIST

    mg.choice_ca_var = "base.destinations"

    mg.plock(EmpRetail_HighInc=0, EmpRetail_LowInc=0)

    # TEST
    assert mg.loglike() == approx(-77777.17321427427)

    # TEST
    assert mg.d_loglike() == approx([-223.95016, -682.1102, 0, 0, -7406.389, -34762.91])

    result = mg.maximize_loglike(stderr=True)
    result

    # TEST
    assert result.loglike == approx(-70650.07578452416)
    assert result.success
    assert result.method == "slsqp"
    assert result.n_cases == 79
    assert result.logloss == approx(3.4066288531040145)
    import pandas as pd

    pd.testing.assert_series_equal(
        result.x.sort_index(),
        pd.Series(
            {
                "EmpNonRetail_HighInc": 1.2453335020460703,
                "EmpNonRetail_LowInc": -1.0893594261458912,
                "EmpRetail_HighInc": 0.0,
                "EmpRetail_LowInc": 0.0,
                "Theta": 0.676440163641688,
                "distance": -0.3347118435209836,
            }
        ).sort_index(),
        rtol=1e-3,
    )
    assert m.pstderr == approx(
        np.array([0.145749, 0.052355, 0.0, 0.0, 0.009012, 0.003812]),
        rel=1e-3,
    )

    # TEST
    assert mg.total_weight() == approx(20739.0)
    assert mg.n_cases == 79

    # TEST
    assert mg.bhhh() == approx(
        np.asarray(
            [
                [
                    4.842784e01,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    1.817289e02,
                    2.330331e02,
                ],
                [
                    0.000000e00,
                    3.653474e02,
                    0.000000e00,
                    0.000000e00,
                    -2.060223e02,
                    5.647817e02,
                ],
                [
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                ],
                [
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                    0.000000e00,
                ],
                [
                    1.817289e02,
                    -2.060223e02,
                    0.000000e00,
                    0.000000e00,
                    1.451344e04,
                    1.209207e04,
                ],
                [
                    2.330331e02,
                    5.647817e02,
                    0.000000e00,
                    0.000000e00,
                    1.209207e04,
                    8.600466e04,
                ],
            ]
        )
    )
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
