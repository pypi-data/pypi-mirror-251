def get_list_pipeline_columns(combination_queries):
    columns = []
    for value in combination_queries.values():
        for column in value['schema']:
            if column['name'].endswith('_pipeline_uuids'):
                columns.append(column['name'])
    # need to sort because selected columns in unioned queries have to have matching column orders
    columns = sorted(list(set(columns)))
    return columns

def remove_pipeline_uuid_columns_from_selects(selects):
    new_select = []
    for select in selects:
        if select['name'] == 'pipeline_uuids' or select['name'].endswith('_pipeline_uuids'):
            continue
        new_select.append(select)
    return new_select


def get_pipeline_selects_from_schema(schema):
    selects = []
    for column in schema:
        name = column['name']
        if name == 'pipeline_uuids' or name.endswith('_pipeline_uuids'):
            if name == 'pipeline_uuids':
                name = 't0_pipeline_uuids'
            selects.append({'value': f"t0.{column['name']}", 'name': name})
    return selects

def get_missing_pipeline_column(column_name):
    return {'value': {'split': {'literal': ' '}}, 'name': column_name}


def add_missing_pipeline_columns_to_pipeline_selects(selects, all_pipeline_columns):
    select_pipeline_columns = {}
    for column in selects:
        if column['name'] == 'pipeline_uuids' or column['name'].endswith('_pipeline_uuids'):
            select_pipeline_columns[column['name']] = True

    for column_name in all_pipeline_columns:
        if column_name not in select_pipeline_columns:
            selects.append(get_missing_pipeline_column(column_name))



def create_select_for_unioned_query(base_select, all_pipeline_columns, query_schema):

    pipeline_selects = get_pipeline_selects_from_schema(query_schema)

    add_missing_pipeline_columns_to_pipeline_selects(pipeline_selects, all_pipeline_columns)

    final_select = [value for value in base_select] + pipeline_selects
    return final_select

def create_union_filter(filters, all_pipeline_columns):
    final_filter = []
    for value in filters:
        if value['name'] != 'pipeline_uuids' and not value['name'].endswith('_pipeline_uuids'):
            final_filter.append(value)

    for column in all_pipeline_columns:
        final_filter.append({'name': column, 'value': f't0.{column}', 'type': 'ARRAY'})

    return final_filter



def wrap_union_ast_in_subquery(base_select, all_pipeline_columns, group_by, union_ast):
    from camtono.derivatives.transforms import apply_transforms
    from_ast = ['t0']
    select_ast = [value for value in base_select]
    for pipeline_name in all_pipeline_columns:
        pipeline_prefix = pipeline_name.split('_')[0]
        from_ast.append({'cross join': {'name': f'{pipeline_prefix}_pipeline_uuid', 'value': {'unnest': f'{pipeline_name}'}}})

        value, data_type = apply_transforms(value=f'{pipeline_prefix}_pipeline_uuid'
                                            , data_type='ARRAY'
                                            , transforms=[{'name':'array_agg_distinct'}] #output['transforms']
                                            )
        select_ast.append(
            dict(
                name=pipeline_name,
                value=value,
                type=data_type
            )
        )
    ast = {'select':select_ast
            , 'from':from_ast
            , 'groupby':[group.replace('base', 't0') for group in group_by]
            , 'with': {'name': 't0',
                       'value': union_ast
           }
        }
    return ast