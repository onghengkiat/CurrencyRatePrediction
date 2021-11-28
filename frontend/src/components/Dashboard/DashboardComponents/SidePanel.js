import React, { useRef } from 'react';
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';
import { MdOutlineArrowLeft, MdOutlineArrowRight } from 'react-icons/md';

export default function SidePanel({ isOpened, setIsOpened, currencyList, setCurrencyCode }){
    const currency_code_field = useRef(null);

    const sidePanelClassname = isOpened ? "side-panel open" : "side-panel";
    const sidePanelToggleClassname = isOpened ? "side-panel-toggle open" : "side-panel-toggle";

    const handleSubmit = async e => {
        e.preventDefault();
        setCurrencyCode(currency_code_field.current.value);
    }

    const toggleSidePanel = e => {
        setIsOpened(!isOpened);
    }

    return (
        <div className={sidePanelClassname}>
            <Form className="side-panel-form" role="form" onSubmit={handleSubmit}>
                <div className="side-panel-title-container">
                    <div className="side-panel-title">Control Panel</div>
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
                <Button type="submit" className="responsive side-panel-button">Apply Changes</Button>
            </Form>
            <div className={sidePanelToggleClassname} onClick={toggleSidePanel}>
                { isOpened? <MdOutlineArrowLeft className="side-panel-toggle-icon"/>:<MdOutlineArrowRight className="side-panel-toggle-icon"/>}
            </div>
        </div>
    )
}