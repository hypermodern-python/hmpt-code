def join_all(joinables):
    for task in joinables:
        task.join()
