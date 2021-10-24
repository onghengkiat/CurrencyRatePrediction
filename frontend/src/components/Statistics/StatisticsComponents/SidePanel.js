import React, { useRef } from 'react';
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';

export default function SidePanel({ currencyList, setCurrencyCode }){
    const currency_code_field = useRef(null);

    const handleSubmit = async e => {
        e.preventDefault();
        setCurrencyCode(currency_code_field.current.value);
    }
    return (
        <Form className="side-panel" role="form" onSubmit={handleSubmit}>
            <div id="side-panel-title-container">
                <div id="side-panel-title">Control Panel</div>
            </div>
            <Form.Group controlId="exampleForm.SelectCustom">
                <Form.Label>Select Currency Code : </Form.Label>
                <Form.Control as="select" ref={ currency_code_field } custom>
                    {
                        currencyList.map((value, _) => {
                            return (  
                                <option value={value}>{value}</option>
                            )
                        })
                    }
                </Form.Control>
            </Form.Group>
            <Button type="submit">Apply Changes</Button>
        </Form>
    )
}