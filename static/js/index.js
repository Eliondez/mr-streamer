function isNotEmpty(value) {
    return value !== undefined && value !== null && value !== "";
}

function parseSearchFromFilter(loadOptions, args) {
    console.log('loadOptions', loadOptions);
    const filter = loadOptions.filter;
    if (filter && filter.length === 3) {
        args['search'] = filter[2]
    }
}

$(function(){
    let itemsGrid, itemsChart;
    let store = new DevExpress.data.CustomStore({
        key: "id",
        load: function (loadOptions) {
            const deferred = $.Deferred(),
                args = {};
            parseSearchFromFilter(loadOptions, args);
            let res = filterToQuery(loadOptions.filter);
            console.log('res', res);

            // params.push(...filterToQuery(loadOptions.filter, {
            //     category: 'category',
            //     start_month: 'start_month',
            //     end_month: 'end_month',
            // }));

            let page_size = loadOptions['take'];
            let skip = loadOptions['skip'];
            args['page'] = skip / page_size + 1;
            args['page_size'] = page_size;
            $.ajax({
                url: "/api/market-data/search_items/",
                dataType: "json",
                data: args,
                success: function(result) {
                    deferred.resolve(result.results, {
                        totalCount: result.count,
                    });
                },
                error: function() {
                    deferred.reject("Data Loading Error");
                },
                timeout: 5000
            });

            return deferred.promise();
        },
        update: function(id, options) {
            console.log('options', id, options);
            const deferred = $.Deferred();
            $.ajax({
                url: `/api/market-data/search_items/${id}/`,
                method: 'PUT',
                dataType: "json",
                data: options,
                success: function(result) {
                    console.log('OK');
                    deferred.resolve();
                },
                error: function() {
                    deferred.reject("Data Loading Error");
                },
                timeout: 5000
            });

            return deferred.promise();
        }
    });

    itemsGrid = $("#items-grid").dxDataGrid({
        dataSource: store,
        showBorders: true,
        remoteOperations: true,
        filterRow: {
            visible: true,
            applyFilter: "auto"
        },
        paging: {
            pageSize: 100
        },
        sorting: {
            mode: "none"
        },
        editing: {
            mode: "row",
            allowUpdating: true,
            allowDeleting: false,
            allowAdding: false
        },
        columns: [
            {
                allowEditing: false,
                dataField: "id",
                width: 70,
                allowFiltering: false
            },
            {
                allowEditing: false,
                dataField: "name",
                filterOperations: ['contains'],
            },
            {
                filterOperations: ['='],
                dataField: "rating",
                dataType: 'number',
                alignment: 'center',
                validationRules: [{
                    type: "range",
                    max: 100,
                    min: 0,
                    message: "0-100"
                }]
            }
        ],
        selection: {
            mode: "multiple"
        },
        onSelectionChanged: function(selectedItems) {
            loadChardDataByIds(selectedItems.selectedRowKeys);
        },
        height: 400,
    }).dxDataGrid("instance");

    itemsChart = $("#chart").dxChart({
        dataSource: [],
        commonSeriesSettings: {
            type: 'spline',
            argumentField: "day",
            aggregation: {
                enabled: true
            }
        },
        legend: {
            verticalAlignment: "bottom",
            horizontalAlignment: "center",
            itemTextPosition: "bottom"
        },
        argumentAxis: {
            tickInterval: 50,
            aggregationInterval: 50,
            label: {
                format: {
                    type: "decimal"
                }
            }
        },
        valueAxis: {
            type: "logarithmic",
            linearThreshold: -3
        },
        series: [],
        size: {
            height: 500
        }
    }).dxChart('instance');

    function loadChardDataByIds(ids) {
        if (ids.length === 0) {
            itemsChart.option('series', [])
            itemsChart.option('dataSource', [])
            return;
        }
        $.ajax({
            url: `/api/market-data/get_chart_data_by_ids/?ids=${ids.join(',')}`,
            dataType: "json",
            success: function(result) {
                itemsChart.option('series', result.series)
                itemsChart.option('dataSource', result.data)
            },
            error: function(e) {
                console.log('Error', e)
            },
            timeout: 5000
        });
    }

    console.log('hehehre!');
    $(window).on('click', '.reduce-rating-1', function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('increase', this);
    })
});