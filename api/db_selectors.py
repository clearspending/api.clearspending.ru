# -*- coding: utf-8 -*-
# HINT: str.encode("UTF-8")
import logging
from time import mktime

from pymongo import MongoClient
from bson import objectid

import memcache

import MySQLdb as Sphinx

from common.settings import MONGO_SERVER, MONGO_PORT, MEMCACHE_ENABLED, MEMCACHED_SERVER, MEMCACHED_PORT, SPHNX_IP, \
    SPHNX_PORT, SPHNX_LIMIT, \
    SPHNX_LIMIT_REPORT, MONGO_LIMIT_REPORT
from common.query_settings import APIdict, notUseParameterVal, typeFunctions, operatorsDontModify, share_parameters
from api.snippets import dbid
from api.converting_response_format import preparation_response, pretty_data, get_report


try:
    MNGclient = MongoClient("mongodb://" + MONGO_USER + ":" + MONGO_PWD + "@" + MONGO_SERVER + ":" + str(MONGO_PORT))
except NameError:
    MNGclient = MongoClient(MONGO_SERVER, MONGO_PORT)
    logging.info("Mongo connection without auth!")

if MEMCACHE_ENABLED:
    mc = memcache.Client([MEMCACHED_SERVER + ':' + str(MEMCACHED_PORT)], debug=0)


def mongo_request(dataset_name, mongo_db_client, db_name, db_collection_name, find_dict, return_fields, per_page,
                  page_num, sort_field=None, sort_direction=None):
    """
    Запрос к базе данных mongoDB
    :return: строка с ответом из базы данных в формате JSON
    """
    response_format = find_dict.pop('format', '')
    report = find_dict.pop('get_report', False)

    if not return_fields: return_fields = {u"FakeField": 0}
    if len(return_fields) == 0: return_fields[u"FakeField"] = 0
    if page_num > 0: page_num -= 1

    if report:
        per_page = MONGO_LIMIT_REPORT

    mongo_db = mongo_db_client[db_name]
    mongo_collection = mongo_db[db_collection_name]
    if sort_field is None or sort_direction is None:
        data_cursor = mongo_collection.find(find_dict, return_fields).limit(per_page).skip(per_page * page_num)
    else:
        try:
            data_cursor = mongo_collection.find(find_dict, return_fields).sort(sort_field, direction=sort_direction).limit(
                per_page) \
                .skip(per_page * page_num)
        except:
            data_cursor = mongo_collection.find(find_dict, return_fields).limit(per_page).skip(per_page * page_num)
    total = data_cursor.count()
    total_on_page = data_cursor.count(True)
    mongo_db_client.disconnect()

    if report and total_on_page > 0:
        data_str = get_report(data_cursor)
    elif total_on_page > 0:
        data_str = pretty_data(data_cursor, dataset_name, total, per_page, page_num, response_format,
                               keys=return_fields)
    else:
        data_str = None
    return data_str


def mongo_request_sorted(Dataset_Name, MongoDBClient, DB_Name, DB_collectionName, findDict, returnFields, sortField,
                         sortDirection, perPage, pageN):
    """
    Запрос к базе данных mongoDB
    :return: строка с ответом из базы данных в формате JSON
    """
    if not returnFields: returnFields = {u"FakeField": 0}
    if len(returnFields) == 0: returnFields[u"FakeField"] = 0
    if pageN > 0: pageN -= 1
    MNGdb = MongoDBClient[DB_Name]
    MNGcoll = MNGdb[DB_collectionName]
    dataCursor = MNGcoll.find(findDict, returnFields).sort(sortField, direction=sortDirection).limit(perPage).skip(
        perPage * pageN)
    total = dataCursor.count()
    totalOnPage = dataCursor.count(True)
    MongoDBClient.disconnect()
    if totalOnPage > 0:
        # TODO: заглушка на json
        dataStr = preparation_response(dataCursor, Dataset_Name, total, perPage, pageN, "json")
    else:
        dataStr = None
    return dataStr


def mongo_requestIN(dataset_name, mongo_db_client, db_name, db_collection_name, id_list, find_dict, return_fields,
                    per_page, page_num, sort_field=None, sort_direction=None, sort_by_revelance=False, search_data=None,
                    format='json', report=False):
    """
    Запрос к базе данных mongoDB (поиск документов только
    :return: строка с ответом из базы данных в формате JSON
    """
    if not return_fields: return_fields = {u"FakeField": 0}
    if len(return_fields) == 0: return_fields[u"FakeField"] = 0
    if page_num > 0: page_num -= 1
    MNGdb = mongo_db_client[db_name]
    MNGcoll = MNGdb[db_collection_name]
    if sort_by_revelance:
        search_id_list = list()
        docList = list()
        for doc_id, search_rank in search_data.iteritems():
            docList.append({u"id": doc_id, u"searchRank": search_rank})
        search_id_list = sorted(docList, key=lambda doc: doc[u"searchRank"])[per_page * page_num:per_page * (page_num + 1)]
        search_id_list = map(lambda doc: dbid(doc[u"id"]), search_id_list)
        find_dict[u"_id"] = {u"$in": search_id_list}
    else:
        find_dict[u"_id"] = {u"$in": id_list}

    if report:
        per_page = SPHNX_LIMIT_REPORT

    if sort_field == None or sort_direction == None:
        if sort_by_revelance:
            data_cursor = MNGcoll.find(find_dict, return_fields)
        else:
            data_cursor = MNGcoll.find(find_dict, return_fields).limit(per_page).skip(per_page * page_num)
    else:
        try:
            data_cursor = MNGcoll.find(find_dict, return_fields).sort(sort_field, direction=sort_direction).limit(
                per_page).skip(per_page * page_num)
        except:
            data_cursor = MNGcoll.find(find_dict, return_fields).limit(per_page).skip(per_page * page_num)
    if sort_by_revelance:
        if len(find_dict) == 1:
            total_on_page = len(search_id_list)
            total = len(id_list)
        else:
            total_on_page = data_cursor.count()
            find_dict[u"_id"] = {u"$in": id_list}
            total = MNGcoll.find(find_dict, return_fields).limit(per_page).skip(per_page * page_num).count()
            find_dict[u"_id"] = {u"$in": search_id_list}
    else:
        total = data_cursor.count()
        total_on_page = data_cursor.count(True)
    mongo_db_client.disconnect()
    if total_on_page > 0:
        # TODO: заглушка на json
        if report:
            data_str = get_report(data_cursor)
        elif sort_by_revelance:
            data_str = preparation_response(data_cursor, dataset_name, total, per_page, page_num, format, search_data)
        else:
            data_str = preparation_response(data_cursor, dataset_name, total, per_page, page_num, format)
    else:
        data_str = None
    return data_str


def parameters_cleaner(parameters_dict, not_use):
    """
    Prepares parameters dict for MongoDB find() method: removes items with values u"None" and u"all"
    Убирает пустые параметры и параметры, которых нет в описании апи (огромный словарь в common.query_settings)
    :param parameters_dict: словарь параметров запроса
    :param not_use: список не используемых параметров
    :return: обработанный словарь параметров запроса
    """
    #TODO: Перепиши генератором
    cleared_dict = dict()
    for key, val in parameters_dict.items():
        try:
            if val not in not_use:
                cleared_dict[key] = val
        except:
            if isinstance(val, dict):
                tmp_dict = dict()
                for (int_key, int_val) in val.iteritems():
                    if isinstance(int_val, list):
                        tmp_list = list()
                        for elem in int_val:
                            try:
                                if elem not in not_use:
                                    tmp_list.append(elem)
                            except:
                                tmp_list.append(elem)
                        if len(tmp_list) > 0: tmp_dict[int_key] = list(tmp_list)
                    else:
                        tmp_dict[int_key] = int_val
                # FIXME: может быть тошлько один OR
                if "$or" in int_key:
                    cleared_dict[int_key] = int_val
                elif len(tmp_dict) > 0:
                    cleared_dict[key] = tmp_dict.copy()
            elif isinstance(val, list):
                try:
                    tmp_list = list()
                    for elem in val:
                        tmp_dict = dict()
                        for (int_key, int_val) in elem.iteritems():
                            try:
                                if int_val not in not_use: tmp_dict[int_key] = int_val
                            except:
                                tmp_dict[int_key] = int_val
                        if len(tmp_dict) > 0: tmp_list.append(tmp_dict.copy())
                    if len(tmp_list) > 0: cleared_dict[key] = list(tmp_list)
                except:
                    cleared_dict[key] = val
    return cleared_dict


def mk_findDict(param_dict, parameters_dict, special_params=None):
    """
    Создаёт из переработанных модификаторами параметров API-словарь с запросом для монго
    :param param_dict: словарь всех возможных параметров api-запроса для конкретной коллекции и метода
    :param parameters_dict: словарь параметров запроса
    :param special_params: аргумент, задающий формат данных в ответе (JSON)
    :return: API-словарь с запросом для монго
    """
    if not special_params: special_params = {}
    find_dict = dict()
    presetted_params_count = 0
    if special_params:
        param_dict.update(
            {
                u'format': {'default': 'json'},
                u'get_report': {'default': False}
            },
        )
    for key, val in param_dict.iteritems():
        if key not in special_params and val["default"] not in notUseParameterVal:
            presetted_params_count += 1
        try:
            # TODO: refactoring
            if 'placing' in key:
                data_filter = typeFunctions[val["type"]](parameters_dict.get(key, val["default"]), val)
            elif key in special_params:
                data_filter = parameters_dict.get(key, val["default"])
            else:
                data_filter = typeFunctions[val["type"]](parameters_dict.get(key, val["default"]))
            if isinstance(data_filter, dict):
                for operator, parameter in data_filter.iteritems():
                    if operator in operatorsDontModify and (not isinstance(operator, list) or len(data_filter) == 1):
                        find_dict[val["field"]] = data_filter
                    else:
                        conditions_list = list()
                        for condition in parameter:
                            conditions_list.append({val["field"]: condition})
                        if find_dict.has_key(operator):
                            find_dict[operator].extend(conditions_list)
                        else:
                            find_dict[operator] = conditions_list
            else:
                if val.get("field", None):
                    find_dict[val["field"]] = data_filter
                else:
                    find_dict[key] = data_filter
        except:
            pass
    return find_dict, presetted_params_count


def mk_sortFields(sort_parameter):
    """
    Подготавливат для монго параметры сортировки из параметров, полученных от апи
    :param sort_parameter: строка со значением параметро get-запроса "sort"
    :return: строка с названием поля сортировки, направление сортировки ( 1 - нисходящая, -1 - восходящая)
    """
    try:
        if sort_parameter == None: return None, None
        sort_direction = sort_parameter[0:1]
        if sort_direction == "-":
            sort_direction = -1
            sort_field = sort_parameter[1:]
        else:
            sort_direction = 1
            sort_field = sort_parameter
        if len(sort_field) < 1: return None, None
        return sort_field, sort_direction
    except:
        return None, None


def underConstruction(parameters_dict):
    return "under construction"


def get_data(parameters_dict):
    """
    Отвечает за все get-запросы, возвращает готовую строку с JSON для клиента
    :param parameters_dict: словарь параметров запроса
    :return: строка с ответом из базы данных в формате JSON
    """
    resource_name = parameters_dict.get("resourceName")
    method_name = parameters_dict.get("methodName")
    queryStr = parameters_dict.get("queryStr").encode("UTF-8").replace(" ", "%20")

    parameters_dict = APIdict[method_name][resource_name]["modifier"](parameters_dict)
    description_dict = APIdict[method_name][resource_name]["description"]
    param_dict = APIdict[method_name][resource_name]["parameters"]

    db_name = description_dict["DB_Name"]
    db_collection_name = description_dict["DB_collectionName"]

    find_dict, presetted_params_count = mk_findDict(param_dict, parameters_dict)
    find_dict = parameters_cleaner(find_dict, notUseParameterVal)
    if len(find_dict) < 1 + presetted_params_count: return None
    return_fields = parameters_dict.get("returnfields", dict())
    try:
        page_n = int(parameters_dict.get("page", 0))
    except:
        page_n = 0
    try:
        per_page = parameters_dict.get("perpage", 0)
    except:
        per_page = 0

    return mongo_request(resource_name, MNGclient, db_name, db_collection_name,
                         find_dict, return_fields, per_page, page_n)


def selectData(parameters_dict):
    """
    Отвечает за select-запросы, возвращает готовую строку с JSON для клиента
    функция содержит много одинакового кода с sphnxSelect — функцию selectData нужно упразднить в пользу sphnxSelect
    :param parameters_dict: словарь параметров запроса
    :return: строка с ответом из базы данных в формате JSON
    """
    resource_name = parameters_dict.get("resourceName")
    method_name = parameters_dict.get("methodName")
    parameters_dict = APIdict[method_name][resource_name]["modifier"](parameters_dict)
    queryStr = parameters_dict.get("queryStr").encode("UTF-8").replace(" ", "%20")

    descr_dict = APIdict[method_name][resource_name]["description"]
    param_dict = APIdict[method_name][resource_name]["parameters"]
    db_name = descr_dict["DB_Name"]
    db_collectionname = descr_dict["DB_collectionName"]

    find_dict, presettedParamsCount = mk_findDict(param_dict, parameters_dict, share_parameters)
    find_dict = parameters_cleaner(find_dict, notUseParameterVal)
    if len(find_dict) < 1 + presettedParamsCount: return None
    sort_field, sort_direction = mk_sortFields(parameters_dict.get("sort", None))

    try:
        sortDict = APIdict[method_name][resource_name]["sort"]
    except:
        sort_field, sort_direction = None, None
    returnfields = parameters_dict.get("returnfields", dict())
    try:
        page_num = int(parameters_dict.get("page", 0))
    except:
        page_num = 0
    try:
        per_page = parameters_dict.get("perpage", 0)
    except:
        per_page = 0
    data_str = mongo_request(resource_name, MNGclient, db_name, db_collectionname, find_dict, returnfields, per_page, page_num,
                            sort_field, sort_direction)
    return data_str


def selectDict(parameters_dict):
    """
    отвечает за select-запросы для справочников, возвращает готовую строку с JSON для клиента
    :param parameters_dict: словарь параметров запроса
    :return: строка с ответом из базы данных в формате JSON
    """
    resource_name = parameters_dict.get("resourceName")
    method_name = parameters_dict.get("methodName")
    parameters_dict = APIdict[method_name][resource_name]["modifier"](parameters_dict)
    query_str = parameters_dict.get("queryStr").encode("UTF-8").replace(" ", "%20")
    descr_dict = APIdict[method_name][resource_name]["description"]
    param_dict = APIdict[method_name][resource_name]["parameters"]
    db_name = descr_dict["DB_Name"]
    db_collectionname = descr_dict["DB_collectionName"]
    find_dict, presented_params_count = mk_findDict(param_dict, parameters_dict)
    find_dict = parameters_cleaner(find_dict, notUseParameterVal)
    sort_field, sort_direction = mk_sortFields(parameters_dict.get("sort", None))
    try:
        sortDict = APIdict[method_name][resource_name]["sort"]
    except:
        sort_field, sort_direction = None, None
    returnfields = parameters_dict.get("returnfields", dict())
    try:
        page_num = int(parameters_dict.get("page", 0))
    except:
        page_num = 0
    try:
        per_page = parameters_dict.get("perpage", 0)
    except:
        per_page = 0
    data_str = mongo_request(resource_name, MNGclient, db_name, db_collectionname, find_dict, returnfields, per_page,
                            page_num, sort_field, sort_direction)
    return data_str


def make_sphinxql(sphinx, index_name, params, api_params):
    """
    Формирует sphinxsql-запрос базе индексов sphinx
    :param sphinx: коннектор к базе sphinx
    :param index_name: название sphinx-индекса
    :param params: словарь параметров запроса
    :param api_params: словарь всех возможных параметров api-запроса для конкретной коллекции и метода
    :return: (сформированноый sphinxsql-запрос, список значений параметров запроса)
    """
    match_expr = ''
    where = []
    args = []
    for key, api_param in api_params.items():
        if key in params and params[key] not in ('', 'None', 'None-None'):
            val = params[key]
            type_function = typeFunctions[api_param['type']]
            if api_param['field'] == 'sphnxsearch':
                match_expr += u' @%s %s' % (api_param['sphinx_field'], val.replace('+', ' '))
            elif api_param['field'] == 'sphnxsearchlist':
                match_expr += u' @%s %s' % (api_param['sphinx_field'],
                                            u'|'.join(['(%s)' % v.replace('+', ' ') for v in type_function(val)]))
            elif 'sphinx_field' in api_param:
                if api_param['type'] == 'okdp_okpd':
                    val = val.replace('.', '_')
                match_expr += u' @%s "%s"' % (api_param['sphinx_field'], val)
            else:
                sphinx_attr = key if '.' in api_param['field'] else api_param['field']
                if api_param['type'] in ('unicode', 'unicode_whitespace'):
                    where.append('%s = %%s' % sphinx_attr)
                    args.append(type_function(val))
                if api_param['type'] in ('budget_unicode', ):
                    where.append('%s = %%s' % sphinx_attr)
                    args.append(type_function(val))
                elif api_param['type'] in ('daterange', 'floatrange'):
                    mongo_range = type_function(val)
                    if mongo_range:
                        if '$gte' in mongo_range:
                            where.append('%s >= %%s' % sphinx_attr)
                            args.append(mktime(mongo_range['$gte'].timetuple()) if api_param['type'] == 'daterange' else
                                        mongo_range['$gte'])
                        if '$lt' in mongo_range:
                            where.append('%s < %%s' % sphinx_attr)
                            args.append(mktime(mongo_range['$lt'].timetuple()))
                        if '$lte' in mongo_range:
                            where.append('%s <= %%s' % sphinx_attr)
                            args.append(mongo_range['$lte'])
    if len(match_expr) > 0:
        where = ['MATCH(%s)'] + where
        args = [match_expr] + args
    sphinx_limit = SPHNX_LIMIT_REPORT if params.get('get_report', False) else SPHNX_LIMIT
    sphinxql = (u'SELECT _id FROM %s WHERE %s LIMIT %d OPTION ranker = proximity, max_matches = %d' %
                (index_name, ' AND '.join(where), sphinx_limit, sphinx_limit))
    return (sphinxql, args)


def sphinx_query(sphinx, index_name, params, api_params):
    """
    Выполняет sphinxsql-запрос
    :param sphinx: коннектор к базе
    :param index_name: название индекса в sphinx
    :param params: параметры запроса и формирования ответа
    :param api_params: словарь всех возможных параметров api-запроса для конкретной коллекции и метода
    :return: курсор, указывающий на запрашиваемые данные в sphinx
    """
    sphinxql, args = make_sphinxql(sphinx, index_name, params, api_params)
    cursor = sphinx.cursor()
    try:
        cursor.execute(sphinxql, args)
    except Exception as e:
        logging.error("sphinxql=%s, args=%s, sphinx error %s" % (sphinxql, args, e))
        raise e
    return cursor


def sphnxSelect(parameters_dict):
    """
    Отвечает за search-запросы, возвращает готовую строку с JSON для клиента
    в дальнейшем должен стать единственным и для всех select-запросов
    :param parameters_dict: словарь параметров запроса
    :return: строка с ответом из базы данных в формате JSON
    """
    resource_name = parameters_dict.get("resourceName")
    method_name = parameters_dict.get("methodName")
    parameters_dict = APIdict[method_name][resource_name]["modifier"](parameters_dict)
    descr_dict = APIdict[method_name][resource_name]["description"]
    param_dict = APIdict[method_name][resource_name]["parameters"]
    db_name = descr_dict["DB_Name"]
    db_collectionname = descr_dict["DB_collectionName"]
    sort_field, sort_direction = mk_sortFields(parameters_dict.get("sort", None))
    sort_by_relevance = True
    try:
        sort_dict = APIdict[method_name][resource_name]["sort"]
    except:
        sort_field, sort_direction = None, None
    if sort_field and sort_direction: sort_by_relevance = False
    returnfields = parameters_dict.get("returnfields", dict())
    try:
        page_num = int(parameters_dict.get("page", 0))
    except:
        page_num = 0
    try:
        per_page = parameters_dict.get("perpage", 0)
    except:
        per_page = 0
    index_name = db_name + db_collectionname
    matches = list()
    sphinx = Sphinx.connect(host=SPHNX_IP, port=SPHNX_PORT, charset='utf8')
    cursor = sphinx_query(sphinx, index_name, params=parameters_dict, api_params=param_dict)
    try:
        matches = [match[0] for match in cursor.fetchall()]
    except Exception as e:
        logging.error("fetching query=%s, index=%s, sphinx error %s" % (parameters_dict, index_name, e))
        raise e
    if len(matches) < 1:
        return None
    _ids = list()
    ranks = dict()
    for search_rank, _id in enumerate(matches, start=1):
        _ids.append(objectid.ObjectId(_id))
        ranks[_id] = search_rank
    data_str = mongo_requestIN(resource_name, MNGclient, db_name, db_collectionname, _ids, {}, returnfields, per_page,
                              page_num, sort_field, sort_direction, sort_by_relevance, ranks,
                              parameters_dict.get('format', 'json'), parameters_dict.get('get_report', False))
    return data_str


def select_budget_dict(parameters_dict):
    """
    Отвечает за select-запросы для справочников, возвращает готовую строку с JSON для клиента
    :param parameters_dict: словарь параметров запроса
    :return: строка с ответом из базы данных в формате JSON
    """
    resource_name = parameters_dict.get("resourceName")
    method_name = parameters_dict.get("methodName")
    parameters_dict = APIdict[method_name][resource_name]["modifier"](parameters_dict)
    query_str = parameters_dict.get("queryStr").encode("UTF-8").replace(" ", "%20")
    descr_dict = APIdict[method_name][resource_name]["description"]
    param_dict = APIdict[method_name][resource_name]["parameters"]
    db_name = descr_dict["DB_Name"]
    db_collectionname = descr_dict["DB_collectionName"]
    find_dict = {}

    keys = {key: True if key in parameters_dict.keys() else False for key in ["grbs", "fkr", "csr", "kvr", "sub-fkr"]}
    if not any([parameters_dict.get(key, '').isdigit() for key in param_dict.keys()]):
        for key, value in keys.iteritems():
            find_dict[param_dict[key]['field']] = {'$exists': value}

    if not find_dict:
        find_dict, presetted_params_count = mk_findDict(param_dict, parameters_dict, share_parameters)
        find_dict = parameters_cleaner(find_dict, notUseParameterVal)
        if len(find_dict) < 1 + presetted_params_count: return None
        sort_field, sort_direction = mk_sortFields(parameters_dict.get("sort", None))
    try:
        sort_dict = APIdict[method_name][resource_name]["sort"]
    except:
        sort_field, sort_direction = None, None
    returnfields = parameters_dict.get("returnfields", dict())
    try:
        page_num = int(parameters_dict.get("page", 0))
    except:
        page_num = 0
    try:
        per_page = parameters_dict.get("perpage", 0)
    except:
        per_page = 0
    data_str = mongo_request(resource_name, MNGclient, db_name, db_collectionname, find_dict, returnfields, per_page,
                            page_num, sort_field, sort_direction)
    return data_str


MNGclient.disconnect()
