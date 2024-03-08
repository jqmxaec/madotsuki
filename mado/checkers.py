def is_foreign_key_violation(err: str) -> bool:
    return err.startswith("FOREIGN KEY constraint failed")


def is_unique_failed(err: str) -> bool:
    return err.startswith("UNIQUE constraint failed")
