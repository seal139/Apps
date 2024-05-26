import math

from ..models import Stock

def select() -> list :
    records = list(Stock.objects.all().values())

    if len(records) == 0 :
        return None
    #end if

    id = 0
    records.sort(key = lambda record: (record['year'], record['month']))
    for record in records :
        id += 1
        record['id']       = id
        record['avgStock'] = record['avgStock'] ** 2
    #end for

    return records
#end def

def insert(entity: dict) -> str :
    month    = entity['param0']
    year     = entity['param1']
    avgStock = entity['param2']

    if Stock.objects.filter (
        month = month,
        year  = year
    ).exists() : return 'Data already exist'

    Stock (
        year     = year, 
        month    = month, 
        avgStock = math.sqrt(int(avgStock))
    ).save()
    
    return None
#end def

def bulkInsert(entities: list) -> str :
    for row in entities:
        month    = row['month']
        year     = row['year']
        avgStock = row['stock']

        errMsg = __valueValidator(month, year, avgStock)
        if errMsg != None :
            return errMsg
        #end if

        if Stock.objects.filter (
            month = month,
            year  = year
        ).exists() : continue

        Stock (
            year     = year, 
            month    = month, 
            avgStock = math.sqrt(int(avgStock))
        ).save()        
    #end for

    return None
#end def

def update(entity: dict) -> str :
    month    = entity['param0']
    year     = entity['param1']
    avgStock = entity['param2']

    errMsg = __valueValidator(month, year, avgStock)
    if errMsg != None :
        return errMsg
    #end if
    
    record = Stock.objects.get(year = year, month = month)
    if record == None :
        return 'Data not exist'
    #end if

    record.avgStock = math.sqrt(int(avgStock))

    record.save()
    return None
#end def
    
def delete(entity: dict) -> str :
    lastRecord = select()[-1]
    lastYear   = lastRecord['year']
    lastMonth  = lastRecord['month']

    month = int(entity['param0'])
    year  = int(entity['param1'])

    if year != lastYear :        
        return 'Can only delete last data'
    #end if

    if month != lastMonth :        
        return 'Can only delete last data'
    #end if
    
    record = Stock.objects.get(year = year, month = month)
    if record == None :
        return 'Data not exist'
    #end if
    
    record.delete()
    return None
#end def

def __valueValidator(month, year, avgStock) -> str :
    intMonth = int(month)
    intYear  = int(year)
    intStock = int(avgStock)

    if intMonth < 1 or intMonth > 12:
        return 'Invalid value for month'
    #end if
    
    if intYear < 1900 or intYear > 2200:
        return 'Invalid value for year'
    #end if
    
    if intStock < 0:
        return 'Invalid value for avgStock'
    #end if
#end def