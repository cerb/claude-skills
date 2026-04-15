#!/usr/bin/env python3
"""
Cerb DAO Generator
Generates boilerplate for a new Cerb record type from a table definition.

Usage:
    python gen-dao.py --plugin-id cerberusweb.core --table my_record \
        --fields "id int unsigned NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL DEFAULT '', updated_at int unsigned NOT NULL DEFAULT 0"

    Or pipe a JSON config:
    echo '{"plugin_id":"cerberusweb.core","table":"my_record","fields":{"id":"int unsigned","name":"varchar(255)","updated_at":"int unsigned"}}' | python gen-dao.py

Output files are printed to stdout as a manifest with file paths and content.
"""

import argparse
import json
import re
import sys
from textwrap import dedent


def to_class_name(table_name: str) -> str:
    """knowledge_source -> KnowledgeSource"""
    return ''.join(w.capitalize() for w in table_name.split('_'))


def to_object_name(table_name: str) -> str:
    """knowledge_source -> Knowledge Source"""
    return ' '.join(w.capitalize() for w in table_name.split('_'))


def ctx_ext_id(table_name: str) -> str:
    """knowledge_source -> cerb.contexts.knowledge.source"""
    return 'cerb.contexts.' + table_name.replace('_', '.')


def field_prefix(table_name: str) -> str:
    """knowledge_source -> k"""
    return table_name[0]


def parse_fields_from_sql(sql: str) -> dict:
    """Parse 'id int unsigned, name varchar(255), ...' into {name: type}"""
    fields = {}
    for part in sql.split(','):
        part = part.strip().rstrip(',')
        if not part:
            continue
        tokens = part.split()
        if tokens:
            fields[tokens[0]] = tokens[1] if len(tokens) > 1 else 'varchar(255)'
    return fields


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def gen_dao(table: str, fields: dict, plugin_id: str) -> str:
    cls = to_class_name(table)
    fp = field_prefix(table)
    has_created_at = 'created_at' in fields
    has_updated_at = 'updated_at' in fields

    field_consts = '\n'.join(
        f"\tconst {f.upper()} = '{f}';" for f in fields
    )

    select_fields = ', '.join(
        f'SearchFields_{cls}::{f.upper()}' for f in fields
    )

    select_sql_parts = []
    for i, f in enumerate(fields):
        sep = '' if i == len(fields) - 1 else ", "
        select_sql_parts.append(f'\t\t\t"{table}.{f} as %s{sep}".')
    select_sql_str = '\n'.join(select_sql_parts)

    object_from_result = '\n'.join(
        f"\t\t\t$object->{f} = $row['{f}'];" for f in fields
    )

    _ts_validations = []
    if has_updated_at:
        _ts_validations.append("\t\t$validation\n\t\t\t->addField(self::UPDATED_AT)\n\t\t\t->timestamp()\n\t\t\t;")
    if has_created_at:
        _ts_validations.append("\t\t$validation\n\t\t\t->addField(self::CREATED_AT)\n\t\t\t->timestamp()\n\t\t\t;")
    timestamp_validations = "\n".join(_ts_validations)

    created_at_create_set = (
        "\t\tif(!isset($fields[self::CREATED_AT]))\n\t\t\t$fields[self::CREATED_AT] = time();"
        if has_created_at else ""
    )
    updated_at_update_set = (
        "\t\tif(!isset($fields[self::UPDATED_AT]))\n\t\t\t$fields[self::UPDATED_AT] = time();"
        if has_updated_at else ""
    )

    return dedent(f"""\
    class DAO_{cls} extends Cerb_ORMHelper {{
    {field_consts}

    \tprivate function __construct() {{}}

    \tstatic function getFields() {{
    \t\t$validation = DevblocksPlatform::services()->validation();

    \t\t$validation
    \t\t\t->addField(self::ID)
    \t\t\t->id()
    \t\t\t->setEditable(false)
    \t\t\t;
    \t\t$validation
    \t\t\t->addField(self::NAME)
    \t\t\t->string()
    \t\t\t->setRequired(true)
    \t\t\t;
    {timestamp_validations}
    \t\t$validation
    \t\t\t->addField('_fieldsets')
    \t\t\t->string()
    \t\t\t->setMaxLength(65535)
    \t\t\t;
    \t\t$validation
    \t\t\t->addField('_links')
    \t\t\t->string()
    \t\t\t->setMaxLength(65535)
    \t\t\t;

    \t\treturn $validation->getFields();
    \t}}

    \tstatic function create($fields) {{
    \t\t$db = DevblocksPlatform::services()->database();

    \t\t$sql = "INSERT INTO {table} () VALUES ()";
    \t\t$db->ExecuteMaster($sql);
    \t\t$id = $db->LastInsertId();

    {created_at_create_set}

    \t\tCerberusContexts::checkpointCreations(Context_{cls}::ID, $id);

    \t\tself::update($id, $fields);

    \t\treturn $id;
    \t}}

    \tstatic function update($ids, $fields, $check_deltas=true) {{
    \t\tif(!is_array($ids))
    \t\t\t$ids = [$ids];

    {updated_at_update_set}

    \t\t$context = Context_{cls}::ID;
    \t\tself::_updateAbstract($context, $ids, $fields);

    \t\t$chunks = array_chunk($ids, 100, true);
    \t\twhile($batch_ids = array_shift($chunks)) {{
    \t\t\tif(empty($batch_ids))
    \t\t\t\tcontinue;

    \t\t\tif($check_deltas) {{
    \t\t\t\tCerberusContexts::checkpointChanges($context, $batch_ids);
    \t\t\t}}

    \t\t\tparent::_update($batch_ids, '{table}', $fields);

    \t\t\tif($check_deltas) {{
    \t\t\t\t$eventMgr = DevblocksPlatform::services()->event();
    \t\t\t\t$eventMgr->trigger(
    \t\t\t\t\tnew Model_DevblocksEvent(
    \t\t\t\t\t\t'dao.{table}.update',
    \t\t\t\t\t\t[
    \t\t\t\t\t\t\t'fields' => $fields,
    \t\t\t\t\t\t]
    \t\t\t\t\t)
    \t\t\t\t);

    \t\t\t\tDevblocksPlatform::markContextChanged($context, $batch_ids);
    \t\t\t}}
    \t\t}}
    \t}}

    \tstatic function updateWhere($fields, $where) {{
    \t\tparent::_updateWhere('{table}', $fields, $where);
    \t}}

    \tstatic public function onBeforeUpdateByActor($actor, &$fields, $id=null, &$error=null) {{
    \t\t$context = Context_{cls}::ID;

    \t\tif(!self::_onBeforeUpdateByActorCheckContextPrivs($actor, $context, $id, $error))
    \t\t\treturn false;

    \t\treturn true;
    \t}}

    \t/**
    \t * @param string $where
    \t * @return Model_{cls}[]
    \t */
    \tstatic function getWhere($where=null, $sortBy=null, $sortAsc=true, $limit=null, $options=null) {{
    \t\t$db = DevblocksPlatform::services()->database();

    \t\tlist($where_sql, $sort_sql, $limit_sql) = self::_getWhereSQL($where, $sortBy, $sortAsc, $limit);

    \t\t$sql = "SELECT {', '.join(fields)} " .
    \t\t\t"FROM {table} " .
    \t\t\t$where_sql .
    \t\t\t$sort_sql .
    \t\t\t$limit_sql
    \t\t;

    \t\tif($options & DevblocksORMHelper::OPT_GET_MASTER_ONLY) {{
    \t\t\t$rs = $db->ExecuteMaster($sql, _DevblocksDatabaseManager::OPT_NO_READ_AFTER_WRITE);
    \t\t}} else {{
    \t\t\t$rs = $db->QueryReader($sql);
    \t\t}}

    \t\treturn self::_getObjectsFromResult($rs);
    \t}}

    \t/**
    \t * @return Model_{cls}[]
    \t */
    \tstatic function getAll($nocache=false) {{
    \t\t$objects = self::getWhere(null, self::NAME, true, null, DevblocksORMHelper::OPT_GET_MASTER_ONLY);
    \t\treturn $objects;
    \t}}

    \t/**
    \t * @param integer $id
    \t * @return Model_{cls}|null
    \t */
    \tstatic function get($id) {{
    \t\tif(empty($id))
    \t\t\treturn null;

    \t\t$objects = self::getWhere(sprintf("%s = %d",
    \t\t\tself::ID,
    \t\t\t$id
    \t\t));

    \t\tif(array_key_exists($id, $objects))
    \t\t\treturn $objects[$id];

    \t\treturn null;
    \t}}

    \t/**
    \t * @param array $ids
    \t * @return Model_{cls}[]
    \t */
    \tstatic function getIds(array $ids) : array {{
    \t\treturn parent::getIds($ids);
    \t}}

    \t/**
    \t * @param mysqli_result|false $rs
    \t * @return Model_{cls}[]
    \t */
    \tstatic private function _getObjectsFromResult($rs) {{
    \t\t$objects = [];

    \t\tif(!($rs instanceof mysqli_result))
    \t\t\treturn [];

    \t\twhile($row = mysqli_fetch_assoc($rs)) {{
    \t\t\t$object = new Model_{cls}();
    {object_from_result}
    \t\t\t$objects[$object->id] = $object;
    \t\t}}

    \t\tmysqli_free_result($rs);

    \t\treturn $objects;
    \t}}

    \tstatic function random() {{
    \t\treturn self::_getRandom('{table}');
    \t}}

    \tstatic function delete($ids) {{
    \t\t$db = DevblocksPlatform::services()->database();

    \t\tif(!is_array($ids)) $ids = [$ids];
    \t\t$ids = DevblocksPlatform::sanitizeArray($ids, 'int');

    \t\tif(empty($ids)) return false;

    \t\t$context = Context_{cls}::ID;
    \t\t$ids_list = implode(',', self::qstrArray($ids));

    \t\tparent::_deleteAbstractBefore($context, $ids);

    \t\t$db->ExecuteMaster(sprintf("DELETE FROM {table} WHERE id IN (%s)", $ids_list));

    \t\tparent::_deleteAbstractAfter($context, $ids);

    \t\treturn true;
    \t}}

    \tpublic static function getSearchQueryComponents($columns, $params, $sortBy=null, $sortAsc=null) {{
    \t\t$fields = SearchFields_{cls}::getFields();

    \t\tlist(,$wheres) = parent::_parseSearchParams($params, $columns, 'SearchFields_{cls}', $sortBy);

    \t\t$select_sql = sprintf("SELECT " .
    {select_sql_str}
    \t\t\t{select_fields}
    \t\t);

    \t\t$join_sql = "FROM {table} ";

    \t\t$where_sql =
    \t\t\t(!empty($wheres) ? sprintf("WHERE %s ",implode(' AND ',$wheres)) : "WHERE 1 ")
    \t\t;

    \t\t$sort_sql = self::_buildSortClause($sortBy, $sortAsc, $fields, $select_sql, 'SearchFields_{cls}');

    \t\treturn [
    \t\t\t'primary_table' => '{table}',
    \t\t\t'select' => $select_sql,
    \t\t\t'join' => $join_sql,
    \t\t\t'where' => $where_sql,
    \t\t\t'sort' => $sort_sql,
    \t\t];
    \t}}

    \tstatic function search($columns, $params, $limit=10, $page=0, $sortBy=null, $sortAsc=null, $withCounts=true) {{
    \t\t$query_parts = self::getSearchQueryComponents($columns,$params,$sortBy,$sortAsc);

    \t\treturn self::_searchWithTimeout(
    \t\t\tSearchFields_{cls}::ID,
    \t\t\t$query_parts['select'],
    \t\t\t$query_parts['join'],
    \t\t\t$query_parts['where'],
    \t\t\t$query_parts['sort'],
    \t\t\t$page,
    \t\t\t$limit,
    \t\t\t$withCounts
    \t\t);
    \t}}
    }};
    """)


def gen_search_fields(table: str, fields: dict) -> str:
    cls = to_class_name(table)
    fp = field_prefix(table)
    translate_key = table
    has_created_at = 'created_at' in fields
    has_updated_at = 'updated_at' in fields

    field_consts = '\n'.join(
        f"\tconst {f.upper()} = '{fp}_{f}';" for f in fields
    )

    search_field_entries = '\n'.join(
        f"\t\t\tself::{f.upper()} => new DevblocksSearchField(self::{f.upper()}, '{table}', '{f}', $translate->_('{translate_key}.{f}'), null, true),"
        for f in fields
    )

    _key_methods = []
    if has_updated_at:
        _key_methods.append(
            f"\tstatic function getUpdatedKey() : string {{\n"
            f"\t\treturn sprintf('%s.%s', self::getTableName(), DAO_{cls}::UPDATED_AT);\n"
            f"\t}}"
        )
    if has_created_at:
        _key_methods.append(
            f"\tstatic function getCreatedKey() : string {{\n"
            f"\t\treturn sprintf('%s.%s', self::getTableName(), DAO_{cls}::CREATED_AT);\n"
            f"\t}}"
        )
    key_methods = "\n\n".join(_key_methods)

    return dedent(f"""\
    class SearchFields_{cls} extends DevblocksSearchFields {{
    {field_consts}

    \tstatic private $_fields = null;

    \tstatic function getTableName() : string {{
    \t\treturn '{table}';
    \t}}

    \tstatic function getPrimaryKey() : string {{
    \t\treturn sprintf('%s.%s', self::getTableName(), DAO_{cls}::ID);
    \t}}

    {key_methods}

    \tstatic function getCustomFieldContextKeys() {{
    \t\treturn [
    \t\t\tContext_{cls}::ID => new DevblocksSearchFieldContextKeys('{table}.id', self::ID),
    \t\t];
    \t}}

    \tstatic function getWhereSQL(DevblocksSearchCriteria $param) {{
    \t\tswitch($param->field) {{
    \t\t\tdefault:
    \t\t\t\tif(DevblocksPlatform::strStartsWith($param->field, 'cf_')) {{
    \t\t\t\t\treturn self::_getWhereSQLFromCustomFields($param);
    \t\t\t\t}} else {{
    \t\t\t\t\tif(null !== ($virtual_where_sql = self::_getWhereSQLForCommonVirtual($param, Context_{cls}::ID, self::getPrimaryKey())))
    \t\t\t\t\t\treturn $virtual_where_sql;

    \t\t\t\t\treturn $param->getWhereSQL(self::getFields(), self::getPrimaryKey());
    \t\t\t\t}}
    \t\t}}
    \t}}

    \tstatic function getLabelsForKeyValues($key, $values) {{
    \t\tswitch($key) {{
    \t\t\tcase self::ID:
    \t\t\t\t$models = DAO_{cls}::getIds($values);
    \t\t\t\treturn array_column(DevblocksPlatform::objectsToArrays($models), 'name', 'id');
    \t\t}}

    \t\treturn parent::getLabelsForKeyValues($key, $values);
    \t}}

    \tstatic function getFields() {{
    \t\tif(is_null(self::$_fields))
    \t\t\tself::$_fields = self::_getFields();

    \t\treturn self::$_fields;
    \t}}

    \tstatic function _getFields() {{
    \t\t$translate = DevblocksPlatform::getTranslationService();

    \t\t$columns = [
    {search_field_entries}
    \t\t];

    \t\tif(($virtual_columns = DevblocksSearchField::getVirtualFields()))
    \t\t\t$columns = array_merge($columns, $virtual_columns);

    \t\t$custom_columns = DevblocksSearchField::getCustomSearchFieldsByContexts(array_keys(self::getCustomFieldContextKeys()));

    \t\tif(!empty($custom_columns))
    \t\t\t$columns = array_merge($columns, $custom_columns);

    \t\tDevblocksPlatform::sortObjects($columns, 'db_label');

    \t\treturn $columns;
    \t}}
    }};
    """)


def gen_model(table: str, fields: dict) -> str:
    cls = to_class_name(table)
    props = '\n'.join(f"\tpublic ${f};" for f in fields)
    return dedent(f"""\
    class Model_{cls} extends DevblocksRecordModel {{
    {props}
    }};
    """)


def gen_view(table: str, fields: dict, plugin_id: str) -> str:
    cls = to_class_name(table)
    obj = to_object_name(table)
    fp = field_prefix(table)
    ctx = ctx_ext_id(table)
    has_created_at = 'created_at' in fields
    has_updated_at = 'updated_at' in fields

    view_columns = '\n'.join(
        f"\t\t\tSearchFields_{cls}::{f.upper()}," for f in fields
    )

    set_criteria_cases = '\n'.join(
        f"\t\t\tcase SearchFields_{cls}::{f.upper()}:" for f in fields
    )

    _date_qs = []
    if has_created_at:
        _date_qs.append(
            f"\t\t\t'created' => [\n"
            f"\t\t\t\t'type' => DevblocksSearchCriteria::TYPE_DATE,\n"
            f"\t\t\t\t'options' => ['param_key' => SearchFields_{cls}::CREATED_AT],\n"
            f"\t\t\t],"
        )
    if has_updated_at:
        _date_qs.append(
            f"\t\t\t'updated' => [\n"
            f"\t\t\t\t'type' => DevblocksSearchCriteria::TYPE_DATE,\n"
            f"\t\t\t\t'options' => ['param_key' => SearchFields_{cls}::UPDATED_AT],\n"
            f"\t\t\t],"
        )
    date_quick_search_fields = "\n".join(_date_qs)

    return dedent(f"""\
    class View_{cls} extends C4_AbstractView implements IAbstractView_Subtotals, IAbstractView_QuickSearch {{
    \tconst DEFAULT_ID = '{cls.lower()}';

    \tfunction __construct() {{
    \t\t$this->id = self::DEFAULT_ID;
    \t\t$this->name = DevblocksPlatform::translateCapitalized('{obj}');
    \t\t$this->renderLimit = 25;
    \t\t$this->renderSortBy = SearchFields_{cls}::ID;
    \t\t$this->renderSortAsc = true;

    \t\t$this->view_columns = [
    {view_columns}
    \t\t];

    \t\t$this->addColumnsHidden([]);

    \t\t$this->doResetCriteria();
    \t}}

    \tprotected function _getData() {{
    \t\treturn DAO_{cls}::search(
    \t\t\t$this->view_columns,
    \t\t\t$this->getParams(),
    \t\t\t$this->renderLimit,
    \t\t\t$this->renderPage,
    \t\t\t$this->renderSortBy,
    \t\t\t$this->renderSortAsc,
    \t\t\t$this->renderTotal
    \t\t);
    \t}}

    \tfunction getData() {{
    \t\t$objects = $this->_getDataBoundedTimed();
    \t\t$this->_lazyLoadCustomFieldsIntoObjects($objects, 'SearchFields_{cls}');
    \t\treturn $objects;
    \t}}

    \tfunction getDataAsObjects($ids=null, &$total=null) {{
    \t\treturn $this->_getDataAsObjects('DAO_{cls}', $ids, $total);
    \t}}

    \tfunction getDataSample($size) {{
    \t\treturn $this->_doGetDataSample('DAO_{cls}', $size);
    \t}}

    \tfunction getSubtotalFields() {{
    \t\t$all_fields = $this->getParamsAvailable(true);
    \t\t$fields = [];

    \t\tif(is_array($all_fields))
    \t\tforeach($all_fields as $field_key => $field_model) {{
    \t\t\t$pass = false;

    \t\t\tswitch($field_key) {{
    \t\t\t\tdefault:
    \t\t\t\t\tif(DevblocksPlatform::strStartsWith($field_key, 'cf_')) {{
    \t\t\t\t\t\t$pass = $this->_canSubtotalCustomField($field_key);
    \t\t\t\t\t}} else if (str_starts_with($field_key, '*_')) {{
    \t\t\t\t\t\t$pass = $this->_canSubtotalVirtualField($field_key);
    \t\t\t\t\t}}
    \t\t\t\t\tbreak;
    \t\t\t}}

    \t\t\tif($pass)
    \t\t\t\t$fields[$field_key] = $field_model;
    \t\t}}

    \t\treturn $fields;
    \t}}

    \tfunction getSubtotalCounts($column) {{
    \t\t$counts = [];
    \t\t$fields = $this->getFields();
    \t\t$context = Context_{cls}::ID;

    \t\tif(!array_key_exists($column, $fields))
    \t\t\treturn [];

    \t\tswitch($column) {{
    \t\t\tdefault:
    \t\t\t\tif(DevblocksPlatform::strStartsWith($column, 'cf_')) {{
    \t\t\t\t\t$counts = $this->_getSubtotalCountForCustomColumn($context, $column);
    \t\t\t\t}} else if(DevblocksPlatform::strStartsWith($column, '*_')) {{
    \t\t\t\t\t$counts = $this->_getSubtotalCountForVirtualField($context, $column);
    \t\t\t\t}}
    \t\t\t\tbreak;
    \t\t}}

    \t\treturn $counts;
    \t}}

    \tfunction getQuickSearchDefaultFilter(?DevblocksSearchCriteria $criteria=null) : string {{
    \t\treturn 'name';
    \t}}

    \tfunction getQuickSearchFields() {{
    \t\t$search_fields = SearchFields_{cls}::getFields();

    \t\t$fields = [
    \t\t\t'fieldset' => [
    \t\t\t\t'type' => DevblocksSearchCriteria::TYPE_VIRTUAL,
    \t\t\t\t'options' => ['param_key' => DevblocksSearchField::VIRTUAL_HAS_FIELDSET],
    \t\t\t\t'examples' => [
    \t\t\t\t\t['type' => 'search', 'context' => CerberusContexts::CONTEXT_CUSTOM_FIELDSET, 'qr' => 'context:' . Context_{cls}::ID],
    \t\t\t\t]
    \t\t\t],
    \t\t\t'id' => [
    \t\t\t\t'type' => DevblocksSearchCriteria::TYPE_NUMBER,
    \t\t\t\t'options' => ['param_key' => SearchFields_{cls}::ID],
    \t\t\t\t'examples' => [
    \t\t\t\t\t['type' => 'chooser', 'context' => Context_{cls}::ID, 'q' => ''],
    \t\t\t\t]
    \t\t\t],
    \t\t\t'name' => [
    \t\t\t\t'type' => DevblocksSearchCriteria::TYPE_TEXT,
    \t\t\t\t'options' => ['param_key' => SearchFields_{cls}::NAME, 'match' => DevblocksSearchCriteria::OPTION_TEXT_PARTIAL],
    \t\t\t],
    {date_quick_search_fields}
    \t\t\t'watchers' => [
    \t\t\t\t'type' => DevblocksSearchCriteria::TYPE_VIRTUAL,
    \t\t\t\t'options' => ['param_key' => DevblocksSearchField::VIRTUAL_WATCHERS],
    \t\t\t\t'examples' => [
    \t\t\t\t\t['type' => 'search', 'context' => CerberusContexts::CONTEXT_WORKER, 'q' => ''],
    \t\t\t\t],
    \t\t\t],
    \t\t];

    \t\t$fields = self::_appendVirtualFiltersFromQuickSearchContexts('links', $fields, 'links', DevblocksSearchField::VIRTUAL_CONTEXT_LINK);
    \t\t$fields = self::_appendFieldsFromQuickSearchContext(Context_{cls}::ID, $fields, null);
    \t\t$fields = self::_setSortableQuickSearchFields($fields, $search_fields);
    \t\tksort($fields);

    \t\treturn $fields;
    \t}}

    \tfunction getParamFromQuickSearchFieldTokens($field, $tokens) {{
    \t\tswitch($field) {{
    \t\t\tcase 'fieldset':
    \t\t\t\treturn DevblocksSearchCriteria::getVirtualQuickSearchParamFromTokens($field, $tokens, '*_has_fieldset');

    \t\t\tcase 'watchers':
    \t\t\t\treturn DevblocksSearchCriteria::getWatcherParamFromTokens(DevblocksSearchField::VIRTUAL_WATCHERS, $tokens);

    \t\t\tdefault:
    \t\t\t\tif($field == 'links' || str_starts_with($field, 'links.'))
    \t\t\t\t\treturn DevblocksSearchCriteria::getContextLinksParamFromTokens($field, $tokens);

    \t\t\t\t$search_fields = $this->getQuickSearchFields();
    \t\t\t\treturn DevblocksSearchCriteria::getParamFromQueryFieldTokens($field, $tokens, $search_fields);
    \t\t}}
    \t}}

    \tfunction render() {{
    \t\t$this->_sanitize();

    \t\t$tpl = DevblocksPlatform::services()->template();
    \t\t$tpl->assign('id', $this->id);
    \t\t$tpl->assign('view', $this);

    \t\t$custom_fields = DAO_CustomField::getByContext(Context_{cls}::ID);
    \t\t$tpl->assign('custom_fields', $custom_fields);

    \t\t$tpl->assign('view_template', 'devblocks:{plugin_id}::records/types/{table}/view.tpl');
    \t\t$tpl->display('devblocks:cerberusweb.core::internal/views/subtotals_and_view.tpl');
    \t}}

    \tfunction renderCriteriaParam($param) {{
    \t\tswitch($param->field) {{
    \t\t\tdefault:
    \t\t\t\tparent::renderCriteriaParam($param);
    \t\t\t\tbreak;
    \t\t}}
    \t}}

    \tfunction renderVirtualCriteria($param) : void {{
    \t\tswitch($param->field) {{
    \t\t\tdefault:
    \t\t\t\t$this->_renderVirtualCriteria($param);
    \t\t\t\tbreak;
    \t\t}}
    \t}}

    \tfunction getFields() {{
    \t\treturn SearchFields_{cls}::getFields();
    \t}}

    \tfunction doSetCriteria($field, $oper, $value) {{
    \t\t$criteria = null;

    \t\tswitch($field) {{
    {set_criteria_cases}
    \t\t\tcase 'placeholder_string':
    \t\t\t\t$criteria = $this->_doSetCriteriaString($field, $oper, $value);
    \t\t\t\tbreak;

    \t\t\tcase 'placeholder_number':
    \t\t\t\t$criteria = new DevblocksSearchCriteria($field,$oper,$value);
    \t\t\t\tbreak;

    \t\t\tcase 'placeholder_date':
    \t\t\t\t$criteria = $this->_doSetCriteriaDate($field, $oper);
    \t\t\t\tbreak;

    \t\t\tcase 'placeholder_bool':
    \t\t\t\t$bool = DevblocksPlatform::importGPC($_POST['bool'] ?? null, 'integer', 1);
    \t\t\t\t$criteria = new DevblocksSearchCriteria($field,$oper,$bool);
    \t\t\t\tbreak;

    \t\t\tdefault:
    \t\t\t\tif(str_starts_with($field, 'cf_')) {{
    \t\t\t\t\t$criteria = $this->_doSetCriteriaCustomField($field, substr($field,3));
    \t\t\t\t}} else if (str_starts_with($field, '*_')) {{
    \t\t\t\t\tif(($virtual_criteria = $this->_doSetCriteriaVirtual($field, $_POST, $oper)))
    \t\t\t\t\t\t$criteria = $virtual_criteria;
    \t\t\t\t}}
    \t\t\t\tbreak;
    \t\t}}

    \t\tif(!empty($criteria)) {{
    \t\t\t$this->addParam($criteria, $field);
    \t\t\t$this->renderPage = 0;
    \t\t}}
    \t}}
    }};
    """)


def gen_context(table: str, fields: dict, plugin_id: str = 'cerberusweb.core') -> str:
    cls = to_class_name(table)
    obj = to_object_name(table)
    ctx = ctx_ext_id(table)
    var = table  # variable name for model
    has_created_at = 'created_at' in fields
    has_updated_at = 'updated_at' in fields

    _standard_fields = {'id', 'name', 'updated_at', 'created_at'}

    field_key_map = '\n'.join(
        f"\t\t\t'{f}' => DAO_{cls}::{f.upper()}," for f in fields
    )

    token_labels = '\n'.join(
        f"\t\t\t'{f}' => $prefix.$translate->_('{table}.{f}')," for f in fields
        if f not in _standard_fields
    )

    token_types_extra = '\n'.join(
        f"\t\t\t'{f}' => Model_CustomField::TYPE_SINGLE_LINE," for f in fields
        if f not in _standard_fields
    )

    token_values_extra = '\n'.join(
        f"\t\t\t$token_values['{f}'] = ${var}->{f};" for f in fields
        if f not in _standard_fields
    )

    created_at_meta_field = (
        f"\t\t\t'created' => ${var}->created_at,"
        if has_created_at else ""
    )
    created_at_token_label = (
        f"\t\t\t'created_at' => $prefix.$translate->_('common.created'),"
        if has_created_at else ""
    )
    created_at_token_type = (
        f"\t\t\t'created_at' => Model_CustomField::TYPE_DATE,"
        if has_created_at else ""
    )
    created_at_token_value = (
        f"\t\t\t$token_values['created_at'] = ${var}->created_at;"
        if has_created_at else ""
    )
    updated_at_token_label = (
        f"\t\t\t'updated_at' => $prefix.$translate->_('common.updated'),"
        if has_updated_at else ""
    )
    updated_at_token_type = (
        f"\t\t\t'updated_at' => Model_CustomField::TYPE_DATE,"
        if has_updated_at else ""
    )
    updated_at_token_value = (
        f"\t\t\t$token_values['updated_at'] = ${var}->updated_at;"
        if has_updated_at else ""
    )

    _default_props = []
    if has_created_at:
        _default_props.append("\t\t\t'created_at',")
    if has_updated_at:
        _default_props.append("\t\t\t'updated_at',")
    default_properties = "\n".join(_default_props)

    return dedent(f"""\
    class Context_{cls} extends Extension_DevblocksContext implements IDevblocksContextProfile, IDevblocksContextPeek {{
    \tconst ID = '{ctx}';
    \tconst URI = '{table}';

    \tstatic function isReadableByActor($models, $actor) {{
    \t\treturn CerberusContexts::allowEverything($models);
    \t}}

    \tstatic function isWriteableByActor($models, $actor) {{
    \t\treturn CerberusContexts::allowEverything($models);
    \t}}

    \tstatic function isDeletableByActor($models, $actor) {{
    \t\treturn self::isWriteableByActor($models, $actor);
    \t}}

    \tfunction getRandom() {{
    \t\treturn DAO_{cls}::random();
    \t}}

    \tfunction profileGetUrl($context_id) {{
    \t\tif(empty($context_id))
    \t\t\treturn '';

    \t\t$url_writer = DevblocksPlatform::services()->url();
    \t\treturn $url_writer->writeNoProxy('c=profiles&type={table}&id='.$context_id, true);
    \t}}

    \tfunction profileGetFields($model=null) {{
    \t\t$translate = DevblocksPlatform::getTranslationService();
    \t\t$properties = [];

    \t\tif(is_null($model))
    \t\t\t$model = new Model_{cls}();

    \t\t$properties['name'] = [
    \t\t\t'label' => mb_ucfirst($translate->_('common.name')),
    \t\t\t'type' => Model_CustomField::TYPE_LINK,
    \t\t\t'value' => $model->id,
    \t\t\t'params' => ['context' => self::ID],
    \t\t];

    \t\t$properties['updated'] = [
    \t\t\t'label' => DevblocksPlatform::translateCapitalized('common.updated'),
    \t\t\t'type' => Model_CustomField::TYPE_DATE,
    \t\t\t'value' => $model->updated_at,
    \t\t];

    \t\t$properties['id'] = [
    \t\t\t'label' => DevblocksPlatform::translate('common.id'),
    \t\t\t'type' => Model_CustomField::TYPE_NUMBER,
    \t\t\t'value' => $model->id,
    \t\t];

    \t\treturn $properties;
    \t}}

    \tfunction getMeta($context_id) {{
    \t\tif(null == (${var} = DAO_{cls}::get($context_id)))
    \t\t\treturn [];

    \t\t$url = $this->profileGetUrl($context_id);
    \t\t$friendly = DevblocksPlatform::strToPermalink(${var}->name);

    \t\tif(!empty($friendly))
    \t\t\t$url .= '-' . $friendly;

    \t\treturn [
    \t\t\t'id' => ${var}->id,
    \t\t\t'name' => ${var}->name,
    \t\t\t'permalink' => $url,
    \t\t\t'updated' => ${var}->updated_at,
    {created_at_meta_field}
    \t\t];
    \t}}

    \tfunction getDefaultProperties() : array {{
    \t\treturn [
    {default_properties}
    \t\t];
    \t}}

    \tfunction getContext(${var}, &$token_labels, &$token_values, $prefix=null) {{
    \t\tif(is_null($prefix))
    \t\t\t$prefix = '{obj}:';

    \t\t$translate = DevblocksPlatform::getTranslationService();
    \t\t$fields = DAO_CustomField::getByContext(Context_{cls}::ID);

    \t\tif(is_numeric(${var})) {{
    \t\t\t${var} = DAO_{cls}::get(${var});
    \t\t}} elseif(${var} instanceof Model_{cls}) {{
    \t\t\tDevblocksPlatform::noop();
    \t\t}} elseif(is_array(${var})) {{
    \t\t\t${var} = Cerb_ORMHelper::recastArrayToModel(${var}, 'Model_{cls}');
    \t\t}} else {{
    \t\t\t${var} = null;
    \t\t}}

    \t\t$token_labels = [
    \t\t\t'_label' => $prefix,
    \t\t\t'id' => $prefix.$translate->_('common.id'),
    \t\t\t'name' => $prefix.$translate->_('common.name'),
    {created_at_token_label}
    {updated_at_token_label}
    \t\t\t'record_url' => $prefix.$translate->_('common.url.record'),
    {token_labels}
    \t\t];

    \t\t$token_types = [
    \t\t\t'_label' => 'context_url',
    \t\t\t'id' => Model_CustomField::TYPE_NUMBER,
    \t\t\t'name' => Model_CustomField::TYPE_SINGLE_LINE,
    {created_at_token_type}
    {updated_at_token_type}
    \t\t\t'record_url' => Model_CustomField::TYPE_URL,
    {token_types_extra}
    \t\t];

    \t\tif(false !== ($custom_field_labels = $this->_getTokenLabelsFromCustomFields($fields, $prefix)) && is_array($custom_field_labels))
    \t\t\t$token_labels = array_merge($token_labels, $custom_field_labels);

    \t\tif(false !== ($custom_field_types = $this->_getTokenTypesFromCustomFields($fields, $prefix)) && is_array($custom_field_types))
    \t\t\t$token_types = array_merge($token_types, $custom_field_types);

    \t\t$token_values = [];
    \t\t$token_values['_context'] = Context_{cls}::ID;
    \t\t$token_values['_type'] = '{table}';
    \t\t$token_values['_types'] = $token_types;

    \t\tif(${var}) {{
    \t\t\t$token_values['_loaded'] = true;
    \t\t\t$token_values['_label'] = ${var}->name;
    \t\t\t$token_values['id'] = ${var}->id;
    \t\t\t$token_values['name'] = ${var}->name;
    {created_at_token_value}
    {updated_at_token_value}
    {token_values_extra}
    \t\t\t$token_values = $this->_importModelCustomFieldsAsValues(${var}, $token_values);

    \t\t\t$url_writer = DevblocksPlatform::services()->url();
    \t\t\t$token_values['record_url'] = $url_writer->writeNoProxy(
    \t\t\t\tsprintf("c=profiles&type={table}&id=%d-%s", ${var}->id, DevblocksPlatform::strToPermalink(${var}->name)), true
    \t\t\t);
    \t\t}}

    \t\treturn true;
    \t}}

    \tfunction getKeyToDaoFieldMap() {{
    \t\treturn [
    {field_key_map}
    \t\t\t'links' => '_links',
    \t\t];
    \t}}

    \tfunction getKeyMeta($with_dao_fields=true) {{
    \t\t$keys = parent::getKeyMeta($with_dao_fields);
    \t\treturn $keys;
    \t}}

    \tfunction getDaoFieldsFromKeyAndValue($key, $value, &$out_fields, $data, &$error) {{
    \t\tswitch(DevblocksPlatform::strLower($key)) {{
    \t\t}}
    \t\treturn true;
    \t}}

    \tfunction lazyLoadGetKeys() {{
    \t\treturn parent::lazyLoadGetKeys();
    \t}}

    \tfunction lazyLoadContextValues($token, $dictionary) {{
    \t\tif(!isset($dictionary['id']))
    \t\t\treturn;

    \t\t$context = Context_{cls}::ID;
    \t\t$context_id = $dictionary['id'];
    \t\t$is_loaded = $dictionary['_loaded'] ?? false;
    \t\t$values = [];

    \t\tif(!$is_loaded) {{
    \t\t\t$labels = [];
    \t\t\tCerberusContexts::getContext($context, $context_id, $labels, $values, null, true, true);
    \t\t}}

    \t\tswitch($token) {{
    \t\t\tdefault:
    \t\t\t\t$defaults = $this->_lazyLoadDefaults($token, $dictionary);
    \t\t\t\t$values = array_merge($values, $defaults);
    \t\t\t\tbreak;
    \t\t}}

    \t\treturn $values;
    \t}}

    \tfunction getChooserView($view_id=null) {{
    \t\tif(empty($view_id))
    \t\t\t$view_id = 'chooser_'.str_replace('.','_',$this->id).time().mt_rand(0,9999);

    \t\t$defaults = C4_AbstractViewModel::loadFromClass($this->getViewClass());
    \t\t$defaults->id = $view_id;
    \t\t$defaults->is_ephemeral = true;

    \t\t$view = C4_AbstractViewLoader::getView($view_id, $defaults);
    \t\t$view->name = '{obj}';
    \t\t$view->renderSortBy = SearchFields_{cls}::UPDATED_AT;
    \t\t$view->renderSortAsc = false;
    \t\t$view->renderLimit = 10;
    \t\t$view->renderTemplate = 'contextlinks_chooser';

    \t\treturn $view;
    \t}}

    \tfunction getView($context=null, $context_id=null, $options=[], $view_id=null) {{
    \t\t$view_id = !empty($view_id) ? $view_id : str_replace('.','_',$this->id);

    \t\t$defaults = C4_AbstractViewModel::loadFromClass($this->getViewClass());
    \t\t$defaults->id = $view_id;

    \t\t$view = C4_AbstractViewLoader::getView($view_id, $defaults);
    \t\t$view->name = '{obj}';

    \t\t$params_req = [];

    \t\tif(!empty($context) && !empty($context_id)) {{
    \t\t\t$params_req = [
    \t\t\t\tnew DevblocksSearchCriteria(DevblocksSearchField::VIRTUAL_CONTEXT_LINK,'in',[$context.':'.$context_id]),
    \t\t\t];
    \t\t}}

    \t\t$view->addParamsRequired($params_req, true);
    \t\t$view->renderTemplate = 'context';
    \t\treturn $view;
    \t}}

    \tfunction renderPeekPopup($context_id=0, $view_id='', $edit=false) {{
    \t\t$tpl = DevblocksPlatform::services()->template();
    \t\t$active_worker = CerberusApplication::getActiveWorker();
    \t\t$context = Context_{cls}::ID;

    \t\t$tpl->assign('view_id', $view_id);

    \t\t$model = null;

    \t\tif($context_id) {{
    \t\t\tif(!($model = DAO_{cls}::get($context_id)))
    \t\t\t\tDevblocksPlatform::dieWithHttpError(null, 403);
    \t\t}}

    \t\tif(empty($context_id) || $edit) {{
    \t\t\tif($model) {{
    \t\t\t\tif(!CerberusContexts::isWriteableByActor($context, $model, $active_worker))
    \t\t\t\t\tDevblocksPlatform::dieWithHttpError(null, 403);

    \t\t\t\t$tpl->assign('model', $model);
    \t\t\t}}

    \t\t\t$custom_fields = DAO_CustomField::getByContext($context, false);
    \t\t\t$tpl->assign('custom_fields', $custom_fields);

    \t\t\t$custom_field_values = DAO_CustomFieldValue::getValuesByContextIds($context, $context_id);
    \t\t\tif(isset($custom_field_values[$context_id]))
    \t\t\t\t$tpl->assign('custom_field_values', $custom_field_values[$context_id]);

    \t\t\t$types = Model_CustomField::getTypes();
    \t\t\t$tpl->assign('types', $types);

    \t\t\t$tpl->assign('id', $context_id);
    \t\t\t$tpl->assign('view_id', $view_id);
    \t\t\t$tpl->display('devblocks:{plugin_id}::records/types/{table}/peek_edit.tpl');

    \t\t}} else {{
    \t\t\tPage_Profiles::renderCard($context, $context_id, $model);
    \t\t}}
    \t}}
    }};
    """)


def gen_peek_edit_tpl(table: str, plugin_id: str) -> str:
    cls = to_class_name(table)
    obj = to_object_name(table)
    ctx = ctx_ext_id(table)

    return dedent(f"""\
    {{$peek_context = '{ctx}'}}
    {{$peek_context_id = $model->id}}
    {{$form_id = uniqid()}}
    <form action="{{devblocks_url}}{{/devblocks_url}}" method="post" id="{{$form_id}}">
    <input type="hidden" name="c" value="profiles">
    <input type="hidden" name="a" value="invoke">
    <input type="hidden" name="module" value="{table}">
    <input type="hidden" name="action" value="savePeekJson">
    <input type="hidden" name="view_id" value="{{$view_id}}">
    {{if !empty($model) && !empty($model->id)}}<input type="hidden" name="id" value="{{$model->id}}">{{/if}}
    <input type="hidden" name="do_delete" value="0">
    <input type="hidden" name="_csrf_token" value="{{$session.csrf_token}}">

    <table cellspacing="0" cellpadding="2" border="0" width="98%">
    \t<tr>
    \t\t<td width="1%" nowrap="nowrap"><b>{{'common.name'|devblocks_translate|capitalize}}:</b></td>
    \t\t<td width="99%">
    \t\t\t<input type="text" name="name" value="{{$model->name}}" style="width:98%;" autofocus="autofocus">
    \t\t</td>
    \t</tr>

    \t{{if !empty($custom_fields)}}
    \t{{include file="devblocks:cerberusweb.core::internal/custom_fields/bulk/form.tpl" bulk=false tbody=true}}
    \t{{/if}}
    </table>

    {{include file="devblocks:cerberusweb.core::internal/custom_fieldsets/peek_custom_fieldsets.tpl" context=$peek_context context_id=$model->id}}

    {{if !empty($model->id)}}
    <fieldset style="display:none;" class="delete">
    \t<legend>{{'common.delete'|devblocks_translate|capitalize}}</legend>

    \t<div>
    \t\tAre you sure you want to permanently delete this {obj.lower()}?
    \t</div>

    \t<button type="button" class="delete red">{{'common.yes'|devblocks_translate|capitalize}}</button>
    \t<button type="button" class="delete-cancel">{{'common.no'|devblocks_translate|capitalize}}</button>
    </fieldset>
    {{/if}}

    <div class="buttons" style="margin-top:10px;">
    \t{{if $model->id}}
    \t\t<button type="button" class="save"><span class="glyphicons glyphicons-circle-ok"></span> {{'common.save_changes'|devblocks_translate|capitalize}}</button>
    \t\t<button type="button" class="save-continue"><span class="glyphicons glyphicons-circle-arrow-right"></span> {{'common.save_and_continue'|devblocks_translate|capitalize}}</button>
    \t\t{{if $active_worker->hasPriv("contexts.{{$peek_context}}.delete")}}<button type="button" class="delete-prompt"><span class="glyphicons glyphicons-circle-remove"></span> {{'common.delete'|devblocks_translate|capitalize}}</button>{{/if}}
    \t{{else}}
    \t\t<button type="button" class="save"><span class="glyphicons glyphicons-circle-plus"></span> {{'common.create'|devblocks_translate|capitalize}}</button>
    \t{{/if}}
    </div>

    </form>

    <script nonce="{{DevblocksPlatform::getRequestNonce()}}" type="text/javascript">
    $(function() {{
    \tlet $frm = $('#{{$form_id}}');
    \tlet $popup = genericAjaxPopupFind($frm);

    \tDevblocks.formDisableSubmit($frm);

    \t$popup.one('popup_open', function(event,ui) {{
    \t\t$popup.dialog('option','title',"{{'{obj}'|devblocks_translate|capitalize|escape:'javascript' nofilter}}");
    \t\t$popup.find('[autofocus]:first').focus();
    \t\t$popup.css('overflow', 'inherit');

    \t\t$popup.find('button.save').click(Devblocks.callbackPeekEditSave);
    \t\t$popup.find('button.save-continue').click({{ mode: 'continue' }}, Devblocks.callbackPeekEditSave);
    \t\t$popup.find('button.delete').click({{ mode: 'delete' }}, Devblocks.callbackPeekEditSave);
    \t\t$popup.find('button.delete-prompt').click(Devblocks.callbackPeekEditDeletePrompt);
    \t\t$popup.find('button.delete-cancel').click(Devblocks.callbackPeekEditDeleteCancel);
    \t}});
    }});
    </script>
    """)


def gen_view_tpl(table: str, plugin_id: str) -> str:
    cls = to_class_name(table)
    ctx = ctx_ext_id(table)
    fp = field_prefix(table)

    return dedent(f"""\
    {{$view_context = '{ctx}'}}
    {{$view_fields = $view->getColumnsAvailable()}}
    {{$results = $view->getData()}}
    {{$total = $results[1]}}
    {{$data = $results[0]}}

    {{include file="devblocks:cerberusweb.core::internal/views/view_marquee.tpl" view=$view}}

    <table cellpadding="0" cellspacing="0" border="0" class="worklist" width="100%" {{if array_key_exists('header_color', $view->options) && $view->options.header_color}}style="background-color:{{$view->options.header_color}};"{{/if}}>
    \t<tr>
    \t\t<td nowrap="nowrap"><span class="title">{{$view->name}}</span></td>
    \t\t<td nowrap="nowrap" align="right" class="title-toolbar">
    \t\t\t{{if $active_worker->hasPriv("contexts.{{$view_context}}.create")}}<a title="{{'common.add'|devblocks_translate|capitalize}}" class="minimal peek cerb-peek-trigger" data-context="{{$view_context}}" data-context-id="0"><span class="glyphicons glyphicons-circle-plus"></span></a>{{/if}}
    \t\t\t<a data-cerb-worklist-icon-search title="{{'common.search'|devblocks_translate|capitalize}}" class="minimal"><span class="glyphicons glyphicons-search"></span></a>
    \t\t\t<a data-cerb-worklist-icon-customize title="{{'common.customize'|devblocks_translate|capitalize}}" class="minimal"><span class="glyphicons glyphicons-cogwheel"></span></a>
    \t\t\t<a data-cerb-worklist-icon-subtotals title="{{'common.subtotals'|devblocks_translate|capitalize}}" class="minimal"><span class="glyphicons glyphicons-signal"></span></a>
    \t\t\t{{if $active_worker->hasPriv("contexts.{{$view_context}}.export")}}<a data-cerb-worklist-icon-export title="{{'common.export'|devblocks_translate|capitalize}}" class="minimal"><span class="glyphicons glyphicons-file-export"></span></a>{{/if}}
    \t\t\t<a data-cerb-worklist-icon-copy title="{{'common.copy'|devblocks_translate|capitalize}}"><span class="glyphicons glyphicons-duplicate"></span></a>
    \t\t\t<a data-cerb-worklist-icon-refresh title="{{'common.refresh'|devblocks_translate|capitalize}}" class="minimal"><span class="glyphicons glyphicons-refresh"></span></a>
    \t\t\t<input type="checkbox" class="select-all">
    \t\t</td>
    \t</tr>
    </table>

    <div id="{{$view->id}}_tips" class="block" style="display:none;margin:10px;padding:5px;">Loading...</div>
    <form id="customize{{$view->id}}" name="customize{{$view->id}}" action="#"></form>
    <form id="viewForm{{$view->id}}" name="viewForm{{$view->id}}" action="{{devblocks_url}}{{/devblocks_url}}" method="post">
    <input type="hidden" name="view_id" value="{{$view->id}}">
    <input type="hidden" name="context_id" value="{{$view_context}}">
    <input type="hidden" name="c" value="profiles">
    <input type="hidden" name="a" value="invoke">
    <input type="hidden" name="module" value="{table}">
    <input type="hidden" name="action" value="">
    <input type="hidden" name="explore_from" value="0">
    <input type="hidden" name="_csrf_token" value="{{$session.csrf_token}}">

    <table cellpadding="1" cellspacing="0" border="0" width="100%" class="worklistBody">
    \t<thead>
    \t<tr>
    \t\t{{if !array_key_exists('disable_watchers', $view->options) || !$view->options.disable_watchers}}
    \t\t<th class="no-sort" style="text-align:center;width:40px;padding-left:0;padding-right:0;" title="{{'common.watchers'|devblocks_translate|capitalize}}">
    \t\t\t<span class="glyphicons glyphicons-eye-open"></span>
    \t\t</th>
    \t\t{{/if}}
    \t\t{{foreach from=$view->view_columns item=header name=headers}}
    \t\t\t<th class="{{if array_key_exists('disable_sorting', $view->options) && $view->options.disable_sorting}}no-sort{{/if}}">
    \t\t\t{{if (!array_key_exists('disable_sorting', $view->options) || !$view->options.disable_sorting) && !empty($view_fields.$header->db_column)}}
    \t\t\t\t<a data-cerb-worklist-sort="{{$header}}">{{$view_fields.$header->db_label|capitalize}}</a>
    \t\t\t{{else}}
    \t\t\t\t<a style="text-decoration:none;">{{$view_fields.$header->db_label|capitalize}}</a>
    \t\t\t{{/if}}
    \t\t\t{{if $header==$view->renderSortBy}}
    \t\t\t\t<span class="glyphicons {{if $view->renderSortAsc}}glyphicons-sort-by-attributes{{else}}glyphicons-sort-by-attributes-alt{{/if}}" style="font-size:14px;{{if array_key_exists('disable_sorting', $view->options) && $view->options.disable_sorting}}color:rgb(80,80,80);{{else}}color:rgb(39,123,213);{{/if}}"></span>
    \t\t\t{{/if}}
    \t\t\t</th>
    \t\t{{/foreach}}
    \t</tr>
    \t</thead>

    \t{{$object_watchers = DAO_ContextLink::getContextLinks($view_context, array_keys($data), CerberusContexts::CONTEXT_WORKER)}}
    \t{{foreach from=$data item=result key=idx name=results}}

    \t{{if $smarty.foreach.results.iteration % 2}}
    \t\t{{$tableRowClass = "even"}}
    \t{{else}}
    \t\t{{$tableRowClass = "odd"}}
    \t{{/if}}
    \t<tbody style="cursor:pointer;">
    \t\t<tr class="{{$tableRowClass}}">
    \t\t\t<td data-column="*_watchers" align="center" nowrap="nowrap" style="padding:5px;">
    \t\t\t\t{{include file="devblocks:cerberusweb.core::internal/watchers/context_follow_button.tpl" context=$view_context context_id=$result.{fp}_id}}
    \t\t\t</td>
    \t\t{{foreach from=$view->view_columns item=column name=columns}}
    \t\t\t{{if DevblocksPlatform::strStartsWith($column, "cf_")}}
    \t\t\t\t{{include file="devblocks:cerberusweb.core::internal/custom_fields/view/cell_renderer.tpl"}}
    \t\t\t{{elseif $column == "{fp}_name"}}
    \t\t\t<td>
    \t\t\t\t<input type="checkbox" name="row_id[]" value="{{$result.{fp}_id}}" style="display:none;">
    \t\t\t\t<a href="{{devblocks_url}}c=profiles&type={table}&id={{$result.{fp}_id}}-{{$result.{fp}_name|devblocks_permalink}}{{/devblocks_url}}" class="subject">{{$result.{fp}_name}}</a>
    \t\t\t\t<button type="button" class="peek cerb-peek-trigger" data-context="{{$view_context}}" data-context-id="{{$result.{fp}_id}}"><span class="glyphicons glyphicons-new-window-alt"></span></button>
    \t\t\t</td>
    \t\t\t{{elseif in_array($column, ["{fp}_created_at", "{fp}_updated_at"])}}
    \t\t\t\t<td>
    \t\t\t\t\t{{if !empty($result.$column)}}
    \t\t\t\t\t\t<abbr title="{{$result.$column|devblocks_date}}">{{$result.$column|devblocks_prettytime}}</abbr>
    \t\t\t\t\t{{/if}}
    \t\t\t\t</td>
    \t\t\t{{else}}
    \t\t\t\t<td data-column="{{$column}}">{{$result.$column}}</td>
    \t\t\t{{/if}}
    \t\t{{/foreach}}
    \t\t</tr>
    \t</tbody>
    \t{{/foreach}}
    </table>

    {{if $total >= 0}}
    <div style="padding-top:5px;">
    \t{{include file="devblocks:cerberusweb.core::internal/views/view_paging.tpl" view=$view}}

    \t<div style="float:left;" id="{{$view->id}}_actions">
    \t\t{{$view_toolbar = $view->getToolbar()}}
    \t\t{{include file="devblocks:cerberusweb.core::internal/views/view_toolbar.tpl" view_toolbar=$view_toolbar}}
    \t\t{{if !$view_toolbar['explore']}}<button type="button" class="action-always-show action-explore"><span class="glyphicons glyphicons-compass"></span> {{'common.explore'|devblocks_translate|lower}}</button>{{/if}}
    \t</div>
    </div>
    {{/if}}

    <div style="clear:both;"></div>
    </form>

    {{include file="devblocks:cerberusweb.core::internal/views/view_common_jquery_ui.tpl"}}

    <script nonce="{{DevblocksPlatform::getRequestNonce()}}" type="text/javascript">
    $(function() {{
    \tlet $frm = $('#viewForm{{$view->id}}');
    }});
    </script>
    """)


def gen_plugin_xml_class_loader(table: str, dao_file: str) -> str:
    cls = to_class_name(table)
    return dedent(f"""\
    <file path="{dao_file}">
    \t<class name="Context_{cls}" />
    \t<class name="DAO_{cls}" />
    \t<class name="Model_{cls}" />
    \t<class name="SearchFields_{cls}" />
    \t<class name="View_{cls}" />
    </file>
    """)


def gen_plugin_xml_context(table: str, plugin_namespace: str, dao_file: str) -> str:
    cls = to_class_name(table)
    obj = to_object_name(table)
    ctx = ctx_ext_id(table)

    return dedent(f"""\
    <extension point="devblocks.context">
    \t<id>{ctx}</id>
    \t<name>{obj}</name>
    \t<class>
    \t\t<file>{dao_file}</file>
    \t\t<name>Context_{cls}</name>
    \t</class>
    \t<params>
    \t\t<param key="names">
    \t\t\t<value>
    \t\t\t\t<data key="{table}" value="singular" />
    \t\t\t\t<data key="{table}s" value="plural" />
    \t\t\t</value>
    \t\t</param>
    \t\t<param key="alias" value="{table}" />
    \t\t<param key="dao_class" value="DAO_{cls}" />
    \t\t<param key="view_class" value="View_{cls}" />
    \t\t<param key="options">
    \t\t\t<value>
    \t\t\t\t<data key="cards" />
    \t\t\t\t<data key="comments" />
    \t\t\t\t<data key="custom_fields" />
    \t\t\t\t<data key="links" />
    \t\t\t\t<data key="records" />
    \t\t\t\t<data key="search" />
    \t\t\t\t<data key="snippets" />
    \t\t\t\t<data key="va_variable" />
    \t\t\t\t<data key="watchers" />
    \t\t\t\t<data key="workspace" />
    \t\t\t</value>
    \t\t</param>
    \t\t<param key="acl">
    \t\t\t<value>
    \t\t\t\t<data key="broadcast" />
    \t\t\t\t<data key="comment" />
    \t\t\t\t<data key="create" />
    \t\t\t\t<data key="delete" />
    \t\t\t\t<data key="export" />
    \t\t\t\t<data key="import" />
    \t\t\t\t<data key="merge" />
    \t\t\t\t<data key="update" />
    \t\t\t\t<data key="update.bulk" />
    \t\t\t</value>
    \t\t</param>
    \t</params>
    </extension>
    """)


def gen_plugin_xml_profile_section(table: str, plugin_namespace: str, profile_file: str) -> str:
    cls = to_class_name(table)
    obj = to_object_name(table)

    return dedent(f"""\
    <extension point="cerberusweb.ui.page.section">
    \t<id>{plugin_namespace}.page.profiles.{table}</id>
    \t<name>{obj} Section</name>
    \t<class>
    \t\t<file>{profile_file}</file>
    \t\t<name>PageSection_Profiles{cls}</name>
    \t</class>
    \t<params>
    \t\t<param key="page_id" value="core.page.profiles" />
    \t\t<param key="uri" value="{table}" />
    \t</params>
    </extension>
    """)


def gen_strings_xml(table: str, fields: dict) -> str:
    cls = to_class_name(table)
    entries = '\n'.join(
        f"<tu tuid='dao.{table}.{f}'>\n\t<tuv xml:lang=\"en_US\">\n\t\t<seg>{' '.join(w.capitalize() for w in f.split('_'))}</seg>\n\t</tuv>\n</tu>"
        for f in fields
    )
    return f"<!-- {cls} -->\n\n{entries}\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def normalize(content: str) -> str:
    """Remove common leading spaces (not tabs) from all lines.
    Fixes the artifact where dedent() can't strip the function's indentation
    level when multi-line interpolated variables break the common prefix."""
    lines = content.split('\n')
    non_empty = [l for l in lines if l.strip()]
    if not non_empty:
        return content
    common = min(
        (len(l) - len(l.lstrip(' '))) for l in non_empty if l.startswith(' ')
    ) if any(l.startswith(' ') for l in non_empty) else 0
    if common > 0:
        lines = [l[common:] if l.startswith(' ' * common) else l for l in lines]
    return '\n'.join(lines)


def print_file(path: str, content: str):
    print(f"\n{'='*70}")
    print(f"FILE: {path}")
    print('='*70)
    print(normalize(content))


def write_file(base_dir: str, rel_path: str, content: str) -> str:
    """Write content to base_dir/rel_path, creating directories as needed. Returns the full path."""
    import os
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(normalize(content))
    return full_path


def main():
    parser = argparse.ArgumentParser(description='Generate Cerb record type boilerplate')
    parser.add_argument('--plugin-id', default='cerberusweb.core', help='Plugin ID (e.g. cerberusweb.core)')
    parser.add_argument('--plugin-namespace', default=None, help='Plugin namespace for extension IDs (defaults to first segment of plugin-id)')
    parser.add_argument('--table', required=True, help='Table/record name in snake_case (e.g. knowledge_source)')
    parser.add_argument('--fields', default="id bigint unsigned NOT NULL AUTO_INCREMENT, name varchar(255) NOT NULL DEFAULT '', created_at int unsigned NOT NULL DEFAULT 0, updated_at int unsigned NOT NULL DEFAULT 0",
                        help='Comma-separated SQL field definitions')
    parser.add_argument('--dao-file', default=None, help='Path to DAO file relative to plugin root (default: api/dao/{table}.php)')
    parser.add_argument('--profile-file', default=None, help='Path to profile file relative to plugin root (default: api/profiles/{table}.php)')
    parser.add_argument('--output-dir', default=None,
                        help='Plugin root directory to write files into (e.g. features/cerberusweb.core). '
                             'When set, files are written directly and only a manifest is printed. '
                             'Without this flag, all content is printed to stdout (dry-run).')

    # Allow JSON on stdin
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
            args = parser.parse_args([
                '--plugin-id', data.get('plugin_id', 'cerberusweb.core'),
                '--table', data['table'],
                '--fields', data.get('fields', 'id int unsigned, name varchar(255), updated_at int unsigned'),
            ])
            if 'plugin_namespace' in data:
                args.plugin_namespace = data['plugin_namespace']
            if 'output_dir' in data:
                args.output_dir = data['output_dir']
            fields = data.get('fields_map', None)
        except (json.JSONDecodeError, KeyError):
            args = parser.parse_args()
            fields = None
    else:
        args = parser.parse_args()
        fields = None

    plugin_id = args.plugin_id
    plugin_namespace = args.plugin_namespace or plugin_id.split('.')[0]
    table = args.table
    dao_file = args.dao_file or f'api/dao/{table}.php'
    profile_file = args.profile_file or f'api/profiles/{table}.php'
    output_dir = args.output_dir

    if fields is None:
        fields = parse_fields_from_sql(args.fields)

    fields = dict(sorted(fields.items()))

    cls = to_class_name(table)

    # Collect all generated files as (rel_path, content) pairs.
    # The DAO file gets all five PHP classes concatenated.
    php_classes = '\n'.join([
        gen_dao(table, fields, plugin_id),
        gen_search_fields(table, fields),
        gen_model(table, fields),
        gen_view(table, fields, plugin_id),
        gen_context(table, fields, plugin_id),
    ])

    generated = [
        (dao_file,                                          php_classes),
        (f'templates/records/types/{table}/peek_edit.tpl', gen_peek_edit_tpl(table, plugin_id)),
        (f'templates/records/types/{table}/view.tpl',       gen_view_tpl(table, plugin_id)),
    ]

    # plugin.xml and strings.xml are snippets only — printed as instructions either way
    xml_snippets = {
        'plugin.xml <class_loader>':           gen_plugin_xml_class_loader(table, dao_file),
        'plugin.xml <devblocks.context>':      gen_plugin_xml_context(table, plugin_namespace, dao_file),
        'plugin.xml <page.section>':           gen_plugin_xml_profile_section(table, plugin_namespace, profile_file),
        'strings.xml':                         gen_strings_xml(table, fields),
    }

    print(f"Cerb Record Type Generator")
    print(f"  Plugin:     {plugin_id}")
    print(f"  Table:      {table}")
    print(f"  Class:      {cls}")
    print(f"  Context ID: {ctx_ext_id(table)}")
    print()

    if output_dir:
        import os
        print(f"Writing files to: {output_dir}")
        for rel_path, content in generated:
            full_path = write_file(output_dir, rel_path, content)
            print(f"  Created: {rel_path}")
        print()
        print("Manual edits still required in plugin.xml and strings.xml:")
        for label, snippet in xml_snippets.items():
            print_file(label, snippet)
    else:
        print("Dry-run mode (no --output-dir). Pass --output-dir <plugin-root> to write files directly.\n")
        for rel_path, content in generated:
            print_file(rel_path, content)
        for label, snippet in xml_snippets.items():
            print_file(label, snippet)


if __name__ == '__main__':
    main()
