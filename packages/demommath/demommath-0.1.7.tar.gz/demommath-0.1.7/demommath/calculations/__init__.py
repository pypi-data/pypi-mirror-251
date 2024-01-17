__all__ = []

from .calc import (
    multiply,
    divide,
    is_prime,
    is_odd_or_even,

)

__all__ += [ "is_prime", "is_odd_or_even",]

from .LCM_of_num import (lcm,)

__all__ += ["lcm",]

from .mean_of_num import (find_mean,)

__all__ += ["find_mean",]