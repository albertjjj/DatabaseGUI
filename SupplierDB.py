from os import close, error, name
from turtle import window_width
from PyPDF2.pdf import PageObject
from dearpygui.core import *
from dearpygui.simple import *
import sqlite3
import os
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections import Counter
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from fpdf import FPDF
import subprocess

'''

TODO:
- Add logo to login page
- small window size in login page which changes to bigger when logged in
- 

Features:

Add files to database:
- links to computer files
- hyperlinks?
- the data type in sqlite

Mobile:
- maybe print to pdf so it can be viewed
- better to make it into a webpage and view it online with flask
- 

Add reports:
- shows ammount of each product, 
- export as pdf
- graphs? pie chart with products.
- https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
- https://stackoverflow.com/questions/281888/open-explorer-on-a-file 
- https://pythonguides.com/python-save-an-image-to-file/ 
- https://realpython.com/python-send-email/
- https://realpython.com/python-send-email/

'''

databasePath = (os.getcwd()+"/IA/SupplierDB.db")
imagePath = (os.getcwd()+"/IA/logo.png")
iconPath = (os.getcwd()+"/IA/icon.png")
logout = False

def employeeView(acc):
    
    def updateSupplierTable():
        clear_table('##SupplierTable') 

        try:
            conn = sqlite3.connect(databasePath,  check_same_thread=False)
            c = conn.cursor()
        except:
            print("failed connection")

        c.execute("SELECT * FROM SupplierTable")
        result = c.fetchall()
        
        #add empty rows
        for i in range(0, len(result)+1):
            rowName = "##row " + str(i)
            add_row('##SupplierTable', [rowName])

        #Add data from result
        for row in result:
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 0, value = str(row[0]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 1, value = str(row[1]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 2, value = str(row[2]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 3, value = str(row[3]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 4, value = str(row[4]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 5, value = str(row[5]))

    def searchSupplier(sender, data):
        clear_table("##ResultsTable")
        #get value
        idInput = get_value("##searchID")
        nameInput = get_value('##searchName')
        emailInput = get_value('##searchEmail')
        productInput = get_value('##searchProduct')
        creationInput = get_value('##searchCreation')
        expiryInput = get_value('##searchExpiry')
        inputArray = [idInput, nameInput, emailInput, productInput, creationInput, expiryInput]
        
        parallelArray = ['SupplierID', 'SupplierName', 'SupplierEmail', 'Product', 'ContractCreationDate', 'ContractExpiryDate']
        for j in range(len(inputArray)):
            for i in range(len(inputArray)):
                try:
                    if inputArray[i] == "":
                        inputArray.pop(i)
                        parallelArray.pop(i)
                except:
                    continue

        searchTerm = ''

        for x in range(len(inputArray)):
            if len(inputArray)-x == 1:
                searchTerm = searchTerm + str(parallelArray[x]) + "='" + str(inputArray[x]) + "'"
            else:
                searchTerm = searchTerm + str(parallelArray[x]) + "='" + str(inputArray[x]) + "' and "

        try:
            conn = sqlite3.connect(databasePath,  check_same_thread=False)
            c = conn.cursor()
        except:
            print("failed connection")
        
        c.execute("SELECT * FROM SupplierTable WHERE " + searchTerm + ";")
        value = c.fetchall()
        
        
        with popup(popupparent='Search', name='results', mousebutton=0, modal=True):
            
            #add_text(value)
            add_table("##ResultsTable", headers = ['Supplier ID', 'Supplier Name', 'SupplierEmail', 'Product', 'ContractCreationDate', 'ContractExpiryDate'])
            clear_table("##ResultsTable")

            #add empty rows
            for i in range(0, len(value)+1):
                rowName = "##row " + str(i)
                add_row('##ResultsTable', [rowName])
            
            #Add data from result
            temp = 0
            for row in value:
                set_table_item(table = '##ResultsTable', row = temp, column = 0, value = str(row[0]))
                set_table_item(table = '##ResultsTable', row = temp, column = 1, value = str(row[1]))
                set_table_item(table = '##ResultsTable', row = temp, column = 2, value = str(row[2]))
                set_table_item(table = '##ResultsTable', row = temp, column = 3, value = str(row[3]))
                set_table_item(table = '##ResultsTable', row = temp, column = 4, value = str(row[4]))
                set_table_item(table = '##ResultsTable', row = temp, column = 5, value = str(row[5]))
                temp+=1
            
            add_button("Close##1", callback=lambda: close_popup("results"))
            add_dummy(width=800)

        '''
        set_value("##searchID", value[0])
        set_value("##searchName", value[1])
        set_value("##searchEmail", value[2])
        set_value("##searchProduct", value[3])
        set_value("##searchCreation", value[4])
        set_value("##searchExpiry", value[5])
        '''
        
    def changePass(sender, data):
        #checks password and then changes it to new one
        testPass = get_value('##currentPass')
        accPass = acc[0][3]
        newPass = get_value('##newPass')
        if testPass == accPass:
            #connect
            try:
                    conn = sqlite3.connect(databasePath,  check_same_thread=False)
                    c = conn.cursor()
            except:
                print("failed connection")
            
            #update password for logged in emplpyee
            command = ("UPDATE EmployeeTable SET EmployeePassword = '" + newPass +  "' WHERE EmployeeName = '" + acc[0][1] + "';")
            c.execute(command)
            conn.commit()
        
            set_value("##currentPass", "")
            set_value("##newPass", "")

            set_value('##passStatus', 'Password Changed')

        else:
            set_value('##passStatus', 'Incorrect Password')
        
    hide_item('Login')

    set_main_window_size(1250, 800)
    
    try:
        conn = sqlite3.connect((databasePath),  check_same_thread=False)
        c = conn.cursor()
    except:
        print("failed connection")

    with window("EmployeeView"):
        set_primary_window('EmployeeView', True)
        set_main_window_size(1250, 800)
        

        #header group
        add_group(name='header', horizontal=True, horizontal_spacing=20)

        #button for file menu (popup)
        add_button(name='File')
        #add name of acc
        add_text(acc[0][1])

        end()

        #make popup for file menu
        with popup(popupparent='File', name='File##1', mousebutton=0, modal=True):
            #add Buttons for different popups
            add_button('Change Password##button')
            #Logout button
            add_button('Logout##button')
            #close button
            add_button("Close##4", callback=lambda: close_popup("File##1"))
            add_dummy(width=600)
        
        #popup for changing password
        with popup(popupparent='Change Password##button', name='Change Password##popup', mousebutton=0, modal=True):
            add_group('current', horizontal=True)
            #Input current password
            add_text('Current password')
            add_input_text("##currentPass", password=True)
            end()
            #input desired password
            add_group('new', horizontal=True)
            add_text('New Password')
            add_input_text('##newPass', password=True)
            end()

            add_text('##passStatus')
            
            add_button('Change', callback=changePass)

            add_button("Close##5", callback=lambda: close_popup("Change Password##popup"))
            add_dummy(width=600)   

        #popup for logout confirmation
        with popup(popupparent='Logout##button', name='Logout##popup', mousebutton=0, modal=True):
            def confirm():
                #hide_item
                delete_item('EmployeeView')
                global logout
                Logout = True
                
                
                show_item('Login')

            add_text("Are you sure you want to logout?")
            add_button("Yes", callback=confirm)
            add_button("Close##6", callback=lambda: close_popup("Logout##popup"))
            add_dummy(width=100)   

        #add logo
        add_image(name = 'logo', value = imagePath, width = round(1584/1.285), height = round(296/1.285))

        #search
        add_group(name = 'parent', horizontal= True, horizontal_spacing= 20)
        
        add_dummy(width=50)

        add_group(name = 'column1', width = 75)
        add_text("ID")
        add_input_text("##searchID")
        end()

        add_group(name = "column2", width = 150)
        add_text('Name')
        add_input_text("##searchName")
        end()

        add_group(name = "column3", width = 150)
        add_text('Email')
        add_input_text("##searchEmail")
        end()
        
        add_group(name = "column4", width = 150)
        add_text('Product')
        add_input_text("##searchProduct")
        end()
        
        add_group(name = "column5", width = 150)
        add_text('Contract Creation')
        add_input_text("##searchCreation")
        end()

        add_group(name = "column6", width = 150)
        add_text('Contract Expiry')
        add_input_text("##searchExpiry")
        end()    

        add_group(name = "column7", width = 150)
        add_text("")
        add_button("Search", callback=searchSupplier)
        end()
        
        end()

        #make table
        add_table("##SupplierTable", headers = ['Supplier ID', 'Supplier Name', 'SupplierEmail', 'Product', 'ContractCreationDate', 'ContractExpiryDate'])
        updateSupplierTable()

        
    try:
        set_main_window_resizable(True)
        set_main_window_size(1250, 800)
        set_style_window_padding(8.00, 8.00)
        set_style_frame_padding(4.00, 3.00)
        set_style_item_spacing(8.00, 4.00)
        set_style_item_inner_spacing(4.00, 4.00)
        set_style_touch_extra_padding(0.00, 0.00)
        set_style_indent_spacing(21.00)
        set_style_scrollbar_size(14.00)
        set_style_grab_min_size(10.00)
        set_style_window_border_size(0.00)
        set_style_child_border_size(1.00)
        set_style_popup_border_size(1.00)
        set_style_frame_border_size(0.00)
        set_style_tab_border_size(0.00)
        set_style_window_rounding(7.00)
        set_style_child_rounding(0.00)
        set_style_frame_rounding(3.00)
        set_style_popup_rounding(0.00)
        set_style_scrollbar_rounding(9.00)
        set_style_grab_rounding(3.00)
        set_style_tab_rounding(4.00)
        set_style_window_title_align(0.00, 0.50)
        set_style_window_menu_button_position(mvDir_Left)
        set_style_color_button_position(mvDir_Right)
        set_style_button_text_align(0.50, 0.50)
        set_style_selectable_text_align(0.00, 0.00)
        set_style_display_safe_area_padding(3.00, 3.00)
        set_style_global_alpha(1.00)
        set_style_antialiased_lines(True)
        set_style_antialiased_fill(True)
        set_style_curve_tessellation_tolerance(1.25)
        set_style_circle_segment_max_error(1.60)
        set_theme_item(mvGuiCol_Text, 0, 0, 0, 255)
        set_theme_item(mvGuiCol_TextDisabled, 153, 153, 153, 255)
        set_theme_item(mvGuiCol_WindowBg, 240, 240, 240, 255)
        set_theme_item(mvGuiCol_PopupBg, 255, 255, 255, 250)
        set_theme_item(mvGuiCol_Border, 0, 0, 0, 77)
        set_theme_item(mvGuiCol_FrameBg, 255, 255, 255, 255)
        set_theme_item(mvGuiCol_FrameBgHovered, 66, 150, 250, 102)
        set_theme_item(mvGuiCol_FrameBgActive, 66, 150, 250, 171)
        set_theme_item(mvGuiCol_TitleBg, 245, 245, 245, 255)
        set_theme_item(mvGuiCol_TitleBgActive, 209, 209, 209, 255)
        set_theme_item(mvGuiCol_TitleBgCollapsed, 255, 255, 255, 130)
        set_theme_item(mvGuiCol_MenuBarBg, 219, 219, 219, 255)
        set_theme_item(mvGuiCol_ScrollbarBg, 250, 250, 250, 135)
        set_theme_item(mvGuiCol_ScrollbarGrab, 176, 176, 176, 204)
        set_theme_item(mvGuiCol_ScrollbarGrabHovered, 125, 125, 125, 204)
        set_theme_item(mvGuiCol_ScrollbarGrabActive, 125, 125, 125, 255)
        set_theme_item(mvGuiCol_CheckMark, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_SliderGrab, 66, 150, 250, 199)
        set_theme_item(mvGuiCol_SliderGrabActive, 117, 138, 204, 153)
        set_theme_item(mvGuiCol_Button, 66, 150, 250, 102)
        set_theme_item(mvGuiCol_ButtonHovered, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_ButtonActive, 15, 135, 250, 255)
        set_theme_item(mvGuiCol_Header, 66, 150, 250, 79)
        set_theme_item(mvGuiCol_HeaderHovered, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_HeaderActive, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_Separator, 99, 99, 99, 158)
        set_theme_item(mvGuiCol_SeparatorHovered, 36, 112, 204, 199)
        set_theme_item(mvGuiCol_SeparatorActive, 36, 112, 204, 255)
        set_theme_item(mvGuiCol_ResizeGrip, 204, 204, 204, 143)
        set_theme_item(mvGuiCol_ResizeGripHovered, 66, 150, 250, 171)
        set_theme_item(mvGuiCol_ResizeGripActive, 66, 150, 250, 242)
        set_theme_item(mvGuiCol_Tab, 195, 203, 213, 237)
        set_theme_item(mvGuiCol_TabHovered, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_TabActive, 152, 186, 225, 255)
        set_theme_item(mvGuiCol_TabUnfocused, 235, 236, 238, 251)
        set_theme_item(mvGuiCol_TabUnfocusedActive, 189, 209, 233, 255)
        set_theme_item(mvGuiCol_DockingPreview, 66, 150, 250, 55)
        set_theme_item(mvGuiCol_PlotLines, 99, 99, 99, 255)
        set_theme_item(mvGuiCol_PlotHistogramHovered, 255, 115, 0, 255)
        set_theme_item(mvGuiCol_DragDropTarget, 66, 150, 250, 242)
        set_theme_item(mvGuiCol_NavHighlight, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_NavWindowingHighlight, 179, 179, 179, 179)
        set_theme_item(mvGuiCol_NavWindowingDimBg, 51, 51, 51, 51)
        set_theme_item(mvGuiCol_ModalWindowDimBg, 51, 51, 51, 89)
    except Exception as e:
        print("styling error")
        print(e)

def managerView(acc):  
    def updateSupplierTable():
        clear_table('##SupplierTable')  
        try:
            conn = sqlite3.connect(databasePath,  check_same_thread=False)
            c = conn.cursor()
        except:
            print("failed connection")
        c.execute("SELECT * FROM SupplierTable")
        result = c.fetchall()

        #print(result)
            
        #add empty rows
        for i in range(0, len(result)+1):
            rowName = "##row " + str(i)
            add_row('##SupplierTable', [rowName])   
        #Add data from result
        for row in result:
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 0, value = str(row[0]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 1, value = str(row[1]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 2, value = str(row[2]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 3, value = str(row[3]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 4, value = str(row[4]))
            set_table_item(table = '##SupplierTable', row = row[0]-1, column = 5, value = str(row[5]))  
    def searchSupplier(sender, data):
        #clear_table("##ResultsTable")
        #get value
        idInput = get_value("##searchID")
        nameInput = get_value('##searchName')
        emailInput = get_value('##searchEmail')
        productInput = get_value('##searchProduct')
        creationInput = get_value('##searchCreation')
        expiryInput = get_value('##searchExpiry')
        inputArray = [idInput, nameInput, emailInput, productInput, creationInput, expiryInput]         
        parallelArray = ['SupplierID', 'SupplierName', 'SupplierEmail', 'Product', 'ContractCreationDate', 'ContractExpiryDate']
        for j in range(len(inputArray)):
            for i in range(len(inputArray)):
                try:
                    if inputArray[i] == "":
                        inputArray.pop(i)
                        parallelArray.pop(i)
                except:
                    continue    
        searchTerm = '' 
        for x in range(len(inputArray)):
            if len(inputArray)-x == 1:
                searchTerm = searchTerm + str(parallelArray[x]) + "='" + str(inputArray[x]) + "'"
            else:
                searchTerm = searchTerm + str(parallelArray[x]) + "='" + str(inputArray[x]) + "' and "  
        
        try:
            conn = sqlite3.connect(databasePath,  check_same_thread=False)
            c = conn.cursor()
        except:
            print("failed connection")

        c.execute("SELECT * FROM SupplierTable WHERE " + searchTerm + ";")
        value = c.fetchall()
        with popup(popupparent='Search', name='results', mousebutton=0, modal=True):                
            #add_text(value)
            add_table("##ResultsTable", headers = ['Supplier ID', 'Supplier Name', 'SupplierEmail', 'Product', 'ContractCreationDate', 'ContractExpiryDate'])
            clear_table("##ResultsTable")   
            #add empty rows
            for i in range(0, len(value)+1):
                rowName = "##row " + str(i)
                add_row('##ResultsTable', [rowName])                
            #Add data from result
            temp = 0
            for row in value:
                set_table_item(table = '##ResultsTable', row = temp, column = 0, value = str(row[0]))
                set_table_item(table = '##ResultsTable', row = temp, column = 1, value = str(row[1]))
                set_table_item(table = '##ResultsTable', row = temp, column = 2, value = str(row[2]))
                set_table_item(table = '##ResultsTable', row = temp, column = 3, value = str(row[3]))
                set_table_item(table = '##ResultsTable', row = temp, column = 4, value = str(row[4]))
                set_table_item(table = '##ResultsTable', row = temp, column = 5, value = str(row[5]))
                temp+=1
            add_button("Close##2", callback=lambda: close_popup("results"))
            add_dummy(width=800)    
        '''
        set_value("##searchID", value[0])
        set_value("##searchName", value[1])
        set_value("##searchEmail", value[2])
        set_value("##searchProduct", value[3])
        set_value("##searchCreation", value[4])
        set_value("##searchExpiry", value[5])
        '''         
    
    def supplierSelect(sender, data):
        #gets values from row of selected cell and coords in table
        coords = get_table_selections("##SupplierTable")
        temp = coords[0]
        row = temp[0]
        column = temp[1]
        value = []
        for i in range(6):
            value.append(get_table_item("##SupplierTable", row, i))
        
        set_value("##searchID", value[0])
        set_value("##searchName", value[1])
        set_value("##searchEmail", value[2])
        set_value("##searchProduct", value[3])
        set_value("##searchCreation", value[4])
        set_value("##searchExpiry", value[5])

        for i in range(6):
            set_table_selection('##SupplierTable', row, i, False)
    
    def supplierAdd(sender, data):
    
        try:
            try:
                conn = sqlite3.connect(databasePath,  check_same_thread=False)
                c = conn.cursor()
            except:
                print("failed connection")  
            idInput = get_value("##searchID").lower()
            nameInput = get_value('##searchName').lower()
            emailInput = get_value('##searchEmail').lower()
            productInput = get_value('##searchProduct').lower()
            creationInput = get_value('##searchCreation').lower()
            expiryInput = get_value('##searchExpiry').lower()
        
            
            if (nameInput != "" or emailInput != "" or productInput != "" or creationInput != "" or expiryInput != ""):

                c.execute("SELECT * FROM SupplierTable")
                tempResult = c.fetchall()

                command = ("INSERT INTO SupplierTable(SupplierID,SupplierName,SupplierEmail,Product,ContractCreationDate, ContractExpiryDate) VALUES(" + str(len(tempResult)+1) + ",'" + str(nameInput) + "','" + str(emailInput) + "','" + str(productInput) + "','" + str(creationInput) + "','" + str(expiryInput) + "');")
                c.execute(command)
                conn.commit()

                updateSupplierTable()

                set_value("##searchID", "")
                set_value("##searchName", "")
                set_value("##searchEmail", "")
                set_value("##searchProduct", "")
                set_value("##searchCreation", "")
                set_value("##searchExpiry", "")

            else:
                print("error")
        except Exception as e:
            print("error")

    def supplierDelete(sender, data):   
        try:
            conn = sqlite3.connect(databasePath,  check_same_thread=False)
            c = conn.cursor()
        except:
            print("failed connection")  


        idInput = get_value("##searchID")

        command = ("DELETE FROM SupplierTable WHERE SupplierID = " + str(idInput) + ";")
        c.execute(command)
        conn.commit()

        updateSupplierTable()
        
    def supplierReload(sender, data):
        updateSupplierTable()

    def supplierEdit(sender, data):
        #try:

            idInput = get_value("##searchID").lower()
            nameInput = get_value('##searchName').lower()
            emailInput = get_value('##searchEmail').lower()
            productInput = get_value('##searchProduct').lower()
            creationInput = get_value('##searchCreation').lower()
            expiryInput = get_value('##searchExpiry').lower()


            if (nameInput != "" or emailInput != "" or productInput != "" or creationInput != "" or expiryInput != ""):

                try:
                    conn = sqlite3.connect(databasePath,  check_same_thread=False)
                    c = conn.cursor()
                except:
                    print("failed connection")

                c.execute("SELECT * FROM SupplierTable")
                tempResult = c.fetchall()

                command = ("UPDATE SupplierTable SET SupplierName = '" + nameInput + "', SupplierEmail = '" + str(emailInput) + "', Product = '" + productInput + "', ContractCreationDate = '" + str(creationInput) + "', ContractExpiryDate = '" + expiryInput + "' WHERE SupplierID = " + str(idInput) + ";")
                c.execute(command)
                conn.commit()

                updateSupplierTable()

                set_value("##searchID", "")
                set_value("##searchName", "")
                set_value("##searchEmail", "")
                set_value("##searchProduct", "")
                set_value("##searchCreation", "")
                set_value("##searchExpiry", "")

            else:
                print("error")
        #except:
            #print("error")

    def addUser(sender, data):
        try:
            try:
                conn = sqlite3.connect(databasePath,  check_same_thread=False)
                c = conn.cursor()
            except:
                print("failed connection")  
            #gets values from entries
            nameInput = get_value("##inputAddName")
            emailInput = get_value("##inputAddEmail")
            passInput = get_value('##addUserPassword')        
            
            if (emailInput != "" or passInput != "" or nameInput != ""):

                c.execute("SELECT * FROM EmployeeTable")
                tempResult = c.fetchall()
                command = ("INSERT INTO EmployeeTable(EmployeeID,EmployeeName,EmployeeEmail,EmployeePassword) VALUES(" + str(len(tempResult)+1) + ",'" + str(nameInput) + "','" + str(emailInput) + "','" + str(passInput) +"');")
                c.execute(command)
                conn.commit()
                #placeholder for update table function
                set_value("##inputAddName", "")
                set_value("##inputAddEmail", "")
                set_value("##addUserPassword", "")
                

            else:
                print("error")
        except Exception as e:
            print("error")
            print(e)

    def createReport(sender, data):
        try:
            conn = sqlite3.connect(databasePath,  check_same_thread=False)
            c = conn.cursor()
        except:
            print("failed connection")  

        #make file and add title to it
        f = open(r"IA/tempReport.txt", "w+")
        f.write("                                                    Supplier Report")
        f.write("\n")
        f.write("\n")

        #get product types from database
        f.write("Product Types:")
        f.write("\n")
        c.execute("SELECT Product FROM SupplierTable;")
        value = c.fetchall()
        array = []
        array2 = []
        amount = []
        for i in range(len(value)):
            array2.append((value[i][0]).capitalize())
            if (value[i][0]).capitalize() not in array:
                array.append((value[i][0]).capitalize())
                f.write("    -")
                f.write((value[i][0]).capitalize())
                f.write("\n")

        count = Counter(array2)
        count = list(set(count.items()))

        #format data for pie chart
        amounts = []
        labels = []
        for i in range(len(count)):
            amounts.append(count[i][1])
            labels.append(count[i][0])

        f.write("\nProduct Distribution:\n")
        print("testpoint")
        f.close
        
        #make pie chart
        y = np.array(amounts)
        plt.pie(y, labels = labels)
        plt.savefig(r'IA/tempPieChart.png')

        #convert to PDF
        pdf = FPDF()   
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        f = open("IA/tempReport.txt", "r")
        text = f.readlines()
        for x in text:
            #pdf.cell(200, 20, txt = x, ln = 1, align = 'C')
            pdf.write(h=10, txt = x)
        pdf.image(name = r"IA/tempPieChart.png", w=200, h=150)
        pdf.output("IA/tempReport.pdf", 'F').encode('latin-1') 
        f.close()

        subprocess.Popen(r'explorer /select,"C:\Users\Albert Jantunen\OneDrive - Innoventures Education\year 12\Computer Science\IA\tempReport.pdf"')



    set_value("##volunteerID", "")

    hide_item('Login')
    set_main_window_size(1250, 800)
    try:
        conn = sqlite3.connect(databasePath,  check_same_thread=False)
        c = conn.cursor()
    except:
        print("failed connection")  
    with window("EmployeeView"):
        set_primary_window('EmployeeView', True)
        set_main_window_size(1250, 800)
        #header
        add_group(name='header', horizontal=True, horizontal_spacing=20)

        #button for file menu (popup)
        add_button(name='File')
        #add name of acc
        add_text(acc[0][1])

        end()

        #make popup for file menu
        with popup(popupparent='File', name='File##1', mousebutton=0, modal=True):
            #add Buttons for different popups
            add_button('Add User##button')
            #view reminders
            add_button('View Reminders##button')
            #Logout button
            add_button('Logout##button')
            #make a report
            add_button('Create Report##button', callback = createReport)
            #close button
            add_button("Close##4", callback=lambda: close_popup("File##1"))
            add_dummy(width=600)   

        #popup for logout confirmation
        with popup(popupparent='Logout##button', name='Logout##popup', mousebutton=0, modal=True):
            def confirm():
                #hide_item
                delete_item('ManagerView')
                global logout
                Logout = True

                show_item('Login')

            add_text("Are you sure you want to logout?")
            add_button("Yes", callback=confirm)
            add_button("Close##6", callback=lambda: close_popup("Logout##popup"))
            add_dummy(width=100)   
            
        #popup for viewing reminders
        with popup(popupparent='View Reminders##button', name='View Reminders##popup', mousebutton=0, modal=True):
            
            try:
                conn = sqlite3.connect(databasePath,  check_same_thread=False)
                c = conn.cursor()
            except:
                print("failed connection")

            c.execute("SELECT * FROM SupplierTable;")
            value = c.fetchall()

            #gets current date and formats it so it can be used with the database
            currentDate = str(date.today())
            currentDate = currentDate.split('-')
            currentDate = date(int(currentDate[0]), int(currentDate[1]), int(currentDate[2]))
            
            expiring = []
            for supplier in range(len(value)):
                iDate = value[supplier][5]
                iDate = iDate.split('/')
                iDate = date(int('20'+iDate[2]), int(iDate[1]), int(iDate[0]))

                daysBetween = (iDate - currentDate).days

                if  daysBetween <= 7: 
                    expiring.append(value[supplier])

            value=expiring
            
            add_table("##ExpiringTable", headers = ['Supplier ID', 'Supplier Name', 'SupplierEmail', 'Product', 'ContractCreationDate', 'ContractExpiryDate'])
            clear_table("##ExpiringTable")
            #add empty rows
            for i in range(0, len(value)+1):
                rowName = "##row " + str(i)
                add_row('##ExpiringTable', [rowName])
            #Add data from result
            temp = 0
            for row in value:
                set_table_item(table = '##ExpiringTable', row = temp, column = 0, value = str(row[0]))
                set_table_item(table = '##ExpiringTable', row = temp, column = 1, value = str(row[1]))
                set_table_item(table = '##ExpiringTable', row = temp, column = 2, value = str(row[2]))
                set_table_item(table = '##ExpiringTable', row = temp, column = 3, value = str(row[3]))
                set_table_item(table = '##ExpiringTable', row = temp, column = 4, value = str(row[4]))
                set_table_item(table = '##ExpiringTable', row = temp, column = 5, value = str(row[5]))
                temp+=1

            add_button("Close##3", callback = lambda:close_popup("View Reminders##popup"))
            add_dummy(width=800)
            #end()

        #popup for adding new users in file menu
        with popup(popupparent='Add User##button', name='Add User##popup', mousebutton=0, modal=True):
            #groups for organization
            add_group('full')
            add_group('nameParent', horizontal=True)
            add_text('Name: ')
            add_input_text('##inputAddName')
            end()
            add_group('EmailParent', horizontal=True)
            add_text('Email: ')
            add_input_text('##inputAddEmail')
            end()
            add_group('PasswordParent', horizontal=True)
            add_text('Password: ')
            add_input_text('##addUserPassword')
            end()
            #button to create user
            add_button('Add##user', callback=addUser)
            
            add_button("Close##9", callback = lambda:close_popup("Add User##popup"))
            add_dummy(width=80)
            end()

        with popup(popupparent='Create Report##button', name='Create Report##popup', mousebutton=0, modal=True):
            #open and make title
            add_text("created")

            add_button("Close##5", callback=lambda: close_popup("Create Report##popup"))
            add_dummy(width=80)

        set_main_window_size(1250, 800)


        #add logo
        add_image(name = 'logo', value = imagePath, width = round(1584/1.285), height = round(296/1.285))
        
        #formatting + adding entry fields
        add_group(name = 'parent', horizontal= True, horizontal_spacing= 20)            
        add_dummy(width=50) 
        add_group(name = 'column1', width = 75)
        add_text("ID")
        add_input_text("##searchID")
        end()   
        add_group(name = "column2", width = 150)
        add_text('Name')
        add_input_text("##searchName")
        end()   
        add_group(name = "column3", width = 150)
        add_text('Email')
        add_input_text("##searchEmail")
        end()           
        add_group(name = "column4", width = 150)
        add_text('Product')
        add_input_text("##searchProduct")
        end()           
        add_group(name = "column5", width = 150)
        add_text('Contract Creation')
        add_input_text("##searchCreation")
        end()   
        add_group(name = "column6", width = 150)
        add_text('Contract Expiry')
        add_input_text("##searchExpiry")
        end()       
        add_group(name = "column7", width = 150)
        add_text("")
        add_button("Search", callback=searchSupplier)
        end()           
        
        end()

        #formatting + addint buttons
        add_group(name = 'buttons', horizontal= True, horizontal_spacing= 20)
        add_group(name='column8', width = 150)
        add_text('')
        add_button('Select', callback=supplierSelect)
        end()
        add_group(name='column9', width = 150)
        add_text('')
        add_button('Add', callback=supplierAdd)
        end()
        add_group(name='column10', width = 150)
        add_text('')
        add_button('Delete', callback=supplierDelete)
        end()
        add_group(name = "column11", width = 150)
        add_text("")
        add_button("Reload", callback=supplierReload)
        end()
        add_group(name = "column12", width = 150)
        add_text("")
        add_button("Edit", callback=supplierEdit)
        end()           
        end()

        #make table
        add_table("##SupplierTable", headers = ['Supplier ID', 'Supplier Name', 'SupplierEmail', 'Product', 'ContractCreationDate', 'ContractExpiryDate'])
        updateSupplierTable()           
    try:
        set_main_window_resizable(True)
        set_main_window_size(1250, 800)
        set_style_window_padding(8.00, 8.00)
        set_style_frame_padding(4.00, 3.00)
        set_style_item_spacing(8.00, 4.00)
        set_style_item_inner_spacing(4.00, 4.00)
        set_style_touch_extra_padding(0.00, 0.00)
        set_style_indent_spacing(21.00)
        set_style_scrollbar_size(14.00)
        set_style_grab_min_size(10.00)
        set_style_window_border_size(0.00)
        set_style_child_border_size(1.00)
        set_style_popup_border_size(1.00)
        set_style_frame_border_size(0.00)
        set_style_tab_border_size(0.00)
        set_style_window_rounding(7.00)
        set_style_child_rounding(0.00)
        set_style_frame_rounding(3.00)
        set_style_popup_rounding(0.00)
        set_style_scrollbar_rounding(9.00)
        set_style_grab_rounding(3.00)
        set_style_tab_rounding(4.00)
        set_style_window_title_align(0.00, 0.50)
        set_style_window_menu_button_position(mvDir_Left)
        set_style_color_button_position(mvDir_Right)
        set_style_button_text_align(0.50, 0.50)
        set_style_selectable_text_align(0.00, 0.00)
        set_style_display_safe_area_padding(3.00, 3.00)
        set_style_global_alpha(1.00)
        set_style_antialiased_lines(True)
        set_style_antialiased_fill(True)
        set_style_curve_tessellation_tolerance(1.25)
        set_style_circle_segment_max_error(1.60)
        set_theme_item(mvGuiCol_Text, 0, 0, 0, 255)
        set_theme_item(mvGuiCol_TextDisabled, 153, 153, 153, 255)
        set_theme_item(mvGuiCol_WindowBg, 240, 240, 240, 255)
        set_theme_item(mvGuiCol_PopupBg, 255, 255, 255, 250)
        set_theme_item(mvGuiCol_Border, 0, 0, 0, 77)
        set_theme_item(mvGuiCol_FrameBg, 255, 255, 255, 255)
        set_theme_item(mvGuiCol_FrameBgHovered, 66, 150, 250, 102)
        set_theme_item(mvGuiCol_FrameBgActive, 66, 150, 250, 171)
        set_theme_item(mvGuiCol_TitleBg, 245, 245, 245, 255)
        set_theme_item(mvGuiCol_TitleBgActive, 209, 209, 209, 255)
        set_theme_item(mvGuiCol_TitleBgCollapsed, 255, 255, 255, 130)
        set_theme_item(mvGuiCol_MenuBarBg, 219, 219, 219, 255)
        set_theme_item(mvGuiCol_ScrollbarBg, 250, 250, 250, 135)
        set_theme_item(mvGuiCol_ScrollbarGrab, 176, 176, 176, 204)
        set_theme_item(mvGuiCol_ScrollbarGrabHovered, 125, 125, 125, 204)
        set_theme_item(mvGuiCol_ScrollbarGrabActive, 125, 125, 125, 255)
        set_theme_item(mvGuiCol_CheckMark, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_SliderGrab, 66, 150, 250, 199)
        set_theme_item(mvGuiCol_SliderGrabActive, 117, 138, 204, 153)
        set_theme_item(mvGuiCol_Button, 66, 150, 250, 102)
        set_theme_item(mvGuiCol_ButtonHovered, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_ButtonActive, 15, 135, 250, 255)
        set_theme_item(mvGuiCol_Header, 66, 150, 250, 79)
        set_theme_item(mvGuiCol_HeaderHovered, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_HeaderActive, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_Separator, 99, 99, 99, 158)
        set_theme_item(mvGuiCol_SeparatorHovered, 36, 112, 204, 199)
        set_theme_item(mvGuiCol_SeparatorActive, 36, 112, 204, 255)
        set_theme_item(mvGuiCol_ResizeGrip, 204, 204, 204, 143)
        set_theme_item(mvGuiCol_ResizeGripHovered, 66, 150, 250, 171)
        set_theme_item(mvGuiCol_ResizeGripActive, 66, 150, 250, 242)
        set_theme_item(mvGuiCol_Tab, 195, 203, 213, 237)
        set_theme_item(mvGuiCol_TabHovered, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_TabActive, 152, 186, 225, 255)
        set_theme_item(mvGuiCol_TabUnfocused, 235, 236, 238, 251)
        set_theme_item(mvGuiCol_TabUnfocusedActive, 189, 209, 233, 255)
        set_theme_item(mvGuiCol_DockingPreview, 66, 150, 250, 55)
        set_theme_item(mvGuiCol_PlotLines, 99, 99, 99, 255)
        set_theme_item(mvGuiCol_PlotHistogramHovered, 255, 115, 0, 255)
        set_theme_item(mvGuiCol_DragDropTarget, 66, 150, 250, 242)
        set_theme_item(mvGuiCol_NavHighlight, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_NavWindowingHighlight, 179, 179, 179, 179)
        set_theme_item(mvGuiCol_NavWindowingDimBg, 51, 51, 51, 51)
        set_theme_item(mvGuiCol_ModalWindowDimBg, 51, 51, 51, 89)
    except Exception as e:
        print("styling error")
        print(e)

def checkLogin(sender, data):
    
    #gets input from entry fields
    emailGet = get_value('##email')
    passGet = get_value('##password')
    #connects to database
    try:
        conn = sqlite3.connect(databasePath,  check_same_thread=False)
        c = conn.cursor()
    except Exception as e:
        print("failed connection") 
        print(e)

    #first execute is getting the result if the username and password are entered wrong and the second and third executes check if the username and password exist in the database.
    c.execute("SELECT * FROM EmployeeTable WHERE EmployeeEmail='" + 'testsetsetstdst' + "' and EmployeePassword='" + 'tesdt' + "'")
    compare=c.fetchall()
    c.execute("SELECT * FROM EmployeeTable WHERE EmployeeEmail='" + emailGet + "' and EmployeePassword='" + passGet + "'")
    empTest=c.fetchall()
    c.execute("SELECT * FROM ManagerTable WHERE ManagerEmail='" + emailGet + "' and ManagerPassword='" + passGet + "'")
    manTest=c.fetchall()
    add_text("##passwordConfirmation", parent='Login')
    
    #if the username and password dont return an error from the database then the appropriate gui is opened.
    if empTest != compare:
        if logout == False:
            employeeView(empTest)
            set_value("##passwordConfirmation", "")
        else:
            hide_item("Login")
            show_item("employeeView")
            set_value("##passwordConfirmation", "")
    elif manTest != compare:
        if logout == False:
            managerView(manTest)
            set_value("##passwordConfirmation", "")
        else:
            hide_item("Login")
            show_item("ManagerView")
            set_value("##passwordConfirmation", "")
    else:
        #otherwise show an error message
        set_value("##passwordConfirmation", "Email or Password Incorrect")

with window("Login"):
    
    #add logo
    add_image(name = 'icon', value = iconPath, width = round(397/4), height = round(435/4))

    #entry field for email
    add_text("Email")
    add_input_text(name = '##email', hint='...', default_value='')
    
    #entry field for password password=True makes text *
    add_text("Password")
    add_input_text(name='##password', hint='...', default_value="", password=True)

    #login button which activates the function above to check the credentials
    add_button("Login##Button", callback=checkLogin)

    try:
        set_main_window_resizable(True)
        set_main_window_size(300, 400)
        set_style_window_padding(8.00, 8.00)
        set_style_frame_padding(4.00, 3.00)
        set_style_item_spacing(8.00, 4.00)
        set_style_item_inner_spacing(4.00, 4.00)
        set_style_touch_extra_padding(0.00, 0.00)
        set_style_indent_spacing(21.00)
        set_style_scrollbar_size(14.00)
        set_style_grab_min_size(10.00)
        set_style_window_border_size(0.00)
        set_style_child_border_size(1.00)
        set_style_popup_border_size(1.00)
        set_style_frame_border_size(0.00)
        set_style_tab_border_size(0.00)
        set_style_window_rounding(7.00)
        set_style_child_rounding(0.00)
        set_style_frame_rounding(3.00)
        set_style_popup_rounding(0.00)
        set_style_scrollbar_rounding(9.00)
        set_style_grab_rounding(3.00)
        set_style_tab_rounding(4.00)
        set_style_window_title_align(0.00, 0.50)
        set_style_window_menu_button_position(mvDir_Left)
        set_style_color_button_position(mvDir_Right)
        set_style_button_text_align(0.50, 0.50)
        set_style_selectable_text_align(0.00, 0.00)
        set_style_display_safe_area_padding(3.00, 3.00)
        set_style_global_alpha(1.00)
        set_style_antialiased_lines(True)
        set_style_antialiased_fill(True)
        set_style_curve_tessellation_tolerance(1.25)
        set_style_circle_segment_max_error(1.60)
        set_theme_item(mvGuiCol_Text, 0, 0, 0, 255)
        set_theme_item(mvGuiCol_TextDisabled, 153, 153, 153, 255)
        set_theme_item(mvGuiCol_WindowBg, 240, 240, 240, 255)
        set_theme_item(mvGuiCol_PopupBg, 255, 255, 255, 250)
        set_theme_item(mvGuiCol_Border, 0, 0, 0, 77)
        set_theme_item(mvGuiCol_FrameBg, 255, 255, 255, 255)
        set_theme_item(mvGuiCol_FrameBgHovered, 66, 150, 250, 102)
        set_theme_item(mvGuiCol_FrameBgActive, 66, 150, 250, 171)
        set_theme_item(mvGuiCol_TitleBg, 245, 245, 245, 255)
        set_theme_item(mvGuiCol_TitleBgActive, 209, 209, 209, 255)
        set_theme_item(mvGuiCol_TitleBgCollapsed, 255, 255, 255, 130)
        set_theme_item(mvGuiCol_MenuBarBg, 219, 219, 219, 255)
        set_theme_item(mvGuiCol_ScrollbarBg, 250, 250, 250, 135)
        set_theme_item(mvGuiCol_ScrollbarGrab, 176, 176, 176, 204)
        set_theme_item(mvGuiCol_ScrollbarGrabHovered, 125, 125, 125, 204)
        set_theme_item(mvGuiCol_ScrollbarGrabActive, 125, 125, 125, 255)
        set_theme_item(mvGuiCol_CheckMark, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_SliderGrab, 66, 150, 250, 199)
        set_theme_item(mvGuiCol_SliderGrabActive, 117, 138, 204, 153)
        set_theme_item(mvGuiCol_Button, 66, 150, 250, 102)
        set_theme_item(mvGuiCol_ButtonHovered, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_ButtonActive, 15, 135, 250, 255)
        set_theme_item(mvGuiCol_Header, 66, 150, 250, 79)
        set_theme_item(mvGuiCol_HeaderHovered, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_HeaderActive, 66, 150, 250, 255)
        set_theme_item(mvGuiCol_Separator, 99, 99, 99, 158)
        set_theme_item(mvGuiCol_SeparatorHovered, 36, 112, 204, 199)
        set_theme_item(mvGuiCol_SeparatorActive, 36, 112, 204, 255)
        set_theme_item(mvGuiCol_ResizeGrip, 204, 204, 204, 143)
        set_theme_item(mvGuiCol_ResizeGripHovered, 66, 150, 250, 171)
        set_theme_item(mvGuiCol_ResizeGripActive, 66, 150, 250, 242)
        set_theme_item(mvGuiCol_Tab, 195, 203, 213, 237)
        set_theme_item(mvGuiCol_TabHovered, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_TabActive, 152, 186, 225, 255)
        set_theme_item(mvGuiCol_TabUnfocused, 235, 236, 238, 251)
        set_theme_item(mvGuiCol_TabUnfocusedActive, 189, 209, 233, 255)
        #set_theme_item(mvGuiCol_DockingPreview, 66, 150, 250, 55)
        set_theme_item(mvGuiCol_PlotLines, 99, 99, 99, 255)
        set_theme_item(mvGuiCol_PlotHistogramHovered, 255, 115, 0, 255)
        set_theme_item(mvGuiCol_DragDropTarget, 66, 150, 250, 242)
        set_theme_item(mvGuiCol_NavHighlight, 66, 150, 250, 204)
        set_theme_item(mvGuiCol_NavWindowingHighlight, 179, 179, 179, 179)
        set_theme_item(mvGuiCol_NavWindowingDimBg, 51, 51, 51, 51)
        set_theme_item(mvGuiCol_ModalWindowDimBg, 51, 51, 51, 89)
    except error as e:
        print("styling error")
        print(e)

set_main_window_resizable(True)
#show_documentation()
start_dearpygui(primary_window="Login")

