from __future__ import annotations


class Settings:
    do_reset_output: bool = True
    allow_out_of_input: bool = False
    catch_stderr: bool = True

    def __init__(self) -> None:
        msg = "Instances of the class Settings are prohibited"
        raise NotImplementedError(msg)
