import React, { useRef } from 'react';
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';

export default function SidePanel({ currencyList, setCurrencyCode, algorithmList, setAlgorithm, setCPI, setGDP }){
    const currency_code_field = useRef(null);
    const algorithm_field = useRef(null);
    const cpi_field = useRef(null);
    const gdp_field = useRef(null);

    const handleSubmit = async e => {
        e.preventDefault();
        setCurrencyCode(currency_code_field.current.value);
        setAlgorithm(algorithm_field.current.value);
        setCPI(cpi_field.current.checked);
        setGDP(gdp_field.current.checked);
    }
    return (
        <Form className="side-panel" role="form" onSubmit={handleSubmit}>
            <div id="side-panel-title-container">
                <div id="side-panel-title">Control Panel</div>
            </div>
            <Form.Group>
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
            
            <Form.Group>
                <Form.Label>Select Algorithm : </Form.Label>
                <Form.Control as="select" ref={ algorithm_field } custom>
                    {
                        algorithmList.map((value, _) => {
                            return (  
                                <option value={value}>{value}</option>
                            )
                        })
                    }
                </Form.Control>
            </Form.Group>

            <Form.Group>
                <Form.Check type="checkbox" ref={ cpi_field } label="Include CPI"/>
            </Form.Group>

            <Form.Group>
                <Form.Check type="checkbox" ref={ gdp_field } label="Include GDP"/>
            </Form.Group>
            <Button type="submit" className="responsive" id="side-panel-button">Apply Changes</Button>
        </Form>
    )
}