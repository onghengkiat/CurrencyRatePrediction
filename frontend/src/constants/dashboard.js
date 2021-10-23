export const columns = [
    {
        title: "Date",
        field: "date",
    },
    {
        title: "Currency Code",
        field: "currency_code",
    },
    {
        title: "To MYR",
        field: "to_myr",
        render: rowData => {
            if (rowData.rate_is_increased) {
                return (
                    <div>
                        {rowData.to_myr} <div className="increase">( + {rowData.rate_changed} % )</div>
                    </div>
                );
            } else {
                return (
                    <div>
                        {rowData.to_myr} <div className="decrease">( - {rowData.rate_changed} % )</div>
                    </div>
                );
            }
        }
    },
    {
        title: "From MYR",
        field: "from_myr",
    },
]