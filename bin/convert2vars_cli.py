#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pathlib

base_path = (pathlib.Path(__file__)).parent.parent
sys.path.append(str(base_path))
from convert2vars import main

if __name__ == '__main__':
    main()
