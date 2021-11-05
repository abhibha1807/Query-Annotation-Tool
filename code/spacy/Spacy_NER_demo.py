import spacy
from tabulate import tabulate
# load model
model=spacy.load('myMdl')

# make predictions
str_ip='Material and method Surface of plain carbon steel plates in the size of 20 mm×20 mm×2 mm was roughened by sand blasting and then coated with an intermediary Ni–Cr layer that increases the adhesion of coating.\n Martensitic stainless steel coating was applied by HVOF thermal spray process on the steel plates.\n The average coating thickness was ≈ 150 µm.\n The HVOF-sprayed 420 martensitic stain- less steel coating was used as the substrate material for the preparation of electroless Ni–P/Ni–B duplex coating.\n To generate a Ni–P/Ni–B duplex coating, the surface of the HVOF-sprayed 420 martensitic stainless steel coa- ting was prepared for plating by mechanical grinding, acetone degreasing and etching in a 30 vol.%HCl solu- tion for 1 min.\n A continuous Ni–P deposit was applied to form the first layer before immersion in the electro- less Ni–B bath for the second layer.\n By the preparation of Ni–P coating, a commercial Ni–P electroless solution (Durni-Coat DNC 520-9) was used.\n The stirring rate of plating bath was about 250 r/min, using a magnetic stir- rer and a polytetrafluoroethylene (PTFE) coated magnet with 2 cm length and 5 mm in diameter.\n The deposition was carried out in a 100 ml thermostated double wall be- aker at 90 ◦C and pH 4.6 for 2 h to achieve a thickness of ≈ 3.5 µm.\n The Ni–B plating took place at 95 ◦C and pH 13.5 for 2 h to achieve a thickness of ≈ 36 µm in a thermostated cell with a volume of 100 ml.\n The elec- troless Ni–B bath used for this study uses sodium bo- rohydride as a reducer, nickel chloride hexahydrate as a nickel source, ethylene diamine as a complexing agent and lead nitrate as a stabilizer.\n More details on the bath composition have been given by Bulbul [7].\n The cross- section of the coating was included in epoxy resin and polished by metallographic procedures.'
doc = model(str_ip)
table=[]
table.append(["WORD","TAG"])
	
for ent in doc.ents:
	table.append([ent.text,ent.label_])

print(tabulate(table,headers="firstrow"))