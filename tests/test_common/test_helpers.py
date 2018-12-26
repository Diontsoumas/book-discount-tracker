from common.helpers import print_mesage
from common.constants import PRINT_NORMAL


def test_print_normal_mesage(capfd):
    msg = "Book 10% discount in Politeia"
    print_mesage(name="Book", discount="10", vendor="Politeia", type=PRINT_NORMAL)
    out, err = capfd.readouterr()
    assert msg == out.strip()
