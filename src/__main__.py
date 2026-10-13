#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/12 12:24:16 by jkrishna            #+#    #+#            #
#   Updated: 2026/10/13 09:37:55 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from CLI/parser import parse_args

def main() -> None:
    # parsing
    args = parse_args()
    
    # Text processing
    # Chunking
    # Embedding
    # Retrieval
    # Generation


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Exception caught: {e}")
        sys.exit(1)