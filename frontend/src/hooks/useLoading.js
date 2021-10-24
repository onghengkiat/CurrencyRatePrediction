import { useState } from 'react';

export default function useLoading() {

  const [loading, setLoading] = useState(false);
  
  const saveLoading = isLoading => {
    setLoading(isLoading);
  };

  return {
    setLoading: saveLoading,
    loading: loading
  }
}