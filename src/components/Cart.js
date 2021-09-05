import React, { useState, useEffect } from 'react';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Button, Badge, Container, Card, ListGroup, ListGroupItem, Row, Col, Image } from 'react-bootstrap';

// Component

export default function Cart(props) {

  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/products').then(res => res.json()).then(data => {
      setProducts(data.products);
    });
  }, []); // Remove dependencies so it only loads once.

  const cartItems = [];
  for (var id in props.cart) {
    let product = products.find(p => p.id === parseInt(id));
    if (product) {
      cartItems.push(
        <ListGroupItem key={id}>
          <Container>
            <Row>
              <Col className="d-inline-flex align-items-center" md="auto">
                <Image src={product.image_thumbnail} rounded/>
              </Col>
              <Col className="d-inline-flex align-items-center">
                {product.name}
                <div class="px-1"/>
                <Badge pill bg="dark" md="auto">x{props.cart[id]}</Badge>
              </Col>
              <Col className="d-inline-flex align-items-center" md="auto">
                <Button href={'/product/'+id}>view details</Button>
                <div class="px-1"/>
                <Button variant="outline-primary" onClick={() => props.addToCart(product.id)}>
                  +1
                </Button>
                <div class="px-1"/>
                <Button variant="outline-danger" onClick={() => props.removeFromCart(product.id)}>
                  -1
                </Button>
                <div class="px-1"/>
                <Button variant="outline-danger" onClick={() => props.removeAllFromCart(product.id)}>
                  remove
                </Button>
              </Col>
            </Row>
          </Container>
        </ListGroupItem>
      );
    }
    
  }
  // Render

  return (
    <Container>
      <Card>
        <Card.Header>My Cart</Card.Header>
        {/* <Card.Body>
          <Button variant="danger" onClick={() => props.emptyCart()}>
            Empty Cart 
          </Button>
        </Card.Body> */}
        <ListGroup variant="flush">
          {
            cartItems.length > 0 
              ? cartItems 
              : <ListGroupItem>Your cart is empty.</ListGroupItem>
          }
        </ListGroup>
      </Card>
    </Container>
  );
}