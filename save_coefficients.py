import pickle


fin = open("keel_coefficients.txt",'r')

coefficients = dict()

i = 0
for line in fin:
	i+=1
	if i>12:
		l = line.split()
		alpha = float(l[0])
		Cl = float(l[1])
		Cd = float(l[2])
		coefficients[alpha] = (Cl,Cd)

print coefficients[alpha]

pickle.dump(coefficients,open("keel_coefficients.p",'w'))
fin.close()