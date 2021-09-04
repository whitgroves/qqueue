import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { Container, Navbar, Nav } from 'react-bootstrap';

function App() {
  const [currentTime, setCurrentTime] = useState(0);
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });

    fetch('/api/products').then(res => res.json()).then(data => {
      setProducts(data.products);
    });
  }, []); // Empty list is used to eliminate dependencies so this is only invoked once.

  const AllProducts = () => {
    return (
      <div class="d-grid gap-3">
        {products.map((product, index) => (
          <div class="p-2 bg-light border">
            <p key={product.id}>{product.name} is {product.price}</p>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div id="page-wrapper" class="d-grid gap-3">
      <Navbar collapseOnSelect bg="dark" variant="dark" expand="lg" sticky="top">
        <Container>
          <Navbar.Brand href="#home">qqueue</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto"> 
              <Nav.Link href="#market">market</Nav.Link>
              <Nav.Link href="#login">login</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Container>
        <AllProducts className="vh-80"/>
      </Container>
      <div class="position-relative">
        <p class="text-center">The current time is {currentTime}.</p>
      </div>
    </div>
  );
}

export default App;
