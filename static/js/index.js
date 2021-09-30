function isNotEmpty(value) {
    return value !== undefined && value !== null && value !== "";
}

function parseSearchFromFilter(loadOptions, args) {
    const filter = loadOptions.filter;
    if (filter && filter.length === 3) {
        args['search'] = filter[2]
    }
}

$(function(){
    let itemsChart;
    const aggregateValues = [1, 5, 10, 25, 50, 100];
    const maxPointsValues = [100, 500, 1000];
    let currentAggregateCount = aggregateValues[3];
    let currentMaxPointsValue = maxPointsValues[2];
    let idsToLoad = [];

    $("#aggregateIntervalRadio").dxRadioGroup({
        items: aggregateValues,
        value: currentAggregateCount,
        layout: "horizontal",
        onValueChanged: function(e){
            currentAggregateCount = e.value;
            itemsChart.option('argumentAxis.tickInterval', e.value);
            itemsChart.option('argumentAxis.aggregationInterval', e.value);
        }
    });

    $("#maxPointsRadio").dxRadioGroup({
        items: maxPointsValues,
        value: currentMaxPointsValue,
        layout: "horizontal",
        onValueChanged: function(e){
            currentMaxPointsValue = e.value;
            loadChartDataByIds();
        }
    });

    let store = new DevExpress.data.CustomStore({
        key: "id",
        load: function (loadOptions) {
            const deferred = $.Deferred(),
                  args = {};
            parseSearchFromFilter(loadOptions, args);
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
            const deferred = $.Deferred();
            $.ajax({
                url: `/api/market-data/search_items/${id}/`,
                method: 'PUT',
                dataType: "json",
                data: options,
                success: function() {
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

    $("#items-grid").dxDataGrid({
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
            idsToLoad = selectedItems.selectedRowKeys;
            loadChartDataByIds();
        },
        height: 350,
    });

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
            tickInterval: currentAggregateCount,
            aggregationInterval: currentAggregateCount,
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
        tooltip: {
            enabled: true,
            contentTemplate: function(info, container) {
                const content = $('<div>');
                $('<div>').text(`День: ${info.argument}`).appendTo(content);
                $('<div>').text(`Цена: ${parseInt(info.value)}`).appendTo(content);
                content.appendTo(container);
            }
        },
        size: {
            height: 500
        }
    }).dxChart('instance');

    function loadChartDataByIds() {
        let ids = idsToLoad;
        if (ids.length === 0) {
            itemsChart.option('series', [])
            itemsChart.option('dataSource', [])
            return;
        }
        $.ajax({
            url: `/api/market-data/get_chart_data_by_ids/?ids=${ids.join(',')}`,
            dataType: "json",
            success: function(result) {
                let data = result.data;
                data = data.slice(0, currentMaxPointsValue)
                itemsChart.option('series', result.series)
                itemsChart.option('dataSource', data)
            },
            error: function(e) {
                console.error(e)
            },
            timeout: 5000
        });
    }
});