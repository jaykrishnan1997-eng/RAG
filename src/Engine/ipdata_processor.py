#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ipdata_processor.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/13 10:43:25 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/13 14:06:53 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os

from Base.model import path_dict


def source_processor() -> None:
    """This is a inital point that divides the task,
     we do through every single file in raw folder
     and this is where the branching happens (like txt or py etc)"""

    for (dirpath, dirname, filename) in os.walk('data/'):
        print(filename)
        breakpoint()





    
# https://www.geeksforgeeks.org/python/python
# -loop-through-folders-and-files-in-directory/

# https://www.tutorialspoint.com/python/os_walk.htm
