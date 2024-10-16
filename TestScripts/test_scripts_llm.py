liste = ['* Employment\n* Poverty\n* Household\n* Working Poor\n* SDGs\n* Sustainability\n* Social Impact\n* Per Capita\n* Income\n* Consumption\n* International Poverty Line\n* Basic Bundle\n* Goods and Services\n* Reference Population\n* Short Reference Period\n* Absolute International Poverty Line\n* Monetary Requirements\n* Per-Capita Monetary Requirements\n* Basic Needs\n* Economic Growth\n* Human Development\n* Human Capital\n* Education\n* Healthcare\n* Access to Finance\n* Access to Technology\n* Climate Change\n* Environmental Protection\nNote:']
liste = liste[0].replace("\n", "")
liste1 = liste[0].replace("*", "")
# print(liste)
liste2 = liste1.split(",")
print(liste2)

# Output: Employment, Poverty, Household, Working Poor, SDGs, Sustainability, Social Impact, Per Capita, Income, Consumption, International Poverty Line, Basic Bundle, Goods and Services, Reference Population, Short Reference Period, Absolute International Poverty Line, Monetary Requirements, Per-Capita Monetary Requirements, Basic Needs, Economic Growth, Human Development, Human Capital, Education, Healthcare,pri