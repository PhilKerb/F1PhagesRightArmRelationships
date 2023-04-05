from openpyxl import Workbook
import requests

response_API = requests.get('https://phagesdb.org/api/subclusters/F1/phagelist/')

nextLetter = 0
currentIdValue = 0
start1 = 0
start2 = 0
phagelist = []
phageSizelist = []

phageNumber = response_API.text.count('phage_name')


# # Looks through API string and pulls phage names and puts them into a list
for name in range(0, phageNumber):
    nameTagLocationStart = response_API.text.find('phage_name', start1)
    nameTagLocationEnd = response_API.text.find(',', nameTagLocationStart)
    nameLength = nameTagLocationEnd - nameTagLocationStart - 14
    nameStart = nameTagLocationStart + 13
    nameEnd = nameTagLocationEnd - 1
    name = response_API.text[nameStart:nameEnd:1]
    start1 = nameTagLocationEnd
    phagelist.append(name)

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

# Creates Nodes Spreadsheet
def create_workbook(path):
    workbook = Workbook()
    nodes = workbook.active
    nodes.title = "Nodes"

    nodes["A1"] = "Id"
    for currentIdValue in range(0, phageNumber): nodes[f"A{currentIdValue + 2}"] = currentIdValue

    nodes["B1"] = "Label"
    for currentIdValue in range(0, len(phagelist)): nodes[f"B{currentIdValue + 2}"] = phagelist[currentIdValue]

    nodes["C1"] = "Size"
    for currentIdValue in range(0, len(phageSizelist)): nodes[f"C{currentIdValue + 2}"] = phageSizelist[currentIdValue]

    workbook.save(path)
if __name__ == "__main__":
    create_workbook("PhageData[TEST9].xlsx")
    
# Creates Edge Spreadsheet
# def create_workbook(path):
#     workbook = Workbook()

#     edges = workbook.create_sheet(title="Edges")
#     edges["A1"] = "Source"
#     edges["B1"] = "Target"
#     edges["C1"] = "Type"
#     edges["D1"] = "Weight"
  
#     workbook.save(path)
# if __name__ == "__main__":
#     create_workbook("PhageDataEdges.xlsx")