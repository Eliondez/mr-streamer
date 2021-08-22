$(function(){
    let itemData = [];
    let itemsGrid, itemsChart, itemNameInput;

    itemsGrid = $("#items-grid").dxDataGrid({
        dataSource: itemData,
        keyExpr: 'id',
        columns: [{
            dataField: "id",
            width: 70
        }, "name"],
        height: 'auto',
        paging: {
            pageSize: 10
        },
        selection: {
            mode: "multiple"
        },
        showBorders: true,
        onSelectionChanged: function(selectedItems) {
            // console.log('selectedItems', selectedItems.selectedRowKeys);
            loadChardDataByIds(selectedItems.selectedRowKeys);
        }
    }).dxDataGrid('instance');

    itemsChart = $("#chart").dxChart({
        dataSource: [],
        legend: {
            visible: false
        },
        commonSeriesSettings: {
            type: 'spline',
            argumentField: "day"
        },
        argumentAxis: {
            tickInterval: 10,
            label: {
                format: {
                    type: "decimal"
                }
            }
        },
        series: [
            {'valueField': 'id30', 'name': '30'},
            {'valueField': 'id31', 'name': '31'},
            {'valueField': 'id29', 'name': '29'}
        ],
        size: {
            height: 500
        }
    }).dxChart('instance');

    itemNameInput = $("#search-box").dxTextBox({
        value: "",
        showClearButton: true,
        placeholder: "Введите название предмета",
        valueChangeEvent: "keyup",
        onValueChanged: function(data) {
            loadItemsByName(data.value);
        }
    }).dxTextBox('instance');


    function loadItemsByName(name) {
        $.ajax({
            url: `/api/market-data/search_items/?page_size=500&search=${name}`,
            dataType: "json",
            success: function(result) {
                itemsGrid.option('dataSource', result.results)
            },
            error: function(e) {
                console.log('Error', e)
            },
            timeout: 5000
        });
    }

    function loadChardDataByIds(ids) {
        if (ids.length === 0) {
            return;
        }
        $.ajax({
            url: `/api/market-data/get_chart_data_by_ids/?ids=${ids.join(',')}`,
            dataType: "json",
            success: function(result) {
                console.log(result);
                itemsChart.option('series', result.series)
                itemsChart.option('dataSource', result.data)
            },
            error: function(e) {
                console.log('Error', e)
            },
            timeout: 5000
        });
    }

    setTimeout(function() {
        itemNameInput.option('value', 'Knife | Night');
    }, 500);
});