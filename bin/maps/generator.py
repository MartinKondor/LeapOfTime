import random as r


nm = []

for y in range(150):
    row = []
    
    for x in range(150):
        if r.random() > .95:
            if r.random() > .5:
                row.append(r.choice([207, 208, 209, 210]))
            elif r.random() > .5:
                row.append(r.choice([271, 272, 273, 274]))
            else:
                row.append(r.choice([335, 336, 337, 338]))
        elif r.random() >= .99:
            row.append(r.choice([69, 133, 197]))
        else:
            row.append(1)
    
    nm.append(row)


file = open('generated.map', 'w+')

for row in nm:
    file.write(str(row)[1:-1] + '\n')

file.close()
