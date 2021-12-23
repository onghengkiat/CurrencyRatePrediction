import React, { useRef } from 'react';
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';
import { MdOutlineArrowLeft, MdOutlineArrowRight } from 'react-icons/md';
import './SidePanel.css'

export default function SidePanel({ token, isOpened, setIsOpened, currencyList, setCurrencyCode, algorithmList, setAlgorithm, setCPI, setGDP }){
    const currency_code_field = useRef(null);
    const algorithm_field = useRef(null);
    const cpi_field = useRef(null);
    const gdp_field = useRef(null);

    const sidePanelClassname = isOpened ? "side-panel open" : "side-panel";
    const sidePanelToggleClassname = isOpened ? "side-panel-toggle open" : "side-panel-toggle";

    const handleSubmit = async e => {
        e.preventDefault();
        setCurrencyCode(currency_code_field.current.value);
        if (token.role === "admin" || token.role === "developer"){
            setAlgorithm(algorithm_field.current.value);
            setCPI(cpi_field.current.checked);
            setGDP(gdp_field.current.checked);
        }
    }

    const toggleSidePanel = e => {
        setIsOpened(!isOpened);
    }

    return (
        <div className={sidePanelClassname}>
            <Form className="side-panel-form" role="form" onSubmit={handleSubmit}>
                <div className="side-panel-title-container">
                    <div className="side-panel-title">CONTROL PANEL</div>
                </div>
                <Form.Group>
                    <Form.Label>Select Currency Code : </Form.Label>
                    <Form.Control as="select" ref={ currency_code_field } custom>
                        {
                            currencyList.map((value, _) => {
                                return (  
                                    value === "USD" ? <option selected value={value}>{value}</option>: <option value={value}>{value}</option>
                                )
                            })
                        }
                    </Form.Control>
                </Form.Group>
                
                { (token.role === "admin" || token.role === "developer") &&
                <Form.Group>
                    <Form.Label>Select Algorithm : </Form.Label>
                    <Form.Control as="select" ref={ algorithm_field } custom>
                        {
                            algorithmList.map((value, _) => {
                                return (  
                                    value === "LINEAR" ? <option selected value={value}>{value}</option>: <option value={value}>{value}</option>
                                )
                            })
                        }
                    </Form.Control>
                </Form.Group>}

                { (token.role === "admin" || token.role === "developer") &&
                <Form.Group>
                    <Form.Check className="side-panel-checkbox" type="checkbox" defaultChecked={ true } ref={ cpi_field } label="Include CPI"/>
                </Form.Group>}  

                { (token.role === "admin" || token.role === "developer") &&
                <Form.Group>
                    <Form.Check className="side-panel-checkbox" type="checkbox" ref={ gdp_field } label="Include GDP"/>
                </Form.Group>}

                <div className="side-panel-button-container">
                    <Button type="submit" className="responsive side-panel-button">Apply Changes</Button>
                </div>
            </Form>
            <div className={sidePanelToggleClassname} onClick={toggleSidePanel}>
                { isOpened? <MdOutlineArrowLeft className="side-panel-toggle-icon"/>:<MdOutlineArrowRight className="side-panel-toggle-icon"/>}
            </div>
        </div>
    )
}