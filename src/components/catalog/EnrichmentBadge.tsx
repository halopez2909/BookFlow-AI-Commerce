interface Props {
  isEnriched: boolean;
}

export const EnrichmentBadge = ({ isEnriched }: Props) => {
  return (
    <span className={`px-2 py-1 text-xs font-bold rounded-full w-fit ${
      isEnriched 
        ? 'bg-green-100 text-green-700' 
        : 'bg-gray-100 text-gray-600'
    }`}>
      {isEnriched ? 'Enriquecido' : 'Básico'}
    </span>
  );
};