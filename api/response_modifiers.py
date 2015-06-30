# coding=utf-8
def modifier_select_rsp_contracts(parametersDict):
    '''
    модификатор входных параметров апи для коллекции контрактов
    '''
    maxResultsPerQuery = 50
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    returnfields = {
        "_id": 1,
        "id": 1,
        "regNum": 1,
        "price": 1,
        "signDate": 1,
        "customer.fullName": 1,
        "customer.inn": 1,
        "customer.kpp": 1,
        "customer.regNum": 1,
        "products": 1,
        "fz": 1,
        "regionCode": 1,
        "suppliers": 1,
        "misuses": 1,
        "finances.budgetary": 1,

        'name': 1,
        "publishDate": 1,
        'economic_sectors': 1
    }
    try:
        parametersDict["supplierinn"] = parametersDict["supplierinn"].replace("%20", " ")
    except:
        pass
    try:
        parametersDict["supplierkpp"] = parametersDict["supplierkpp"].replace("%20", " ")
    except:
        pass
    if parametersDict.get("returnfields", None) == None:
        parametersDict["returnfields"] = returnfields
    else:
        pass
    return parametersDict


def modifier_select_rsp_notifications(parametersDict):
    '''
    модификатор входных параметров апи для коллекции контрактов
    '''
    maxResultsPerQuery = 50
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    if parametersDict.get("returnfields", None):
        parametersDict["returnfields"] = {
            "number": 1,
            "placingWay": 1,
            "orderName": 1,
            "lots": 1,
            'lot': 1,
            'regionCode': 1,
            "publishDate": 1,
            "notificationCommission": 1,
            "contactInfo": 1,
            "href": 1,
            "documentMetas": 1
        }
    return parametersDict


def modifier_select_rsp_grants(parametersDict):
    '''
    модификатор входных параметров апи для коллекции контрактов
    '''
    maxResultsPerQuery = 50
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    if parametersDict.get("returnfields", None):
        parametersDict["returnfields"] = {
            "name_organization": 1,
            "status": 1,
            "grant_status": 1,
            "description": 1,
            "grant": 1,
            "price": 1,
            "site": 1,
            "OGRN": 1,
            "filing_date": 1,
            "form_number": 1,
            "address": 1,
            "operator": 1,
            "name_project": 1,
        }
    return parametersDict


def modifier_select_rsp_invalidcontracts(parametersDict):
    '''
    модификатор входных параметров апи для коллекции контрактов с проблемными инн/кпп
    '''
    maxResultsPerQuery = 50
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    try:
        parametersDict["supplierinn"] = parametersDict["supplierinn"].replace("%20", " ")
    except:
        pass
    try:
        parametersDict["supplierkpp"] = parametersDict["supplierkpp"].replace("%20", " ")
    except:
        pass
    return parametersDict


def modifier_select_rsp_customers(parametersDict):
    '''
    модификатор входных параметров апи для коллекции заказчиков
    '''
    maxResultsPerQuery = 50
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    returnfields = {
        "_id": 1,
        "id": 1,
        "regNumber": 1,
        "fullName": 1,
        "inn": 1,
        "kpp": 1,
        "contractsSum": 1,
        "contractsCount": 1,
        "_orgClass": 1
    }
    if parametersDict.get("returnfields", None) == None:
        parametersDict["returnfields"] = returnfields
    else:
        pass
    return parametersDict


def modifier_select_rsp_suppliers(parametersDict):
    '''
    модификатор входных параметров апи для коллекции поставщиков
    '''
    maxResultsPerQuery = 50
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    try:
        parametersDict["inn"] = parametersDict["inn"].replace("%20", " ")
    except:
        pass
    try:
        parametersDict["kpp"] = parametersDict["kpp"].replace("%20", " ")
    except:
        pass
    return parametersDict


def modifier_select_rsp_dictionaries(parametersDict):
    '''
    модификатор входных параметров апи для коллекций справочников
    '''
    maxResultsPerQuery = 1000
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    return parametersDict


def modifier_get_notifications_rsp(parametersDict):
    if not parametersDict.get("returnfields", None):
        parametersDict["returnfields"] = {
            "number": 1,
            "placingWay": 1,
            "orderName": 1,
            'purchaseObjectInfo': 1,
            'purchaseResponsible': 1,
            'procedureInfo': 1,
            "lots": 1,
            'lot': 1,
            'fz': 1,
            "publishDate": 1,
            'regionCode': 1,
            "notificationCommission": 1,
            "contactInfo": 1,
            "href": 1,
            "documentMetas": 1,
            'customers': 1,
        }
    return parametersDict


def modifier_get_grants_rsp(parametersDict):
    if not parametersDict.get("returnfields", None):
        parametersDict["returnfields"] = {
            "name_organization": 1,
            "status": 1,
            "grant_status": 1,
            "description": 1,
            "grant": 1,
            "price": 1,
            "site": 1,
            "OGRN": 1,
            "filing_date": 1,
            "form_number": 1,
            "address": 1,
            "operator": 1,
            "name_project": 1,
        }
    return parametersDict


def modifier_get_rsp(parametersDict):
    '''
    модификатор входных параметров апи всех get-запросов
    '''
    parametersDict["perpage"] = 1
    try:
        parametersDict["supplierinn"] = parametersDict["supplierinn"].replace("%20", " ")
    except:
        pass
    try:
        parametersDict["supplierkpp"] = parametersDict["supplierkpp"].replace("%20", " ")
    except:
        pass
    try:
        parametersDict["inn"] = parametersDict["inn"].replace("%20", " ")
    except:
        pass
    try:
        parametersDict["kpp"] = parametersDict["kpp"].replace("%20", " ")
    except:
        pass
    return parametersDict


def modifier_top_rsp_contracts(parametersDict):
    '''
    модификатор входных параметров апи для коллекции топ контрактов
    '''
    maxResultsPerQuery = 100
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    returnfields = {
        "year": 1,
        "regNum": 1,
        "price": 1,
        "signDate": 1,
        "customer.fullName": 1,
        "customer.inn": 1,
        "customer.kpp": 1,
        "customer.regNum": 1,
        "regionCode": 1,
        "products": 1,
        "suppliers": 1
    }
    if parametersDict.get("returnfields", None) == None:
        parametersDict["returnfields"] = returnfields
    else:
        pass
    return parametersDict


def modifier_top_rsp_notifications(parametersDict):
    '''
    модификатор входных параметров апи для коллекции топ контрактов
    '''
    maxResultsPerQuery = 100
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    if parametersDict.get("returnfields", None):
        parametersDict["returnfields"] = {
            "number": 1,
            "placingWay": 1,
            "orderName": 1,
            "lots": 1,
            'lot': 1,
            'regionCode': 1,
            "publishDate": 1,
            "notificationCommission": 1,
            "contactInfo": 1,
            "href": 1,
            "documentMetas": 1,
        }
    return parametersDict


def modifier_top_rsp_grants(parametersDict):
    '''
    модификатор входных параметров апи для коллекции топ контрактов
    '''
    maxResultsPerQuery = 100
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    if parametersDict.get("returnfields", None):
        parametersDict["returnfields"] = {
            "name_organization": 1,
            "status": 1,
            "grant_status": 1,
            "description": 1,
            "grant": 1,
            "price": 1,
            "site": 1,
            "OGRN": 1,
            "filing_date": 1,
            "form_number": 1,
            "address": 1,
            "operator": 1,
            "name_project": 1,
        }
    return parametersDict


def modifier_top_rsp_organizations(parametersDict):
    '''
    модификатор входных параметров апи для коллекции топ заказчиков и поставщиков
    '''
    maxResultsPerQuery = 100
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    returnfields = {u"_id": 0}
    if parametersDict.get("returnfields", None) == None:
        parametersDict["returnfields"] = returnfields
    else:
        pass
    return parametersDict


def modifier_top_rsp_farma(parametersDict):
    '''
    модификатор входных параметров апи для коллекции топ заказчиков и поставщиков
    '''
    maxResultsPerQuery = 100
    try:
        perpage = int(parametersDict.get("perpage", maxResultsPerQuery))
    except:
        perpage = maxResultsPerQuery
    if perpage > maxResultsPerQuery or perpage == 0: perpage = maxResultsPerQuery
    parametersDict["perpage"] = perpage
    if not parametersDict.get("returnfields", None):
        parametersDict["returnfields"] = {
            "_id": 0,
            "name": 1,
            "share": 1,
            "summ": 1,
            "inn": 1,
            "num": 1,
        }
    return parametersDict
