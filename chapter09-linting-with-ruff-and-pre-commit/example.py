def create_frobnicator_factory(
    the_factory_name,
    interval_in_secs=100,
    dbg=False,
    use_singleton=None,
    frobnicate_factor=4.5,
):
    if dbg:
        print("creating frobnication factory " + the_factory_name + "...")
    if use_singleton:
        return _frob_sngltn  # we're done
    return FrobnicationFactory(
        the_factory_name, intrvl=interval_in_secs, f=frobnicate_factor
    )
