import React, { useState, useEffect } from 'react';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Col, Row } from 'react-bootstrap';
import ItemCard from './ItemCard';

// Component

export default function Market(props) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/market/').then(res => res.json()).then(data => {
      setProducts(data.products);
    });
  }, []); // Remove dependencies so it only loads once.

  return (
    <Container fluid>
      <Row className="gap-4">
          {products.map((product, index) => (
          <Col key={index}>
            <ItemCard
              product={product}
              isVendor={false}
            />
          </Col>
          ))}
      </Row>
    </Container>
  );
}