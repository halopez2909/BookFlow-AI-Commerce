interface Props {
  price: number | null;
  explanation?: string;
}

export const PriceSummary = ({ price, explanation }: Props) => {
  if (!price) return <p className="text-gray-500 font-medium">Precio no disponible</p>;

  return (
    <div className="flex flex-col gap-1">
      <span className="text-2xl font-bold text-blue-600">${price.toFixed(2)}</span>
      {explanation && <p className="text-xs text-gray-500">{explanation}</p>}
    </div>
  );
};