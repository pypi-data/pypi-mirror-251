def example(extract='m', estimate=False):
    import pandas as pd

    import larch as lx

    raw_data = pd.read_csv(lx.example_file("swissmetro.csv.gz")).rename_axis(index="CASEID")
    data = lx.Dataset.construct.from_idco(raw_data, alts={1: "Train", 2: "SM", 3: "Car"})
    data

    m = lx.Model(data.dc.query_cases("PURPOSE in (1,3) and CHOICE != 0"))

    m.title = "swissmetro example 02 (weighted logit)"

    m.availability_co_vars = {
        1: "TRAIN_AV * (SP!=0)",
        2: "SM_AV",
        3: "CAR_AV * (SP!=0)",
    }
    m.choice_co_code = "CHOICE"

    m.weight_co_var = "1.0*(GROUP==2)+1.2*(GROUP==3)"

    from larch import P, X

    m.utility_co[1] = P("ASC_TRAIN")
    m.utility_co[2] = 0
    m.utility_co[3] = P("ASC_CAR")
    m.utility_co[1] += X("TRAIN_TT") * P("B_TIME")
    m.utility_co[2] += X("SM_TT") * P("B_TIME")
    m.utility_co[3] += X("CAR_TT") * P("B_TIME")
    m.utility_co[1] += X("TRAIN_CO*(GA==0)") * P("B_COST")
    m.utility_co[2] += X("SM_CO*(GA==0)") * P("B_COST")
    m.utility_co[3] += X("CAR_CO") * P("B_COST")

    m.ordering = [
        (
            "ASCs",
            "ASC.*",
        ),
        (
            "LOS",
            "B_.*",
        ),
    ]
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    m.set_cap(15)
    result = m.maximize_loglike(method="SLSQP")
    result

    m.calculate_parameter_covariance()
    m.parameter_summary()

    # TEST
    assert m.pvals == approx(
        [-0.114834339145, -0.756969214206, -0.011197899961, -0.013210667574], rel=1e-2
    )
    assert m.pstderr == approx(
        [0.040689138346, 0.052839270341, 0.000490421261, 0.000536780123], rel=1e-2
    )
    assert m.parameter_summary().data["t Stat"].values.astype(float) == approx(
        [-2.82, -14.33, -22.83, -24.61], rel=1e-2
    )
    assert m.parameter_summary().data["Signif"].values == approx(
        ["**", "***", "***", "***"]
    )

    # TEST numba
    m.compute_engine = "numba"
    m.pvals = 0
    m.clear_cache()
    assert m.loglike() == approx(-7892.111473285806)
    result_n = m.maximize_loglike(method="SLSQP", quiet=True)
    assert m.pvals == approx(
        [-0.114834339145, -0.756969214206, -0.011197899961, -0.013210667574], rel=1e-3
    )
    assert m.pstderr == approx(
        [0.040689138346, 0.052839270341, 0.000490421261, 0.000536780123], rel=1e-3
    )
    assert m.parameter_summary().data["t Stat"].values.astype(float) == approx(
        [-2.82, -14.33, -22.83, -24.61], rel=1e-2
    )
    assert m.parameter_summary().data["Signif"].values == approx(
        ["**", "***", "***", "***"]
    )
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
