from openpyxl import Workbook
import requests

response_API = requests.get('https://phagesdb.org/api/subclusters/F1/phagelist/')

nextLetter = 0
currentCell = 0
start1 = 0
start2 = 0

phagelist = []
phageSizelist = []

HNH_currentPhage = 0
HNHlist = []

ruler_currentPhage = 0
rulerlist = []

difference = 0
differencelist = []

qFactor = 0
qFactorlist = []

temp = 0
templist = []

# phageNumber = response_API.text.count('phage_name')
phageNumber = 10


#-----------------------------------------------------------------------------------------------------------------------------------------------

# Looks through API string and pulls phage names and puts them into a list
for name in range(0, phageNumber):
    nameTagLocationStart = response_API.text.find('phage_name', start1)
    nameTagLocationEnd = response_API.text.find(',', nameTagLocationStart)
    nameLength = nameTagLocationEnd - nameTagLocationStart - 14
    nameStart = nameTagLocationStart + 13
    nameEnd = nameTagLocationEnd - 1
    name = response_API.text[nameStart:nameEnd:1]
    start1 = nameTagLocationEnd
    phagelist.append(name)

#------------------------------------------------------------------------------------------------------------------------------------------------

# Looks through API string and pulls phage genome size and put them into a list
for size in range(0, phageNumber):
    sizeTagLocationStart = response_API.text.find('genome_length', start2)
    sizeTagLocationEnd = response_API.text.find(',', sizeTagLocationStart)
    sizeLength = sizeTagLocationEnd - sizeTagLocationStart - 15
    sizeStart = sizeTagLocationStart + 15
    sizeEnd = sizeTagLocationEnd 
    size = response_API.text[sizeStart:sizeEnd:1]
    start2 = sizeTagLocationEnd
    phageSizelist.append(size)


#finds whether or not a phage has a HNH nuclease gene, then creates a list where that gene ends in base-pairs
for geneStop in range(0, phageNumber):
    
    geneAPI_response = requests.get(f'https://phagesdb.org/api/genesbyphage/{phagelist[HNH_currentPhage]}/')
    geneInfo = geneAPI_response.text.replace('"phams":["69531"]', '"phams":["73486"]')
    HNHstringlocation = geneInfo.find('"phams":["73486"]')

    if (HNHstringlocation > 0):
        geneStartstringlocationStart = geneInfo.find(',', HNHstringlocation) + 9
        geneStartstringlocationStop = geneInfo.find(',', geneStartstringlocationStart) 
        geneStopstringlocationStart = geneInfo.find(':', geneStartstringlocationStop) + 1
        geneStopstringlocationStop = geneInfo.find(',', geneStopstringlocationStart)

        geneStart = geneInfo[geneStartstringlocationStart:geneStartstringlocationStop:1]
        geneStop = geneInfo[geneStopstringlocationStart:geneStopstringlocationStop:1]


        # print(f'HNHnuclease found in {phagelist[currentPhage]} that starts at {geneStart} bp and ends at {geneStop} bp')
        HNHlocation = f'{geneStop}'
        HNH_currentPhage = HNH_currentPhage + 1

    else: 
        # print(f'no HNHnuclease found in {phagelist[currentPhage]}')
        HNHlocation = '0'
        HNH_currentPhage = HNH_currentPhage + 1

    HNHlist.append(HNHlocation)
    print(f'HNH Documentation progress... {HNH_currentPhage} / {phageNumber}', end="\r")
print()
print(f'HNH Documentation progress... COMPLETE')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------

#finds whether or not a phage has a 'ruler' gene, then creates a list where that gene starts in base-pairs
for ruler_geneStart in range(0, phageNumber):
    
    ruler_geneAPI_response = requests.get(f'https://phagesdb.org/api/genesbyphage/{phagelist[ruler_currentPhage]}/')
    ruler_geneInfo = ruler_geneAPI_response.text
    rulerstringlocation = ruler_geneInfo.find('"phams":["67068"]')

    if (rulerstringlocation > 0):
        ruler_geneStartstringlocationStart = ruler_geneInfo.find(',', rulerstringlocation) + 9
        ruler_geneStartstringlocationStop = ruler_geneInfo.find(',', ruler_geneStartstringlocationStart) 
        # ruler_geneStopstringlocationStart = ruler_geneInfo.find(':', ruler_geneStartstringlocationStop) + 1
        # ruler_geneStopstringlocationStop = ruler_geneInfo.find(',', ruler_geneStopstringlocationStart)

        ruler_geneStart = ruler_geneInfo[ruler_geneStartstringlocationStart:ruler_geneStartstringlocationStop:1]
        # ruler_geneStop = ruler_geneInfo[ruler_geneStopstringlocationStart:ruler_geneStopstringlocationStop:1]


        # print(f'HNHnuclease found in {phagelist[currentPhage]} that starts at {geneStart} bp and ends at {geneStop} bp')
        rulerlocation = f'{ruler_geneStart}'
        ruler_currentPhage = ruler_currentPhage + 1

    else: 
        # print(f'no HNHnuclease found in {phagelist[currentPhage]}')
        rulerlocation = '0'
        ruler_currentPhage = ruler_currentPhage + 1

    rulerlist.append(rulerlocation)
    print(f'ruler Documentation progress... {ruler_currentPhage} / {phageNumber}', end='\r')
print()
print(f'ruler Documentation progress... COMPLETE')



# subtracts HNHlist from rulerlist to base-pair distance between HNH gene and ruler gene
subtractionIterator = 0
for difference in range(0, phageNumber):
    if (int(rulerlist[subtractionIterator]) > 0 and int(HNHlist[subtractionIterator]) > 0):
        difference = (int(rulerlist[subtractionIterator]) - int(HNHlist[subtractionIterator]))
        subtractionIterator = subtractionIterator + 1

    else:
        difference = 0
        subtractionIterator = subtractionIterator + 1

    differencelist.append(difference)

    print(f'Subtraction progress... {subtractionIterator} / {phageNumber}', end="\r")
print()
print(f'Subtraction progress... COMPLETE', end="\r")
print()


# bro idk how to even explain this it just does what it does
quotientIterator_1 = 0
quotientIterator_2 = 0

for qFactor in range(0, phageNumber):
    for temp in range(0, pow(2, phageNumber)):

        if (int(differencelist[quotientIterator_1]) > 0 and int(differencelist[quotientIterator_2]) > 0):
            qFactor = differencelist[quotientIterator_1]/differencelist[quotientIterator_2]
        
            

            if (quotientIterator_2 >= phageNumber - 1):
                quotientIterator_2 = quotientIterator_2 - phageNumber - 1
            else:
                quotientIterator_2 = quotientIterator_2 + 1
            
        else:
            qFactor = None
            if (quotientIterator_2 >= phageNumber - 1):
                quotientIterator_2 = quotientIterator_2 - phageNumber - 1
            else:
                quotientIterator_2 = quotientIterator_2 + 1
            
        qFactorlist.append(qFactor) 

    quotientIterator_1 = quotientIterator_1 + 1

    print(f'qFactor progress... {len(qFactorlist)} / {pow(2, phageNumber)}', end="\r")
print()
print(f'qFactor progress... COMPLETE', end="\r")
print()

# print(qFactorlist)


# Creates Nodes Spreadsheet
def create_workbook(path):
    workbook = Workbook()
    nodes = workbook.active
    nodes.title = "Nodes"

    nodes["A1"] = "Id"
    for currentCell in range(0, phageNumber): nodes[f"A{currentCell + 2}"] = currentCell

    nodes["B1"] = "Label"
    for currentCell in range(0, len(phagelist)): nodes[f"B{currentCell + 2}"] = phagelist[currentCell]

    nodes["C1"] = "Size"
    for currentCell in range(0, len(phageSizelist)): nodes[f"C{currentCell + 2}"] = phageSizelist[currentCell]

    workbook.save(path)
if __name__ == "__main__":
    create_workbook("PhageDataNodes.xlsx")
    
# Creates Edge Spreadsheet
def create_workbook(path):
    workbook = Workbook()
    edges = workbook.active
    edges.title = "Edges"

    edges["A1"] = "Source"
    for currentCell in range(0, len(qFactorlist)): edges[f"A{currentCell + 2}"] = currentCell

    edges["B1"] = "Target"
    for currentCell in range(0, len(qFactorlist)):
        for currentCell in range(0, phageNumber): edges[f"A{currentCell + 2}"] = currentCell

    edges["C1"] = "Type"

    edges["D1"] = "Weight"
    for currentCell in range(0, len(qFactorlist)): edges[f"D{currentCell + 2}"] = qFactorlist[currentCell]
  
    workbook.save(path)
if __name__ == "__main__":
    create_workbook("PhageDataEdges.xlsx")