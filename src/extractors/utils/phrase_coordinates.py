class PhraseCoordinates:
   def __init__(self, page_number, x0, y0, x1, y1):
       self.page_number = page_number
       self.x0 = x0
       self.y0 = y0
       self.x1 = x1
       self.y1 = y1
  
   def __repr__(self):
       return f"PhraseCoordinates(page_number={self.page_number}, x0={self.x0}, y0={self.y0}, x1={self.x1}, y1={self.y1})"