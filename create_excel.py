import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Inventory"

# Headers
ws.append([
    "external_code", "book_reference", "quantity_available",
    "quantity_reserved", "condition", "defects", "observations"
])

# Valid rows
ws.append(["EXT001", "REF-GATSBY", 5, 0, "new", "", "First edition"])
ws.append(["EXT002", "REF-ORWELL", 3, 1, "good", "", "Good condition"])
ws.append(["EXT003", "REF-TOLKIEN", 2, 0, "worn", "Cover slightly damaged", "Pages intact"])
ws.append(["EXT004", "REF-AUSTEN", 8, 0, "new", "", ""])
ws.append(["EXT005", "REF-KAFKA", 1, 0, "damaged", "Water damage on pages 10-20", "Still readable"])

# Invalid rows (to show validation)
ws.append(["", "REF-INVALID1", 3, 0, "new", "", ""])  # missing external_code
ws.append(["EXT007", "REF-INVALID2", 2, 0, "broken", "", ""])  # invalid condition
ws.append(["EXT008", "REF-INVALID3", 4, 0, "worn", "", ""])  # worn without defects

wb.save("test_inventory.xlsx")
print("File created: test_inventory.xlsx")
