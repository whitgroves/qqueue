import { render, screen } from '@testing-library/react';
import AuthCard from './AuthCard';

test('renders as login', () => {
  render(
    <AuthCard
      isRegistration={false}
      onAuthenticated={() => { }}
    />
  );

  const titleElement = screen.getByTestId('auth-card-title');
  expect(titleElement).toBeInTheDocument();
  expect(titleElement.innerText).toEqual < String > ('sign in');

  const emailField = screen.getByTestId('auth-card-email');
  expect(emailField).toBeInTheDocument();

  const passwordField = screen.getByTestId('auth-card-password');
  expect(passwordField).toBeInTheDocument();

  const submitButton = screen.getByTestId('auth-submit-button');
  expect(submitButton).toBeInTheDocument();
  expect(submitButton.innerText).toEqual < String > ('sign in');
})

test('renders as registration', () => {
  render(
    <AuthCard
      isRegistration={true}
      onAuthenticated={() => { }}
    />
  );

  const titleElement = screen.getByTestId('auth-card-title');
  expect(titleElement).toBeInTheDocument();
  expect(titleElement.innerText).toEqual < String > ('sign up');

  const emailField = screen.getByTestId('auth-card-email');
  expect(emailField).toBeInTheDocument();

  const passwordField = screen.getByTestId('auth-card-password');
  expect(passwordField).toBeInTheDocument();

  const passwordConfirmField = screen.getByTestId('auth-card-password-confirm');
  expect(passwordConfirmField).toBeInTheDocument();

  const submitButton = screen.getByTestId('auth-submit-button');
  expect(submitButton).toBeInTheDocument();
  expect(submitButton.innerText).toEqual < String > ('sign up');
})