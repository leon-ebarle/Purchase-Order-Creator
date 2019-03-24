#!/usr/bin/env python3

##Program created by Leon Marco M. Ebarle
##Date: March 2019

from datetime import date, datetime
from objects import POSummary, LineItems
from decimal import Decimal
import db
import tkinter as tk
from tkinter import ttk, Text
import os, sys

sys.path.insert(0, "c:\\prodprog\\vendor database")
from vendorUI import addVendor
import vendorDB

#dateToday = date.today()

class poFrame(ttk.Frame):
    def __init__(self, parent, padding = "10 10 10 10"):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack()

        self.dateToday = date.today()
        #Declare StringVars
        self.poNumber = tk.StringVar()
        self.vendorName = tk.StringVar()
        self.vendorAddress1 = tk.StringVar()
        self.vendorState = tk.StringVar()
        self.vendorCity = tk.StringVar()
        self.vendorZip = tk.StringVar()
        #self.description1 = tk.StringVar()
        #self.description2 = tk.StringVar()
        #self.description3 = tk.StringVar()
        self.dateRequired1 = tk.StringVar()
        self.dateRequired2 = tk.StringVar()
        self.dateRequired3 = tk.StringVar()
        self.quantity1 = tk.StringVar()
        self.quantity2 = tk.StringVar()
        self.quantity3 = tk.StringVar()
        self.unitPrice1 = tk.StringVar()
        self.unitPrice2 = tk.StringVar()
        self.unitPrice3 = tk.StringVar()
        self.tax1 = tk.StringVar()
        self.tax2 = tk.StringVar()
        self.tax3 = tk.StringVar()
        self.subTotal1 = tk.StringVar()
        self.subTotal2 = tk.StringVar()
        self.subTotal3 = tk.StringVar()
        self.total = tk.StringVar()
        self.totalTax = tk.StringVar()
        self.totalWithGST = tk.StringVar()

        self.poNumber.set(db.poCount()+1)

        self.setFields()

    def setFields(self):

        ttk.Label(self, text="PO Number: ").grid(row=0, column=0, sticky=tk.E)
        ttk.Entry(self, width=5, textvariable=self.poNumber, state="readonly").grid(row=0, column=1, sticky=tk.W)
        ttk.Label(self, text="Vendor: ").grid(row=1, column=0, sticky=tk.E)
        ttk.Entry(self, width=20, textvariable=self.vendorName).grid(row=1, column=1, sticky=tk.W)

        ttk.Button(self, text="Find Vendor", command=self.searchVendorDB).grid(row=1, column=2, sticky=tk.W)

        ttk.Label(self, text="Address: ").grid(row=2, column=0, sticky=tk.E)
        ttk.Entry(self, width=20, textvariable=self.vendorAddress1, state="readonly").grid(row=2, column=1, sticky=tk.W)
        ttk.Label(self, text="City: ").grid(row=3, column=0, sticky=tk.E)
        ttk.Entry(self, width=15, textvariable=self.vendorCity, state="readonly").grid(row=3, column=1, sticky=tk.W)
        ttk.Label(self, text="State: ").grid(row=4, column=0, sticky=tk.E)
        ttk.Entry(self, width=5, textvariable=self.vendorState, state="readonly").grid(row=4, column=1, sticky=tk.W)
        ttk.Label(self, text="Zip: ").grid(row=5, column=0, sticky=tk.E)
        ttk.Entry(self, width=5, textvariable=self.vendorZip, state="readonly").grid(row=5, column=1, sticky=tk.W)

        self.setFieldsFrame = ttk.Frame(self)
        self.setFieldsFrame.grid(row=6, column=0, columnspan=5, sticky=tk.E)
        
        ttk.Label(self.setFieldsFrame, text="Description").grid(row=6, column=0)
        ttk.Label(self.setFieldsFrame, text="Date Req'd").grid(row=6, column=1)
        ttk.Label(self.setFieldsFrame, text="Qty").grid(row=6, column=2)
        ttk.Label(self.setFieldsFrame, text="Unit Price").grid(row=6, column=3)
        ttk.Label(self.setFieldsFrame, text=" Tax").grid(row=6, column=4)
        ttk.Label(self.setFieldsFrame, text="  Sub-total").grid(row=6, column=5)

        ##Text declarations have to be separate from grid() function because grid functions always return None.
        self.description1 = Text(self.setFieldsFrame, height=2, width=20)
        self.description1.grid(row=7, column=0, padx=5)
        ttk.Entry(self.setFieldsFrame, width=12, textvariable=self.dateRequired1).grid(row=7, column=1)
        ttk.Entry(self.setFieldsFrame, width=5, textvariable=self.quantity1).grid(row=7, column=2, padx=5)
        ttk.Entry(self.setFieldsFrame, width=8, textvariable=self.unitPrice1).grid(row=7, column=3, padx=10)
        ttk.Entry(self.setFieldsFrame, width=10, textvariable=self.tax1).grid(row=7, column=4)
        ttk.Entry(self.setFieldsFrame, width=15, textvariable=self.subTotal1, state="readonly").grid(row=7, column=5, padx=5)

        self.description2 = Text(self.setFieldsFrame, height=2, width=20)
        self.description2.grid(row=8, column=0, pady=5)
        ttk.Entry(self.setFieldsFrame, width=12, textvariable=self.dateRequired2).grid(row=8, column=1)
        ttk.Entry(self.setFieldsFrame, width=5, textvariable=self.quantity2).grid(row=8, column=2)
        ttk.Entry(self.setFieldsFrame, width=8, textvariable=self.unitPrice2).grid(row=8, column=3, padx=10)
        ttk.Entry(self.setFieldsFrame, width=10, textvariable=self.tax2).grid(row=8, column=4)
        ttk.Entry(self.setFieldsFrame, width=15, textvariable=self.subTotal2, state="readonly").grid(row=8, column=5, padx=5)

        self.description3 = Text(self.setFieldsFrame, height=2, width=20)
        self.description3.grid(row=9, column=0, pady=5)
        ttk.Entry(self.setFieldsFrame, width=12, textvariable=self.dateRequired3).grid(row=9, column=1)
        ttk.Entry(self.setFieldsFrame, width=5, textvariable=self.quantity3).grid(row=9, column=2)
        ttk.Entry(self.setFieldsFrame, width=8, textvariable=self.unitPrice3).grid(row=9, column=3, padx=10)
        ttk.Entry(self.setFieldsFrame, width=10, textvariable=self.tax3).grid(row=9, column=4)
        ttk.Entry(self.setFieldsFrame, width=15, textvariable=self.subTotal3, state="readonly").grid(row=9, column=5, padx=5)

        ttk.Label(self, text="Total: ").grid(row=11, column=3, sticky=tk.E)
        ttk.Entry(self, width=15, textvariable=self.total, state="readonly").grid(row=11, column=4, pady=5)
        ttk.Label(self, text="Total Tax: ").grid(row=12, column=3, sticky=tk.E)
        ttk.Entry(self, width=15, textvariable=self.totalTax, state="readonly").grid(row=12, column=4, pady=5)
        ttk.Label(self, text="Total (incl. GST)").grid(row=13, column=3, sticky=tk.E)
        ttk.Entry(self, width=15, textvariable=self.totalWithGST, state="readonly").grid(row=13, column=4, pady=5)

        ttk.Label(self, text="When done, press Calculate, \nthen Generate PO").grid(row=15, column=2)
    
        ttk.Button(self, text="Calculate", command=self.calculate).grid(row=15, column=3)
        ttk.Button(self, text="Generate PO", command=self.generatePO).grid(row=15, column=4)

    def calculate(self):
        self.finalDescription1 = self.description1.get(1.0, "end-1c")
        self.finalDateRequired1 = self.dateRequired1.get()
        
        self.finalDescription2 = self.description2.get(1.0, "end-1c")
        self.finalDateRequired2 = self.dateRequired2.get()

        self.finalDescription3 = self.description3.get(1.0, "end-1c")
        self.finalDateRequired3 = self.dateRequired3.get()
        
        if not self.dateRequired1.get():
            assignedDate = self.setDate(str(self.dateToday))
        else:
            assignedDate=self.setDate(self.dateRequired1.get())
        self.dateRequired1.set(assignedDate)
        #We let the default vaules of quantity, unit price, and tax
        #be equal to 0
        if not self.quantity1.get():
            self.quantity1.set("0")
        if not self.unitPrice1.get():
            self.unitPrice1.set("0")
        if not self.tax1.get():
            self.tax1.set("0")

        self.finalQuantity1 = Decimal(self.quantity1.get())
        self.finalUnitPrice1 = Decimal(self.unitPrice1.get())
        tax = self.tax1.get()
        if "%" in tax:
            tax = tax[:tax.find("%")]

        self.finalTax1 = Decimal(tax)
        self.finalTax1 /= 100

        if self.finalDescription2.strip() != "":
            if not self.quantity2.get():
                self.quantity2.set("0")
            if not self.unitPrice2.get():
                self.unitPrice2.set("0")
            if not self.tax2.get():
                self.tax2.set("0")
            #Date for row 2
            if not self.dateRequired2.get():
                assignedDate = self.setDate(str(self.dateToday))
            else:
                assignedDate = self.setDate(self.dateRequired2.get())
            self.dateRequired2.set(str(assignedDate))

            self.finalQuantity2 = Decimal(self.quantity2.get())
            self.finalUnitPrice2 = Decimal(self.unitPrice2.get())
            tax = self.tax2.get()
            if "%" in tax:
                tax = tax[:tax.find("%")]
            self.finalTax2 = Decimal(tax)
            self.finalTax2 /= 100
        else:
            self.finalQuantity2 = Decimal("0")
            self.finalUnitPrice2 = Decimal("0")
            self.finalTax2 = Decimal("0")


        if self.finalDescription3.strip() != "":
            if not self.quantity3.get():
                self.quantity3.set("0")
            if not self.unitPrice3.get():
                self.unitPrice3.set("0")
            if not self.tax3.get():
                self.tax3.set("0")
            #Date for row 3
            if not self.dateRequired3.get():
                assignedDate = self.setDate(str(self.dateToday))
            else:
                assignedDate=self.setDate(self.dateRequired3.get())
            self.dateRequired3.set(assignedDate)
                
            self.finalQuantity3 = Decimal(self.quantity3.get())
            self.finalUnitPrice3 = Decimal(self.unitPrice3.get())
            tax = self.tax3.get()
            if "%" in tax:
                tax = tax[:tax.find("%")]
            self.finalTax3 = Decimal(tax)
            self.finalTax3 /=100
        else:
            self.finalQuantity3 = Decimal("0")
            self.finalUnitPrice3 = Decimal("0")
            self.finalTax3 = Decimal("0")


        try:
            self.finalSubTotal1 = self.finalQuantity1 * self.finalUnitPrice1
            self.finalSubTotal2 = self.finalQuantity2 * self.finalUnitPrice2
            self.finalSubTotal3 = self.finalQuantity3 * self.finalUnitPrice3
            
            self.subTotal1.set("{:,.2f}".format(self.finalSubTotal1))
            if self.finalDescription2:
                self.subTotal2.set("{:,.2f}".format(self.finalSubTotal2))
            if self.finalDescription3:
                self.subTotal3.set("{:,.2f}".format(self.finalSubTotal3))

            total = self.finalSubTotal1 + self.finalSubTotal2 + self.finalSubTotal3
            totalTax = self.finalSubTotal1 * self.finalTax1 + self.finalSubTotal2 * self.finalTax2 + self.finalSubTotal3 * self.finalTax3  
            totalWithGST = total + totalTax

            self.total.set("{:,.2f}".format(total))           
            self.totalTax.set("{:,.2f}".format(totalTax))
            self.totalWithGST.set("{:,.2f}".format(totalWithGST))
        except TypeError:
            tk.messagebox.showinfo("Error", "Please enter valid values for Quantity, Unit Price, and Tax")

        
    def searchVendorDB(self):
        vendorName = self.vendorName.get()
        vendor = vendorDB.retrieveVendor(vendorName)

        if vendor is None:
            tk.messagebox.showinfo("Error", "Vendor not in database. Please add Vendor")
            self.addWindow = tk.Toplevel(self.parent)
            self.addWindow.title("Add Vendor")
            #addVendor is from vendorUI class
            addVendor(self.addWindow)
        else:
            self.vendorName.set(vendor[0])
            self.vendorAddress1.set(vendor[2])
            self.vendorCity.set(vendor[4])
            self.vendorState.set(vendor[5])
            self.vendorZip.set(vendor[6])

    def setDate(self, dateRequired):
        formatDates = ["%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y", "%m/%d/%Y", "%m/%d/%y", "%m-%d-%Y", "%m-%d-%y", "%Y-%m-%d", "%Y/%m/%d", "%y-%m-%d", "%y/%m/%d"]
        for formatDate in formatDates:
            try:
                dateFinal = datetime.strptime(dateRequired, formatDate)
                dateFinal = str(dateFinal.day) + "/" + str(dateFinal.month) + "/" + str(dateFinal.year) 
                return dateFinal
            except ValueError as e:
                pass

    def generatePO(self):
        poSummary = POSummary(int(self.poNumber.get()), self.vendorName.get(), float(self.totalTax.get().replace(",", "")), float(self.totalWithGST.get().replace(",", "")), self.finalDescription1 + ", " + self.finalDescription2 + ", " + self.finalDescription3)
        #inserts a summary of the PO into the POTable
        db.insertPO(poSummary)

        lineItems = LineItems()
        lineItems.appendRowAndTotalList(self.finalDescription1, self.tax1.get(), self.dateRequired1.get(), self.quantity1.get(), self.unitPrice1.get(), self.subTotal1.get())
        lineItems.appendRowAndTotalList(self.finalDescription2, self.tax2.get(), self.dateRequired2.get(), self.quantity2.get(), self.unitPrice2.get(), self.subTotal2.get())
        lineItems.appendRowAndTotalList(self.finalDescription3, self.tax3.get(), self.dateRequired3.get(), self.quantity3.get(), self.unitPrice3.get(), self.subTotal3.get())

        db.writeToPDF(poSummary, lineItems)
        tk.messagebox.showinfo("Success", "Purchase Order created!")
        
def main():
    db.connect()
    vendorDB.connect()
    root = tk.Tk()
    root.title("PO Creator")
    poFrame(root)
    root.mainloop()
    db.closeConnection()
    vendorDB.closeConnection()


if __name__ == "__main__":
    main()
