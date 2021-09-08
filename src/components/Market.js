import React, { useState, useEffect } from 'react';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Card, Col, Row, Button } from 'react-bootstrap';
import ItemCard from './ItemCard';

// Component

export default function Market(props) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/products').then(res => res.json()).then(data => {
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
              isVendor={props.isVendor}
            />
          </Col>
          ))}
      </Row>
    </Container>
  );
}