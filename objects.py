##Program created by Leon Marco M. Ebarle
##Date: March 2019

class POSummary:
    def __init__(self, poNumber, vendor, totalTax, totalAmount, description):
        self.poNumber = poNumber
        self.vendor = vendor
        self.totalTax = totalTax
        self.totalAmount = totalAmount
        self.description = description

class LineItems:
    def __init__(self):
        self.totalList = []

    def appendRowAndTotalList(self, description, taxes, dateRequired,
                              quantity, unitPrice, lineTotal):
        rowList = []
        rowList.append(description)
        rowList.append(taxes)
        rowList.append(dateRequired)
        rowList.append(quantity)
        rowList.append(unitPrice)
        rowList.append(lineTotal)
        
        self.totalList.append(rowList)
#        print(rowList)

    def returnTotalList(self):
        return self.totalList

    #The next two methods will not be used in PO.py, but are overridden
    #to account for future upgrades
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index >= len(self.totalList)-1:
            raise StopIteration()
        self.__index += 1
        return self.totalList[self.__index]

def main():
    lineItems = LineItems()
    lineItems.appendRowAndTotalList("MS Surface Pro i5", "10%", "March 10", 10, 10.50, 105.00)
    #print(lineItems.rowList)
    lineItems.appendRowAndTotalList("NUC i7", "10%", "March 10", 10, 10.50, 105.00)
    #print(lineItems.rowList)
    print(lineItems.returnTotalList())
    for data in lineItems:
        print(data)
    print("\n")
    for row in lineItems:
        for data in row:
            print(data, end=" | ")
        print("\n")

if __name__ == "__main__":
    main()
