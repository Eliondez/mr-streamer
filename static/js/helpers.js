function filterToQuery(filter, remap) {
    // Превращает filter-праметр из dx-элемента в query-параметры.
    // filter имеет вложенную структуру, поэтому разбираем его рекурсивно.
    // В ходе разбора все параметры объединяются через И.
    remap = remap || {};
    let res = [];
    if (!filter) return res;
    let operators = {
        '=': '=',
        'contains': '__icontains=',
        '>=': '__gte=',
        '<=': '__lte=',
        '>': '__gt=',
        '<': '__lt='
    }

    if (Array.isArray(filter)) {
        if (Array.isArray(filter[0])) {
            filter.forEach(item => {
                if (Array.isArray(item)) {
                    res = res.concat(filterToQuery(item, remap));
                }
            })
            return res;
        }
        let name;
        if (filter[0] in remap) {
            name = remap[filter[0]]
        } else {
            name = filter[0]
        }
        res.push(`${name}${operators[filter[1]]}${filter[2]}`);
        return res;
    }
}
