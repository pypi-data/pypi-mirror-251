def example(extract='m', estimate=False):
    import pandas as pd

    import larch as lx

    raw_data = pd.read_csv(lx.example_file("swissmetro.csv.gz")).rename_axis(index="CASEID")
    data = lx.Dataset.construct.from_idco(raw_data, alts={1: "Train", 2: "SM", 3: "Car"})
    m = lx.Model(data.dc.query_cases("PURPOSE in (1,3) and CHOICE != 0"))

    m.title = "swissmetro example 09 (nested logit)"

    m.availability_co_vars = {
        1: "TRAIN_AV * (SP!=0)",
        2: "SM_AV",
        3: "CAR_AV * (SP!=0)",
    }
    m.choice_co_code = "CHOICE"

    from larch import P, X

    m.utility_co[1] = P.ASC_TRAIN + P.B_TIME * X.TRAIN_TT + P.B_COST * X("TRAIN_CO*(GA==0)")
    m.utility_co[2] = P.B_TIME * X.SM_TT + P.B_COST * X("SM_CO*(GA==0)")
    m.utility_co[3] = P.ASC_CAR + P.B_TIME * X.CAR_TT + P.B_COST * X("CAR_CO")

    m.graph.new_node(parameter="existing", children=[1, 3], name="Existing")

    m.graph

    m.ordering = [
        (
            "ASCs",
            "ASC.*",
        ),
        (
            "LOS",
            "B_.*",
        ),
        ("LogSums", "existing"),
    ]
    if not estimate:
        if isinstance(extract, str):
            return locals()[extract]
        else:
            _locals = locals()
            return [_locals.get(i) for i in extract]
    m.set_cap(15)
    result = m.maximize_loglike()
    result

    m.calculate_parameter_covariance(robust=True)
    m.parameter_summary()

    # TEST
    assert m.pstderr == approx(
        [0.037138242, 0.045185346, 0.00046280216, 0.00056991476, 0.027901005], rel=1e-2
    )
    assert m.parameter_summary().data["t Stat"].values.astype(float) == approx(
        [-4.5, -11.33, -18.52, -15.77, -18.39], rel=1e-2
    )
    assert m.parameter_summary().data["Signif"].values == approx(
        ["***", "***", "***", "***", "***"]
    )
    assert m.parameter_summary().data["Robust t Stat"].values.astype(float) == approx(
        [-3.06, -6.47, -14.27, -8.39, -13.18], rel=1e-2
    )
    assert m.parameter_summary().data["Robust Signif"].values == approx(
        ["**", "***", "***", "***", "***"]
    )
    if isinstance(extract, str):
        return locals()[extract]
    else:
        _locals = locals()
        return [_locals.get(i) for i in extract]
