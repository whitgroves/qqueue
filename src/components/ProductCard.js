import React from 'react';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Col, Row, Button } from 'react-bootstrap';

// Component

export default function ProductCard(props) {
  let product = props.product;
  
  // Default values for non-required fields
  let imageUrl = product && product.image_url ? product.image_url : 'https://via.placeholder.com/150';
  let price = product && product.price ? `$${product.price.toFixed(2)}` : 'not for sale';
  let tagline = product && product.tagline ? product.tagline : '';

  return (
    <Card style={{ width: '15rem' }}>
      <Card.Img variant="top" src={imageUrl}/>
      <Card.Body>
          <Card.Title>{product.name}</Card.Title>
          <Card.Subtitle>{price}</Card.Subtitle>
          <Card.Text>{tagline}</Card.Text>
          <Row>
            <Col>
              <Button variant="outline-dark" size="sm" href={'/product/'+product.id}>view →</Button>{' '}
            </Col>
            <Col md="auto">
              {
                false  // should be a check if user is the item's seller
                  ? ''
                  : 
                    <Button variant="outline-primary" size="sm" onClick={() => props.addToCart(product.id)}>
                      add to cart +
                    </Button>
              }
            </Col>
          </Row>
      </Card.Body>
    </Card>
  );
}