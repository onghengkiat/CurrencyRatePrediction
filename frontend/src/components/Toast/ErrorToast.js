import Toast from 'react-bootstrap/Toast';
import React, {useState, useEffect} from 'react';
import './Toast.css'

export default function ErrorToast({ error, setError, setToken }){
    const [show, setShow] = useState(false)

    useEffect( () => {
        if(error) {
            if(!error.code) {
                setError({
                    "code": "Test Error", 
                    "message": "Something wrong happened. Try to reload or contact the administrator."
                })
            }
            if(error.code === "Not Authenticated") {
                setToken({
                    "isLoggedIn": false,
                    "role": "visitor",
                })
            }
            setShow(true);
        }
    }, [error]);

    // show the error toast if error occurs when API calls
    // the toast will be hidden after 5 seconds
    return (
        <Toast type="info" id="toast-error" onClose={() => {setShow(false); setError("")}} show={show} delay={5000} autohide>
                <Toast.Header id="toast-error-header">
                    {error.code}
                </Toast.Header>
            <Toast.Body>{error.message}</Toast.Body>
        </Toast>
    )
}