import { render, screen } from '@testing-library/react';
import ProductCard from './ProductCard';

test('renders product data', () => {

  let testProduct = { 'id': 1, 'name': 'Test Product' };

  render(<ProductCard product={testProduct} />);

  const nameElement = screen.getByText(testProduct.name);
  expect(nameElement).toBeInTheDocument();

});