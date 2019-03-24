##Program created by Leon Marco M. Ebarle
##Date: March 2019

import sqlite3
import os
import sys
from contextlib import closing

from objects import LineItems, POSummary

from fpdf import FPDF

sys.path.insert(0, "C:\\prodprog\\vendor database")
import vendorDB

conn = None

## User may notice that there is no provision to delete rows in this table.
## Usually, PO numbers are never deleted in an organization. Once entered,
## it will remain in the database for good.

def connect():
    global conn

    if not conn:
        if sys.platform == "win32":
            DB_FILE = "c:\\prodprog\\database\\vendor.db"
        else:
            HOME = os.environ["HOME"]
            DB_FILE = HOME + "Documents/python/prod_programs/database/vendor.db"

        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def closeConnection():
    global conn
    if conn:
        conn.close()

def searchPO(PONumber):
    query = '''
                SELECT  PONumber,
                        Vendor,
                        TotalTax,
                        TotalAmount,
                        Description
                  FROM  POTable
                 WHERE  PONumber = ? 
            '''

    with closing(conn.cursor()) as c:
        c.execute(query, (PONumber,))
        rowData = c.fetchall()

    if len(rowData) >= 1:
        return rowData
    else:
        return None

def insertPO(poSummary):

    poNumber = searchPO(poSummary.poNumber)

    if poNumber is None:
        query = '''
                    INSERT INTO
                            POTable (PONumber, Vendor, TotalTax, TotalAmount,
                                     Description)
                            VALUES  (?, ?, ?, ?, ?)
                '''
        with closing (conn.cursor()) as c:
            c.execute(query, (poSummary.poNumber, poSummary.vendor, poSummary.totalTax,
                              poSummary.totalAmount, poSummary.description))
            conn.commit()
        return 0
    else:
        return 803

def poCount():
    query = '''
                SELECT COUNT(*) as number
                  FROM POTable
            '''
    with closing(conn.cursor()) as c:
        c.execute(query)
        count = c.fetchone()

    return count["number"]

def writeToPDF(poSummary, lineItems):
    companyInfo = ["Company Name", "Address Line 1", "City", "State", "Zip"]
    vendorInfo = vendorDB.retrieveVendor(poSummary.vendor)
    poFileName = "PO" + str(poSummary.poNumber) + ".pdf"

    pdf = FPDF()
    pdf.add_page()

    #Company Name and Address being written in PDF file
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(200, 6, txt=companyInfo[0],ln=1)
    pdf.set_font("Arial", size=8)
    for index in range(1, len(companyInfo)):
        pdf.cell(200, 6, txt=companyInfo[index], ln=1)

    #Vendor Name and Address being written into PDF file
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(200, 6, txt="To: " + vendorInfo[0], ln=1)
    pdf.set_font("Arial", size=8)
    pdf.cell(200, 6, txt=vendorInfo[2], ln=1)
    pdf.cell(200, 6, txt=vendorInfo[4], ln=1)
    pdf.cell(200, 6, txt=vendorInfo[5]+", "+str(vendorInfo[6]), ln=1)
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(200, 6, txt="Purchase Order PO" + str(poSummary.poNumber), ln=1)

    #Purchase orders being written into PDF file
    col_width = pdf.w/6
    row_height = pdf.font_size
    pdf.ln(row_height)
    pdf.set_font("Arial", size=8)
    i=0
    
    pdf.cell(200, 6, txt="{:60} {:20} {:40} {:40} {:24} {:20}".format("Description", "Tax", "Date Required", "Quantity", "Unit Price", "Total"), ln=1)
    for row in lineItems:
        for item in row:
            if i==0:
                pdf.cell(col_width+20, row_height, txt=item)
            elif i==1:
                pdf.cell(col_width-15, row_height, txt=item)
            elif i==2:
                pdf.cell(col_width+5, row_height, txt=item)
            elif i==4:
                pdf.cell(col_width-15, row_height, txt=item)
            else:
                pdf.cell(col_width, row_height, txt=item)
            i +=1
        pdf.ln(row_height)
        i = 0

    #Totals being written into PDF file
    pdf.ln(row_height*2)
    pdf.set_font("Arial", size=10, style="B")
    pdf.cell(190, 6, txt="Total: "+"{:,.2f}".format(poSummary.totalAmount), align="R", ln=1)
    pdf.cell(190, 6, txt="Total Tax: "+"{:,.2f}".format(poSummary.totalTax), align="R", ln=1)
    pdf.output(poFileName)
    
    
##testing correctness of output
def main():
    connect()
    vendorDB.connect()
    rowData = searchPO(1)
    if rowData is not None:
        for data in rowData:
            print(data["PONumber"], end=" | ")
            print(data["Vendor"])
    print(poCount())
    poSummary = POSummary(2, "Sigma Aldrich", 150, 1500.00, "Propanol")
    sqlcode = insertPO(poSummary)
    rowData = searchPO(poSummary.poNumber)
    if sqlcode == 0:
        for data in rowData:
            print(data["PONumber"], end=" | ")
            print(data["Vendor"])
    else:
        print("PO already in table.")

    poSummary = POSummary(4, "Element14", 1400, 15400, "NUC, Soldering Iron, ")
    lineItems = LineItems()
    lineItems.appendRowAndTotalList("NUC i7", "10%", "31/3/2019", "10", "1,000.00", "10,000.00")
    lineItems.appendRowAndTotalList("MS Surface Pro i5", "10%", "31/3/2019", "2", "2,000.00", "4,000.00")
    writeToPDF(poSummary, lineItems.totalList)
    closeConnection()
    vendorDB.closeConnection()
        

if __name__ == "__main__":
    main()
