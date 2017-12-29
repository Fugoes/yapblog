__all__ = ["date"]

import re

date = re.compile("(\d{4})-(\d{1,2})-(\d{1,2})")
email = re.compile(r"(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)")
