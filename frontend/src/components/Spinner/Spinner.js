import React, {useState, useEffect} from 'react';
import './Spinner.css'

export default function Spinner({ loading }){

    const [show, setShow] = useState(false)

    useEffect( () => {
        if (loading) {
            setShow(true);
        } else {
            setShow(false);
        }
    }, [loading]);

    return (
        show && <div class="loader-container">
            <div class="loader"></div>
        </div>
        
    )
}