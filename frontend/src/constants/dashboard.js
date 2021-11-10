export const columns = [
    {
        title: "Date",
        field: "date",
        type: "date",
    },
    {
        title: "Currency Code",
        field: "currency_code",
    },

    {
        title: "CPI (Prev Month)",
        field: "cpi",
    },
    {
        title: "GDP Growth Rate (Prev Year)",
        field: "gdp",
    },
    {
        title: "To MYR",
        field: "to_myr",
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
]