import { useState } from 'react';

// to store and access the error object
export default function useError() {

  const [error, setError] = useState("");
  
  const saveError = err => {
    setError(err);
  };

  return {
    setError: saveError,
    error: error
  }
}