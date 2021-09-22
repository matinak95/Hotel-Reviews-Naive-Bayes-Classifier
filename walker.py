import re
import sys
import os

path = "op_spam_training_data/negative_polarity/truthful_from_Web/fold1/"

for file in path:
    print(str(file))
    # with open(path + str(file), 'r') as f:
    #     print(f.read())
    #     f.close()
    sys.exit()




# for (root, dirs, files) in os.walk(path):
#     for file in files:
#         if len(file) > 4 and str(file)[-4:] == '.pdf':
#             print(str(root)+ "/" + str(file))
#
#
# tokens = ['abns', 'nasjs', 'nnassa', 'kdinfa', 'd', 's', 'ssses']
# for i in range(len(tokens)):
#     if len(tokens[i]) > 1 and tokens[i][-1] == 's':
#         tokens[i] = tokens[i][0:-1]
#     print(tokens[i][-1])





