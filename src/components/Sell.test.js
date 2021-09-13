import { render, screen } from '@testing-library/react';
import Sell from './Sell';

test('renders the selling form', () => {
    render(<Sell />);

    const titleElement = screen.getByTestId('sell-card-title');
    expect(titleElement).toBeInTheDocument();
    expect(titleElement.innerText).toEqual < String > ('sell a product');

    const nameElement = screen.getByTestId('sell-card-name');
    expect(nameElement).toBeInTheDocument();

    const detailElement = screen.getByTestId('sell-card-detail');
    expect(detailElement).toBeInTheDocument();

    const submitButton = screen.getByTestId('sell-submit-button');
    expect(submitButton).toBeInTheDocument();
    expect(submitButton.innerText).toEqual < String > ('list for sale →');
});