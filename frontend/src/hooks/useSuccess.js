import { useState } from 'react';

// to store and access the error object
export default function useSuccess() {

  const [success, setSuccess] = useState("");
  
  const saveSuccess = err => {
    setSuccess(err);
  };

  return {
    setSuccess: saveSuccess,
    success: success
  }
}