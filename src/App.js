import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Switch, Redirect,  } from 'react-router-dom';
import Cookies from 'js-cookie';

// Styles

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Navbar, Nav, NavDropdown } from 'react-bootstrap';

// Components

import Market from './components/Market';
import Product from './components/Product';
import Cart from './components/Cart';
import Login from './components/Login';
import Register from './components/Register';
import Store from './components/Store';

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

  let storedCart = JSON.parse(Cookies.get('qq_cart'));
  const [cart, setCart] = useState(storedCart ? storedCart : {});
  const [itemsInCart, setItemsInCart] = useState(0);

  useEffect(() => {
    if (Object.keys(cart).length > 0) {
      setItemsInCart(Object.values(cart).reduce((a, b) => a + b));
    } else {
      setItemsInCart(0);
    }
  }, [cart]);

  const updateCart = (update) => {
    let hardCopy = { ...cart };
    update(hardCopy);
    setCart(hardCopy);

    // A cookie is used to persist the cart between pages.
    Cookies.set('qq_cart', JSON.stringify(hardCopy));
  }

  const addToCartHandler = (product_id) => {
    updateCart((cartCopy) => {
      if (product_id in cartCopy) {
        cartCopy[product_id] += 1;
      } else {
        cartCopy[product_id] = 1;
      }
    });
  }

  const removeFromCartHandler = (product_id) => {
    updateCart((cartCopy) => {
      cartCopy[product_id] -= 1;
      if (cartCopy[product_id] === 0) {
        delete cartCopy[product_id];
      }
    });
  }

  const removeAllFromCartHandler = (product_id) => {
    updateCart((cartCopy) => {
      delete cartCopy[product_id];
    });
  }

  const emptyCartHandler = () => {
    updateCart((cartCopy) => {
      for (var key in cartCopy) {
        delete cartCopy[key];
      }
    });
  }

  // Auth
  const [loggedIn, setLoggedIn] = useState(false);
  const [loggedOut, setLoggedOut] = useState(false);  // it'll make sense trust me
  const [userEmail, setUserEmail] = useState('');
  const [userId, setUserId] = useState(0); // There are no users with ID 0.

  const [isVendor, setIsVendor] = useState(false);

  useEffect(() => {
    let access_token = Cookies.get('qq_access_token');
    if (access_token) {
      fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          access_token: access_token,
          id: Cookies.get('qq_account_id'),
          email: Cookies.get('qq_account_email'),
          is_vendor: Cookies.get('qq_is_vendor')
        })
      }).then(res => res.json()).then(data => {
        onLoginHandler(data);
      });
    } else {
      onLogoutHandler();
    }
  }, []);  // Only runs once at render

  const onLoginHandler = (data) => {
    let success = data.status === 200;  // Huge success
    setLoggedIn(success);
    setLoggedOut(!success);

    if (success) {
      setUserId(data.id);
      setUserEmail(data.email);

      setIsVendor(data.is_vendor);

      const expires = (60 * 60) * 1000;
      const inOneHour = new Date(new Date().getTime() + expires);

      Cookies.set('qq_access_token', data.access_token, { expires: inOneHour });
      Cookies.set('qq_account_id', data.id, { expires: inOneHour });
      Cookies.set('qq_account_email', data.email, { expires: inOneHour });

      Cookies.set('qq_is_vendor', data.is_vendor, { expires: inOneHour });

      emptyCartHandler();  // hack to clear the cart on login.
    } else {
      console.log(data);
    }
  }

  const onLogoutHandler = () => {
    setLoggedOut(true);
    setLoggedIn(false);

    setUserId(0);
    setUserEmail('');
    
    setIsVendor(false);

    Cookies.remove('qq_access_token');
    Cookies.remove('qq_account_id');
    Cookies.remove('qq_account_email');

    Cookies.remove('qq_is_vendor');
  }

  const registerLinks = () => {
    return (
      <NavDropdown title="register" id="nav_login_dropdown" bg="dark">
        <NavDropdown.Item href="/register/customer">customer</NavDropdown.Item>
        <NavDropdown.Item href="/register/vendor">vendor</NavDropdown.Item>
      </NavDropdown>
    );
  }

  const loginLinks = () => {
    return (
      <NavDropdown title="login" id="nav_login_dropdown" bg="dark">
        <NavDropdown.Item href="/login/customer">customer</NavDropdown.Item>
        <NavDropdown.Item href="/login/vendor" >vendor</NavDropdown.Item>
      </NavDropdown>
    );
  }

  const customerAccountLinks = () => {
    return (
      <NavDropdown title={userEmail} id="nav_account_dropdown" bg="dark">
        <NavDropdown.Item href="/account">orders</NavDropdown.Item>
        <NavDropdown.Item href="/logout" onClick={onLogoutHandler}>logout</NavDropdown.Item>
      </NavDropdown>
    );
  }

  // Store

  const [itemsInStore, setItemsInstore] = useState(0);

  // Render

  return (
    <div id="wrapper" className="d-grid gap-3">

      <Navbar collapseOnSelect bg="dark" variant="dark" expand="lg" sticky="top">
        <Container>

          <Navbar.Brand href="/home">qqueue</Navbar.Brand>

          <Navbar.Toggle aria-controls="basic-navbar-nav" />

          <Navbar.Collapse id="basic-navbar-nav">

            <Nav className="me-auto">
              <Nav.Link href="/market">market</Nav.Link>
            </Nav>

            <Nav>
              { isVendor ? '' : <Nav.Link href="/cart">cart</Nav.Link> }
              { isVendor ? <Nav.Link href={`/store/${userId}`}>store</Nav.Link> : '' }

              { loggedIn ? <Nav.Link href="/orders">orders</Nav.Link> : '' }
              { loggedOut ? registerLinks() : '' }{' '}
              { loggedOut ? loginLinks() : '' }{' '}
              { loggedIn ? customerAccountLinks() : '' }
            </Nav>

          </Navbar.Collapse>

        </Container>
      </Navbar>
      
      <Container>
        <BrowserRouter>
          <Switch>

            <Route path="/market">
              <Market
                isVendor={isVendor}
                addToCart={addToCartHandler}
              />
            </Route>

            <Route path="/product/:id">
              <Product
                isVendor={isVendor}
                vendorId={isVendor ? userId : 0}
                addToCart={addToCartHandler}
              />
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

            <Route path="/store/:id">
              <Store />
            </Route>

            <Route path="/login/:loginType">
              <Login 
                onLogin={onLoginHandler}
              />
            </Route>

            <Route path="/logout">
              <Redirect to="/home" />
            </Route>

            <Route path="/register/:registrationType">
              <Register 
                onRegister={onLoginHandler}
              />
            </Route>


            <Route path="/404">
              Looks like you got here by accident. Try one of these:{' '}
              <a href="/home">home</a>{' '}
              <a href="/market">market</a>{' '}
              <a href="/orders">orders</a>{' '}
            </Route>

          </Switch>
        </BrowserRouter>
      </Container>

      <div className="py-5"/>  {/* so last row isn't covered by footer */}

      <Navbar className="fixed-bottom" bg="dark" variant="dark">
        <Container>
          <Navbar.Text className="text-muted">
            The current time is {currentTime}.
          </Navbar.Text>
          <Navbar.Text className="text-muted">
            <Container >
              {
                isVendor
                  ? itemsInStore === 1
                    ? 'There is 1 item in '
                    : `There are ${itemsInStore} items in `
                  : itemsInCart === 1
                    ? 'There is 1 item in '
                    : `There are ${itemsInCart} items in `
              }
              {
                isVendor
                  ? <a href={`/store/${userId}`} className="text-muted">my store</a>
                  : <a href="/cart" className="text-muted">my cart</a>
              }
              .
            </Container>
          </Navbar.Text>
        </Container>
      </Navbar>

    </div>
  );

}

export default App;
