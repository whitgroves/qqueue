import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

// Styles

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Navbar, Nav } from 'react-bootstrap';

// Components

import Market from './components/Market';
import Product from './components/Product';
import Cart from './components/Cart';

// App

function App() {

  // Time

  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []); // Empty dependencies so it doesn't constantly reload.

  // Cart

  // localStorage is used to persist cart between pages.
  let storedCart = JSON.parse(localStorage.getItem('cart'));

  const [cart, setCart] = useState(storedCart ? storedCart : {});
  const [itemsInCart, setItemsInCart] = useState(0);

  useEffect(() => {
    if (Object.keys(cart).length > 0) {
      setItemsInCart(Object.values(cart).reduce((a, b) => a + b));
    }
  }, [cart]);

  useEffect(() => {}, [itemsInCart]); // Empty handler to enable updates.

  const updateCart = (update) => {
    let hardCopy = { ...cart };
    update(hardCopy);
    setCart(hardCopy);
    // localStorage is used to persist cart between pages.
    localStorage.setItem('cart', JSON.stringify(hardCopy));
  }

  const addToCartHandler = (product_id) => {
    const addToCart = (cartCopy) => {
      if (product_id in cartCopy) {
        cartCopy[product_id] += 1;
      } else {
        cartCopy[product_id] = 1;
      }
    }
    updateCart(addToCart);
  }

  const removeFromCartHandler = (product_id) => {
    const removeFromCart = (cartCopy) => {
      cartCopy[product_id] -= 1;
      if (cartCopy[product_id] === 0) {
        delete cartCopy[product_id];
      }
    }
    updateCart(removeFromCart);
  }

  const removeAllFromCartHandler = (product_id) => {
    const removeAllFromCart = (cartCopy) => {
        delete cartCopy[product_id];
    }
    updateCart(removeAllFromCart);
  }

  const emptyCartHandler = () => {
    const emptyCart = (cartCopy) => {
      for (var item in cartCopy) {
        delete cartCopy[item];
      }
    }
    updateCart(emptyCart);
  }

  // Render

  return (
    <div id="wrapper" class="d-grid gap-3">

      <Navbar collapseOnSelect bg="dark" variant="dark" expand="lg" sticky="top">
        <Container>
          <Navbar.Brand href="/market">qqueue</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto"> 
              <Nav.Link href="/market">market</Nav.Link>
              <Nav.Link href="/cart">my cart</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      
      <Container>
        <BrowserRouter>
          <Switch>
            <Route path="/market">
              <Market addToCart={addToCartHandler}/>
            </Route>
            <Route path="/product/:id">
              <Product addToCart={addToCartHandler}/>
            </Route>
            <Route path="/cart">
              <Cart 
                cart={cart}
                cartCount={itemsInCart}
                addToCart={addToCartHandler}
                removeFromCart={removeFromCartHandler}
                removeAllFromCart={removeAllFromCartHandler}
                emptyCart={emptyCartHandler}
              />
            </Route>
          </Switch>
        </BrowserRouter>
      </Container>

      <div class="py-5"/>  {/* so last row isn't covered by footer */}

      <Navbar className="fixed-bottom" bg="dark" variant="dark">
        <Container>
          <Navbar.Text className="text-muted">
            The current time is {currentTime}.
          </Navbar.Text>
          <Navbar.Text className="text-muted">
            <Container >
              There are {itemsInCart} items in <a href="/cart">my cart</a>.
            </Container>
          </Navbar.Text>
        </Container>
      </Navbar>

    </div>
  );
}

export default App;
