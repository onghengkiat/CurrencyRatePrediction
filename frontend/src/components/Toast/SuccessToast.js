import Toast from 'react-bootstrap/Toast';
import React, {useState, useEffect} from 'react';
import './Toast.css'

export default function SuccessToast({ success, setSuccess }){
    const [show, setShow] = useState(false)

    useEffect( () => {
        if(success?.code) {
            setShow(true);
        }
    }, [success]);

    // show the error toast if error occurs when API calls
    // the toast will be hidden after 5 seconds
    return (
        <Toast type="info" id="toast-success" onClose={() => {setShow(false); setSuccess("")}} show={show} delay={5000} autohide>
                <Toast.Header id="toast-success-header">
                    {success.code}
                </Toast.Header>
            <Toast.Body>{success.message}</Toast.Body>
        </Toast>
    )
}