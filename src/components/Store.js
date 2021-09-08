import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { 
  Container
} from 'react-bootstrap';

// Component

export default function Store() {
  const { id } = useParams();
  let history = useHistory();

  if (parseInt(id) === 0) {
    history.push('/404');
  }

  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/store/'+id).then(res => res.json()).then(data => {
      setProducts(data.products);
    });
  }, [id]);

  return (
    <Container>
      Welcome to {id}'s store.
    </Container>
  );
}