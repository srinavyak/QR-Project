id=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
name=['ABC', 'AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'ABCD', 'ABCDA', 'FormA', 'XXX', 'YYY', 'www', 'vvv', 'ttt', 'ZZZ']


res = {} 
for key in id: 
    for value in name: 
        res[key] = value 
        name.remove(value) 
        break 
print(str(res)) 