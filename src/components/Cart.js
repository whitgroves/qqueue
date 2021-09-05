import React, { useState, useEffect } from 'react';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { 
  Button, Badge, Container, Card, ListGroup, ListGroupItem, Row, Col, Image 
} from 'react-bootstrap';

// Component

export default function Cart(props) {

  // Cart items
  const [products, setProducts] = useState([]);

  useEffect(() => {
    // product catalog fetched to reference details
    // TODO: store the product information in props.cart
    // OR cache the product list in the db so it's not expensive to fetch
    fetch('/api/products').then(res => res.json()).then(data => {
      setProducts(data.products);
    });
  }, []); // Remove dependencies so it only loads once.

  const cartItems = [];
  let cartSubtotal = 0.0;
  for (var id in props.cart) {
    let product = products.find(p => p.id === parseInt(id));
    if (product) {
      let itemSubtotal = product.price * props.cart[id];
      cartItems.push(
        <ListGroupItem key={id}>
          <Container>
            <Row>

              <Col className="d-inline-flex align-items-center" md="auto">
                <Image src={product.image_thumbnail} rounded/>
              </Col>

              <Col className="d-inline-flex align-items-center">
                {product.name}
              </Col>

              {/* <Col className="d-inline-flex align-items-center" md="auto">
                <Button variant="outline-primary" href={'/product/'+id}
                  >← details
                </Button>
                <div class="px-1"/>
              </Col> */}

              <Col className="d-inline-flex align-items-center" md="auto">
                <Badge bg="success" md="auto">${product.price.toFixed(2)}</Badge>
                <div class="px-1"/>
                <Badge pill bg="secondary" md="auto">x{props.cart[id]}</Badge>
                <div class="px-2" />
              </Col>

              <Col className="d-inline-flex align-items-center" md="auto"> 
                <Button
                  variant="outline-primary"
                  size="sm"
                  onClick={() => props.addToCart(product.id)}
                >
                  +1
                </Button>
                <div class="px-1"/>

                <Button variant="outline-success" disabled>
                  ${itemSubtotal.toFixed(2)}
                </Button>
                <div class="px-1"/>

                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => props.removeFromCart(product.id)}
                >
                  -1
                </Button>
                <div class="px-1"/>
              </Col>

              <Col className="d-inline-flex align-items-center" md="auto">
                <Button variant="outline-danger" onClick={() => props.removeAllFromCart(product.id)}>
                  🗑
                </Button>
              </Col>

            </Row>
          </Container>
        </ListGroupItem>
      );
      cartSubtotal += itemSubtotal;
    }
  }

  return (
    <Container>
      <Card>
        <Card.Header>my cart</Card.Header>
        <ListGroup variant="flush">
          {
            cartItems.length > 0 
              ? cartItems 
              : <ListGroupItem>
                  Your cart is empty. Try checking out the <a href="/market">market</a>.
                </ListGroupItem>
          }
        </ListGroup>
        <Card.Body>
          <Container>
            <Row>

              <Col md="auto">
                <Button href="/market" variant="dark">← market</Button>
              </Col>

              <Col></Col> {/* Spacer column */}

              <Col className="d-inline-flex align-items-center" md="auto">
                <Button variant="success" onClick={() => console.log('checkout')}>
                  checkout →
                </Button>
                <div class="px-1" />

                <Badge bg="secondary">
                  {props.cartCount} items
                </Badge>
              </Col>

              <Col className="d-inline-flex align-items-center" md="auto">
                <Button style={{ width: "164px"}} variant="outline-success" disabled>
                  ${cartSubtotal.toFixed(2)}
                </Button>
              </Col>

              <Col md="auto">
                <Button variant="danger" onClick={() => props.emptyCart()}>
                  🗑
                </Button>
              </Col>

            </Row>
          </Container>
        </Card.Body>
      </Card>
    </Container>
  );
}