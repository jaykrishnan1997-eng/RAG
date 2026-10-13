#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ipdata_processor.py                                  :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/13 10:43:25 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/13 15:16:44 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os

from Base.model import path_dict


def source_processor() -> None:
    """This is a inital point that divides the task,
     we do through every single file in raw folder
     and this is where the branching happens (like txt or py etc)"""

    for dirpath, dirnames, filenames in os.walk(path_dict("DATA_PATH")):
        breakpoint()
        for file in filenames:
            print(os.path.join(dirpath, file))





    
# https://www.geeksforgeeks.org/python/python
# -loop-through-folders-and-files-in-directory/

# https://www.tutorialspoint.com/python/os_walk.htm
