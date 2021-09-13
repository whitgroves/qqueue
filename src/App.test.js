import { render, screen } from '@testing-library/react';
import App from './App';

test('renders time element', () => {
  render(<App />);

  const timeElement = screen.getByText(/The current time is/i);
  expect(timeElement).toBeInTheDocument();
});

test('renders navigation links while signed out', () => {
  render(<App />);

  const marketLink = screen.getByText(/market/i);
  expect(marketLink).toBeInTheDocument();

  const cartLink = screen.getByTestId('nav-link-cart');
  expect(cartLink).toBeInTheDocument();

  const registerLink = screen.getByText(/register/i);
  expect(registerLink).toBeInTheDocument();

  const loginLink = screen.getByText(/login/i);
  expect(loginLink).toBeInTheDocument();
});

test('renders the app container while signed in', () => {
  let testUser = {
    id: 1,
    email: 'AppTest@test.net'
  }

  render(
    <App
      testToken={'doesntMatter'}  // client doesn't care about the token value, just that it has one 
      testUser={testUser}
    />
  );

  const marketLink = screen.getByText(/market/i);
  expect(marketLink).toBeInTheDocument();

  const ordersLink = screen.getByText(/orders/i);
  expect(ordersLink).toBeInTheDocument();

  const sellLink = screen.getByText(/sell/i);
  expect(sellLink).toBeInTheDocument();

  const cartLink = screen.getByTestId('nav-link-cart');
  expect(cartLink).toBeInTheDocument();

  const userDropdown = screen.getByText(testUser.email);
  expect(userDropdown).toBeInTheDocument();
});
