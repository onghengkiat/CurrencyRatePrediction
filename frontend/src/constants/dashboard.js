export const columns = [
    {
        title: "Date",
        field: "date",
        type: "date",
        render: (rowData, renderType) => {
            if (renderType === 'row') {
                return <div>{rowData.date}</div>;
            }
            if (renderType === 'group') {
                return rowData
            }
        }
    },
    {
        title: "Currency Code",
        field: "currency_code",
        defaultGroupOrder: 0,
    },
    {
        title: "To MYR",
        field: "to_myr",
        grouping: false,
        render: rowData => {
            if (rowData.rate_changed_to_myr === 0) {
                return (
                    <div>
                        {rowData.to_myr} <div></div>
                    </div>
                )
            } else if (rowData.rate_is_increased_to_myr) {
                return (
                    <div>
                        {rowData.to_myr} <div className="increase">( + {rowData.rate_changed_to_myr} % )</div>
                    </div>
                );
            } else {
                return (
                    <div>
                        {rowData.to_myr} <div className="decrease">( - {rowData.rate_changed_to_myr} % )</div>
                    </div>
                );
            }
        }
    },
    {
        title: "From MYR",
        field: "from_myr",
        grouping: false,
        render: rowData => {
            if (rowData.rate_changed_from_myr === 0) {
                return (
                    <div>
                        {rowData.from_myr} <div></div>
                    </div>
                )
            } else if (rowData.rate_is_increased_from_myr) {
                return (
                    <div>
                        {rowData.from_myr} <div className="increase">( + {rowData.rate_changed_from_myr} % )</div>
                    </div>
                );
            } else {
                return (
                    <div>
                        {rowData.from_myr} <div className="decrease">( - {rowData.rate_changed_from_myr} % )</div>
                    </div>
                );
            }
        }
    },
    {
        title: "Prediction",
        field: "is_prediction",
    },
]