"""
Here we can add every new unit group, to make our unit factory work without
any possible issues in PyCharm

Note: it will still work if you remove this, and import units explicitly to
      register. But threre will be a slight change that imports will be unused and
      PyCharm might/will REMOVE them on the next refactor/rename operation
"""
from . import armies
from . import formations
from . import vehicles
from . import infantry
