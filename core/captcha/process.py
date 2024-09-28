from PIL import Image


# COLS
def find_white_cols(image_path: str) -> list[int]:
    
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    width, height = img.size
    col_results = []
    
    for col in range(width):
        
        column_has_white = False
                
        for row in range(height):
            r, g, b = img.getpixel((col, row))
            if (r, g, b) == (255, 255, 255):
                column_has_white = True
                break
        
        col_results.append(int(column_has_white))   
    
    return col_results                    

def find_prev_white_cols(cols: list[int]) -> list[int]:
    
    size = len(cols)
    res = []
    prev_white = cols[0]
    
    for i in range(1,size):
        cur = cols[i]
        if prev_white and not cur:
            res.append(i)
        prev_white = cur
    
    return res
            
def find_next_white_cols(cols: list[int]) -> list[int]:
    
    size = len(cols)
    res = []
    prev_white = cols[0]
    
    for i in range(1,size):
        cur = cols[i]
        if cur and not prev_white:
            res.append(i-1)
        prev_white = cur
    
    return res

def find_surrounded_white_cols(cols: list[int]) -> list[int]:
    
    size = len(cols)
    res = []
    
    prev_prev_white = cols[0]
    prev_white = cols[1]
    
    for i in range(2,size-2):
        cur = cols[i]
        if cur and prev_prev_white and not prev_white:
            res.append(i-1)
        prev_prev_white = prev_white
        prev_white = cur
    
    return res


# ROWS
def find_white_rows(image_path: str) -> list[int]:
    
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    width, height = img.size
    row_results = []
    
    for row in range(height):
        
        row_result = []
        row_has_white = False
                
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if (r, g, b) == (255, 255, 255):
                row_result.append(1)
            else:
                row_result.append(0)
        
        row_results.append(row_result)
    
    return row_results

def find_prev_white_rows(rows: list[int]) -> list[int]:
        
    size = len(rows)
    res = []
    prev_white = rows[0]
    
    for i in range(1, size):
        cur = rows[i]
        if prev_white and not cur:
            res.append(i)
        prev_white = cur
    
    return res

def find_next_white_rows(rows: list[int]) -> list[int]:
        
    size = len(rows)
    res = []
    prev_white = rows[0]
    
    for i in range(1, size):
        cur = rows[i]
        if cur and not prev_white:
            res.append(i-1)
        prev_white = cur
    
    return res

def find_surrounded_white_rows(rows: list[int]) -> list[int]:
    
    size = len(rows)
    res = []
    
    prev_prev_white = rows[0]
    prev_white = rows[1]
    
    for i in range(2, size-2):
        cur = rows[i]
        if cur and prev_prev_white and not prev_white:
            res.append(i-1)
        prev_prev_white = prev_white
        prev_white = cur
    
    return res
    

# Test
for i in range(1, 1005):
    non_white_cols = find_prev_white_cols(find_white_cols("tmp/images/" + str(i) + ".png"))
    print(i,non_white_cols)